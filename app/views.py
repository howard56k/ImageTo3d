from app import app
from app import q
from app.tasks import imageEmailAndCreate
from flask import render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import random
import string
from rq import Retry
import pickle
import datetime
from PIL import Image 
from app.imageto3dWrapper import imageTo3d

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def png2jpg(filename):
    im = Image.open("{}".format(filename)) 
    rgb_im = im.convert("RGB") 
    imgFolderPath, _ = os.path.splitext(filename)
    fullImgPath = "{}.jpg".format(imgFolderPath)
    rgb_im.save(fullImgPath)
    return fullImgPath


app.config["IMAGE_UPLOADS"] = "./model/image"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            effectType = request.form['radioEffect']
            email = request.form['email']
            image = request.files["images"]
            if image.filename != "":

                #MAKES SURE FILE NAME IS SECURE AND IS NOT MALICIOUS 
                filename = secure_filename(image.filename)          

                _, file_extension = os.path.splitext(filename)
                
                convertToJpg = False
                if file_extension.lower() == '.png' or file_extension.lower() == '.jpeg':
                    convertToJpg = True
                filename = str(randomString(12))

                imgFolderPath = "{}/{}".format(app.config["IMAGE_UPLOADS"], filename)
                imgFullPath = os.path.join(imgFolderPath, filename+file_extension)

                if(os.path.isfile(imgFullPath)):
                    #CHECKS FOR WEIRD EDGE CASES IF THE FILE IS A REPEAT
                    while(os.path.isfile(imgFullPath)):
                        filename = str(randomString(12))
                        imgFullPath = os.path.join(imgFolderPath, filename+file_extension)
                    os.mkdir(imgFolderPath)
                    image.save(os.path.join(imgFolderPath, filename+file_extension))
                    if convertToJpg:
                        temp = png2jpg(imgFullPath)
                        imgFullPath = temp
                else:
                    os.mkdir(imgFolderPath)
                    image.save(os.path.join(imgFolderPath, filename+file_extension))
                    if convertToJpg:
                        temp = png2jpg(imgFullPath)
                        imgFullPath = temp

                waitTime = str(datetime.timedelta(seconds=((len(q) + 1) * 900)))
                
                imageOBJ = imageTo3d(filename, effectType, email,waitTime)
                with open('./model/pickles/{}.obj'.format(filename), 'wb') as handle:
                    pickle.dump(imageOBJ, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
                #adds CONVERTING IMAGE TO 3d to a task queue
                jobs = q.jobs
                url = request.args.get("url")
                task = q.enqueue(imageEmailAndCreate, imageOBJ, job_timeout=4620, retry=Retry(max=2))
                jobs = q.jobs
                q_len = len(q)


                return redirect("/email/{}".format(filename))
            else:
                return redirect("/")
            

    return render_template("public/upload_image.html")

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")



@app.route("/email/<filename>", methods=["GET"])
def email(filename):
    print(os.getcwd())
    notFound = True
    imgFileNameMatch = ""
    for i in os.listdir('./model/pickles'):
        if filename in os.path.splitext(i)[0]:
            print(i)
            imgFileNameMatch = i
            notFound = False
            continue
    if(notFound):
        return redirect("/")
    else:
        filename = imgFileNameMatch
        with open('./model/pickles/{}'.format(filename), 'rb') as handle:
            imageOBJ = pickle.load(handle)
        return render_template("public/postSubmit.html", Email=imageOBJ.email,waitTime=imageOBJ.waitTime)

        

    
