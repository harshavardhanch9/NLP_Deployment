from flask import Flask, request, render_template
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from wtform import RegistrationForm
from wtform import * 
from user_data import *

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

app = Flask(__name__)
app.secret_key = 'replace later'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app) ## initialize the database
db.create_all(app=app) ## create table

db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def Sentiment():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Username has already taken by someone!"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Successfully entered into DB!"

    return render_template('home.html', form=reg_form)

@app.route('/stocks')
def Stocks():
    return render_template('stocks.html')

@app.route('/contact')
def Contact():
    return render_template('contact.html')


@app.route('/hello', methods=['POST'])
def post():
    parser = reqparse.RequestParser()  # used to parse incoming requests
    parser.add_argument('typetext', required=True,
                help='Review cannot be blank!')
    args = parser.parse_args()
    review = args['typetext']
    doc = nlp(review)
    score = doc._.polarity
    if score  <0:
        sentiment = 'Negative😞😞😞'
       
        
    elif score >0: 
        sentiment = 'Positive😊😊😊'
       
    else:
        sentiment = 'Neutral😐😐😐'
    
    return render_template('stocks.html', prediction=sentiment)

    

if __name__ == '__main__':
    app.run(debug=True)