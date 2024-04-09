from django.template import loader
from django.http import HttpResponse as response
from Person.models import Person 
from django.shortcuts import redirect, render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score as accuracy


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
            return redirect("/register/")
    except Person.DoesNotExist:
        return redirect("/register/")
    

def chat(request):
    if request.method == 'GET':
        personEmail = request.session.get('person_email')
        person = Person.objects.get(email=personEmail)
        template = loader.get_template('chat.html')
        context = {'person': person}
        return response(template.render(context,request))
    
    train = pd.read_csv('/home/godalway/Programs/Python/Emotions-CRUD/Emotions/Person/inputs/train.txt',names=["Emotion","Feeling"],sep=';')
    test = pd.read_csv('/home/godalway/Programs/Python/Emotions-CRUD/Emotions/Person/inputs/test.txt',names=["Emotion","Feeling"],sep=';')

    trainInput =train.drop('Feeling', axis=1)['Emotion']
    y_train = train['Feeling']

    testInput = test.drop('Feeling', axis=1)['Emotion']
    y_test = test['Feeling']

    converter = TfidfVectorizer()
    x_train = converter.fit_transform(trainInput)
    x_test = converter.transform(testInput)

    classifier = RandomForestClassifier()
    classifier.fit(x_train, y_train)

    predictions = classifier.predict(x_test)

    print(f'The accuracy is {accuracy(y_test,predictions)*100}')