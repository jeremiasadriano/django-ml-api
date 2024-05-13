from django.template import loader
from django.http import HttpResponse as response
from Person.models import Person, Message
from Person.ml_model import predict
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db import IntegrityError

def register(request):
    if request.method == 'GET':
        return response(loader.get_template('signUp.html').render())
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    person = Person(firstName = firstName,lastName= lastName,email = email,password = password)
    try:
        person.save();
        request.session['person_email'] = person.email
        return redirect('/chat/')
    except IntegrityError:
        context = {'messageError': "User with such email already exists!"}
        return response(loader.get_template('signUp.html').render(context,request))

def login(request):
    if request.method == 'GET':
        return response(loader.get_template('login.html').render())
    email = request.POST['email']
    password = request.POST['password']

    try:
        person = Person.objects.get(email=email)
        if person.password == password:
            request.session['person_email'] = person.email
            return redirect('/chat/')
        else:
            context = {'messageError': "No user with such email or password was found!"}
            return response(loader.get_template('login.html').render(context,request))
    except Person.DoesNotExist:
        context = {'messageError': "No user with such email or password was found!"}
        return response(loader.get_template('login.html').render(context,request))

def update(request):
    personEmail = request.session.get('person_email')
    person = Person.objects.get(email=personEmail)
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    person.firstName = firstName
    person.lastName = lastName
    person.email = email
    person.password = password

    request.session.pop('person_email')
    request.session['person_email'] = person.email
    person.save();

    return redirect('/chat/') 

def delete(request):
    personEmail = request.session.get('person_email')
    person = Person.objects.get(email=personEmail)
    person.delete()
    request.session.pop('person_email')
    return redirect("/login/") 

def chat(request):
    personEmail = request.session.get('person_email')
    if request.method == 'GET':
        if personEmail is None:
            return redirect("/login/") 
        person = Person.objects.get(email=personEmail)
        template = loader.get_template('chat.html')
        messages = Message.objects.filter(person=person)
        context = {'person': person, 'message': messages }
        return response(template.render(context,request))

    message = request.POST['question']
    template = loader.get_template('chat.html')
    return response(template.render(predict(message,personEmail),request))

def logout_view(request):
    logout(request)
    return redirect('/login/')