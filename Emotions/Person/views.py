from django.template import loader
from django.http import HttpResponse as response
from Person.models import Person, Message
from django.shortcuts import redirect
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from django.conf import settings
from django.contrib.auth import logout
import os 

def register(request):
    if request.method == 'GET':
        return response(loader.get_template('signUp.html').render())
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    person = Person(firstName = firstName,lastName= lastName,email = email,password = password)
    person.save();
    return redirect("/login/")  

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

def predict(message,email):
    train_file_path = os.path.join(settings.BASE_DIR, 'static/datasets/train.txt')
    test_file_path = os.path.join(settings.BASE_DIR, 'static/datasets/test.txt')

    train = pd.read_csv(train_file_path,names=["Emotion","Feeling"],sep=';')
    test = pd.read_csv(test_file_path,names=["Emotion","Feeling"],sep=';')

    trainInput =train.drop('Feeling', axis=1)['Emotion']
    y_train = train['Feeling']

    testInput = test.drop('Feeling', axis=1)['Emotion']
    y_test = test['Feeling']

    converter = TfidfVectorizer()
    x_train = converter.fit_transform(trainInput)
    x_test = converter.transform(testInput)

    classifier = SGDClassifier()
    classifier.fit(x_train, y_train)
    prediction = classifier.predict(x_test)

    accuray = (accuracy_score(y_test,prediction)*100)

    predictionsResult = classifier.predict(converter.transform([message]))
    person = Person.objects.get(email=email)
    answer = Message(phrase=message, answer=predictionsResult[0],person=person)
    answer.save()
    messages = Message.objects.filter(person=person)
    return {'predict' : messages, 'accuracy': accuray, 'person': person}

def logout_view(request):
    logout(request)
    return redirect('/login/')