from flask import Flask, request, render_template, send_from_directory
import requests
from PIL import Image, ImageDraw
import sys
import xml.etree.ElementTree as ET
import os
import traceback
import random
import json
from pprint import pprint
import matplotlib.pyplot as plt
from flask import jsonify
from flask_cors import CORS
from datetime import timedelta  
from flask import  make_response, request, current_app  
from functools import update_wrapper
from flask import send_file
import string
import random

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
#CORS(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

    
'''@app.route("/upload/", methods=["POST","GET"])
def upload():
    target = os.path.join(APP_ROOT, 'images')
    #target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
          os.mkdir(target)
    else:
       print("Couldn't create upload directory: {}".format(target))
    print("zzzzzzzz"+ str (request.files.getlist("file")))
    
    for upload in request.files.getlist("file"):
        print("zzzzzzzzz")
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
     url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/d836ee83-9a1b-457f-8b3e-37967827568c/LabelFile/'
        data = {'file': open(destination, 'rb')}
        response = requests.post(url, auth=requests.auth.HTTPBasicAuth('B7cxMinB_wZrMyemi04FjuHgprZLuBCM', ''), files=data)
        os.remove("C:/Users/Helmi/Desktop/data1.txt")
        fichier = open("C:/Users/Helmi/Desktop/data1.txt", "a")
        fichier.write(response.text)
        fichier.close()
    #return send_from_directory("images", filename, as_attachment=True) 
    return render_template("upload.html", image_name=filename)'''

@app.route('/upload/<filename>')
def send_image(filename):
    #return send_file(filename, mimetype='images/')
    return send_from_directory("images", filename)

'''@app.route('/count',methods=["POST","GET"])
def Comptage():

    print("hello from contage")
    f = open("C:/Users/Helmi/Desktop/storage_path.txt", "r")
    destination=f.read()
    return jsonify(destination)'''
    
@app.route('/count2',methods=["GET"])
def draw_rectangle(im, coordinates, color, width=1):
    drawing = ImageDraw.Draw(im)
    
    for i in range(width):       
        rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)    
        rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)  
        drawing.rectangle((rect_start, rect_end))       
	#del drawing
    return im

@app.route('/drow/',methods=["POST"])
def Drow():
    #os.remove("C:/Users/Helmi/Desktop/website/static/imagesOutfile.jpg")
    f = open("C:/Users/Helmi/Desktop/storage_path.txt", "r")
    destination=f.read()
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/d836ee83-9a1b-457f-8b3e-37967827568c/LabelFile/'
    data = {'file': open(destination, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('B7cxMinB_wZrMyemi04FjuHgprZLuBCM', ''), files=data)
    os.remove("C:/Users/Helmi/Desktop/data1.txt")
    fichier = open("C:/Users/Helmi/Desktop/data1.txt", "a")
    fichier.write(response.text)
    fichier.close()
    xmax=[]
    xmin=[]
    ymax=[]
    ymin=[]
    with open('C:/Users/Helmi/Desktop/data1.txt') as f:
        data = json.load(f)
        for i in range (len (data['result'][0]['prediction'])):
            xmax.append(data['result'][0]['prediction'][i]['xmax'])
            xmin.append(data['result'][0]['prediction'][i]['xmin'])
            ymin.append(data['result'][0]['prediction'][i]['ymin'])
            ymax.append(data['result'][0]['prediction'][i]['ymax'])

    im = Image.open(destination)
    r_color = lambda: 200
    print("aaaaaaaaaaa")
    for i in range(len (data['result'][0]['prediction'])):
        im = draw_rectangle(im, [(xmin[i], ymin[i]), (xmax[i], ymax[i])], r_color, 3)
    random_txt=id_generator()
    filename="Outfile"+str(random_txt)+".jpg"
    target = target = "C://Users/Helmi/Desktop/website/images/"
    destination2 = str(target)+str(filename)
    im.save(destination2) 
    print(str(destination2))
    print(str(filename))

    nbr_orange= len (data['result'][0]['prediction'])
    poids=(nbr_orange*5*200)/1000
    os.remove("C:/Users/Helmi/Desktop/poids.txt")
    fichier = open("C:/Users/Helmi/Desktop/poids.txt", "a")
    fichier.write(str(poids))
    fichier.close()

    msg='Le poids estimer pour cet arbre est '+ str ((nbr_orange*5*200)/1000)+' KG'
    print(msg)
    return render_template("Count.html", image_name=filename,  msg=msg )
    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
@app.route('/drow/<filename>')
def get_image(filename):
    #return send_file(filename, mimetype='images/')
    print(filename)
    return send_from_directory("C:/Users/Helmi/Desktop/website/images/", filename)

@app.route('/estimate', methods=[ 'POST'])
def estimate():
 
    nb_arbre= request.form['nb']
    print(nb_arbre)
    f = open("C:/Users/Helmi/Desktop/poids.txt", "r")
    poids=f.read()
    poids_Total=float(poids)*float(nb_arbre)
    msg1='Le poids Total estimer pour ce champs est '+ str (poids_Total)+' KG'
    return render_template("Count.html",  msg1=msg1 )

@app.route("/upload2/", methods=["POST","GET"])
def upload2():
    target = "C://Users/Helmi/Desktop/website/images/"
    #target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
          os.mkdir(target)
    else:
       print("Couldn't create upload directory: {}".format(target))
    print("zzzzzzzz"+ str (request.files.getlist("file")))
    
    for upload in request.files.getlist("file"):
        print("zzzzzzzzz")
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = str(target)+str(filename)
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        os.remove("C:/Users/Helmi/Desktop/storage_path.txt")
        fichier = open("C:/Users/Helmi/Desktop/storage_path.txt", "a")
        fichier.write(destination)
        fichier.close()

    #return send_from_directory("images", filename, as_attachment=True) 
        return render_template("upload.html", image_name=filename)

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0", port=8000)