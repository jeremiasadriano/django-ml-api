from Person.models import Person, Message
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import os 

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