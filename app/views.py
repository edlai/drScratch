#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, HttpResponseServerError
from django.utils.datastructures import MultiValueDictKeyError
from django.core.context_processors import csrf
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from django.template import Context, loader
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate,get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext as _
from django.utils.encoding import force_bytes
from django.db.models import Avg
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from app.models import Project, Dashboard, Attribute, Game,\
    ChallengesOfTournament, CreatorHash, Coder
from app.models import Dead, Sprite, Mastery, Duplicate, File, CSVs
from app.models import Creator, Participant, Tournament, Team
from background_task.models import Task
from app.tasks import *
from app.models import Teacher, Organization, OrganizationHash, Challenge
from app.forms import UploadFileForm, UserForm, NewUserForm, UrlForm, TeacherForm,\
    UpdateForm, TeamForm, TournamentForm
from app.forms import OrganizationForm, OrganizationHashForm, LoginForm, EditTournamentForm, ParticipantForm, ChallengeForm, CreatorForm
from django.contrib.auth.models import User
from datetime import datetime,timedelta,date
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
#from email.MIMEText import MIMEText
from django.utils.encoding import smart_str
import re
import smtplib
import email.utils
import os
import ast
import json
import sys
import urllib2
import shutil
import unicodedata
import csv
import kurt
import zipfile
import copy
from zipfile import ZipFile
from django.template.context import RequestContext
from pickle import NONE
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Stats

from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError

import analyzer
import spriteNaming
import backdropNaming
import duplicateScripts
import deadCode

#Global variables
#pMastery = "hairball -p mastery.Mastery "
pDuplicateScript = "D:\home\Python27\Scripts\hairball -p duplicate.DuplicateScripts "
pSpriteNaming = "D:\home\Python27\Scripts\hairball -p convention.SpriteNaming "
pDeadCode = "D:\home\Python27\Scripts\hairball -p blocks.DeadCode "
pInitialization = "D:\home\Python27\Scripts\hairball -p initialization.AttributeInitialization "

#Tournaments constants
paginator_creator_challenges=3
paginator_creator_teams=3
paginator_creator_tournaments=3
paginator_participant_teams=1
max_participants_per_team=5
max_teams_per_tournament=4
max_challenges_per_tournament=4
paginator_participant_touraments=1
paginator_creator_progress_teams=1
paginator_validate_games=4
max_new_participants=20

#_____________________________ MAIN ______________________________________#

