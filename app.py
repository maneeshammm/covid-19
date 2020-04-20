from cassandra.cluster import Cluster
#Connecting to the Cassandra Cluster
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
#Create a session by connecting to cluster
session = cluster.connect()


from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    country = TextField('Country:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST']) #REST api GET ,POST method
def hello():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        country=request.form['country']
        #corona url
        url = f'https://corona-api.com/countries/{country}'
        resp = requests.get(url)
        if resp.ok:
            country_data = resp.json()
            name=str(country_data['data'].get('name'))
            date=str(country_data['data'].get('updated_at')[0:10])
            recovered=country_data['data']['latest_data'].get('recovered')
            confirmed=country_data['data']['latest_data'].get('confirmed')
            deaths=country_data['data']['latest_data'].get('deaths')
            flash(f'Country: {name}\n Date: {date}\n Recovered: {str(recovered)}\nConfirmed: {str(confirmed)} \nDeaths: {str(deaths)}')
            #flash(f'Country: {name}\n Recovered: {str(recovered)}\nConfirmed: {str(confirmed)} \nDeaths: {str(deaths)}')
            session.execute(f"INSERT INTO covid.stats(ID,Name,Date,recovered,confirmed,deaths) VALUES('{country}','{name}','{date}',{recovered},{confirmed},{deaths});")
        else:
            print(resp.reason)   
    return render_template('index.html', form=form)

#A route to return all of the available countries in the database
@app.route("/countries", methods=['GET']) #REST api Get method
def profile():
    rows = session.execute( 'Select * From covid.stats')
    countries=[]
    for row in rows:
        countries.append(row.name)
    return (str(countries))


@app.route('/countries_stats', methods=['GET']) #REST api GET method
def countries_stats():
    rows = session.execute("Select * From covid.stats")
    result = []
    for r in rows:
        result.append({"country":r.name,"confirmed":r.confirmed,"deaths":r.deaths,"recovered":r.recovered})
    return jsonify(result)

@app.route('/country',  methods=['POST']) #REST api POST method
def create():
    session.execute( """INSERT INTO covid.stats(name,confirmed,deaths,recovered) VALUES('{}', {}, {}, {})""".format(request.json['name'],int(request.json['confirmed']),int(request.json['deaths']),int(request.json['recovered'])))
    return jsonify({'message': 'created: /country/{}'.format(request.json['name'])}), 201

@app.route('/country',  methods=['PUT']) #REST api PUT method
def update():
    session.execute("""UPDATE covid.stats SET confirmed= {},deaths= {}, recovered= {} WHERE name= '{}'""".format(int(request.json['confirmed']),int(request.json['deaths']),int(request.json['recovered']),request.json['name']))
    return jsonify({'message': 'updated: /country/{}'.format(request.json['name'])}), 200

@app.route('/country',  methods=['DELETE']) #REST api DELETE method
def delete():
    session.execute("""DELETE FROM covid.stats WHERE name= '{}'""".format(request.json['name']))
    return jsonify({'message': 'deleted: /country/{}'.format(request.json['name'])}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443,ssl_context=('cert.pem', 'key.pem'))
    #app.run(host='0.0.0.0',port=80)