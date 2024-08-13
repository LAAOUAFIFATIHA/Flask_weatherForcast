# importing Flask and other modules
from flask import Flask, request, render_template , flash , redirect ,url_for
import requests
import json
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

##### for sql alchemy

from sqlalchemy import create_engine, ForeignKey, Column, String, Float, CHAR ,Boolean ,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask , redirect , render_template ,request
#####
#-------------------------les fonction qui j'ai besoin 


def distance(v ,v2 , car):
    d = 0 
    for i in range (len(v)):
        if isinstance(v2[i], tuple):
            r = float(v2[i][0])  # Assuming you want to use the first element of the tuple
            d += (v[i] - r)**2
        elif isinstance(v2[i], str):
            r = float(v2[i][0])  # Assuming you want to use the first element of the tuple
            d += (v[i] - r)**2
        else :  
            d += (v[i] - v2[i])**2

    return d**(1/2)
def distanceRef(s ,car):
    d = 0
    cards = car
    for i in range (cards):
        for j in range(cards ):
            print("hdddddddddddddddddd",s[i],"hhhhhhhhhhhhhhhhhhh",s[j])
            d = d+distance(s[i],s[j] ,car)

    return d/((cards-1)*cards)
def cardspp(s , vt ,car):
    dref = distanceRef(s ,car)
    spp = []
    for v in s :
        if (distance (v , vt ,car)< dref):
            spp.append(v)
    return(len(spp))

def propavrai(s,vt ,car):
    return  float(cardspp(s , vt ,car)/car) 


#-------------------------fin fonction

# creation of data base 


base = declarative_base()

engine2 = create_engine("sqlite:///DB_WEATHER.db", echo=True)
base.metadata.create_all(bind=engine2)
Session = sessionmaker(bind=engine2)
session = Session()


class weatherbad(base):
    __tablename__ = 'forcastbad'
    date = Column('date', String, primary_key=True)
    temperature = Column('temperature', Float)
    rain = Column('rain', Float)
    wind = Column('wind', Float)
    cloud = Column('cloud', Float)


    def __init__(self, date, temp, rain , wind, cloud ) :
        self.date = date
        self.temperature = temp
        self.rain = rain
        self.wind = wind
        self.cloud = cloud
       

    def __repr__(self):
        return f"({self.date} {self.temperature} {self.rain} {self.wind} {self.cloud} )"
    

#weather bad 


class weathergood(base):
    __tablename__ = 'forcastgood'
    date = Column('date', String, primary_key=True)
    temperature = Column('temperature', Float)
    rain = Column('rain', Float)
    wind = Column('wind', Float)
    cloud = Column('cloud', Float)


    def __init__(self, date, temp, rain , wind, cloud ) :
        self.date = date
        self.temperature = temp
        self.rain = rain
        self.wind = wind
        self.cloud = cloud
       

    def __repr__(self):
        return f"({self.date} {self.temperature} {self.rain} {self.wind} {self.cloud} )"

#fin pour base de donnee