def main(request):
    """Main page"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    # The first time one user enters
    # Create the dashboards associated to users
    createDashboards()
    return render_to_response('main/main.html',
                                {'user':user},
                                RC(request))

#___________________________ REDIRECT ____________________________________#

def redirectMain(request):
    """Page not found redirect to main"""
    return HttpResponseRedirect('/')

#_______________________________ ERROR ___________________________________#

def error404(request):
    response = render_to_response('404.html', {},
                                  context_instance = RC(request))
    response.status_code = 404
    return response

def error500(request):
    response = render_to_response('500.html', {},
                                  context_instance = RC(request))
    return response

def proc_mastery(request,lines, filename):
    """Returns the information of Mastery"""


    dic = {}
    lLines = lines.split('\n')
    d = {}
    d = ast.literal_eval(lLines[1])
    lLines = lLines[2].split(':')[1]
    points = int(lLines.split('/')[0])
    maxi = int(lLines.split('/')[1])

    #Save in DB
    filename.score = points
    filename.abstraction = d["Abstraction"]
    filename.parallelization = d["Parallelization"]
    filename.logic = d["Logic"]
    filename.synchronization = d["Synchronization"]
    filename.flowControl = d["FlowControl"]
    filename.userInteractivity = d["UserInteractivity"]
    filename.dataRepresentation = d["DataRepresentation"]
    filename.save()

    #Translation
    d_translated = translate(request,d, filename)

    dic["mastery"] = d_translated
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi

    return dic


def proc_duplicate_script(lines, filename):


    dic = {}
    number = 0
    lLines = lines.split('\n')
    #if len(lLines) > 2:
    number = lLines[0][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number

    #Save in DB
    filename.duplicateScript = number
    filename.save()

    return dic


def proc_sprite_naming(lines, filename):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal

    #Save in DB
    filename.spriteNaming = str(number)
    filename.save()

    return dic


def proc_backdrop_naming(lines, filename):

    dic = {}
    lLines = lines.split('\n')
    number = lLines[0].split(' ')[0]
    lObjects = lLines[1:]
    lfinal = lObjects[:-1]
    dic['backdropNaming'] = dic
    dic['backdropNaming']['number'] = str(number)
    dic['backdropNaming']['backdrop'] = lfinal

    #Save in DB
    filename.backdropNaming = str(number)
    filename.save()

    return dic



def proc_dead_code(lines, filename):
    
    dic = {}
    dead_code = lines.split("\n")[1:]
    iterator = 0
    lcharacter = []
    lblocks = []
    if dead_code:
        d = ast.literal_eval(dead_code[0])
        keys = d.keys()
        values = d.values()
        items = d.items()

        for keys, values in items:
            lcharacter.append(keys)
            lblocks.append(values) 
            iterator += 1
    dic = {}
    dic["deadCode"] = dic
    dic["deadCode"]["number"] = iterator
    number = len(lcharacter)
    for i in range(number):
        dic["deadCode"][str(lcharacter[i])] = str(lblocks[i])

    #Save in DB
    filename.deadCode = iterator
    filename.save()

    return dic


def check_version(filename):
    """Check the version of the project and return it"""

    extension = filename.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    elif extension == 'sb3':
        version = '3.0'
    else:
        version = '1.4'

    return version

def analyze_project(request, file_name, filename):


    dictionary = {}
    
    if os.path.exists(file_name):
        
        list_file = file_name.split('(')
       
        #if len(list_file) > 1:
        #    file_name = list_file[0] + '\(' + list_file[1]
        #    list_file = file_name.split(')')
        #    file_name = list_file[0] + '\)' + list_file[1]


        resultMastery = analyzer.main(file_name)
        resultSpriteNaming = spriteNaming.main(file_name)
        resultBackdropNaming = backdropNaming.main(file_name)
        resultDuplicateScript = duplicateScripts.main(file_name)
        resultDeadCode = deadCode.main(file_name)

             
        #Create a dictionary with necessary information
        dictionary.update(proc_mastery(request,resultMastery, filename))
        dictionary.update(proc_sprite_naming(resultSpriteNaming, filename))
        dictionary.update(proc_backdrop_naming(resultBackdropNaming, filename))
        dictionary.update(proc_duplicate_script(resultDuplicateScript, filename))
        dictionary.update(proc_dead_code(resultDeadCode, filename))
        #dictionary.update(proc_initialization(resultInitialization, filename))
        #code = {'dupCode':duplicate_script_scratch_block(resultDuplicateScript)}
        #dictionary.update(code)
        #code = {'dCode':dead_code_scratch_block(resultDeadCode)}
        #dictionary.update(code)


        return dictionary

    else:
        return HttpResponseRedirect('/')

def _upload(request):
    """Upload file from form POST for unregistered users"""


    if request.method == 'POST':
        #Revise the form in main
        #If user doesn't complete all the fields,it'll show a warning
        try:
            file = request.FILES['zipFile']
        except:
            d = {'Error': 'MultiValueDict'}
            return  d

        
        # Create DB of files
        now = datetime.now()
        method = "project"
        filename = File (filename = file.name.encode('utf-8'),
                        organization = "",
                        method = method , time = now,
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0)
        filename.save()

        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(filename.id) + ".sb3"

        # Version of Scratch 1.4Vs2.0Vs3.0
        version = check_version(filename.filename)
        if version == "1.4":
            fileSaved = dir_zips + str(filename.id) + ".sb"
        elif version == "2.0":
            fileSaved = dir_zips + str(filename.id) + ".sb2"
        else:
            fileSaved = dir_zips + str(filename.id) + ".sb3"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(filename.filename) + "\t\t\t" + \
            "ID: " + str(filename.id) + "\t\t\t" + \
            "Method: " + str(filename.method) + \
            "\t\t\tTime: " + str(filename.time) + "\n")


       
        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)

        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


        # Analyze the scratch project
        try:
            d = analyze_project(request, file_name, filename)
        except:
            #There ir an error with kutz or hairball
            #We save the project in folder called error_analyzing
            filename.method = 'project/error'
            filename.save()
            oldPathProject = fileSaved
            newPathProject = fileSaved.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             fileSaved.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}
            return d
        # Show the dashboard
        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'

        return d
    
    else:
        return HttpResponseRedirect('/')

def process_string_url(url):
    """Process String of URL from Form"""


    idProject = ''
    auxString = url.split("/")[-1]
    if auxString == '':
        # we need to get the other argument
        possibleId = url.split("/")[-2]
        if possibleId == "#editor":
            idProject = url.split("/")[-3]
        else:
            idProject = possibleId
    else:
        if auxString == "#editor":
            idProject = url.split("/")[-2]
        else:
            # To get the id project
            idProject = auxString
    try:
        checkInt = int(idProject)
    except ValueError:
        idProject = "error"

    return idProject

def new_getSb3(file_name, dir_zips,fileName):
    if zipfile.is_zipfile(file_name):
        os.rename(dir_zips + "project.json",dir_zips + str(fileName.id) + ".sb3")
    else:
        current = os.getcwd()
        os.chdir(dir_zips)
        with ZipFile(str(fileName.id) + ".sb3", 'w') as myzip:
            myzip.write("project.json")
        os.chdir(current)
        try:
            os.remove(dir_zips + "project.json")
        except:
            print "No existe"

    file_name = dir_zips + str(fileName.id) + ".sb3"
   
    return file_name

def send_request_getSb3(idProject, username, method):
    """First request to getSb3"""

    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    try:
        os.remove(dir_zips + "project.json")
    except:
        print "No existe"

    getRequestSb3 = "https://projects.scratch.mit.edu/" + idProject + "/get"
    fileURL = idProject + ".sb3"

    # Create DB of files
    now = datetime.now()

    if Organization.objects.filter(username=username):
        fileName = File (filename = fileURL,
                         organization = username,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    elif Coder.objects.filter(username = username):
        fileName = File (filename = fileURL,
                         coder = username,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    else:
        fileName = File (filename = fileURL,
                         method = method , time = now,
                         score = 0, abstraction = 0, parallelization = 0,
                         logic = 0, synchronization = 0, flowControl = 0,
                         userInteractivity = 0, dataRepresentation = 0,
                         spriteNaming = 0 ,initialization = 0,
                         deadCode = 0, duplicateScript = 0)
    
    fileName.save()
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_zips + "project.json"

    #Write the activity in log
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + \
        "\t\t\t" + "Time: " + str(fileName.time) + "\n")

    
    # Save file in server
    counter = 0

    file_name = handler_upload(fileSaved, counter)
    outputFile = open(file_name, 'wb')
    try:
        sb3File = urllib2.urlopen(getRequestSb3)
        outputFile.write(sb3File.read())
        outputFile.close()
    except:
        outputFile.write("ERROR downloading")
        outputFile.close()
    

    #New getSb3
    file_name = new_getSb3(file_name, dir_zips,fileName)
    

    return (file_name, fileName)

def generator_dic(request, idProject):
    """Returns dictionary with analyzes and errors"""


    if idProject == "error":
        d = {'Error': 'id_error'}

        return d

    else:
        try:
            if request.user.is_authenticated():
                username = request.user.username
            else:
                username = None
            method = "url"
            (pathProject, file) = send_request_getSb3(idProject,
                                                      username, 
                                                      method)
        except:
            #When your project doesn't exist
            d = {'Error': 'no_exists'}

            return d


        try:
            d = analyze_project(request, pathProject, file)
        except:
            #There is an error with kutz or hairball
            #We save the project in folder called error_analyzing
            file.method = 'url/error'
            file.save()
            oldPathProject = pathProject
            newPathProject = pathProject.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             pathProject.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}

            return d

        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'

        return d
   
def _url(request):
    """Process Request of form URL"""


    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = process_string_url(url)
            d = generator_dic(request,idProject)
            return d
        else:
            d = {'Error': 'MultiValueDict'}

            return  d
    else:

        return HttpResponseRedirect('/')

#_______________________ TO UNREGISTERED USER ___________________________#

def selector(request):
    if request.method == 'POST':
        error = False
        id_error = False
        no_exists = False
        if "_upload" in request.POST:
            d = _upload(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            else:
                filename = request.FILES['zipFile'].name.encode('utf-8')
                dic = {'url': "",'filename':filename}
                d.update(dic)
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
        elif '_url' in request.POST:
            d = _url(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return render_to_response('main/main.html',
                            {'error':error},
                            RC(request))
            elif d['Error'] == 'id_error':
                id_error = True
                return render_to_response('main/main.html',
                            {'id_error':id_error},
                            RC(request))
            elif d['Error'] == 'no_exists':
                no_exists = True
                return render_to_response('main/main.html',
                    {'no_exists':no_exists},
                    RC(request))
            else:
                form = UrlForm(request.POST)
                url = request.POST['urlProject']
                filename = url
                dic = {'url': url, 'filename':filename}
                d.update(dic)
                if d["mastery"]["points"] >= 15:
                    return render_to_response("upload/dashboard-unregistered-master.html", d)
                elif d["mastery"]["points"] > 7:
                    return render_to_response("upload/dashboard-unregistered-developing.html", d)
                else:
                    return render_to_response("upload/dashboard-unregistered-basic.html", d)
    else:
        return HttpResponseRedirect('/')



def handler_upload(fileSaved, counter):
    """ Necessary to uploadUnregistered"""
    # If file exists,it will save it with new name: name(x)
    if os.path.exists(fileSaved):
        counter = counter + 1
        #Check the version of Scratch 1.4Vs2.0
        version = checkVersion(fileSaved)
        if version == "2.0":
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb2"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb2"
        else:
            if counter == 1:
                fileSaved = fileSaved.split(".")[0] + "(1).sb"
            else:
                fileSaved = fileSaved.split('(')[0] + "(" + str(counter) + ").sb"


        file_name = handler_upload(fileSaved, counter)
        return file_name
    else:
        file_name = fileSaved
        return file_name


def checkVersion(fileName):
    extension = fileName.split('.')[-1]
    if extension == 'sb2':
        version = '2.0'
    else:
        version = '1.4'
    return version


#_______________________Project Analysis Project___________________#

def uploadUnregistered(request):
    """Upload file from form POST for unregistered users"""
    if request.method == 'POST':
        #Revise the form in main
        #If user doesn't complete all the fields,it'll show a warning
        try:
            file = request.FILES['zipFile']
        except:
            d = {'Error': 'MultiValueDict'}
            return  d
        # Create DB of files
        now = datetime.now()
        method = "project"
        fileName = File (filename = file.name.encode('utf-8'),
                        organization = "",
                        method = method , time = now,
                        score = 0, abstraction = 0, parallelization = 0,
                        logic = 0, synchronization = 0, flowControl = 0,
                        userInteractivity = 0, dataRepresentation = 0,
                        spriteNaming = 0 ,initialization = 0,
                        deadCode = 0, duplicateScript = 0)
        fileName.save()
        dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
        fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Version of Scratch 1.4Vs2.0
        version = checkVersion(fileName.filename)
        if version == "1.4":
            fileSaved = dir_zips + str(fileName.id) + ".sb"
        else:
            fileSaved = dir_zips + str(fileName.id) + ".sb2"

        # Create log
        pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
        logFile = open (pathLog + "logFile.txt", "a")
        logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
        str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
        "Time: " + str(fileName.time) + "\n")

        # Save file in server
        counter = 0
        file_name = handler_upload(fileSaved, counter)

        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        #Create 2.0Scratch's File
        file_name = changeVersion(request, file_name)

        # Analyze the scratch project
        try:
            d = analyzeProject(request, file_name, fileName)

        except:
            #There ir an error with kutz or hairball
            #We save the project in folder called error_analyzing
            fileName.method = 'project/error'
            fileName.save()
            oldPathProject = fileSaved
            newPathProject = fileSaved.split("/uploads/")[0] + \
                             "/error_analyzing/" + \
                             fileSaved.split("/uploads/")[1]
            shutil.copy(oldPathProject, newPathProject)
            d = {'Error': 'analyzing'}
            return d
        # Show the dashboard
        # Redirect to dashboard for unregistered user
        d['Error'] = 'None'
        return d
    else:
        return HttpResponseRedirect('/')



def changeVersion(request, file_name):
    p = kurt.Project.load(file_name)
    p.convert("scratch20")
    p   .save()
    file_name = file_name.split('.')[0] + '.sb2'
    return file_name



#_______________________URL Analysis Project_________________________________#


def urlUnregistered(request):
    """Process Request of form URL"""
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            d = {}
            url = form.cleaned_data['urlProject']
            idProject = processStringUrl(url)
            if idProject == "error":
                d = {'Error': 'id_error'}
                return d
            else:
                try:
                    organization = ""
                    method = "url"
                    (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                except:
                    #When your project doesn't exist
                    d = {'Error': 'no_exists'}
                    return d
                try:
                    d = analyzeProject(request, pathProject, file)
                except:
                    #There ir an error with kutz or hairball
                    #We save the project in folder called error_analyzing
                    file.method = 'url/error'
                    file.save()
                    oldPathProject = pathProject
                    newPathProject = pathProject.split("/uploads/")[0] + \
                                     "/error_analyzing/" + \
                                     pathProject.split("/uploads/")[1]
                    shutil.copy(oldPathProject, newPathProject)
                    d = {'Error': 'analyzing'}
                    return d

                #Create Json
                djson = createJson(d)

                # Redirect to dashboard for unregistered user
                d['Error'] = 'None'
                return d
        else:
            d = {'Error': 'MultiValueDict'}
            return  d
    else:
        return HttpResponseRedirect('/')


def processStringUrl(url):
    """Process String of URL from Form"""
    idProject = ''
    auxString = url.split("/")[-1]
    if auxString == '':
        # we need to get the other argument
        possibleId = url.split("/")[-2]
        if possibleId == "#editor":
            idProject = url.split("/")[-3]
        else:
            idProject = possibleId
    else:
        if auxString == "#editor":
            idProject = url.split("/")[-2]
        else:
            # To get the id project
            idProject = auxString
    try:
        checkInt = int(idProject)
    except ValueError:
        idProject = "error"
    return idProject

def sendRequestgetSB2(idProject, organization, method):
    """First request to getSB2"""
    getRequestSb2 = "http://drscratch.cloudapp.net:8080/" + idProject
    fileURL = idProject + ".sb2"
    # Create DB of files
    now = datetime.now()
    fileName = File (filename = fileURL,
                     organization = organization,
                     method = method , time = now,
                     score = 0, abstraction = 0, parallelization = 0,
                     logic = 0, synchronization = 0, flowControl = 0,
                     userInteractivity = 0, dataRepresentation = 0,
                     spriteNaming = 0 ,initialization = 0,
                     deadCode = 0, duplicateScript = 0)
    fileName.save()
    dir_zips = os.path.dirname(os.path.dirname(__file__)) + "/uploads/"
    fileSaved = dir_zips + str(fileName.id) + ".sb2"
    pathLog = os.path.dirname(os.path.dirname(__file__)) + "/log/"
    logFile = open (pathLog + "logFile.txt", "a")
    logFile.write("FileName: " + str(fileName.filename) + "\t\t\t" + "ID: " + \
    str(fileName.id) + "\t\t\t" + "Method: " + str(fileName.method) + "\t\t\t" + \
    "Time: " + str(fileName.time) + "\n")
    # Save file in server
    counter = 0
    file_name = handler_upload(fileSaved, counter)
    outputFile = open(file_name, 'wb')
    sb2File = urllib2.urlopen(getRequestSb2)
    outputFile.write(sb2File.read())
    outputFile.close()
    return (file_name, fileName)



#________________________ CREATE JSON _________________________________#

def createJson(d):
    flagsPlugin = {"Mastery":0, "DeadCode":0, "SpriteNaming":1, "Initialization":0, "DuplicateScripts":0}


#________________________ LEARN MORE __________________________________#

def learn(request,page):
    #Unicode to string(page)
    page = unicodedata.normalize('NFKD',page).encode('ascii','ignore')

    dic = {'Pensamiento':'Logic',
           'Paralelismo':'Parallelism',
          'Representacion':'Data representation',
          'Sincronizacion':'Synchronization',
          'Interactividad':'User interactivity',
          'Control':'Flow control',
          'Abstraccion':'Abstraction'}

    if page in dic:
        page = dic[page]

    page = "learn/" + page + ".html"

    if request.user.is_authenticated():

        return render_to_response(page,
                                RC(request))
    else:

        return render_to_response(page,
                                RC(request))

def learnUnregistered(request):

    return render_to_response("learn/learn-unregistered.html",)

#________________________ COLLABORATORS _____________________________#

def collaborators(request):

    return render_to_response("main/collaborators.html",)


#________________________ TO REGISTER ORGANIZATION __________________#

def organizationHash(request):
    """Method for to sign up in the platform"""
    if request.method == "POST":
        form = OrganizationHashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/organizationHash')
    elif request.method == 'GET':
        return render_to_response("sign/organizationHash.html", context_instance = RC(request))

def signUpOrganization(request):
    """Method which allow to sign up organizations"""
    flagHash = 0
    flagName = 0
    flagEmail = 0
    flagForm = 0
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashkey = form.cleaned_data['hashkey']

            try:
                #This name already exists
                organization = Organization.objects.get(username=username)
                flagName = 1
                return render_to_response("sign/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
            except:
                try:
                    #This email already exists
                    email = Organization.objects.get(email=email)
                    flagEmail = 1
                    return render_to_response("sign/signup_error.html",
                                            {'flagName':flagName,
                                            'flagEmail':flagEmail,
                                            'flagHash':flagHash,
                                            'flagForm':flagForm},
                                            context_instance = RC(request))
                except:
                    try:
                        organizationHashkey = OrganizationHash.objects.get(hashkey=hashkey)
                        organizationHashkey.delete()
                        organization = Organization.objects.create_user(username = username, email=email, password=password, hashkey=hashkey)
                        organization = authenticate(username=username, password=password)
                        user=Organization.objects.get(email=email)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token=default_token_generator.make_token(user)
                        c = {
                                'email':email,
                                'uid':uid,
                                'token':token}

                        body = render_to_string("sign/email.html",c)
                        subject = "Welcome to Dr.Scratch for organizations"
                        sender ="afdezroig@gmail.com"
                        to = [email]
                        email = EmailMessage(subject,body,sender,to)
                        #email.attach_file("static/app/images/logo_main.png")
                        email.send()
                        login(request, organization)
                        return HttpResponseRedirect('/organization/' + organization.username)

                    except:
                        #Doesn't exist this hash
                        flagHash = 1

                        return render_to_response("sign/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
        else:
            flagForm = 1
            return render_to_response("sign/signup_error.html",
                  {'flagName':flagName,
                   'flagEmail':flagEmail,
                   'flagHash':flagHash,
                   'flagForm':flagForm},
                  context_instance = RC(request))

    elif request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/organization/' + request.user.username)
        else:
            return render_to_response("sign/organization.html", context_instance = RC(request))

#_________________________ TO SHOW ORGANIZATION'S DASHBOARD ___________#

def loginOrganization(request):
    """Log in app to user"""
    if request.method == 'POST':
        flag = False
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            organization = authenticate(username=username, password=password)
            if organization is not None:
                if organization.is_active:
                    login(request, organization)
                    try:
                        Organization.objects.get(username=username)
                        return HttpResponseRedirect('/organization/' + organization.username)
                    except Organization.DoesNotExist:
                        flag = True
                        return render_to_response("password/user_doesntorg.html",
                                            {'flag': flag, 'username':request.user.username},
                                            context_instance=RC(request))
            else:
                flag = True
                return render_to_response("password/user_doesntexist.html",
                                            {'flag': flag},
                                            context_instance=RC(request))

    else:
        return HttpResponseRedirect("/")


def logoutOrganization(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

def organization(request, name):
    if request.method == 'GET':
        if request.user.is_authenticated():
            username = request.user.username
            if username == name:
                try:
                    user = Organization.objects.get(username=username)
                except Organization.DoesNotExist:
                    flag = True
                    return render_to_response("password/user_doesntorg.html",
                                            {'flag': flag, 'username':request.user.username},
                                            context_instance=RC(request))
                date_joined= user.date_joined
                end = datetime.today()
                y = end.year
                m = end.month
                d = end.day
                end = date(y,m,d)
                y = date_joined.year
                m = date_joined.month
                d = date_joined.day
                start = date(y,m,d)
                dateList = date_range(start, end)
                daily_score = []
                mydates = []
            
                for n in dateList:
                    mydates.append(n.strftime("%d/%m"))
                    points = File.objects.filter(organization=username).filter(time=n)
                    points = points.aggregate(Avg("score"))["score__avg"]
                    daily_score.append(points)
            
                for n in daily_score:
                    if n==None:
                        daily_score[daily_score.index(n)]=0
            
            
                dic={"date":mydates,"daily_score":daily_score,'username':username}
                return render_to_response("main/main_organization.html",
                        dic,
                        context_instance = RC(request))
            else:
                return render_to_response("sign/organization.html",
                                        context_instance = RC(request))
        return render_to_response("sign/organization.html", context_instance = RC(request))
    else:
        return HttpResponseRedirect("/")
    

#________________________ ANALYZE CSV FOR ORGANIZATIONS ____________#

def analyzeCSV(request):
    if request.method =='POST':
        if "_upload" in request.POST:
            csv_data = 0
            flag_csv = False
            file = request.FILES['csvFile']
            file_name = file.name.encode('utf-8')
            dir_csvs = os.path.dirname(os.path.dirname(__file__)) + "/csvs/" + file_name
            #Save file .csv
            with open(dir_csvs, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            infile = open(dir_csvs, 'r')
            dictionary = {}
            for line in infile:
                row = len(line.split(","))
                type_csv = ""
                organization = request.user.username
                if row == 2:
                    type_csv = "2_row"
                    code = line.split(",")[0]
                    url = line.split(",")[1]
                    url = url.split("\n")[0]
                    method = "csv"
                    print "ESTE" + str(url) + "VALE"
                    if url.isdigit():
                        print "FUNCIONA"
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]



                    try:
                        (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                        d = analyzeProject(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    dic = {}
                    dic[line] = d
                    dictionary.update(dic)
                elif row == 1:
                    type_csv = "1_row"
                    url = line.split("\n")[0]
                    method = "csv"
                    if url.isdigit():
                        idProject = url
                    else:
                        slashNum = url.count('/')
                        if slashNum == 4:
                            idProject = url.split("/")[-1]
                        elif slashNum == 5:
                            idProject = url.split('/')[-2]



                    try:
                        (pathProject, file) = sendRequestgetSB2(idProject, organization, method)
                        d = analyzeProject(request, pathProject, file)
                    except:
                        d = ["Error analyzing project", url]

                    dic = {}
                    dic[url] = d
                    dictionary.update(dic)
            infile.close()
            try:
                csv_data = generatorCSV(request, dictionary, file_name, type_csv)
                flag_csv = True
            except:
                flag_csv = False


            if request.user.is_authenticated():
                username = request.user.username

            csv_save = CSVs(filename = file_name, directory = csv_data, organization = username)
            csv_save.save()

            return render_to_response("upload/dashboard-organization.html",
                                    {'username': username,
                                     'flag_csv': flag_csv,},
                                     context_instance=RC(request))

        elif "_download" in request.POST:
            """Export a CSV File"""
            if request.user.is_authenticated():
                username = request.user.username
            csv = CSVs.objects.latest('date')

            path_to_file = os.path.dirname(os.path.dirname(__file__)) + "/csvs/Dr.Scratch/" + csv.filename
            csv_data = open(path_to_file, 'r')
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(csv.filename)
            return response

    else:
        return HttpResponseRedirect("/organization")


#_________________________GENERATOR CSV FOR ORGANIZATION____________________________#

def generatorCSV(request, dictionary, file_name, type_csv):
    """Generator of a csv file"""
    csv_directory = os.path.dirname(os.path.dirname(__file__)) + "/csvs/Dr.Scratch/"
    csv_data = csv_directory + file_name
    writer = csv.writer(open(csv_data, "wb"))

    if request.LANGUAGE_CODE == "es":
        if type_csv == "2_row":
            writer.writerow(["CÓDIGO", "URL", "Mastery", "Abstracción", "Paralelismo", "Pensamiento lógico", "Sincronización", "Control de flujo", "Interactividad con el usuario", "Representación de la información", "Código repetido", "Nombres por defecto", "Código muerto",  "Inicialización atributos"])
        elif type_csv == "1_row":
            writer.writerow(["URL", "Mastery", "Abstracción", "Paralelismo", "Pensamiento lógico", "Sincronización", "Control de flujo", "Interactividad con el usuario", "Representación de la información", "Código repetido", "Nombres por defecto", "Código muerto",  "Inicialización atributos"])
        for key, value in dictionary.items():
            total = 0
            flag = False
            try:
                if value[0] == "Error analyzing project":
                    if type_csv == "2_row":
                        row1 = key.split(",")[0]
                        row2 = key.split(",")[1]
                        row2 = row2.split("\n")[0]
                        writer.writerow([row1, row2, "Error analizando el proyecto"])
                    elif type_csv == "1_row":
                        row1 = key.split(",")[0]
                        writer.writerow([row1, "Error analizando el proyecto"])
            except:
                total = 0
                row1 = key.split(",")[0]
                if type_csv == "2_row":
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]

                for key, subvalue in value.items():
                    if key == "duplicateScript":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row11 = sub2value
                    if key == "spriteNaming":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row12 = sub2value
                    if key == "deadCode":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row13 = sub2value
                    if key == "initialization":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row14 = sub2value

                for key, value in value.items():
                    if key == "mastery":
                        for key, subvalue in value.items():
                            if key!="maxi" and key!="points":
                                if key == "Paralelismo":
                                    row5 = subvalue
                                elif key == "Abstracción":
                                    row4 = subvalue
                                elif key == "Pensamiento lógico":
                                    row6 = subvalue
                                elif key == "Sincronización":
                                    row7 = subvalue
                                elif key == "Control de flujo":
                                    row8 = subvalue
                                elif key == "Interactividad con el usuario":
                                    row9 = subvalue
                                elif key == "Representación de la información":
                                    row10 = subvalue
                                total = total + subvalue
                        row3 = total
                if type_csv == "2_row":
                    writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
                elif type_csv == "1_row":
                    writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    else:
        if type_csv == "2_row":
            writer.writerow(["CODE", "URL", "Mastery", "Abstraction", "Parallelism", "Logic", "Synchronization", "Flow control", "User interactivity", "Data representation", "Duplicate script", "Sprites naming", "Dead code",  "Sprite attributes"])
        elif type_csv == "1_row":
            writer.writerow(["URL", "Mastery", "Abstraction", "Parallelism", "Logic", "Synchronization", "Flow control", "User interactivity", "Data representation", "Duplicate script", "Sprites naming", "Dead code",  "Sprite attributes"])

        for key, value in dictionary.items():
            total = 0
            flag = False
            try:
                if value[0] == "Error analyzing project":
                    if type_csv == "2_row":
                        row1 = key.split(",")[0]
                        row2 = key.split(",")[1]
                        row2 = row2.split("\n")[0]
                        writer.writerow([row1, row2, "Error analyzing project"])
                    elif type_csv == "1_row":
                        row1 = key.split(",")[0]
                        writer.writerow([row1, "Error analyzing project"])
            except:
                total = 0
                row1 = key.split(",")[0]
                if type_csv == "2_row":
                    row2 = key.split(",")[1]
                    row2 = row2.split("\n")[0]

                for key, subvalue in value.items():
                    if key == "duplicateScript":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row11 = sub2value
                    if key == "deadCode":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row12 = sub2value
                    if key == "initialization":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row13 = sub2value
                    if key == "spriteNaming":
                        for key, sub2value in subvalue.items():
                            if key == "number":
                                row14 = sub2value

                for key, value in value.items():
                    if key == "mastery":
                        for key, subvalue in value.items():
                            if key!="maxi" and key!="points":
                                if key == "Abstraction":
                                    row4 = subvalue
                                elif key == "Parallelism":
                                    row5 = subvalue
                                elif key == "Logic":
                                    row6 = subvalue
                                elif key == "Synchronization":
                                    row7 = subvalue
                                elif key == "Flow control":
                                    row8 = subvalue
                                elif key == "User interactivity":
                                    row9 = subvalue
                                elif key == "Data representation":
                                    row10 = subvalue
                                total = total + subvalue
                        row3 = total
                if type_csv == "2_row":
                    writer.writerow([row1,row2,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
                elif type_csv == "1_row":
                    writer.writerow([row1,row3,row4,row5,row6,row7,row8,
                                row9,row10,row11,row12,row13,row14])
    return csv_data



#________________________ TO REGISTER USER __________________________#

def createUserHash(request):
    """Method for to sign up in the platform"""
    logout(request)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            nickName = form.cleaned_data['nickname']
            emailUser = form.cleaned_data['emailUser']
            passUser = form.cleaned_data['passUser']
            user = User.objects.create_user(nickName, emailUser, passUser)
            return render_to_response("profile.html", {'user': user}, context_instance=RC(request))
    elif request.method == 'GET':
        return render_to_response("sign/createUserHash.html", context_instance = RC(request))

def signUpUser(request):
    form = TeacherForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            hashkey = form.cleaned_data['hashkey']
            #classroom = form.cleaned_data['classroom']
            invite(request, username, email, hashkey)
            teacher = Teacher(teacher = request.user, username = username,
                              password = password, email = email,
                              hashkey = hashkey)
            teacher.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        return render_to_response("sign/createUser.html", context_instance = RC(request))
    
def invite(request, username, email, hashkey):
    """method invite"""

def loginUser(request):
    """Log in app to user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        Organization.objects.get(username=username)
                        return HttpResponseRedirect('/myDashboard')
                    except Organization.DoesNotExist:
                        flag = True
                        return render_to_response("password/user_doesntorg.html",
                                            {'flag': flag, 'username':request.user.username},
                                            context_instance=RC(request))
            else:
                flag = True
                return render_to_response("password/user_doesntexist.html",
                                            {'flag': flag},
                                            context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


def logoutUser(request):
    """Method for logging out"""
    logout(request)
    return HttpResponseRedirect('/')

#_________________________ CHANGE PASSWORD __________________________________#

def changePwd(request):
    if request.method == 'POST':
        recipient = request.POST['email']
        try:
            user=Organization.objects.get(email=recipient)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)

            c = {
                    'email':recipient,
                    'uid':uid,
                    'token':token,
                    'id':user.username}

            body = render_to_string("password/email.html",c)

            try:
                subject = "Dr.Scratch: Did you forget your password?"
                sender ="afdezroig@gmail.com"
                to = [recipient]
                email = EmailMessage(subject,body,sender,to)
                #email.attach_file("static/app/images/logo_main.png")
                email.send()
                return render_to_response("password/email_sended.html",
                                        context_instance=RC(request))

            except:
                 return render_to_response("password/user_doesntexist.html",
                                           context_instance=RC(request))
        except:
            return render_to_response("password/user_doesntexist.html",
                                       context_instance=RC(request))
    else:
        return render_to_response("password/password.html",
                                   context_instance=RC(request))

