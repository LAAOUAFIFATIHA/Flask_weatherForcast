
# importing Flask and other modules
from flask import Flask, request, render_template , flash
import requests
import json
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



if request.method == "POST":
        from datetime import datetime
        jour = request.form.get("jour")
        date_obj = datetime.strptime(jour, '%Y-%m-%d')
        nhar =date_obj.strftime('%A')
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
        
  
        
        gpsdict = {'Essaouira':( "31.51", "-9.77"),
                    'Asafi':("32.2994" , "-9.2372"),
                    'Ouajda':("34.0132500",  "-6.8325500"),
                    'Marakech':("31.6342" , "-7.9999"),
                    'Zagora':( "28.5" , "-10"),
                    'caza_blanka':("33.5883","-7.6114")}


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

        print ("rlllllllllllllllllllllllllllllllllllllll",data)

        # Fonction pour extraire chaque troisième élément d'une liste
        def ri3valeur(listy):
                li = []
                for i in range(0, len(listy), 3):
                    li.append(listy[i])
                return li
        print( data)
            # Traiter les données météorologiques
        listrain = ri3valeur(data["hourly"]["rain"])
        listeTemp = data["hourly"]["temperature_2m"]
        listeTemp1 = ri3valeur(data["hourly"]["temperature_2m"])
        listwind1 = data["hourly"]["wind_speed_10m"]
        listwind = ri3valeur(data["hourly"]["wind_speed_10m"])
        listecloud = ri3valeur(data["hourly"]["cloud_cover"])
        listecloud1 = data["hourly"]["cloud_cover"]
        windlist = data["hourly"]["wind_speed_10m"]

        listsunset = data["daily"]["sunset"]
        listsunrise = data["daily"]["sunrise"]

            
            #-------------------new time---------------------------
        from datetime import datetime
        dateLyouma = datetime.today().strftime("%Y-%m-%d")
            
            #---------------function----pour---metre----les--images-----------------
        heurs = ["00:00","03:00","09:00","12:00","15:00","18:00","21:00","24:00"]
        suns =int(listsunset[0][11:13])
        sunr = int(listsunrise[0][11:13])



            #--------------dict pour envoyer
        listdict =[]
        for i in range(9-1):
                dicttow={}
                dicttow["temperature"] =(max([listeTemp[0+i*3] ,listeTemp[1+i*3],listeTemp[2+i*3]]),(min([listeTemp[0+i*3] ,listeTemp[1+i*3],listeTemp[2+i*3]])))
                if i >= 4 :
                    dicttow["temps"] = "{}:00".format(i*3)
                else:
                    dicttow["temps"] = "0{}:00".format(i*3)
                dicttow["rain"] = listrain[i]
                dicttow["wind"] =(max([windlist[0+i*3] ,windlist[1+i*3],windlist[2+i*3]]),(min([windlist[0+i*3] ,windlist[1+i*3],windlist[2+i*3]])))
                dicttow["cloud"] = listecloud[i]
                listdict.append(dicttow)
        listdict

            #---------------function----pour---metre----les--images-----------------
        def getImagesSoliel (listeTemp,listecloud,listrain,listdict):
                for j,i  in enumerate(listeTemp) :
                    heur =int(heurs[j][0:2])
                    if i < 10 and listecloud[j] != 0 and listrain[j] == 0 :
                        if sunr <= heur and suns > heur:
                            listdict[j]["image"] = "images/sunCloudy.png"
                        else :
                            listdict[j]["image"] = "images/moon_cloudy.png"

                    elif  i < 10 and listrain[j] != 0 :
                        if sunr <= heur and suns > heur:
                            listdict[j]["image"]="images/sunRain.png"
                        else :
                            listdict[j]["image"]="images/moon_rain.png"

                    elif i < 20 and  listrain[j] != 0 :
                        if sunr <= heur and suns > heur and i < 20 :
                            listdict[j]["image"]="images/sunRain.png"
                        else :
                            listdict[j]["image"]="images/moon_rain.png"
                        
                    elif i <20 and listecloud[j] != 0 and  listrain[j] == 0 :
                        if sunr <= heur and suns > heur and i <20:
                            listdict[j]["image"]="images/sunCloudy.png"
                        else :
                            listdict[j]["image"]="images/moon_cloudy.png"
                    elif i <20   :
                        if sunr <= heur and suns > heur and i <20:
                            listdict[j]["image"]="images/1.png"
                        else :
                            listdict[j]["image"]="images/moon_cloudy.png"
                    elif i <27  :
                        if sunr <= heur and suns > heur :
                            listdict[j]["image"]="images/sunchoud.png"
                        else :
                            listdict[j]["image"]="images/moon.png"
                    else :
                        if sunr <= heur and suns > heur  :
                            listdict[j]["image"]="images/soliel_choud.png"
                        else:
                            listdict[j]["image"]="images/moon.png"

                return listdict 
        listdict = getImagesSoliel(listeTemp1,listecloud,listrain,listdict)