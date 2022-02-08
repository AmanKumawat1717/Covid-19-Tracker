from flask import Flask, render_template,request
import requests

app=Flask(__name__)

url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

headers = {
    'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
    'x-rapidapi-key': "62b0921c89msh8a0246fc018e40ep18eadcjsn52a4f257c139"
    }
response = requests.get( url, headers=headers)
resp=response.json()

def api_data():
    global resp
    t_active=resp['total_values']['active']
    t_confirmed=resp['total_values']['confirmed']
    t_deaths=resp['total_values']['deaths']
    t_recovered=resp['total_values']['recovered']
    return t_active,t_confirmed,t_deaths,t_recovered


@app.route("/")
def index():
    t_active,t_confirmed,t_deaths,t_recovered = api_data()
    return render_template('index.html',t_active=t_active,t_confirmed=t_confirmed,t_deaths=t_deaths,t_recovered=t_recovered)

@app.route("/statename/",methods=["GET","POST"])
def statename():
    if request.method=="GET":
        Statelist=[]
        t_active,t_confirmed,t_deaths,t_recovered = api_data()
        for i in list(resp['state_wise'].keys())[:-1]:
            Statelist.append(i.capitalize())
        return render_template('index.html',t_active=t_active,t_confirmed=t_confirmed,t_deaths=t_deaths,t_recovered=t_recovered,Statelist=Statelist)
        

    else:
        t_active,t_confirmed,t_deaths,t_recovered = api_data()
        state=request.form.get("state_name")
        state=state.title()
        st_name=resp['state_wise'].keys()
        Active=resp['state_wise'][state]['active']
        Recover=resp['state_wise'][state]['recovered']
        Death=resp['state_wise'][state]['deaths']
        return render_template('index.html',Active=Active,Recover=Recover,Death=Death,t_active=t_active,t_confirmed=t_confirmed,t_deaths=t_deaths,t_recovered=t_recovered,state_n=state)
        



app.run(host="localhost",port=5000,debug=True)