def reset_password_confirm(request,uidb64=None,token=None,*arg,**kwargs):
    UserModel = get_user_model()
    try:
        uid=urlsafe_base64_decode(uidb64)
        user=Organization.hashkey
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if request.method == "POST":
        flag_error = False
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST['password']
            new_confirm = request.POST['confirm']
            if new_password == "":
                return render_to_response("password/new_password.html",
                        context_instance=RC(request))

            elif new_password == new_confirm:
                user.set_password(new_password)
                user.save()
                return render_to_response("sign/organization.html",
                                            context_instance = RC(request))
            else:
                flag_error = True
                return render_to_response("password/new_password.html",
                                    {'flag_error':flag_error},
                                    context_instance=RC(request))

    else:
         if user is not None and default_token_generator.check_token(user, token):
             return render_to_response("password/new_password.html",
                                        context_instance=RC(request))
         else:
             return render_to_response("sign/organization.html",
                        context_instance = RC(request))

#_______________________ STATISTICS _________________________________#

def date_range(start, end):
    r = (end+timedelta(days=1)-start).days
    return [start+timedelta(days=i) for i in range(r)]

def statistics(request):
    """ Initializing variables"""
    start = date(2015,8,1)
    end = datetime.today()
    y = end.year
    m = end.month
    d = end.day
    end = date(y,m,d)
    dateList = date_range(start, end)
    mydates=[]
    for n in dateList:
        mydates.append(n.strftime("%d/%m")) #used for x axis in

    """This final section stores all data for the template"""

    obj= Stats.objects.order_by("-id")[0]
    data = {"date":mydates,
             "dailyRate":obj.daily_score,
             "levels":{"basic":obj.basic,
                     "development":obj.development,
                     "master":obj.master},
             "totalProjects":obj.daily_projects,
             "skillRate":{"parallelism":obj.parallelism,
                          "abstraction":obj.abstraction,
                          "logic": obj.logic,
                          "synchronization":obj.synchronization,
                          "flowControl":obj.flowControl,
                          "userInteractivity":obj.userInteractivity,
                          "dataRepresentation":obj.dataRepresentation},
             "codeSmellRate":{"deadCode":obj.deadCode,
                              "duplicateScript":obj.duplicateScript,
                              "spriteNaming":obj.spriteNaming,
                              "initialization":obj.initialization }}
    return render_to_response("statistics/statistics.html",
                                    data, context_instance=RC(request))



