import base64

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import json
from base64 import decodebytes
from PIL import Image
from io import BytesIO
# in the form of a string which will be added to the given url
# used to look up quite honestly anything on wikipedia
main = Flask(__name__)


uname = ""
images = ""

if __name__ == '__main__':
    # webSite.debug = True
    main.run()

@main.route('/')
def instructions():
    return render_template('index.html')




@main.route('/loggedIN', methods = ['post'])
def instructions2():
    pws = request.form["psw"]
    urlEncrypt = 'https://realpython-example-app2.herokuapp.com/?username='+pws
    # returnFromRequest = requests.get(urlEncrypt)
    # encryptPW = decode_to_string(returnFromRequest)
    pws = requests.get(urlEncrypt).content
    uname = request.form["uname"]


    urlRules = 'https://team-anything-microservice.herokuapp.com/get_rules'
    jsonresponse = requests.get(urlRules).json()
    rules = jsonresponse['deal']
    objective = jsonresponse['objective']
    pack = jsonresponse['pack']
    rank =  jsonresponse['rank']
    score = jsonresponse['score']
    link = jsonresponse['youtube']
    urlImages = 'https://team-anything-microservice.herokuapp.com/get_images'
    # images = requests.get(urlImages).json()
    # byte_array = bytes(images)
    # images_decoded = base64.decodebytes(byte_array)
    # images_decoded = BytesIO(images_decoded)

    return render_template("loggedIn.html", name = uname, rules = rules, objective = objective, pack = pack , rank = rank, score = score, link = link, pws = pws)

# @main.route('/getImages')
# def instructions3():
#     urlImages = 'https://team-anything-microservice.herokuapp.com/get_images'
#
#     # returnFromRequest = requests.get(urlEncrypt)
#     # encryptPW = decode_to_string(returnFromRequest)
#     return requests.get(urlImages).content
