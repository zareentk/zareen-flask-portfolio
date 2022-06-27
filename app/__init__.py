from flask import Flask, render_template, request, json,  url_for, request, redirect
from app.map_app import map_app
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime
import folium
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')

app = Flask(__name__)
app.register_blueprint(map_app)
dataFile = open("./app/static/data.json" , encoding = "utf-8")

data = json.load(dataFile)
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
	user= os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PASSWORD"),
	host=os.getenv("MYSQL_HOST"),
	port=3306)

print(mydb)
class TimelinePost(Model):
	name = CharField()
	email = CharField()
	content = TextField()
	created_at = DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():    
    allUsers = data    
    return render_template('index.html', title="Home", allUsers=allUsers)

@app.route('/zareen-kabir-portfolio')
def zareen_portfolio():
    allUsers = data    
    return render_template('zareen-kabir-portfolio.html', allUsers=allUsers)
@app.route('/aleena-tim-portfolio')
def aleena_portfolio():
    allUsers = data    
    return render_template('aleena-tim-portfolio.html', allUsers=allUsers)
@app.route('/hobbies')
def hobbies():    
    return render_template('hobbies.html')
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
	name = request.form['name']
	email = request.form['email']
	content = request.form['content']
	timeline_post = TimelinePost.create(name=name, email=email, content=content)
	return model_to_dict(timeline_post)
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
	return {
		'timeline_post':[
			model_to_dict(p) 
			for p in 
TimelinePost.select().order_by(TimelinePost.created_at.desc())
		]
	}	
@app.route('/timeline')
def timeline():
		posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

		return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), posts=posts, data=data)
if __name__ == "__main__":
    app.run(debug=True)