#_______________________ AUTOMATIC ANALYSIS _________________________________#

def analyzeProject(request,file_name, fileName):
    dictionary = {}
    if os.path.exists(file_name):
        """list_file = file_name.split('(')
        if len(list_file) > 1:
            file_name = list_file[0] + '\(' + list_file[1]
            list_file = file_name.split(')')
            file_name = list_file[0] + '\)' + list_file[1]"""
        #Request to hairball
        metricMastery = "D:\home\Python27\Scripts\hairball -p mastery.Mastery " + file_name
        metricDuplicateScript = "D:\home\Python27\Scripts\hairball -p \
                                duplicate.DuplicateScripts " + file_name
        metricSpriteNaming = "D:\home\Python27\Scripts\hairball -p convention.SpriteNaming " + file_name
        metricDeadCode = "D:\home\Python27\Scripts\hairball -p blocks.DeadCode " + file_name
        metricInitialization = "D:\home\Python27\Scripts\hairball -p \
                           initialization.AttributeInitialization " + file_name

        #Plug-ins not used yet
        #metricBroadcastReceive = "hairball -p
        #                          checks.BroadcastReceive " + file_name
        #metricBlockCounts = "hairball -p blocks.BlockCounts " + file_name
        #Response from hairball
        resultMastery = os.popen(metricMastery).read()
        resultDuplicateScript = os.popen(metricDuplicateScript).read()
        resultSpriteNaming = os.popen(metricSpriteNaming).read()
        resultDeadCode = os.popen(metricDeadCode).read()
        resultInitialization = os.popen(metricInitialization).read()
        #Plug-ins not used yet
        #resultBlockCounts = os.popen(metricBlockCounts).read()
        #resultBroadcastReceive = os.popen(metricBroadcastReceive).read()

        #Create a dictionary with necessary information
        dictionary.update(procMastery(request,resultMastery, fileName))
        dictionary.update(procDuplicateScript(resultDuplicateScript, fileName))
        dictionary.update(procSpriteNaming(resultSpriteNaming, fileName))
        dictionary.update(procDeadCode(resultDeadCode, fileName))
        dictionary.update(procInitialization(resultInitialization, fileName))
        code = {'dupCode':DuplicateScriptToScratchBlock(resultDuplicateScript)}
        dictionary.update(code)
        code = {'dCode':DeadCodeToScratchBlock(resultDeadCode)}
        dictionary.update(code)
        #Plug-ins not used yet
        #dictionary.update(procBroadcastReceive(resultBroadcastReceive))
        #dictionary.update(procBlockCounts(resultBlockCounts))
        return dictionary
    else:
        return HttpResponseRedirect('/')

# __________________________ TRANSLATE MASTERY ______________________#

def translate(request,d, fileName):
    if request.LANGUAGE_CODE == "es":
        d_translate_es = {}
        d_translate_es['Abstracción'] = d['Abstraction']
        d_translate_es['Paralelismo'] = d['Parallelization']
        d_translate_es['Pensamiento lógico'] = d['Logic']
        d_translate_es['Sincronización'] = d['Synchronization']
        d_translate_es['Control de flujo'] = d['FlowControl']
        d_translate_es['Interactividad con el usuario'] = d['UserInteractivity']
        d_translate_es['Representación de la información'] = d['DataRepresentation']
        fileName.language = "es"
        fileName.save()
        return d_translate_es
    elif request.LANGUAGE_CODE == "en":
        d_translate_en = {}
        d_translate_en['Abstraction'] = d['Abstraction']
        d_translate_en['Parallelism'] = d['Parallelization']
        d_translate_en['Logic'] = d['Logic']
        d_translate_en['Synchronization'] = d['Synchronization']
        d_translate_en['Flow control'] = d['FlowControl']
        d_translate_en['User interactivity'] = d['UserInteractivity']
        d_translate_en['Data representation'] = d['DataRepresentation']
        fileName.language = "en"
        fileName.save()
        return d_translate_en
    else:
        return d


# __________________________ PROCESSORS _____________________________#

def procMastery(request,lines, fileName):
    """Mastery"""
    dic = {}
    lLines = lines.split('\n')
    d = {}
    if (lines != ''):
        d = ast.literal_eval(lLines[1])
        lLines = lLines[2].split(':')[1]
        points = int(lLines.split('/')[0])
        maxi = int(lLines.split('/')[1])
    else:
        d = ast.literal_eval('None')
        points = 0
        maxi = 0

    #Save in DB
    fileName.score = points
    fileName.abstraction = d["Abstraction"]
    fileName.parallelization = d["Parallelization"]
    fileName.logic = d["Logic"]
    fileName.synchronization = d["Synchronization"]
    fileName.flowControl = d["FlowControl"]
    fileName.userInteractivity = d["UserInteractivity"]
    fileName.dataRepresentation = d["DataRepresentation"]
    fileName.save()

    #Translation
    d_translated = translate(request,d, fileName)

    dic["mastery"] = d_translated
    dic["mastery"]["points"] = points
    dic["mastery"]["maxi"] = maxi
    return dic

def procDuplicateScript(lines, fileName):
    """Return number of duplicate scripts"""
    dic = {}
    number = 0
    lLines = lines.split('\n')
    if len(lLines) > 2:
        number = lLines[1][0]
    dic["duplicateScript"] = dic
    dic["duplicateScript"]["number"] = number

    #Save in DB
    fileName.duplicateScript = number
    fileName.save()

    return dic


def procSpriteNaming(lines, fileName):
    """Return the number of default spring"""
    dic = {}
    lLines = lines.split('\n')
    number = lLines[1].split(' ')[0]
    lObjects = lLines[2:]
    lfinal = lObjects[:-1]
    dic['spriteNaming'] = dic
    dic['spriteNaming']['number'] = str(number)
    dic['spriteNaming']['sprite'] = lfinal

    #Save in DB
    fileName.spriteNaming = str(number)
    fileName.save()

    return dic


def procDeadCode(lines, fileName):
    """Number of dead code with characters and blocks"""
    lLines = lines.split('\n')
    lLines = lLines[1:]
    lcharacter = []
    literator = []
    iterator = 0
    for frame in lLines:
        if '[kurt.Script' in frame:
            # Found an object
            name = frame.split("'")[1]
            lcharacter.append(name)
            if iterator != 0:
                literator.append(iterator)
                iterator = 0
        if 'kurt.Block' in frame:
            iterator += 1
    literator.append(iterator)

    number = len(lcharacter)
    dic = {}
    dic["deadCode"] = dic
    dic["deadCode"]["number"] = number
    for i in range(number):
        dic["deadCode"][lcharacter[i]] = literator[i]

    #Save in DB
    fileName.deadCode = number
    fileName.save()

    return dic


def procInitialization(lines, fileName):
    """Initialization"""
    dic = {}
    lLines = lines.split('\n')
    if (lLines[1]):
        d = ast.literal_eval(lLines[1])
        keys = d.keys()
        values = d.values()
        items = d.items()
        number = 0
    else:
        d = ast.literal_eval('None')
        keys = []
        values = []
        items = []
        number = 0

    for keys, values in items:
        list = []
        attribute = ""
        internalkeys = values.keys()
        internalvalues = values.values()
        internalitems = values.items()
        flag = False
        counterFlag = False
        i = 0
        for internalkeys, internalvalues in internalitems:
            if internalvalues == 1:
                counterFlag = True
                for value in list:
                    if internalvalues == value:
                        flag = True
                if not flag:
                    list.append(internalkeys)
                    if len(list) < 2:
                        attribute = str(internalkeys)
                    else:
                        attribute = attribute + ", " + str(internalkeys)
        if counterFlag:
            number = number + 1
        d[keys] = attribute
    dic["initialization"] = d
    dic["initialization"]["number"] = number

    #Save in DB
    fileName.initialization = number
    fileName.save()

    return dic

def DuplicateScriptToScratchBlock(code):
    try:
        code = code.split("\n")[2:][0]
        code = code[1:-1].split(",")
    except:
        code = ""

    return code

def DeadCodeToScratchBlock(code):
    try:
        code = code.split("\n")[2:-1]
        for n in code:
            n = n[15:-2]
    except:
        code = ""
    return code



#_________________________CSV File____________________________#
def exportCsvFile(request):
    """Export a CSV File"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="some.csv"'
    d = {"Abstraction": 2, "level": " Developing", "Parallelization": 1, "Logic": 1, "Synchronization": 2, "FlowControl": 2, "UserInteractivity": 1, "maxPoints": 21, "DataRepresentation": 1, "points": 10}
    writer = csv.writer(response)
    for key, value in d.items():
           writer.writerow([key, value])

    """
    writer = csv.writer(response)
    writer.writerow(['First row', 'Paco', '21', 'Madrid'])
    writer.writerow(['Second row', 'Lucia', '25', 'Quito'])
    """
    return response






##############################################################################
#                           UNDER DEVELOPMENT
##############################################################################

#________________________ DASHBOARD ____________________________#

def createDashboards():
    """Get users and create dashboards"""
    allUsers = User.objects.all()
    for user in allUsers:
        try:
            newdash = Dashboard.objects.get(user=user)
        except:
            fupdate = datetime.now()
            newDash = Dashboard(user=user.username, frelease=fupdate)
            newDash.save()

def myDashboard(request):
    """Dashboard page"""
    if request.user.is_authenticated():
        user = request.user.username
        # The main page of user
        # To obtain the dashboard associated to user
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        beginner = mydashboard.project_set.filter(level="beginner")
        developing = mydashboard.project_set.filter(level="developing")
        advanced = mydashboard.project_set.filter(level="advanced")
        return render_to_response("upload/dashboard-organization.html",
                                {'user': user,
                                'beginner': beginner,
                                'developing': developing,
                                'advanced': advanced,
                                'projects': projects},
                                context_instance=RC(request))
    else:
        user = None
        return HttpResponseRedirect("/")

def myProjects(request):
    """Show all projects of dashboard"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myProjects/content-projects.html",
                                {'projects': projects,
                                 'user':user},
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


