from django.template import loader
from django.http import HttpResponse as response
from Person.models import Person, Message
from django.shortcuts import redirect
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from django.conf import settings
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
            return redirect("/login/")
    except Person.DoesNotExist:
        return redirect("/register/")
    

def chat(request):
    if request.method == 'GET':
        personEmail = request.session.get('person_email')
        if personEmail is None:
            return redirect("/login/") 
        person = Person.objects.get(email=personEmail)
        template = loader.get_template('chat.html')
        context = {'person': person}
        return response(template.render(context,request))

    message = request.POST['question']
    template = loader.get_template('chat.html')
    return response(template.render(predict(message),request))


def predict(message):
    train_file_path = os.path.join(settings.BASE_DIR, 'static/datasets/train.txt')
    train = pd.read_csv(train_file_path,names=["Emotion","Feeling"],sep=';')

    trainInput =train.drop('Feeling', axis=1)['Emotion']
    y_train = train['Feeling']

    converter = TfidfVectorizer()
    x_train = converter.fit_transform(trainInput)

    classifier = SGDClassifier()
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(converter.transform([message]))

    answer = Message(phrase=message, answer=predictions[0])
    answer.save()
    messages = Message.objects.all().values()
    return {'predict' : messages}