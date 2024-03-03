from mongoengine import Document, StringField, IntField, connect

connect('student_db', host='localhost', port=27017)


class Student(Document):
    name = StringField(required=True)
    age = IntField(required=True)
    email = StringField(required=True)
