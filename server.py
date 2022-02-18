from flask import Flask, request, redirect,session
from flask_session import Session
import api_functions

app = Flask(__name__,static_folder='../frontend',template_folder='../frontend/views')
app.config['SESSION_PERMANENET'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.config['SECRET_KEY'] = api_functions.generate_secret_key(64)
Session(app)

@app.route('/')
def index():
    response_data = api_functions.get_all_base_data()
    session['base_data'] = response_data
    return redirect('/naraen/noblelaureates/api/')

@app.route('/naraen/noblelaureates/api/',methods=['GET'])
def get_noble_list():
    if request.method == "GET":
        category = request.args.get('category','all')
        year = request.args.get('year','all')
        base_data = session.get('base_data','')
        rendered_data = api_functions.get_noble_laureates_data(base_data,category,year)
        return rendered_data

@app.route('/naraen/topnoblelaureates/api/',methods=['GET'])
def get_toplaureates():
    if request.method == "GET":
        base_data = session.get('base_data','')
        rendered_data = api_functions.get_people_won_multiple(base_data)
        return rendered_data



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