engine = create_engine("sqlite:///DB_WEATHER.db", echo=True)
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()



 
# Flask constructor
app = Flask(__name__)
@app.route('/home', methods =["GET", "POST"])
def gfg(res =2 ):
    print("wweeeeeeeeeeeeeeeeeeeeeelcome ",res)
    # flash("log in successful" , "success")
    if request.method == "POST":
        from datetime import datetime
        jour = request.form.get("jour")
        date_obj = datetime.strptime(jour, '%Y-%m-%d')
        nhar =date_obj.strftime('%A')
        jours = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
                    'Thursday': 'jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'dimanche'}
        nhar = jours[nhar]


    else:
        from datetime import datetime
        dateLyouma = datetime.today().strftime("%Y-%m-%d")
        jour = dateLyouma
        nomLyouma = datetime.today().strftime("%A")
        jours = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
                    'Thursday': 'jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'dimanche'}
        nhar = jours[nomLyouma]

    if request.method == "POST":
        ville = request.form.get("ville")
        if ville =='':
            ville ="Essaouira"

    

        import time
        heure_locale = time.localtime()
        # Formater l'heure au format HH:MM:SS
        heure_now = time.strftime("%H:%M:%S", heure_locale)
        
  
        gpsdict = {'Essaouira':( "31.51", "-9.77"),
                    'Asafi':("32.2994" , "-9.2372"),
                    'Ouajda':("34.0132500",  "-6.8325500"),
                    'Marakech':("31.6342" , "-7.9999"),
                    'Zagora':( "28.5" , "-10"),
                    'caza_blanka':("33.5883","-7.6114")}
        jours = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
                    'Thursday': 'jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'dimanche'}


            # List des heures
        heurs = ["0:00", "3:00", "9:00", "12:00", "15:00", "18:00", "21:00", "24:00"]

        url = "https://api.open-meteo.com/v1/forecast?"
        url += "latitude="+gpsdict[ville][0]+"&longitude="+gpsdict[ville][1]
        url += "&hourly=temperature_2m"
        url += "&hourly=wind_speed_10m"
        url += "&hourly=cloud_cover"
        url += "&daily=sunrise"
        url += "&daily=sunset"
        url += "&hourly=rain"
        url += f"&start_date={jour}"
        url += f"&end_date={jour}"
        print(url)

        response = requests.get(url)
        data = json.loads(response.content.decode('utf-8'))


        # Fonction pour extraire chaque troisième élément d'une liste
        def moyenne (listy) :
            som = 0
            for i in listy :
                if i :
                    som += i
            return som / len(listy)
            # Traiter les données météorologiques
        listrain = data["hourly"]["rain"]
        listeTemp = data["hourly"]["temperature_2m"]
        listwind = data["hourly"]["wind_speed_10m"]
        listecloud = data["hourly"]["cloud_cover"]
        windlist = data["hourly"]["wind_speed_10m"]

        mrain = moyenne(listrain)
        mtemp = str(moyenne(listeTemp))
        mwind = moyenne(listwind)
        mcloud = moyenne(listecloud)

        listsunset = data["daily"]["sunset"]
        listsunrise = data["daily"]["sunrise"]

            
            #-------------------new time---------------------------
        from datetime import datetime
        dateLyouma = datetime.today().strftime("%Y-%m-%d")
            
            #---------------function----pour---metre----les--images-----------------
        heurs = ["00:00","03:00","09:00","12:00","15:00","18:00","21:00","24:00"]
        suns =int(listsunset[0][11:13])
        sunr = int(listsunrise[0][11:13])


            #-----------------static----------------------
        # f = open("data.txt" , "w")



        # f = open("data.txt" , "r")
        # d = f.readline()
        # t =d.split (" ")
        # # print(t[0])
        # f.close()


        # x=range(24)
        # d1=[float(t[i]) for i in range (24)]
        # plt.plot(x,d1,"green")
        # pic =plt.savefig('temperature')
        # f = open("data.txt" , "w")

        # # for  t in listeTemp :
        # f.write(str(data['hourly']))
        # # f.write(" ")
        # f.close()

        # f = open("data.txt" , "r")
        # d = f.read()
        # t1 =d.split (":")
        # f.close()
        # def file ():
        #     print("hi in file    ")


        x=range(24)
        d1=[float(i) for i in listeTemp if i != '']
        plt.plot(x,d1   ,"orange")
        plt.xlabel("Heurs")
        plt.ylabel("Temperature")
        # plt.legend(( 'd1' ))
        plt.title("evoluation de la temperature dans ce jour")
        # f = open("data.txt" , "r")
        # d = f.readline()
        # t =d.split (" ")
        # print(t[0])
        photo = f'temp{jour[8:12]}{ville}{jour[8:12]}{ville}{jour[2:4]}{jour[5:7]}{jour[8:10]}.png'
        # f.close()

    # Chemin absolu du dossier static
        dossier_static = os.path.join(app.root_path, 'static')

    # Chemin absolu de l'image à rechercher
        chemin_image = os.path.join(dossier_static, 'images', photo)

    # Vérifie si l'image existe dans le dossier static
        if not(os.path.exists(chemin_image)):
            plt.savefig(f'static/images/temp{jour[8:12]}{ville}{jour[8:12]}{ville}{jour[2:4]}{jour[5:7]}{jour[8:10]}.png')



     #--------------dict pour envoyer
        listdictt =[]
        listdict ={}
    
        listdict["temperature"] = mtemp
        listdict["rain"] = mrain
        listdict["wind"] =mwind
        listdict["cloud"] = mcloud
        listjour = list(jours)
        listjourvrai =  [ i for i in jours.values() ]
        print(listjour,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")



            #---------------function----pour---metre----les--images-----------------
        def getImagesSoliel (mtemp,mcloud,mrain,listdict):
                    i  =  float(mtemp) 
                    heur =int(heure_now[0:2])
                    if i < 10 and mcloud != 0 and mrain == 0 :
                        if sunr <= heur and suns > heur:
                            listdict["image"] = "images/suncloudy.gif"
                        else :
                            listdict["image"] = "images/moon_cloudy.gif"

                    elif  i < 10 and  mrain != 0 :
                        if sunr <= heur and suns > heur:
                            listdict["image"]="images/sun_rain.gif"
                        else :
                            listdict["image"]="images/moon_rain.gif"

                    elif i < 20   and mrain != 0 :
                        if sunr <= heur and suns > heur and i < 20 :
                            listdict["image"]="images/sun_rain.gif"
                        else :
                            listdict["image"]="images/moon_rain.gif"
                        
                    elif i <20 and mcloud != 0 and  mrain == 0 :
                        if sunr <= heur and suns > heur and i <20:
                            listdict["image"]="images/sun_cloudy.gif"
                        else :
                            listdict["image"]="images/moon_cloudy.gif"
                    elif i <20   :
                        if sunr <= heur and suns > heur and i <20:
                            listdict["image"]="images/suun.png"
                        else :
                            listdict["image"]="images/moon_cloudy.gif"
                    elif i <27  :
                        if sunr <= heur and suns > heur :
                            listdict["image"]="images/sun_hot.gif"
                        else :
                            listdict["image"]="images/Moon.gif"
                    else :
                        if sunr <= heur and suns > heur  :
                            listdict["image"]="images/hot_sun.gif"
                        else:
                            listdict["image"]="images/Moon.gif"
        getImagesSoliel(mtemp,mcloud,mrain,listdict)
        listdictt.append(listdict)

        #------------------of days ___________________

        journ = jour
        lyoum = int(journ[8:10])+1
        jourf = journ[:8]+str(lyoum)
        lyoum = int(journ[8:10])+7
        joure = journ[:8]+str(lyoum)
        url = "https://api.open-meteo.com/v1/forecast?"
        url += "latitude="+gpsdict[ville][0]+"&longitude="+gpsdict[ville][1]
        url=url+"&daily=temperature_2m_max"
        url=url+"&daily=wind_speed_10m_max"
        url=url+"&daily=sunrise"
        url=url+"&daily=sunset"
        url=url+"&daily=rain_sum"
        url += f"&start_date={jourf}"
        url += f"&end_date={joure}"
        response = requests.get(url)
        data = json.loads(response.content.decode('utf-8'))
        listeTemp = data["daily"]["temperature_2m_max"]   
        listrain = data["daily"]["rain_sum"]
        listwind = data["daily"]["wind_speed_10m_max"]
        listecloud = data["daily"]["rain_sum"]
        listtime = data["daily"]["time"][:10]
        # f = open("datadays.txt" , "w")

        # for  t in listeTemp :
        # f.write(str(data['daily']))
        # f.write(" ")
        # f.close()
        listdicttt ={}
        for J in range ( 0,7):
                listdicttt ={}
                listdicttt["temperature"] = listeTemp[J]
                listdicttt["rain"] = listrain[J]
                listdicttt["wind"] = listwind[J]
                listdicttt["cloud"] = listecloud[J]
                listdicttt['time'] =listtime[J]
                dayindex = listjourvrai.index(nhar) 
                listdicttt ["jour"] = listjourvrai[(dayindex +J +1)%7] 
                mRain =listrain[J]
                mTemp = str(listeTemp[J])
                mWind = listwind[J]
                mCloud = listecloud[J]
                getImagesSoliel(mTemp,mCloud,mRain,listdicttt)
                listdictt.append(listdicttt)
        print('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        if  request.form.get('rain') and request.form.get('etat')=="bonne" :
                print('jfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
                temp = request.form.get('temp')
                rain = request.form.get('rain')
                wind = request.form.get('wind')
                cloud = request.form.get('cloud')
                from datetime import datetime
                date = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
                p1 = weathergood(date,temp, rain , wind ,cloud)
                session.add(p1)
                session.commit()
                res1 = session.query(weathergood.cloud,weathergood.rain,weathergood.temperature,weathergood.wind).all()
        elif  request.form.get('rain') and request.form.get('etat')=="mauvaise" :
                print('jfffffffffffffkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkffffff')
                temp = request.form.get('temp')
                rain = request.form.get('rain')
                wind = request.form.get('wind')
                cloud = request.form.get('cloud')
                from datetime import datetime
                date = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
                p1 = weatherbad(date,temp, rain , wind ,cloud)
                session.add(p1)
                session.commit()



        listeprog =[]
        listeprom =[]
        f = 'vide'
        res1 = session.query(weathergood.cloud,weathergood.rain,weathergood.temperature,weathergood.wind).all()
        res2 = session.query(weatherbad.cloud,weatherbad.rain,weatherbad.temperature,weatherbad.wind).all()
        if (len(res1) > 1) and (len(res2)  > 1) :
            for i in range(8):
                Vec = (listdictt[i]['temperature'] , listdictt[i]['rain'] ,listdictt[i]['wind'],listdictt[i]['cloud'])
                card1 = session.query(weathergood).count()
                card2 = session.query(weatherbad).count()
                listeprog.append(float('%.2f'%(propavrai(res1 , Vec ,card1 )*100)))
                listeprom.append(float('%.2f'%(propavrai(res2 , Vec , card2)*100)))
        f = res2
        f1 = res1
        f2 = res2
                   
                    ##------------fin of days _____________________

        return render_template('home.html',listdict = listdictt,res =res1 , f = f ,f1 = f1,f2 = f2 ,listeprom = listeprom ,listeprog = listeprog, ville =ville ,photo1 = 'static/images/'+photo,gpsdictt = gpsdict , nhar = nhar , newlyouma = jour)

    return render_template('dossier.HTML')

                                
