from datetime import datetime
import time
from flask import Flask,redirect,render_template,request,session,jsonify,render_template_string,url_for, redirect,send_from_directory
import json
import os
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
import smtplib
from itertools import groupby
from threading import Thread
import requests

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/navigate')
def navigate():
    return render_template('/navigate/navigate.html')

@app.route('/apod',methods=['GET','POST'])
def apod():
    if request.method == 'POST':
        date=request.form.get('date')
        print(date)
        params = {'date': date}
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=<place-api-key>",params=params)
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            print(json.dumps(response,indent=4))
            hdurl=response['hdurl']
            explanation=response['explanation']
            title=response['title']
            if hdurl:
                return render_template('/navigate/apod.html',hdurl=hdurl,explanation=explanation,title=title,date=date)
        else :
            msg="please check if the selected date is correct."
            return render_template('/error/error.html',msg=msg)
    return render_template('/navigate/apod.html',hdurl=None)

@app.route('/neows',methods=['GET','POST'])
def neows():
    global links , ids , neo_reference_ids,names,nasa_jpl_urls,absolute_magnitude_hs,estimated_diameters,is_potentially_hazardous_asteroids,close_approach_datas
    links = []
    ids=[]
    neo_reference_ids=[]
    names=[]
    nasa_jpl_urls=[]
    absolute_magnitude_hs=[]
    estimated_diameters=[]
    is_potentially_hazardous_asteroids=[]
    close_approach_datas=[]
    if request.method == 'POST':
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        print(start_date,end_date)
        params = {'start_date': start_date,'end_date': end_date}
        response = requests.get("https://api.nasa.gov/neo/rest/v1/feed?api_key=<place-api-key>",params=params)
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            print(json.dumps(response,indent=4))
            count=0
            for key,value in response.items():
                if key == "near_earth_objects":
                    for k,v in value.items():
                        print('date: ', k)
                        #print('value',v)
                        for record in v:
                            count += 1
                            link = record.get('links')['self']
                            links.append(link.split())
                            id = record.get('id')
                            ids.append(id.split())
                            neo_reference_id = record.get('neo_reference_id')
                            neo_reference_ids.append(neo_reference_id.split())
                            name = record.get('name')
                            names.append(name.split())
                            nasa_jpl_url = record.get('nasa_jpl_url')
                            nasa_jpl_urls.append(nasa_jpl_url.split())
                            absolute_magnitude_h = record.get('absolute_magnitude_h')
                            absolute_magnitude_hs.append(str(absolute_magnitude_h))
                            estimated_diameter = record.get('estimated_diameter')
                            estimated_diameters.append(list(estimated_diameter.items()))
                            is_potentially_hazardous_asteroid=record.get('is_potentially_hazardous_asteroid')
                            is_potentially_hazardous_asteroids.append(str(is_potentially_hazardous_asteroid))
                            close_approach_data=record.get('close_approach_data')
                            close_approach_datas.append(close_approach_data)
                            print('Links :',link,'\n','ID :',id,'\n','NEO Reference ID :',neo_reference_id,'\n','Name :',name,'\n','NASA JPL URL :',nasa_jpl_url,'\n',
                            'ABSOLUTE MAGNITUDE :',absolute_magnitude_h,'\n','ESTIMATED DIAMETER : ',estimated_diameter,'\n','HAZARDOUS : ',is_potentially_hazardous_asteroid,'\n','CLOSE APPROACH DATE :',
                                    close_approach_data,'\n')
            print("----------------------------\n------------------------",links,"----------------------------\n------------------------",ids,"----------------------------\n------------------------",neo_reference_ids,"----------------------------\n------------------------"
            ,names,"----------------------------\n------------------------",nasa_jpl_urls,"----------------------------\n------------------------",absolute_magnitude_hs,"----------------------------\n------------------------",
            estimated_diameters,"----------------------------\n------------------------",is_potentially_hazardous_asteroids,"----------------------------\n------------------------", close_approach_datas)
            return render_template('/navigate/neows.html',id=ids,neo_reference_id=neo_reference_ids,name=names,nasa_jpl_url=nasa_jpl_urls,absolute_magnitude_h=absolute_magnitude_hs,
                    estimated_diameter=estimated_diameters,is_potentially_hazardous_asteroid=is_potentially_hazardous_asteroids,close_approach_data=close_approach_datas,length=count)
        else :
            msg="please check if the selected date is correct.Make sure there not more than 7 days gap in between the selected dates."
            return render_template('/error/error.html',msg=msg)
    return render_template('/navigate/neows.html')

@app.route('/donkiCME',methods=['GET','POST'])
def donki():
    #Coronal Mass Ejection (CME)
    global  instruments,cmeAnalyses,activityIDs,catalogs,startTimes,sourceLocations,activeRegionNums,CoronalLinks,CoronalNotes
    instruments=[]
    cmeAnalyses=[]
    activityIDs=[]
    catalogs=[]
    startTimes=[]
    sourceLocations=[]
    activeRegionNums=[]
    CoronalLinks=[]
    CoronalNotes=[]
    linkedEvents=[]
    if request.method == 'POST':
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        print(start_date,end_date)
        params = {'start_date': start_date,'end_date': end_date}
        response = requests.get("https://api.nasa.gov/DONKI/CME?api_key=<place-api-key>",params=params)
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            #print(json.dumps(response,indent=4))
            count =0 
            for item in response:
               count +=1
               activity_id = item['activityID']
               catalog =item['catalog']
               startTime = item['startTime']
               sourceLocation=item['sourceLocation']
               activeRegionNum=item['activeRegionNum']
               CoronalLink = item['link']
               CoronalNote=item['note']
               cmeAnalyse=item['cmeAnalyses']
               linkedEvent = item['linkedEvents']
               activityIDs.append(activity_id)
               catalogs.append(catalog)
               startTimes.append(startTime)
               sourceLocations.append(sourceLocation)
               activeRegionNums.append(activeRegionNum)
               CoronalLinks.append(CoronalLink)
               CoronalNotes.append(CoronalNote)
               cmeAnalyses.append(cmeAnalyse)
               linkedEvents.append(linkedEvent)
            return render_template('/navigate/donki/coronal_mass_ejection.html',id=activityIDs,catalog=catalogs,
            startTime=startTimes,sourceLocation = sourceLocations,activeRegion=activeRegionNums,links=CoronalLinks,notes=CoronalNotes,
            cmeAnalyse=cmeAnalyses,events=linkedEvents,length=count)
        else :
            msg="please check if the selected date is correct.Make sure there not more than 7 days gap in between the selected dates."
            return render_template('/error/error.html',msg=msg)
    return render_template('/navigate/donki/coronal_mass_ejection.html')

if __name__ == "__main__":
    app.run(debug=True)