def myRoles(request):
    """Show the roles in Doctor Scratch"""
    if request.user.is_authenticated():
        user = request.user.username
        return render_to_response("myRoles/content-roles.html",
                                context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")



def myHistoric(request):
    """Show the progress in the application"""
    if request.user.is_authenticated():
        user = request.user.username
        mydashboard = Dashboard.objects.get(user=user)
        projects = mydashboard.project_set.all()
        return render_to_response("myHistoric/content-historic.html",
                                    {'projects': projects},
                                    context_instance=RC(request))
    else:
        return HttpResponseRedirect("/")


#________________________ PROFILE ____________________________#


def updateProfile(request):
    """Update the pass, email and avatar"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            newPass = form.cleaned_data['newPass']
            newEmail = form.cleaned_data['newEmail']
            choiceField = form.ChoiceField(widget=form.RadioSelect())
            return HttpResponseRedirect('/mydashboard')
        else:
            return HttpResponseRedirect('/')


def changePassword(request, new_password):
    """Change the password of user"""
    user = User.objects.get(username=request.user)
    user.set_password(new_password)
    user.save()

# ___________________ PROCESSORS OF PLUG-INS NOT USED YET ___________________#

#def procBlockCounts(lines):
#    """CountLines"""
#    dic = {}
#    dic["countLines"] = lines
#    return dic


#def procBroadcastReceive(lines):
#    """Return the number of lost messages"""
#    dic = {}
#    lLines = lines.split('\n')
    # messages never received or broadcast
#    laux = lLines[1]
#    laux = laux.split(':')[0]
#    dic["neverRB"] = dic
#    dic["neverRB"]["neverReceive"] = laux
#    laux = lLines[3]
#    laux = laux.split(':')[0]
#    dic["neverRB"]["neverBroadcast"] = laux

#    return dic


#_____________________ CREATE STATS OF ANALYSIS PERFORMED ___________#

def createStats(file_name, dictionary):
    flag = True
    return flag




#___________________________ UNDER DEVELOPMENT _________________________#

#UNDER DEVELOPMENT: Children!!!Carefull
def registration(request):
    """Registration a user in the app"""
    return render_to_response("formulary.html")


#UNDER DEVELOPMENT: Children!!!Carefull
def profileSettings(request):
    """Main page for registered user"""
    return render_to_response("profile.html")

#UNDER DEVELOPMENT:
#TO REGISTERED USER
def uploadRegistered(request):
    """Upload and save the zip"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        # Analyze the scratch project and save in our server files
        fileName = handle_uploaded_file(request.FILES['zipFile'])
        # Analize project and to save in database the metrics
        d = analyzeProject(request,fileName)
        fupdate = datetime.now()
        # Get the short name
        shortName = fileName.split('/')[-1]
        # Get the dashboard of user
        myDashboard = Dashboard.objects.get(user=user)
        # Save the project
        newProject = Project(name=shortName, version=1, score=0, path=fileName, fupdate=fupdate, dashboard=myDashboard)
        newProject.save()
        # Save the metrics
        dmaster = d["mastery"]
        newMastery = Mastery(myproject=newProject, abstraction=dmaster["Abstraction"], paralel=dmaster["Parallelization"], logic=dmaster["Logic"], synchronization=dmaster["Synchronization"], flowcontrol=dmaster["FlowControl"], interactivity=dmaster["UserInteractivity"], representation=dmaster["DataRepresentation"], TotalPoints=dmaster["TotalPoints"])
        newMastery.save()
        newProject.score = dmaster["Total{% if forloop.counter0|divisibleby:1 %}<tr>{% endif %}Points"]
        if newProject.score > 15:
            newProject.level = "advanced"
        elif newProject.score > 7:
            newProject.level = "developing"
        else:
            newProject.level = "beginner"
        newProject.save()
        for charx, dmetrics in d["attribute"].items():
            if charx != 'stage':
                newAttribute = Attribute(myproject=newProject, character=charx, orientation=dmetrics["orientation"], position=dmetrics["position"], costume=dmetrics["costume"], visibility=dmetrics["visibility"], size=dmetrics["size"])
            newAttribute.save()

        iterator = 0
        for deadx in d["dead"]:
            if (iterator % 2) == 0:
                newDead = Dead(myproject=newProject, character=deadx, blocks=0)
            else:
                newDead.blocks = deadx
            newDead.save()
            iterator += 1

        newDuplicate = Duplicate(myproject=newProject, numduplicates=d["duplicate"][0])
        newDuplicate.save()
        for charx in d["sprite"]:
            newSprite = Sprite(myproject=newProject, character=charx)
            newSprite.save()
        return HttpResponseRedirect('/myprojects')
    
def handle_uploaded_file(request):
    """handle_uploaded_file"""

#_____ ID/BUILDERS ____________#

def idProject(request, idProject):
    """Resource uniquemastery of project"""
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = None
    dmastery = {}
    project = Project.objects.get(id=idProject)
    item = Mastery.objects.get(myproject=project)
    dmastery = buildMastery(item)
    TotalPoints = dmastery["TotalPoints"]
    dsprite = Sprite.objects.filter(myproject=project)
    ddead = Dead.objects.filter(myproject=project)
    dattribute = Attribute.objects.filter(myproject=project)
    listAttribute = buildAttribute(dattribute)
    numduplicate = Duplicate.objects.filter(myproject=project)[0].numduplicates
    return render_to_response("project.html", {'project': project,
                                                'dmastery': dmastery,
                                                'lattribute': listAttribute,
                                                'numduplicate': numduplicate,
                                                'dsprite': dsprite,
                                                'Total points': TotalPoints,
                                                'ddead': ddead},
                                                context_instance=RequestContext(request))




def buildMastery(item):
    """Generate the dictionary with mastery"""
    dmastery = {}
    dmastery["Total points"] = item.TotalPoints
    dmastery["Abstraction"] = item.abstraction
    dmastery["Parallelization"] = item.paralel
    dmastery["Logic"] = item.logic
    dmastery["Synchronization"] = item.synchronization
    dmastery["Flow Control"] = item.flowcontrol
    return dmastery

def buildAttribute(qattribute):
    """Generate dictionary with attribute"""
    # Build the dictionary
    dic = {}
    for item in qattribute:
        dic[item.character] = {"orientation": item.orientation,
                                "position": item.position,
                                "costume": item.costume,
                                "visibility":item.visibility,
                                "size": item.size}
    listInfo = writeErrorAttribute(dic)
    return listInfo

#_______BUILDERS'S HELPERS ________#

def writeErrorAttribute(dic):
    """Write in a list the form correct of attribute plugin"""
    lErrors = []
    for key in dic.keys():
        text = ''
        dx = dic[key]
        if key != 'stage':
            if dx["orientation"] == 1:
                text = 'orientation,'
            if dx["position"] == 1:
                text += ' position, '
            if dx["visibility"] == 1:
                text += ' visibility,'
            if dx["costume"] == 1:
                text += 'costume,'
            if dx["size"] == 1:
                text += ' size'
            if text != '':
                text = key + ': ' + text + ' modified but not initialized correctly'
                lErrors.append(text)
            text = None
        else:
            if dx["background"] == 1:
                text = key + ' background modified but not initialized correctly'
                lErrors.append(text)
    return lErrors



# _________________________  _______________________________ #

def uncompress_zip(zip_file):
    unziped = ZipFile(zip_file, 'r')
    for file_path in unziped.namelist():
        if file_path == 'project.json':
            file_content = unziped.read(file_path)
    show_file(file_content)
    
def show_file(request):
    """show_file"""
    
    
#-------------------TOURNAMENTS---------------------# 
"""TODO:------------TOURNAMENTS---------------------"""

def reset_password_tournaments(request,uidb64=None,token=None,*arg,**kwargs):
    UserModel = get_user_model()
    try:
        uid=urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if request.method == "POST":
        flag_error = False
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST['password']
            new_confirm = request.POST['confirm']
            if new_password == "":
                return render_to_response("password/new_password.html",
                        context_instance=RC(request))

            elif new_password == new_confirm:
                user.set_password(new_password)
                user.save()
                messages.add_message(request, messages.SUCCESS, _('Password changed successfully.'))
                return HttpResponseRedirect("/tournaments")
            else:
                flag_error = True
                return render_to_response("tournaments/password/new_password.html",
                                    {'flag_error':flag_error},
                                    context_instance=RC(request))

    else:
         if user is not None and default_token_generator.check_token(user, token):
             return render_to_response("tournaments/password/new_password.html",
                                        context_instance=RC(request))
         else:
            return HttpResponseRedirect("/tournaments")

def tourChangePwd(request):
    if request.method == 'POST':
        recipient = request.POST['email']
        try:
            user=User.objects.get(email=recipient)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            c = {
                    'email':recipient,
                    'uid':uid,
                    'token':token,
                    'id':user.username}

            body = render_to_string("tournaments/password/email.html",c)

            try:
                subject = _("Dr.Scratch: Did you forget your password?")
                sender ="afdezroig@gmail.com"
                to = [recipient]
                email = EmailMessage(subject,body,sender,to)
                email.send()
                return render_to_response("password/email_sended.html",
                                        context_instance=RC(request))

            except:
                 return render_to_response("tournaments/password/user_doesntexist.html",
                                           context_instance=RC(request))
        except:
            return render_to_response("tournaments/password/user_doesntexist.html",
                                       context_instance=RC(request))
    else:
        return render_to_response("password/password.html",
                                   context_instance=RC(request))
        
def initTournaments (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            creator = Creator.objects.filter(username=request.user.username)
            if creator:
                return render_to_response('tournaments/creator/main_creator.html', {'username':request.user.username}, RC(request))
            else:
                participant = Participant.objects.filter(username=request.user.username)
                if participant:
                    return HttpResponseRedirect("/participant/teams")
                else:
                    messages.add_message(request, messages.ERROR, _('Logged user is not a creator or a participant.'))
                    return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        else:
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")
    
def signUpCreator(request):
    """Method which allow to sign up creators"""
    flagHash = False
    flagName = False
    flagEmail = False
    flagForm = False
    if request.method == 'POST':
        form = CreatorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            hashkey = form.cleaned_data['hashkey']
            try:
                #This name already exists
                creator = User.objects.get(username=username)
                flagName = True
                return render_to_response("tournaments/creator/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
            except:
                try:
                    #This email already exists
                    email = User.objects.get(email=email)
                    flagEmail = True
                    return render_to_response("tournaments/creator/signup_error.html",
                                            {'flagName':flagName,
                                            'flagEmail':flagEmail,
                                            'flagHash':flagHash,
                                            'flagForm':flagForm},
                                            context_instance = RC(request))
                except:
                    try:
                        creatorHashkey = CreatorHash.objects.get(hashkey=hashkey)
                        creatorHashkey.delete()
                        creator = Creator.objects.create_user(username = username, email=email, password=password, hashkey=hashkey)
                        creator = authenticate(username=username, password=password)
                        user=Creator.objects.get(email=email)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token=default_token_generator.make_token(user)
                        c = {
                                'email':email,
                                'uid':uid,
                                'token':token}

                        body = render_to_string("tournaments/creator/email.html",c)
                        subject = _("Welcome to Dr.Scratch tournaments")
                        sender ="afdezroig@gmail.com"
                        to = [email]
                        email = EmailMessage(subject,body,sender,to)
                        email.send()
                        login(request, creator)
                        return HttpResponseRedirect('/tournaments')

                    except:
                        #Doesn't exist this hash
                        flagHash = True

                        return render_to_response("tournaments/creator/signup_error.html",
                                          {'flagName':flagName,
                                           'flagEmail':flagEmail,
                                           'flagHash':flagHash,
                                           'flagForm':flagForm},
                                          context_instance = RC(request))
        else:
            flagForm = True
            return render_to_response("tournaments/creator/signup_error.html",
                  {'flagName':flagName,
                   'flagEmail':flagEmail,
                   'flagHash':flagHash,
                   'flagForm':flagForm},
                  context_instance = RC(request))

    elif request.method == 'GET':
        return HttpResponseRedirect('/tournaments')

def loginTournaments(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    creator = Creator.objects.filter(username=username)
                    if creator:
                        return render_to_response('tournaments/creator/main_creator.html', {'username':request.user.username}, RC(request))
                    else:
                        participant = Participant.objects.filter(username=request.user.username)
                if participant:
                    return HttpResponseRedirect("/participant/teams")
                else:
                    messages.add_message(request, messages.ERROR, _('Logged user is not a creator or a participant.'))
                    return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            else:
                flag = True
                return render_to_response("tournaments/password/user_doesntexist.html",
                                            {'flag': flag},
                                            context_instance=RC(request))
        else:
            messages.add_message(request, messages.ERROR, _("User doesn't exist or the password is incorrect."))
            return HttpResponseRedirect('/tournaments')
    else:
        return HttpResponseRedirect("/")   

def getElementsPaginador (elementList, page, numElemPerPage):
    paginator = Paginator(elementList, numElemPerPage)
    try:
        elementsPage = paginator.page(page)
    except PageNotAnInteger:
        elementsPage = paginator.page(1)
    except EmptyPage:
        elementsPage = paginator.page(paginator.num_pages)
    return elementsPage
    
def adminCreator (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                Creator.objects.get(username=request.user.username)
                return render_to_response('tournaments/creator/admin/admin_creator.html', {'username':request.user.username}, RC(request))
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        
    else:
        return HttpResponseRedirect("/")

def adminCreatorChallenges (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            form = ChallengeForm()
            """Muestro los retos creados por dicho creador"""
            challenges = Challenge.objects.filter(creator=creator.username)
            page = request.GET.get('page', 1)
            challengesPagina = getElementsPaginador (challenges, page, paginator_creator_challenges)
            return render_to_response('tournaments/creator/admin/challenges/challengesList.html', {'username':request.user.username, 
                                                                                        'challengesPagina': challengesPagina, 'form': form}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")

def newChallenge (request):
    if request.method == "POST": 
        form = ChallengeForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            parallelism = form.cleaned_data['parallelism']
            logic = form.cleaned_data['logic']
            flowControl = form.cleaned_data['flowControl']
            userInteractivity = form.cleaned_data['userInteractivity']
            dataRepresentation = form.cleaned_data['dataRepresentation']
            abstraction = form.cleaned_data['abstraction']
            synchronization = form.cleaned_data['synchronization']
            challenge = Challenge(name=name, description=description, parallelism=parallelism, logic=logic, 
                                  flowControl=flowControl, userInteractivity=userInteractivity, dataRepresentation=dataRepresentation, 
                                  abstraction=abstraction, synchronization=synchronization, creator=creator)
            challenge.save()
            messages.add_message(request, messages.SUCCESS, _('Challenge added.'))
            page = request.GET.get('page', 1)
            if (request.path == '/newChallenge'):
                return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))
            elif (request.path == '/tournamentNewChallenge'):
                idTournament = request.POST.get('idTournament', None)
                if (idTournament == ''):
                    return HttpResponseRedirect("/newTournamentGet?page=" + str(page))
                else:
                    return HttpResponseRedirect("/editTournamentGet?tournament=" + idTournament + "&page=" + str(page))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/") 
    
def deleteChallenge (request):
    if request.method == "POST":
        idChallenge = request.POST.get('idChallenge', None)
        if idChallenge is not None:
            challengeDelete = Challenge.objects.get(id=idChallenge)
            #Compruebo si el reto tiene torneos asociados, en cuyo caso, no se puede eliminar
            if (len(challengeDelete.tournament_set.all()) > 0):
                messages.add_message(request, messages.ERROR, _('The challenge cannot be deleted because is asociated to one or more tournaments.'))
            else:
                challengeDelete.delete();
                messages.add_message(request, messages.SUCCESS, _('Challenge deleted.'))
            page = request.GET.get('page', 1)    
            return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))
        else:
            messages.add_message(request, messages.ERROR, _('The selected challenge cannot be found.'))
            page = request.GET.get('page', 1)
            return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))  
    else:
        return HttpResponseRedirect("/")    
    
def editChallenge (request):
    if request.method == "GET":
        try:
            Creator.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        idChallenge = request.GET.get('challenge', None)
        page = request.GET.get('page', 1)
        if idChallenge is not None:
            challengeEdit = Challenge.objects.get(id=idChallenge)
            form = ChallengeForm(initial={'name': challengeEdit.name, 
                                          'description': challengeEdit.description, 
                                            'parallelism': challengeEdit.parallelism,
                                              'logic': challengeEdit.logic,
                                                'flowControl': challengeEdit.flowControl,
                                                  'userInteractivity': challengeEdit.userInteractivity,
                                                    'dataRepresentation': challengeEdit.dataRepresentation,
                                                      'abstraction': challengeEdit.abstraction,
                                                        'synchronization': challengeEdit.synchronization})
            
            return render_to_response('tournaments/creator/admin/challenges/editChallenge.html', {'username':request.user.username, 
                                                                                        'form': form, 'challengeName': challengeEdit.name, 'challengeId': challengeEdit.id, 
                                                                                        'page': page}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('The selected challenge cannot be found.'))
            page = request.GET.get('page', 1)
            return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))  
    else:
        form = ChallengeForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            idChallenge = request.POST.get('idChallenge', None)
            if idChallenge is not None:
                #Editamos el reto
                challengeEdit = Challenge.objects.get(id=idChallenge)
                challengeEdit.name = form.cleaned_data['name']
                challengeEdit.description = form.cleaned_data['description']
                challengeEdit.parallelism = form.cleaned_data['parallelism']
                challengeEdit.logic = form.cleaned_data['logic']
                challengeEdit.flowControl = form.cleaned_data['flowControl']
                challengeEdit.userInteractivity = form.cleaned_data['userInteractivity']
                challengeEdit.dataRepresentation = form.cleaned_data['dataRepresentation']
                challengeEdit.abstraction = form.cleaned_data['abstraction']
                challengeEdit.synchronization = form.cleaned_data['synchronization']
                challengeEdit.save()
                # Translators: Challenge edited.
                messages.add_message(request, messages.SUCCESS, _('Challenge edited.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))  
            else:
                messages.add_message(request, messages.ERROR, _('The selected challenge cannot be found.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/challenges?page="+str(page))  
        else:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
        
def adminCreatorTeams (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            form = TeamForm()
            """Muestro los equipos creados por dicho creador"""
            teams = Team.objects.filter(creator=creator.username)
            page = request.GET.get('page', 1)
            teamsPagina = getElementsPaginador (teams, page, paginator_creator_teams)
            return render_to_response('tournaments/creator/admin/teams/teamsList.html', {'username':request.user.username, 
                                                                               'teamsPagina': teamsPagina, 'form': form}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")
    
def deleteTeam (request):
    if request.method == "POST":
        idTeam = request.POST.get('idTeam', None)
        if idTeam is not None:
            teamDelete = Team.objects.get(id=idTeam)
            #Compruebo si el equipo tiene torneos asociados, en cuyo caso, no se puede eliminar
            if (len(teamDelete.tournament_set.all()) > 0):
                messages.add_message(request, messages.ERROR, _('The team cannot be deleted because is asociated to one or more tournaments.'))
            else:
                teamDelete.delete();
                messages.add_message(request, messages.SUCCESS, _('Team deleted.'))
            page = request.GET.get('page', 1)    
            return HttpResponseRedirect("/creator/admin/teams?page="+str(page))   
    else:
        return HttpResponseRedirect("/")
    
def newEditTeam (request):
    if request.method == "GET":
        try:
            creator = Creator.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        if (request.path == '/editTeamGet'):
            idTeam = request.GET.get('team', None)
            page = request.GET.get('page', 1)
            if idTeam is not None:
                teamEdit = Team.objects.get(id=idTeam)
                form = TeamForm(initial={'name': teamEdit.name, 
                                              'description': teamEdit.description})
                """Busco todos los participantes incluidos por el creador para poder seleccionarlos"""
                participants = Participant.objects.filter(creator_username=creator.username)
                return render_to_response('tournaments/creator/admin/teams/newEditTeam.html', 
                                          {'username':request.user.username, 'form': form, 'team': teamEdit, 
                                           'page': page, 'participants': participants, 'totalParticipants': int (max_participants_per_team),
                                           'maxParticipants': range(len(teamEdit.participant_set.all()), int (max_participants_per_team)),'editTeam': True}, RC(request))
            else:
                messages.add_message(request, messages.ERROR, _('The selected team cannot be found.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/teams?page="+str(page))
        elif (request.path == '/newTeamGet'):
            page = request.GET.get('page', 1)
            form = TeamForm()
            """Busco todos los participantes incluidos por el creador para poder seleccionarlos"""
            participants = Participant.objects.filter(creator_username=creator.username)
            return render_to_response('tournaments/creator/admin/teams/newEditTeam.html', 
                                      {'username':request.user.username, 'form': form, 'page': page, 
                                       'participants': participants, 'maxParticipants': range(int (max_participants_per_team)), 
                                       'newTeam': True}, RC(request))
        else:
            page = request.GET.get('page', 1)
            return HttpResponseRedirect("/creator/admin/teams?page="+str(page))
    else:
        return HttpResponseRedirect("/")

def editTeam (request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            idTeam = request.POST.get('idTeam', None)
            if idTeam is not None:
                #Editamos el equipo
                teamEdit = Team.objects.get(id=idTeam)
                teamEdit.name = form.cleaned_data['name']
                teamEdit.description = form.cleaned_data['description']
                teamEdit.save()
                teamEdit.participant_set.clear()
                for i in range(int (max_participants_per_team)):
                    p_id = request.POST['p_id_'+str(i)]
                    if p_id != '':
                        partObj = Participant.objects.get(id=p_id)
                        if (partObj):
                            partObj.teams.add(teamEdit)
                messages.add_message(request, messages.SUCCESS, _('Team edited.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/teams?page="+str(page))  
            else:
                messages.add_message(request, messages.ERROR, _('The selected team cannot be found.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/teams?page="+str(page))  
        else:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/")

def newTeam (request):
    if request.method == "POST": 
        form = TeamForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            team = Team(name=name, description=description, creator=creator)
            team.save()
            """Compruebo si hay participantes asociados al equipo y los incluyo"""
            for i in range(int (max_participants_per_team)):
                p_id = request.POST['p_id_'+str(i)]
                if p_id != '':
                    partObj = Participant.objects.get(id=p_id)
                    if (partObj):
                        partObj.teams.add(team)
            messages.add_message(request, messages.SUCCESS, _('Team added.'))
            page = request.GET.get('page', 1)
            if (request.path == '/newTeamPost'):
                return HttpResponseRedirect("/creator/admin/teams?page="+str(page))
            elif (request.path == '/tournamentNewTeam'):
                idTournament = request.POST.get('idTournament', None)
                if (idTournament == ''):
                    return HttpResponseRedirect("/newTournamentGet?page=" + str(page))
                else:
                    return HttpResponseRedirect("/editTournamentGet?tournament=" + idTournament + "&page=" + str(page))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/")
    
def adminCreatorTournaments (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            form = TournamentForm()
            """Muestro los torneos creados por dicho creador"""
            tournaments = Tournament.objects.filter(creator=creator.username)
            page = request.GET.get('page', 1)
            tournamentsPagina = getElementsPaginador (tournaments, page, paginator_creator_tournaments)
            return render_to_response('tournaments/creator/admin/tournaments/tournamentsList.html', {'username':request.user.username, 'tournamentsPagina': tournamentsPagina,
                                                                                     'form': form}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")
    
def newEditTournament (request):
    if request.method == "GET":
        try:
            creator = Creator.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        if (request.path == '/editTournamentGet'):
            idTournament = request.GET.get('tournament', None)
            page = request.GET.get('page', 1)
            if idTournament is not None:
                tournamentEdit = Tournament.objects.get(id=idTournament)
                challengeForm  = ChallengeForm()
                teamForm  = TeamForm()
                """Busco todos los participantes incluidos por el creador para poder seleccionarlos"""
                participants = Participant.objects.filter(creator_username=creator.username)
                
                form = TournamentForm(initial={'name': tournamentEdit.name, 
                                              'description': tournamentEdit.description,
                                              'manualValidation': tournamentEdit.manualValidation,
                                              'notificationPeriod': tournamentEdit.notificationPeriod})
                """Busco todos los equipos incluidos por el creador para poder seleccionarlos"""
                teams = Team.objects.filter(creator=creator.username)
                """Busco todos los retos incluidos por el creador para poder seleccionarlos"""
                challenges = Challenge.objects.filter(creator=creator.username)
                
                return render_to_response('tournaments/creator/admin/tournaments/newEditTournament.html', 
                                          {'username':request.user.username, 'form': form, 'tournament': tournamentEdit, 
                                           'challengeForm': challengeForm, 'teamForm': teamForm,
                                           'participants': participants, 'maxParticipants': range(int (max_participants_per_team)), 
                                           'page': page, 'teams': teams, 'totalTeams': int (max_teams_per_tournament),
                                           'challenges': challenges, 'totalChallenges': int (max_challenges_per_tournament),
                                           'maxTeams': range(len(tournamentEdit.teams.all()), int (max_teams_per_tournament)),
                                           'maxChallenges': range(len(tournamentEdit.get_challenges()), int (max_challenges_per_tournament)),
                                           'editTournament': True}, RC(request))
            else:
                messages.add_message(request, messages.ERROR, _('The selected tournament cannot be found.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))
        elif (request.path == '/newTournamentGet'):
            page = request.GET.get('page', 1)
            form = TournamentForm()
            challengeForm  = ChallengeForm()
            teamForm  = TeamForm()
            """Busco todos los participantes incluidos por el creador para poder seleccionarlos"""
            participants = Participant.objects.filter(creator_username=creator.username)
            """Busco todos los equipos incluidos por el creador para poder seleccionarlos"""
            teams = Team.objects.filter(creator=creator.username)
            """Busco todos los retos incluidos por el creador para poder seleccionarlos"""
            challenges = Challenge.objects.filter(creator=creator.username)
            
            return render_to_response('tournaments/creator/admin/tournaments/newEditTournament.html', 
                                      {'username':request.user.username, 'form': form, 'page': page, 
                                       'challengeForm': challengeForm, 'teamForm': teamForm,
                                       'participants': participants, 'maxParticipants': range(int (max_participants_per_team)), 
                                       'challenges': challenges, 'maxChallenges':range(int (max_challenges_per_tournament)),
                                       'teams': teams, 'maxTeams': range(int (max_teams_per_tournament)), 
                                       'newTournament': True}, RC(request))
        else:
            page = request.GET.get('page', 1)
            return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))
    else:
        return HttpResponseRedirect("/")
    
def deleteTournament (request):
    if request.method == "POST":
        idTournament = request.POST.get('idTournament', None)
        if idTournament is not None:
            tournamentDelete = Tournament.objects.get(id=idTournament)
            for task in Task.objects.filter(verbose_name=tournamentDelete.id):
                task.delete();
            tournamentDelete.delete();
            messages.add_message(request, messages.SUCCESS, _('Tournament deleted.'))
            page = request.GET.get('page', 1)    
            return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))   
    else:
        return HttpResponseRedirect("/")
    
def newTournament (request):
    if request.method == "POST": 
        form = TournamentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            manualValidation = form.cleaned_data['manualValidation']
            notificationPeriod = form.cleaned_data['notificationPeriod']
            tournament = Tournament(name=name, description=description, manualValidation=manualValidation, notificationPeriod=notificationPeriod, creator=creator)
            tournament.save()
            """Compruebo si hay retos asociados al torneo y los incluyo"""
            for i in range(int (max_challenges_per_tournament)):
                ce_id = request.POST['ce_id_'+str(i)]
                if ce_id != '':
                    challengeObj = Challenge.objects.get(id=ce_id)
                    if (challengeObj):
                        ct = ChallengesOfTournament(position=i, tournament=tournament, challenge=challengeObj)
                        try:
                            ChallengesOfTournament.objects.get(tournament=tournament, challenge=challengeObj)
                        except ChallengesOfTournament.DoesNotExist:
                            ct.save()
            """Compruebo si hay equipos asociados al torneo y los incluyo"""
            for i in range(int (max_teams_per_tournament)):
                te_id = request.POST['te_id_'+str(i)]
                if te_id != '':
                    teamObj = Team.objects.get(id=te_id)
                    if (teamObj):
                        tournament.teams.add(teamObj)
            if (tournament.notificationPeriod == str(2)):
                summary_email(tournament.id, creator.email, schedule=(24*60*60), repeat=(24*60*60), verbose_name=tournament.id) #(once a day)
            elif (tournament.notificationPeriod == str(3)):
                summary_email(tournament.id, creator.email, schedule=(7*24*60*60), repeat=(7*24*60*60), verbose_name=tournament.id) #(once a week)
            messages.add_message(request, messages.SUCCESS, _('Tournament added.'))
            page = request.GET.get('page', 1)
            return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/")
    
def editTournament (request):
    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            idTournament = request.POST.get('idTournament', None)
            if idTournament is not None:
                #Editamos el torneo
                tournamentEdit = Tournament.objects.get(id=idTournament)
                tournamentEdit.name = form.cleaned_data['name']
                tournamentEdit.description = form.cleaned_data['description']
                tournamentEdit.manualValidation = form.cleaned_data['manualValidation']
                if (tournamentEdit.manualValidation == False):
                    tournamentEdit.notificationPeriod = 0
                else:
                    tournamentEdit.notificationPeriod = form.cleaned_data['notificationPeriod']
                tournamentEdit.save()
                tournamentEdit.challenges.clear()
                """Compruebo si hay retos asociados al torneo y los incluyo"""
                for i in range(int (max_challenges_per_tournament)):
                    ce_id = request.POST['ce_id_'+str(i)]
                    if ce_id != '':
                        challengeObj = Challenge.objects.get(id=ce_id)
                        if (challengeObj):
                            ct = ChallengesOfTournament(position=i, tournament=tournamentEdit, challenge=challengeObj)
                            try:
                                ChallengesOfTournament.objects.get(tournament=tournamentEdit, challenge=challengeObj)
                            except ChallengesOfTournament.DoesNotExist:
                                ct.save()
                tournamentEdit.teams.clear()
                """Compruebo si hay equipos asociados al torneo y los incluyo"""
                for i in range(int (max_teams_per_tournament)):
                    te_id = request.POST['te_id_'+str(i)]
                    if te_id != '':
                        teamObj = Team.objects.get(id=te_id)
                        if (teamObj):
                            tournamentEdit.teams.add(teamObj)
                for task in Task.objects.filter(verbose_name=tournamentEdit.id):
                    task.delete();
                if (tournamentEdit.notificationPeriod == str(2)):
                    summary_email(tournamentEdit.id, creator.email, schedule=(24*60*60), repeat=(24*60*60), verbose_name=tournamentEdit.id) #(once a day)
                elif (tournamentEdit.notificationPeriod == str(3)):
                    summary_email(tournamentEdit.id, creator.email, schedule=(7*24*60*60), repeat=(7*24*60*60), verbose_name=tournamentEdit.id) #(once a week)
                        
                messages.add_message(request, messages.SUCCESS, _('Tournament edited.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))  
            else:
                messages.add_message(request, messages.ERROR, _('The selected team cannot be found.'))
                page = request.GET.get('page', 1)
                return HttpResponseRedirect("/creator/admin/tournaments?page="+str(page))  
        else:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/")
    
def tournamentsCreator (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            """Muestro los torneos creados por dicho creador"""
            tournaments = Tournament.objects.filter(creator=creator.username)
            page = request.GET.get('page', 1)
            tournamentsPagina = getElementsPaginador (tournaments, page, paginator_creator_tournaments)
            return render_to_response('tournaments/creator/progress/tournamentsProgress.html', {'username':request.user.username, 'tournamentsPagina': tournamentsPagina}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")
    
def challengesCreator (request):
    if request.method == "GET":
        try:
            Creator.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        pageTour = request.GET.get('pageTour', 1)
        pageTeam = request.GET.get('pageTeam', 1)
        idTournament = request.GET.get('tournament', None)
        if idTournament is not None:
            tour = Tournament.objects.get(id=idTournament)
            teamsPagina = getElementsPaginador (tour.teams.all(), pageTeam, paginator_creator_progress_teams)
            if (not teamsPagina):
                messages.add_message(request, messages.ERROR, _('The tournament has not teams.'))
                return HttpResponseRedirect("/creator/tournaments?page="+pageTour)
            dict = {}
            for team in teamsPagina:
                dict[team.id] = []
                for ch in tour.get_challenges():
                    try:
                        chTour = ChallengesOfTournament.objects.get(challenge=ch, tournament=tour)
                        game = Game.objects.get(challengeOfTournament=chTour, team=team)
                        if game.completed:
                            dict[team.id].append(game)
                        else:
                            dict[team.id].append(game)
                    except Game.DoesNotExist:
                        game = None
                        dict[team.id].append(ch)
            return render_to_response('tournaments/creator/progress/teamsProgress.html', {'username':request.user.username,
                                             'team': team, 'maxChallenges': max_challenges_per_tournament,
                                             'teamsPagina': teamsPagina, 'dict': dict, 'tour': tour,
                                             'pageTeam': pageTeam, 'pageTour': pageTour}, RC(request))    
                
                    
        return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request)) 
    else:
        return HttpResponseRedirect("/")
    
def register_participant (email, creator_username, error_msg, success_msg, show_error_msg, show_success_msg):
    try:
        user=User.objects.get(username=email)
        error_msg = error_msg + email + "; "
        show_error_msg = True
    except User.DoesNotExist:
        try:
            user=User.objects.get(email=email)
            error_msg = error_msg + email + "; "
            show_error_msg = True
        except User.DoesNotExist:
            password = get_random_string(length=32)
            user = Participant.objects.create_user(username = email, email=email, password=password, creator_username=creator_username)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            c = {
                    'email':email,
                    'uid':uid,
                    'token':token,
                    'id':user.username}
    
            body = render_to_string("tournaments/password/email_new_participant.html",c)
            try:
                subject = _("Welcome to Dr.Scratch for tournaments")
                sender ="afdezroig@gmail.com"
                to = [email]
                mail = EmailMessage(subject,body,sender,to)
                mail.send()
            except:
                """"""
            success_msg = success_msg + email + "; "
            show_success_msg = True
    return error_msg, success_msg, show_error_msg, show_success_msg
    
def creatorNewParticipants (request):
    if request.method == "GET":
        return render_to_response('tournaments/creator/newParticipant/main_new_participants.html', 
                                  {'username':request.user.username, 'maxNewPart': range(int (max_new_participants))}, RC(request))
    else:
        try:
            creator = Creator.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        error_msg = _('The following emails are already included in Dr. Scratch (they where not registered): ')
        show_error_msg = False
        success_msg = _('The following emails were successfully registered in Dr. Scratch: ')
        show_success_msg = False
        format_msg = _('The following emails have wrong format (they where not registered): ')
        show_format_msg = False
        if "uploadCSV" in request.POST:
            try:
                file = request.FILES['csvFile']
            except MultiValueDictKeyError:
                messages.add_message(request, messages.ERROR, _('You have to include a CSV file.'))
                return render_to_response('tournaments/creator/newParticipant/main_new_participants.html', 
                                          {'username':request.user.username, 'maxNewPart': range(int (max_new_participants))}, RC(request))
            file_name = file.name.encode('utf-8')
            if file_name.endswith('.csv'):
                for i in range(int (max_new_participants)):
                    # read line
                    email = file.readline().rstrip()
                    # check if line is not empty
                    if email:
                        if re.match("[^@]+@[^\.]+\..+", email) != None:
                            error_msg, success_msg, show_error_msg, show_success_msg = register_participant (email, creator.username, error_msg, success_msg, show_error_msg, show_success_msg)
                        else:
                            format_msg = format_msg + email + "; "
                            show_format_msg = True 
                file.close()
            else:
                messages.add_message(request, messages.ERROR, _('The file added is not a CSV file.'))
        elif "uploadTXT" in request.POST:
            try:
                file = request.FILES['txtFile']
            except MultiValueDictKeyError:
                messages.add_message(request, messages.ERROR, _('You have to include a TXT file.'))
                return render_to_response('tournaments/creator/newParticipant/main_new_participants.html', 
                                          {'username':request.user.username, 'maxNewPart': range(int (max_new_participants))}, RC(request))
            file_name = file.name.encode('utf-8')
            if file_name.endswith('.txt'):
                for i in range(int (max_new_participants)):
                    # read line
                    email = file.readline().rstrip()
                    # check if line is not empty
                    if email:
                        if re.match("[^@]+@[^\.]+\..+", email) != None:
                            error_msg, success_msg, show_error_msg, show_success_msg = register_participant (email, creator.username, error_msg, success_msg, show_error_msg, show_success_msg)
                        else:
                            format_msg = format_msg + email + "; "
                            show_format_msg = True 
                file.close()
            else:
                messages.add_message(request, messages.ERROR, _('The file added is not a TXT file.'))
        else:    
            for i in range(int (max_new_participants)):
                email = request.POST['email_'+str(i)]
                if (email != ''):
                    error_msg, success_msg, show_error_msg, show_success_msg = register_participant (email, creator.username, error_msg, success_msg, show_error_msg, show_success_msg)
                    
        if show_error_msg:            
            messages.add_message(request, messages.ERROR, error_msg)
        if show_success_msg:
            messages.add_message(request, messages.SUCCESS, success_msg)
        if show_format_msg:
            messages.add_message(request, messages.ERROR, format_msg)
        return render_to_response('tournaments/creator/newParticipant/main_new_participants.html', 
            {'username':request.user.username, 'maxNewPart': range(int (max_new_participants))}, RC(request))
        
def validationCreator (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                creator = Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            """Muestro los torneos con validacion manual creados por dicho creador"""
            tour = Tournament.objects.filter(creator=creator.username, manualValidation=True)
            tournaments = []
            for t in tour:
                chTour = ChallengesOfTournament.objects.filter(tournament=t)
                games = Game.objects.none()
                for c in chTour:
                    games = games | Game.objects.filter(challengeOfTournament=c, completed=False, done=True)
                if games:
                    tournaments.append(t)
            page = request.GET.get('page', 1)
            tournamentsPagina = getElementsPaginador (tournaments, page, paginator_creator_tournaments)
            return render_to_response('tournaments/creator/validation/validation.html', {'username':request.user.username, 'tournamentsPagina': tournamentsPagina}, RC(request))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        return HttpResponseRedirect("/")   
    
def validateTournamentCreator (request):
    if request.method == "GET":
        if request.user.is_authenticated():
            try:
                Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            idTournament = request.GET.get('tournament', None)
            page = request.GET.get('page', 1)
            pageGame = request.GET.get('pageGame', 1)
            if idTournament is not None:
                tour = Tournament.objects.get(id=idTournament)
                chTour = ChallengesOfTournament.objects.filter(tournament=tour)
                games = Game.objects.none()
                for c in chTour:
                    games = games | Game.objects.filter(challengeOfTournament=c, completed=False, done=True)
                gamesPagina = getElementsPaginador (games, pageGame, paginator_validate_games)
                return render_to_response('tournaments/creator/validation/validate.html', 
                                          {'username':request.user.username, 'gamesPagina': gamesPagina, 'page': page, 'tour': tour}, RC(request))
            else:
                messages.add_message(request, messages.ERROR, _('The selected tournament cannot be found.'))
                return HttpResponseRedirect("/creator/validation?page="+str(page))
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
    else:
        if request.user.is_authenticated():
            try:
                Creator.objects.get(username=request.user.username)
            except:
                messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
                return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
            page = request.GET.get('page', 1)
            pageGame = request.GET.get('pageGame', 1)
            idGame = request.POST.get('idGame', None)
            if idGame is not None:
                game = Game.objects.get(id=idGame)
                game.completed = True
                game.save()
                messages.add_message(request, messages.SUCCESS, _('Game validated successfully.'))
                return HttpResponseRedirect("/creator/validate/tournament?page="+str(page)+"&pageGame="+str(pageGame)+"&tournament="+str(game.challengeOfTournament.tournament.id)) 
            else:
                messages.add_message(request, messages.ERROR, _('The selected game cannot be found.'))
                return HttpResponseRedirect("/creator/validation?page="+str(page)) 
        else:
            messages.add_message(request, messages.ERROR, _('Session expired. Please log in again.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))

def teamsParticipant (request):
    if request.method == "GET":
        try:
            participant = Participant.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        """Busco los equipos asociados al participante"""
        teams = Team.objects.filter(participant=participant.id)
        page = request.GET.get('pageTeam', 1)
        teamsPagina = getElementsPaginador (teams, page, paginator_participant_teams)
        return render_to_response('tournaments/participant/teamsPart.html', {'username':request.user.username, 'participant': participant,
                                                                         'teamsPagina': teamsPagina}, RC(request))
    else:
        return HttpResponseRedirect("/")
    
def tournamentsParticipant (request):
    if request.method == "GET":
        try:
            participant = Participant.objects.get(username=request.user.username)
        except:
            messages.add_message(request, messages.ERROR, _('Logged user cannot be found.'))
            return render_to_response('tournaments/main_tournaments.html', {'username':None}, RC(request))
        idTeam = request.GET.get('team', None)
        if idTeam is not None:
            team = Team.objects.get(id=idTeam)
            pageTour = request.GET.get('pageTour', 1)
            error = request.GET.get('error', None)
            if error is not None:
                error = bool(error)
            id_error = request.GET.get('id_error', None)
            if id_error is not None:
                id_error = bool(id_error)
            no_exists = request.GET.get('no_exists', None)
            if no_exists is not None:
                no_exists = bool(no_exists)
            if team:
                totalTours = []
                for t in team.tournament_set.all():
                    totalTours.append(t)
                tournamentsPagina = getElementsPaginador (totalTours, pageTour, paginator_participant_touraments)
                dict = {}
                for tour in tournamentsPagina:
                    """Obtengo los retos y juegos (si los hay) de cada torneo"""
                    dict[tour.id] = []
                    for ch in tour.get_challenges():
                        try:
                            chTour = ChallengesOfTournament.objects.get(challenge=ch, tournament=tour)
                            game = Game.objects.get(challengeOfTournament=chTour, team=team)
                            if game.completed:
                                dict[tour.id].append(game)
                            else:
                                dict[tour.id].append(game)
                                break
                        except Game.DoesNotExist:
                            game = None
                            dict[tour.id].append(ch)
                            break
                pageTeam = request.GET.get('pageTeam', 1)
                return render_to_response('tournaments/participant/tournamentsPart.html', {'username':request.user.username, 'participant': participant,
                                                                         'team': team, 'maxChallenges': max_challenges_per_tournament,
                                                                         'error': error, 'id_error': id_error, 'no_exists': no_exists,
                                                                         'tournamentsPagina': tournamentsPagina, 'dict': dict,
                                                                         'pageTeam': pageTeam}, RC(request))
            else:
                messages.add_message(request, messages.ERROR, _('The selected team cannot be found.'))
                page = request.GET.get('pageTeam', 1)
                return HttpResponseRedirect("/participant/teams?page="+str(page))  
        else:
            messages.add_message(request, messages.ERROR, _('The selected team cannot be found.'))
            page = request.GET.get('pageTeam', 1)
            return HttpResponseRedirect("/participant/teams?page="+str(page))  
    else:
        return HttpResponseRedirect("/")

def get_trans_keys ():
    dict = {}
    dict['Abstracción'] = 'abstraction'
    dict['Paralelismo'] = 'parallelism'
    dict['Pensamiento lógico'] = 'logic'
    dict['Sincronización'] = 'synchronization'
    dict['Control de flujo'] = 'flowControl'
    dict['Interactividad con el usuario'] = 'userInteractivity'
    dict['Representación de la información'] = 'dataRepresentation'
    return dict

def evaluate(d, idChallenge, idTeam, idTournament):
    try:
        challenge = Challenge.objects.get(id=idChallenge)
        team = Team.objects.get(id=idTeam)
        tournament = Tournament.objects.get(id=idTournament)
    except Challenge.DoesNotExist or Team.DoesNotExist or Tournament.DoesNotExist:
        return None
    if challenge and team and tournament:
        trans_keys = get_trans_keys()
        total_points = 0
        try:
            chTour = ChallengesOfTournament.objects.get(challenge=challenge, tournament=tournament)
            game = Game.objects.get(challengeOfTournament=chTour, team=team)
        except ChallengesOfTournament.DoesNotExist:
            return None
        except Game.DoesNotExist:
            newGame = Game()
            newGame.challengeOfTournament = chTour
            newGame.team = team
            newGame.done = True
            if (tournament.manualValidation):
                newGame.completed = False
            else:
                newGame.completed = True
            for key, value in d["mastery"].items():
                if (key != 'points' and key != 'maxi'):
                    setattr(newGame, trans_keys[key], value)
                    if(getattr(newGame, trans_keys[key]) < getattr(challenge, trans_keys[key])):
                        newGame.completed = False
                        newGame.done = False
                    game_value = getattr(newGame, trans_keys[key])
                    total_points = total_points + game_value
                    d["mastery"][key] = game_value
            d["mastery"]["points"] = total_points
            if (newGame.done == True and tournament.notificationPeriod == 1):
                try:
                    creator = Creator.objects.get(username = team.creator)
                    c = {'tournament':tournament.name}
                    body = render_to_string("tournaments/creator/email_valid.html",c)
                    subject = _("Dr. Scratch Tournaments: Manual Validation")
                    sender ="afdezroig@gmail.com"
                    to = [creator.email]
                    email = EmailMessage(subject,body,sender,to)
                    email.send()
                except Exception as e:
                    print '%s (%s)' % (e.message, type(e))
            return newGame
        if (game):
            if (game.done == False):
                enviar = True
            else:
                enviar = False
                
            game.done = True
            if (tournament.manualValidation):
                game.completed = False
            else:
                game.completed = True
            for key, value in d["mastery"].items():
                if (key != 'points' and key != 'maxi'):
                    if (value > getattr(game, trans_keys[key])):
                        setattr(game, trans_keys[key], value)
                    if (getattr(game, trans_keys[key]) < getattr(challenge, trans_keys[key])):
                        game.completed = False
                        game.done = False
                    game_value = getattr(game, trans_keys[key])
                    total_points = total_points + game_value
                    d["mastery"][key] = game_value
            d["mastery"]["points"] = total_points
            if (enviar == True and game.done == True and tournament.notificationPeriod == 1):
                try:
                    creator = Creator.objects.get(username = team.creator)
                    c = {'tournament':tournament.name}
                    body = render_to_string("tournaments/creator/email_valid.html",c)
                    subject = _("Dr. Scratch Tournaments: Manual Validation")
                    sender ="afdezroig@gmail.com"
                    to = [creator.email]
                    email = EmailMessage(subject,body,sender,to)
                    email.send()
                except Exception as e:
                    print '%s (%s)' % (e.message, type(e))
            return game
        else:
            return None
    else:
        return None
    
def playParticipant (request):
    if request.method == "POST": 
        idChallenge = request.POST.get('finalIdChallenge', None)
        idTeam = request.POST.get('idTeam', None)
        idTournament = request.POST.get('idTournament', None)
        pageTour = request.GET.get('pageTour', 1)
        pageTeam = request.GET.get('pageTeam', 1)
        error = False
        id_error = False
        no_exists = False
        if "_upload" in request.POST:
            d = _upload(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam+"&error="+str(error))
            else:
                filename = request.FILES['zipFile'].name.encode('utf-8')
                dic = {'url': "",'filename':filename}
                d.update(dic)
                game = evaluate(d, idChallenge, idTeam, idTournament)
                if (game is None):
                    messages.add_message(request, messages.ERROR, _('There was an error analyzing your project'))
                    return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam)
                else:
                    game.save()
                    d['username'] = request.user.username
                    d['elem'] = game
                    d['pageTour'] = pageTour
                    d['pageTeam'] = pageTeam
                    return render_to_response("tournaments/participant/results.html", d)
        elif '_url' in request.POST:
            d = _url(request)
            if d['Error'] == 'analyzing':
                return render_to_response('error/analyzing.html',
                                          RC(request))
            elif d['Error'] == 'MultiValueDict':
                error = True
                return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam+"&error="+str(error))
            elif d['Error'] == 'id_error':
                id_error = True
                return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam+"&id_error="+str(id_error))
            elif d['Error'] == 'no_exists':
                no_exists = True
                return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam+"&no_exists="+str(no_exists))
            else:
                form = UrlForm(request.POST)
                url = request.POST['urlProject']
                filename = url
                dic = {'url': url, 'filename':filename}
                d.update(dic)
                game = evaluate(d, idChallenge, idTeam, idTournament)
                if (game is None):
                    messages.add_message(request, messages.ERROR, _('There was an error analyzing your project'))
                    return HttpResponseRedirect("/participant/tournaments?team="+idTeam+"&pageTour="+pageTour+"&pageTeam="+pageTeam)
                else:
                    game.save()
                    d['username'] = request.user.username
                    d['elem'] = game
                    d['pageTour'] = pageTour
                    d['pageTeam'] = pageTeam
                    return render_to_response("tournaments/participant/results.html", d)