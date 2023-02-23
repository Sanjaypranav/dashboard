from operator import pos
from flask import Flask, json, jsonify, request, Blueprint, send_file, Response
from flask_httpauth import HTTPBasicAuth
from app import session, app
import datetime
import time
import pytz
from dateutil.relativedelta import relativedelta
import pymongo

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from werkzeug.utils import redirect

import bcrypt

apiBlueprint = Blueprint('pureAPI', __name__)

from twilio.twiml.voice_response import VoiceResponse, Connect, Gather
from twilio.rest import Client

import requests
from requests.auth import HTTPBasicAuth as ReqHTTPBasicAuth

import config
from pyAreadCodes import areaCodeTZ
from pyStateLaws import stateLaws
import pyAreadCodes
import pyPostalCodes

import string
import random
import os
import math
from bson.objectid import ObjectId

import stripe

from app import logger
from vicidialAPI import getGMTOffset

import pymysql.cursors
from sqlescapy import sqlescape

auth = HTTPBasicAuth()

def getConnection(host, user, passwd, db='asterisk'):
    return pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=passwd,
                             database=db,
                             cursorclass=pymysql.cursors.DictCursor)

def connectToDB():
    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    return mongoDB

def unsetCompanyID():
    try:
        session['user']['company_id'] = None
        session.modified = True
    except:
        pass

def validateLogin():
    try:
        if session['user']:
            return True
        else:
            return False
    except:
        return False

def validateCompany(companyID):
    try:
        if str(companyID) in session['companies']:
            return True
    except:
        pass
    return False

@apiBlueprint.route('/api/v1/validate-login', methods=['GET'])
def apiValidateLogin():
    if validateLogin():
        return jsonify({'Message':"Success"})
    return jsonify({'Message':"Failure"})

@apiBlueprint.route('/set-company-id')
def setCompanyID():
    if validateLogin():
        if request.args.get('companyid') and request.args.get('call_type'):
            companyID = request.args.get('companyid')
            if validateCompany(companyID):
                session['user']['company_id'] = companyID
                #company = Companies.query.filter_by(id=companyID).first()
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                company = companies_col.find_one({"_id":ObjectId(companyID)})
                session['company'] = {
                    'id':companyID,
                    'logo':company['logo'],
                    'package_type':company['package_type'],
                    'name':company['name'],
                    'email':company['email'],
                    'phone':company['phone'],
                    'website':company['website'],
                    'address':company['address'],
                    'app_layout':company['app_layout'],
                    'rtl':company['rtl'],
                    'status':company['status']
                }
                session['call_type'] =  request.args.get('call_type')
                if session['user']['super_admin'] == True:
                    session['permission_sets'] = {
                        companyID:{
                            "613b89ed3e1f2f627b4892f2":{
                                "display_name":"Staff Create",
                                "id":"613b89ed3e1f2f627b4892f2",
                                "name":"staff_create"
                            },
                            "613b89ed3e1f2f627b4892f3":{
                                "display_name":"Staff Edit",
                                "id":"613b89ed3e1f2f627b4892f3",
                                "name":"staff_edit"
                            },
                            "613b89ed3e1f2f627b4892f4":{
                                "display_name":"Staff Delete",
                                "id":"613b89ed3e1f2f627b4892f4",
                                "name":"staff_delete"
                            },
                            "613b89ed3e1f2f627b4892f5":{
                                "display_name":"Staff Assign Role",
                                "id":"613b89ed3e1f2f627b4892f5",
                                "name":"assign_role"
                            },
                            "613b89ed3e1f2f627b4892f6":{
                                "display_name":"Sales Member Create",
                                "id":"613b89ed3e1f2f627b4892f6",
                                "name":"sales_member_create"
                            },
                            "613b89ed3e1f2f627b4892f7":{
                                "display_name":"Sales Member Edit",
                                "id":"613b89ed3e1f2f627b4892f7",
                                "name":"sales_member_edit"
                            },
                            "613b89ed3e1f2f627b4892f8":{
                                "display_name":"Sales Member Delete",
                                "id":"613b89ed3e1f2f627b4892f8",
                                "name":"sales_member_delete"
                            },
                            "613b89ed3e1f2f627b4892f9":{
                                "display_name":"Import Lead",
                                "id":"613b89ed3e1f2f627b4892f9",
                                "name":"import_lead"
                            },
                            "613b89ed3e1f2f627b4892fa":{
                                "display_name":"Export Lead",
                                "id":"613b89ed3e1f2f627b4892fa",
                                "name":"export_lead"
                            },
                            "613b89ed3e1f2f627b4892fb":{
                                "display_name":"View Campaigns",
                                "id":"613b89ed3e1f2f627b4892fb",
                                "name":"campaign_view"
                            },
                            "613b89ed3e1f2f627b4892fc":{
                                "display_name":"View All Campaigns",
                                "id":"613b89ed3e1f2f627b4892fc",
                                "name":"campaign_view_all"
                            },
                            "613b89ed3e1f2f627b4892fd":{
                                "display_name":"Campaign Create",
                                "id":"613b89ed3e1f2f627b4892fd",
                                "name":"campaign_create"
                            },
                            "613b89ed3e1f2f627b4892fe":{
                                "display_name":"Campaign Edit",
                                "id":"613b89ed3e1f2f627b4892fe",
                                "name":"campaign_edit"
                            },
                            "613b89ed3e1f2f627b4892ff":{
                                "display_name":"Campaign Delete",
                                "id":"613b89ed3e1f2f627b4892ff",
                                "name":"campaign_delete"
                            },
                            "613b89ed3e1f2f627b489300":{
                                "display_name":"View Email Template",
                                "id":"613b89ed3e1f2f627b489300",
                                "name":"email_template_view"
                            },
                            "613b89ed3e1f2f627b489301":{
                                "display_name":"View All Email Templates",
                                "id":"613b89ed3e1f2f627b489301",
                                "name":"email_template_view_all"
                            },
                            "613b89ed3e1f2f627b489302":{
                                "display_name":"Email Template Create",
                                "id":"613b89ed3e1f2f627b489302",
                                "name":"email_template_create"
                            },
                            "613b89ed3e1f2f627b489303":{
                                "display_name":"Email Template Edit",
                                "id":"613b89ed3e1f2f627b489303",
                                "name":"email_template_edit"
                            },
                            "613b89ed3e1f2f627b489304":{
                                "display_name":"Email Template Delete",
                                "id":"613b89ed3e1f2f627b489304",
                                "name":"email_template_delete"
                            },
                            "613b89ed3e1f2f627b489305":{
                                "display_name":"View Campaign Forms",
                                "id":"613b89ed3e1f2f627b489305",
                                "name":"form_view"
                            },
                            "613b89ed3e1f2f627b489306":{
                                "display_name":"View All Campaign Forms",
                                "id":"613b89ed3e1f2f627b489306",
                                "name":"form_view_all"
                            },
                            "613b89ed3e1f2f627b489307":{
                                "display_name":"Form Campaign Create",
                                "id":"613b89ed3e1f2f627b489307",
                                "name":"form_create"
                            },
                            "613b89ed3e1f2f627b489308":{
                                "display_name":"Form Campaign Edit",
                                "id":"613b89ed3e1f2f627b489308",
                                "name":"form_edit"
                            },
                            "613b89ed3e1f2f627b489309":{
                                "display_name":"Form Campaign Delete",
                                "id":"613b89ed3e1f2f627b489309",
                                "name":"form_delete"
                            },
                            "61575f55679cf939aca4ad74":{
                                "display_name":"AI Agents View",
                                "id":"61575f55679cf939aca4ad74",
                                "name":"ai_agents_view"
                            },
                            "61575f56679cf939aca4ad75":{
                                "display_name":"AI Agents Edit",
                                "id":"61575f56679cf939aca4ad75",
                                "name":"ai_agents_edit"
                            },
                            "61575f56679cf939aca4ad76":{
                                "display_name":"AI Agents Delete",
                                "id":"61575f56679cf939aca4ad76",
                                "name":"ai_agents_delete"
                            },
                            "61575f823c986a2f938bc0be":{
                                "display_name":"Call Manager View",
                                "id":"61575f823c986a2f938bc0be",
                                "name":"call_manager_view"
                            },
                            "61575f833c986a2f938bc0bf":{
                                "display_name":"Call Manager Edit",
                                "id":"61575f833c986a2f938bc0bf",
                                "name":"call_manager_edit"
                            },
                            "61575f843c986a2f938bc0c0":{
                                "display_name":"Call Manager Delete",
                                "id":"61575f843c986a2f938bc0c0",
                                "name":"call_manager_delete"
                            },
                            "61575fb85e41d8e13fea3888":{
                                "display_name":"Call History View",
                                "id":"61575fb85e41d8e13fea3888",
                                "name":"call_history_view"
                            },
                            "61575fb95e41d8e13fea3889":{
                                "display_name":"Call History Edit",
                                "id":"61575fb95e41d8e13fea3889",
                                "name":"call_history_edit"
                            },
                            "61575fb95e41d8e13fea388a":{
                                "display_name":"Call History Delete",
                                "id":"61575fb95e41d8e13fea388a",
                                "name":"call_history_delete"
                            },
                            "6157600411599235efcae347":{
                                "display_name":"Import Caller IDs",
                                "id":"6157600411599235efcae347",
                                "name":"import_caller_ids"
                            },
                            "61576045b38aa96d7e7e566f":{
                                "display_name":"Caller IDs View",
                                "id":"61576045b38aa96d7e7e566f",
                                "name":"caller_id_view"
                            },
                            "61576046b38aa96d7e7e5670":{
                                "display_name":"Caller IDs Edit",
                                "id":"61576046b38aa96d7e7e5670",
                                "name":"caller_id_edit"
                            },
                            "61576046b38aa96d7e7e5671":{
                                "display_name":"caller_id_delete",
                                "id":"61576046b38aa96d7e7e5671",
                                "name":"Caller IDs Delete"
                            },
                            "6157607468e998dff84941a7":{
                                "display_name":"Billing View",
                                "id":"6157607468e998dff84941a7",
                                "name":"billing_view"
                            },
                            "6157607568e998dff84941a8":{
                                "display_name":"Billing Edit",
                                "id":"6157607568e998dff84941a8",
                                "name":"billing_edit"
                            },
                            "6157607568e998dff84941a9":{
                                "display_name":"Billing Delete",
                                "id":"6157607568e998dff84941a9",
                                "name":"billing_delete"
                            },
                            "6157637df5708a04ced1ba68":{
                                "display_name":"Settings View",
                                "id":"6157637df5708a04ced1ba68",
                                "name":"settings_view"
                            },
                            "6157637ef5708a04ced1ba69":{
                                "display_name":"Settings Edit",
                                "id":"6157637ef5708a04ced1ba69",
                                "name":"settings_edit"
                            },
                            "6157637ef5708a04ced1ba6a":{
                                "display_name":"Settings Delete",
                                "id":"6157637ef5708a04ced1ba6a",
                                "name":"settings_delete"
                            },
                            "613b89ed3e1f2f627b4892fb":{
                                "display_name":"View Campaigns",
                                "id":"613b89ed3e1f2f627b4892fb",
                                "name":"campaign_view"
                            },
                            "613b89ed3e1f2f627b4892fc":{
                                "display_name":"View All Campaigns",
                                "id":"613b89ed3e1f2f627b4892fc",
                                "name":"campaign_view_all"
                            },
                            "613b89ed3e1f2f627b489300":{
                                "display_name":"View Email Template",
                                "id":"613b89ed3e1f2f627b489300",
                                "name":"email_template_view"
                            },
                            "613b89ed3e1f2f627b489306":{
                                "display_name":"View All Campaign Forms",
                                "id":"613b89ed3e1f2f627b489306",
                                "name":"form_view_all"
                            },
                            "61575f823c986a2f938bc0be":{
                                "display_name":"Call Manager View",
                                "id":"61575f823c986a2f938bc0be",
                                "name":"call_manager_view"
                            },
                            "61575fb85e41d8e13fea3888":{
                                "display_name":"Call History View",
                                "id":"61575fb85e41d8e13fea3888",
                                "name":"call_history_view"
                            },
                            "61576045b38aa96d7e7e566f":{
                                "display_name":"Caller IDs View",
                                "id":"61576045b38aa96d7e7e566f",
                                "name":"caller_id_view"
                            },
                            "6157607468e998dff84941a7":{
                                "display_name":"Billing View",
                                "id":"6157607468e998dff84941a7",
                                "name":"billing_view"
                            },
                            "618e9207b915bfe19a75e2f2":{
                                "display_name":"Campaign Management",
                                "id":"618e9207b915bfe19a75e2f2",
                                "name":"campaign_management"
                            },
                            "618e922cb915bfe19a75e2f3":{
                                "display_name":"Lead Management",
                                "id":"618e922cb915bfe19a75e2f3",
                                "name":"lead_management"
                            },
                            "618e924bb915bfe19a75e2f4":{
                                "id":"618e924bb915bfe19a75e2f4"
                            }
                        }
                    }
                    
                #client.close()
                return redirect('/')
            try:  
                session['user'].pop('company_id', None)
            except:
                pass
            return redirect('/companies')
    return redirect('/login')

@apiBlueprint.route('/api/bot', methods=['GET', 'POST', 'PUT', 'DELETE'])
def aiAPI():
    return send_file('static/testResponse.xml')

@apiBlueprint.route('/api/v1/ai-agents', methods=['GET', 'POST', 'PUT', 'DELETE'])
def aiAgentsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        aiAgents = mongoDB['ai_agents']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('agentid'):
                    filterBy['id'] = request.args.get('agentid')

                if request.args.get('userid'):
                    filterBy['user_id'] = request.args.get('userid')
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for aiAgent in aiAgents.find():
                    valid = True
                    try:
                        if session['user']['company_id']:
                            users_col = mongoDB['users']
                            aiAgentCompany = users_col.find_one({'id':ObjectId(aiAgent['user_id'])})
                            if str(aiAgentCompany['company_id']) != str(session['user']['company_id']):
                                valid = False
                    except:
                        pass
                    
                    if valid:
                        returnPost.append(convertToJSON(aiAgent))
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                simpleUpdateRow(aiAgents, request.json, request.method)
                #client.close()
                return jsonify({'Message':'Success'})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/virtual-agents', methods=['GET', 'POST', 'PUT', 'DELETE'])
def virtualAgentsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        virtualAgents = mongoDB['virtual_agents']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('agentid'):
                    filterBy['_id'] = ObjectId(request.args.get('agentid'))

                try:
                    if session['user']['company_id']:
                        try:
                            filterBy['company_id'] = ObjectId(session['user']['company_id'])
                        except:
                            pass
                        filterBy['status'] = True
                    else:
                        company_list = []
                        for company in session['companies']:
                            company_list.append(ObjectId(company))
                        filterBy['company_id'] = {
                            "$in" : company_list
                        }
                except:
                    pass
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                
                returnPost = []
                for virtualAgent in virtualAgents.find(filterBy):
                    virtualAgentData = convertToJSON(virtualAgent)
                    try:
                        companies_col = mongoDB['companies']
                        company = companies_col.find_one({'_id':ObjectId(virtualAgentData['company_id'])})
                        virtualAgentData['company_name'] = company['name']
                    except:
                        pass
                    returnPost.append(virtualAgentData)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                message = simpleUpdateRow(virtualAgents, request.json, request.method)
                #client.close()
                return jsonify({'Message':message['Message']})
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/articles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def articlesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        articles = mongoDB['articles']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('articleid'):
                    filterBy['_id'] = ObjectId(request.args.get('articleid'))
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                
                returnPost = []

                for article in articles.find(filterBy):
                    user_col = mongoDB['users']
                    user = user_col.find_one({'_id':ObjectId(article['user_id'])})
                    articleData = convertToJSON(article)
                    articleData['user_first_name'] = user['first_name']
                    articleData['user_last_name'] = user['last_name']
                    returnPost.append(articleData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                try:
                    return jsonify(simpleUpdateRow(articles, request.json, request.method))
                except:
                    return jsonify({'Message':'Failure'})
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/appointments', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appointmentsAPI():
    if validateLogin():
        if request.method == 'GET':
            return jsonify({"Message":"Failure"})
@apiBlueprint.route('/api/v1/follow-calls', methods=['GET', 'POST', 'PUT', 'DELETE'])
def followUpCallsAPI():
    if validateLogin():
        if request.method == 'GET':
            return jsonify({"Message":"Failure"})
@apiBlueprint.route('/api/v1/campaigns', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('campaignid'):
                    filterBy['_id'] = ObjectId(request.args.get('campaignid'))

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass

                if request.args.get('status'):
                    filterBy['status'] = request.args.get('status')

                if request.args.get('created_by'):
                    filterBy['created_by'] = request.args.get('created_by')
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = []
                for campaign in campaigns_col.find(filterBy):
                    userData = []
                    users_col = mongoDB['users']
                    for user in users_col.find({'company_id':campaign['company_id']}):
                        compaign_user_col = mongoDB['users']
                        if compaign_user_col.find_one({'user_id':user['_id']}):
                            userData.append({
                                'user_id':str(user['_id']),
                                'first_name':user['first_name'],
                                'last_name':user['last_name'],
                                'enabled':True
                            })
                        else:
                            userData.append({
                                'user_id':str(user['_id']),
                                'first_name':user['first_name'],
                                'last_name':user['last_name'],
                                'enabled':False
                            })

                    campaignData = convertToJSON(campaign)

                    campaignData['leads'] = []
                    campaignData['user_data'] = userData
                    campaignData['schedules'] = {}
                    
                    if request.args.get('summary'):
                        leads_total_summary_col = mongoDB['leads_total_summary']
                        summaryFilterBy = {
                            'campaign_id':campaign['_id']
                        }
                        lead_summary = leads_total_summary_col.find_one(summaryFilterBy)
                        try:
                            campaignData['total_leads'] = getInt(lead_summary['total_leads'])
                            campaignData['remaining_leads'] = getInt(lead_summary['remaining_leads'])
                        except:
                            campaignData['total_leads'] = 0
                            campaignData['remaining_leads'] = 0

                    if request.args.get('campaignid'):
                        # JUST BASE DATA FOR DEFAULTS
                        campaignData['schedules'] = {
                                    "friday": {
                                        "enabled": True,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "friday",
                                            "enabled": True,
                                            "hour": 9,
                                            "id": 13,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "friday",
                                            "enabled": True,
                                            "hour": 17,
                                            "id": 14,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "monday": {
                                        "enabled": True,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "monday",
                                            "enabled": True,
                                            "hour": 9,
                                            "id": 5,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "monday",
                                            "enabled": True,
                                            "hour": 17,
                                            "id": 6,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "saturday": {
                                        "enabled": False,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "saturday",
                                            "enabled": False,
                                            "hour": 9,
                                            "id": 15,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "saturday",
                                            "enabled": False,
                                            "hour": 17,
                                            "id": 16,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "sunday": {
                                        "enabled": False,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "sunday",
                                            "enabled": False,
                                            "hour": 9,
                                            "id": 3,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "sunday",
                                            "enabled": False,
                                            "hour": 17,
                                            "id": 4,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "thursday": {
                                        "enabled": True,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "thursday",
                                            "enabled": True,
                                            "hour": 9,
                                            "id": 11,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "thursday",
                                            "enabled": True,
                                            "hour": 17,
                                            "id": 12,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "tuesday": {
                                        "enabled": True,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "tuesday",
                                            "enabled": True,
                                            "hour": 9,
                                            "id": 7,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "tuesday",
                                            "enabled": True,
                                            "hour": 17,
                                            "id": 8,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    },
                                    "wednesday": {
                                        "enabled": True,
                                        "start": {
                                            "campaign_id": 63,
                                            "day_value": "wednesday",
                                            "enabled": True,
                                            "hour": 9,
                                            "id": 9,
                                            "minute": 0,
                                            "status": "start",
                                            "time_full": "09:00:00"
                                        },
                                        "stop": {
                                            "campaign_id": 63,
                                            "day_value": "wednesday",
                                            "enabled": True,
                                            "hour": 17,
                                            "id": 10,
                                            "minute": 0,
                                            "status": "stop",
                                            "time_full": "17:00:00"
                                        }
                                    }
                                }
                        scheduleFilterBy = {
                            'campaign_id':ObjectId(request.args.get('campaignid'))
                        }
                        schedule_col = mongoDB['campaign_schedule']
                        for schedule in schedule_col.find(scheduleFilterBy):
                            if not campaignData['schedules'].get(schedule['day_value']):
                                campaignData['schedules'][schedule['day_value']] = {}
                            
                            users_col = mongoDB['users']
                            loggedInUser = users_col.find_one({'_id':ObjectId(session['user']['user_id'])})

                            ## THIS IS FOR CONVERTING TIMES TO LOCAL TIME FOR THE LOGGED IN USER ##
                            source_date = datetime.datetime.now()
                            source_time_zone = pytz.timezone('UTC')
                            source_date = source_date.replace(hour=schedule['hour'], minute=schedule['minute'])
                            source_date_with_timezone = source_time_zone.localize(source_date)

                            ## WE THEN CONVERT IT TO THE TIMEZONE OF THE LOGGED IN USER ##
                            target_time_zone = pytz.timezone(loggedInUser['timezone'])
                            target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
                            campaignData['schedules'][schedule['day_value']][schedule['status']] = {
                                "id":str(schedule['_id']),
                                "campaign_id":str(schedule['campaign_id']),
                                "day_value":schedule['day_value'],
                                "status":schedule['status'],
                                "time_full":str(target_date_with_timezone.strftime('%H:%M')),
                                "hour":int(target_date_with_timezone.strftime('%H')),
                                "minute":int(target_date_with_timezone.strftime('%M')),
                                "enabled":schedule['enabled']
                            }
                            campaignData['schedules'][schedule['day_value']]['enabled'] = schedule['enabled']

                    returnPost.append(campaignData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                
                try:
                    users = postData['user_data']
                except:
                    users = None
                try:
                    if session['user']['company_id']:
                        postData['company_id'] = session['user']['company_id']
                except:
                    pass
                returnData = simpleUpdateRow(campaigns_col, request.json, request.method)

                if users:
                    campaignID = returnData['id']
                    campaign_member_col = mongoDB['campaign_members']
                    for user in users:
                        user['campaign_id'] = campaignID
                        simpleUpdateRow(campaign_member_col, user, request.method)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    schedules = updateData['schedule_data']
                    updateData.pop('schedule_data')
                except:
                    schedules = None
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                returnData = simpleUpdateRow(campaigns_col, updateData, request.method)

                if schedules:
                    for schedule in schedules:
                        try:
                            users_col = mongoDB['users']
                            loggedInUser = users_col.find_one({'_id':ObjectId(session['user']['user_id'])})

                            ## THIS IS FOR CONVERTING TIMES TO LOCAL TIME FOR THE LOGGED IN USER ##
                            time_full = datetime.datetime.strptime(schedule['time_full'], '%H:%M:%S')
                            offsetHours = tz_diff(loggedInUser['timezone'])
                            source_date = time_full.replace(hour=time_full.hour+offsetHours, minute=time_full.minute, second=0)

                            schedule['hour'] = int(source_date.strftime('%H'))
                            schedule['minute'] = int(source_date.strftime('%M'))
                            schedule['time_full'] = str(source_date.strftime('%H:%M:%S'))
                            schedule['campaign_id'] = updateData['id']
                            filterBy = {
                                'campaign_id':ObjectId(updateData['id']),
                                'day_value':schedule['day_value'],
                                'status':schedule['status']
                            }
                            campaign_schedule_col = mongoDB['campaign_schedule']
                            updateRow = campaign_schedule_col.find_one(filterBy)
                            if updateRow:
                                schedule['id'] = str(updateRow['_id'])
                                schedule['campaign_id'] = ObjectId(updateData['id'])
                                returnData = simpleUpdateRow(campaign_schedule_col, schedule, 'PUT')
                            else:
                                schedule['campaign_id'] = ObjectId(updateData['id'])
                                time_full = str(source_date.strftime('%H:%M:%S'))
                                schedule['hour'] = int(source_date.strftime('%H'))
                                schedule['minute'] = int(source_date.strftime('%M'))
                                
                                returnData = simpleUpdateRow(campaign_schedule_col, schedule, 'POST')
                        except:
                            pass          
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            #client.close()
            return jsonify(simpleUpdateRow(campaigns_col, request.json, request.method))

@apiBlueprint.route('/api/v1/campaigns/caller-ids', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignCallerIDsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        company_caller_ids_col = mongoDB['company_caller_ids']
        if request.method == 'GET':
            try:
                filterBy = {}
                valid = False
                if request.args.get('companyid'):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    valid = True
                else:
                    filterBy['company_id'] = ObjectId(session['company']['id'])
                    valid = True

                if request.args.get('callerid'):
                    filterBy['_id'] = ObjectId(request.args.get('callerid'))
                    valid = True
                
                if valid == False:
                    return jsonify({'Message':'Failure'})

                returnPost = []
                print(filterBy)
                for caller in company_caller_ids_col.find(filterBy):
                    callerData = convertToJSON(caller)
                    returnPost.append(callerData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            #try:
            postDataList = request.json

            companyID = session['company']['id']
            currList = []
            for caller in company_caller_ids_col.find({'company_id':ObjectId(companyID)}):
                currList.append(caller['caller_id'])

            filteredList = []
            for postData in postDataList:
                print(postData)
                if postData['caller_id'] not in currList:
                    postData['company_id'] = ObjectId(companyID)
                    filteredList.append(postData)

            returnPost = simpleUpdateRow(company_caller_ids_col, filteredList, request.method)
            #client.close()
            return jsonify(returnPost)
            #except:
            #    return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            returnPost = simpleUpdateRow(company_caller_ids_col, request.json, request.method)
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/campaigns/caller-ids/verify', methods=['GET','POST'])
def campaignCallerIDsVerifyAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaign_caller_ids_verify_col = mongoDB['caller_id_verifications']
        if request.method == 'GET':
            filterBy = {}
            if request.args.get('callerid'):
                filterBy['caller_id'] = ObjectId(request.args.get('callerid'))
            print(filterBy)
            verification_row = campaign_caller_ids_verify_col.find_one(filterBy)
            #verificationRow = CallerIDVerifications.query.filter_by(**filterBy).first()
            #client.close()
            return verification_row['status']

        elif request.method == 'POST':
            postDataList = request.json
            company_caller_ids_col = mongoDB['company_caller_ids']
            callerRow = company_caller_ids_col.find_one({'_id':ObjectId(postDataList['id'])})

            company_col = mongoDB['companies']
            company = company_col.find_one({'_id':ObjectId(callerRow['company_id'])})

            account_sid = company['twilio_account_sid']
            auth_token = company['twilio_auth_token']
            
            ref_num = ''.join(filter(str.isdigit, callerRow['caller_id']))
            if len(ref_num) == 10:
                ref_num = '+1'+ref_num
            try:
                friendly_name = callerRow['name']
            except:
                friendly_name = str(ref_num)
            twilClient = Client(account_sid, auth_token)
            validation_request = twilClient.validation_requests.create(
                friendly_name=friendly_name,
                status_callback='{}/api/v1/campaigns/caller-ids/verify/hook'.format(config.hostname),
                phone_number=ref_num
            )
            
            newRowData = {
                "caller_id":postDataList['id'],
                "verification_code":str(validation_request.validation_code),
                "account_sid":account_sid,
                "caller_id_number":ref_num,
                'status':'incomplete'
            }
            simpleUpdateRow(campaign_caller_ids_verify_col, newRowData, request.method)
            newRowData['caller_id'] = str(newRowData['caller_id'])
            newRowData['_id'] = str(newRowData['_id'])
            #client.close()
            return jsonify(newRowData)

@apiBlueprint.route('/api/v1/campaigns/caller-ids/verify/hook', methods=['POST'])
def campaignCallerIDsVerifyHookAPI():
    filterBy = {
        'account_sid':request.form.get('AccountSid'),
        'caller_id_number':request.form.get('Called'),
        'status':'incomplete'
    }

    #client = app.mongo_client
    mongoDB = app.mongo_client['jamesbon']
    campaign_caller_ids_verify_col = mongoDB['caller_id_verifications']
    campaign_caller_ids_verify_col.update_one(filterBy, { "$set": { "status" : request.form.get('VerificationStatus') } })

    if request.form.get('VerificationStatus') == 'success':
        filterBy = {
            'account_sid':request.form.get('AccountSid'),
            'caller_id_number':request.form.get('Called'),
            'status':'success'
        }
        verification_row = campaign_caller_ids_verify_col.find_one(filterBy)
        campaign_caller_ids_col = mongoDB['company_caller_ids']
        campaign_caller_ids_col.update_one({"_id":verification_row['caller_id']}, { "$set": { "verified" : True } })
    #client.close()
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/api/v1/campaigns/counts')
def campaignCountsAPI():
    if validateLogin():
        try:
            filterBy = {
                'status': {
                    '$ne':'completed'
                }
            }

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))

            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = ObjectId(session['user']['company_id'])
            except:
                pass
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass

            returnPost = []

            campaign_list = {}
            campaign_ids = []
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            for campaign in campaigns_col.find(filterBy):
                campaign_list[str(campaign['_id'])] = {
                    "id":campaign['_id'],
                    "name":campaign['name'],
                    "status":campaign['status']
                }
                campaign_ids.append(campaign['_id'])
            
            filterBy = {
                "campaign_id": {
                    "$in":campaign_ids
                }
            }
            leads_interest_col = mongoDB['leads_interest_summary']
            returnPost = []
            for campaign in leads_interest_col.find(filterBy):
                returnPost.append({
                    "interested": campaign['total_interested'], 
                    "name": campaign_list[str(campaign['campaign_id'])]['name'], 
                    "not_interested": campaign['total_uninterested']
                })
            #client.close()
            return jsonify(returnPost)
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/campaigns/make-call', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignCallerAPI():
    if validateLogin():
        if request.method == 'POST':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']
            try:
                postData = request.json
                phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
                
                refNum = None
                for x in postData['lead_data']:
                    if str(x['field_name']) in phoneNames:
                        refNum = ''.join(filter(str.isdigit, x['field_value']))
                        if len(refNum) == 10:
                            refNum = '+1'+refNum

                if refNum:
                    try:
                        leadID = ObjectId(postData['lead_id'])
                    except:
                        leadID = None
                    if leadID == None:
                        leadRow = leads_col.find_one({'campaign_id':ObjectId(postData['campaign_id']), 'reference_number':refNum})
                        if leadRow:
                            leadID = leadRow['_id']
                        if leadID == None:
                            updateData = {
                                'reference_number':refNum,
                                'campaign_id':ObjectId(postData['campaign_id']),
                                'lead_data':postData['lead_data'],
                                'call_logs':[],
                                'status':'unactioned'
                            }
                            
                            newRow = simpleUpdateRow(leads_col, updateData, request.method)
                            leadID = newRow['id']
                    else:
                        leadRow = leads_col.find_one({'_id':leadID})
                        refNum = ''.join(filter(str.isdigit, leadRow['reference_number']))
                        if len(refNum) == 10:
                            refNum = '+1'+refNum
                    campaign_col = mongoDB['campaigns']
                    campaign = campaign_col.find_one({'_id':ObjectId(postData['campaign_id'])})
                    if campaign:
                        company_col = mongoDB['companies']
                        company = company_col.find_one({'_id':campaign['company_id']})
                        account_sid = company['twilio_account_sid']
                        auth_token = company['twilio_auth_token']
                        print(account_sid)
                        print(auth_token)
                        virtual_agent_col = mongoDB['virtual_agents']
                        virtual_agent = virtual_agent_col.find_one({'_id':campaign['virtual_agent_id']})
                        if virtual_agent:
                            twilio_settings_col = mongoDB['twilio_numbers']
                            twilio_settings = twilio_settings_col.find_one({'company_id':campaign['company_id']})
                            transfer_number = virtual_agent['phone']
                            outbound_recording = twilio_settings['outbound_recording']
                            
                            # GRAB CALLER ID
                            caller_ids = campaign['caller_ids']
                            caller_id = caller_ids[random.randint(0,len(caller_ids)-1)]['caller_id']
                            #company_caller_ids_col = mongoDB['company_caller_ids']
                            #filter_by = {
                            #    "_id":ObjectId(campaign['caller_id'])
                            #}
                            #caller_id = company_caller_ids_col.find_one(filter_by)

                            account_sid = account_sid
                            auth_token = auth_token
                            twilClient = Client(account_sid, auth_token)
                            company_wallet_balance_col = mongoDB['company_wallet_balance']
                            filterBy = {
                                'company_id':campaign['company_id']
                            }
                            company_wallet_balance = company_wallet_balance_col.find_one(filterBy)
                            returnBalance = {
                                "paid_balance":getDecimal(company_wallet_balance['paid_amount']),
                                "refunded_balance":getDecimal(company_wallet_balance['refunded_amount']),
                                "charged_balance":getDecimal(company_wallet_balance['charge_amount'])
                            }
                            returnBalance['balance'] = returnBalance['paid_balance'] - returnBalance['refunded_balance'] - returnBalance['charged_balance']
                            if returnBalance['balance']  > .5:
                                call = twilClient.calls.create(
                                                        timeout=28,
                                                        application_sid=virtual_agent['app_id'],
                                                        to=refNum,
                                                        from_=caller_id,
                                                        caller_id=caller_id,
                                                        record=True,
                                                        recording_status_callback='{}recording/callback'.format(config.webhooks),
                                                        recording_status_callback_method='POST'
                                                )
                                print(call)
                                updateData = {
                                    'id':str(leadID),
                                    'status':'calling'
                                }
                                simpleUpdateRow(leads_col, updateData, 'PUT')
                                print(str(call.sid))
                                updateQuery = {
                                    "$push":{
                                        "call_logs":{
                                            'lead_id':leadID,
                                            'call_id':str(call.sid),
                                            'reference_number':refNum,
                                            'created_at':str(datetime.datetime.utcnow())[:-3],
                                            'updated_at':str(datetime.datetime.utcnow())[:-3]
                                        }
                                    }
                                }
                                leads_col.update_one({'_id':leadID}, updateQuery)

            except:
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/campaigns/schedule', methods=['GET', 'POST', 'PUT', 'DELETE'])
def campaignScheduleAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaignSchedules = mongoDB['campaign_schedule']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('campaignid'):
                    filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))

                returnPost = []

                for schedule in campaignSchedules.find(filterBy):
                    scheduleData = convertToJSON(schedule)
                    returnPost.append(scheduleData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        else:
            returnPost = simpleUpdateRow(campaignSchedules, request.json, request.method)
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/companies', methods=['GET', 'POST', 'PUT', 'DELETE'])
def companiesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies = mongoDB['companies']
        if request.method == 'GET':
            try:
                company_list = []
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    filterBy = {
                        "_id":{
                            "$in" : company_list
                        }
                    }
                
                limit = 10
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = []
                for company in companies.find(filterBy):
                    logoName = '/static/img/brand/default.png'
                    companyData = convertToJSON(company)
                    if company['logo']:
                        logoName = '/static/img/brand/'+str(company['logo'])
                    companyData['logo'] = logoName

                    companyData['total_users'] = 0
                    
                    if request.args.get('companyid'):
                        filterBy = {
                            'company_id':company['_id']
                        }
                        company_billing_col = mongoDB['company_billing']
                        billing = company_billing_col.find_one(filterBy)
                        if billing:
                            companyData['charge_type'] = billing['charge_type']
                            companyData['charge_amount'] = billing['charge_amount']
                        else:
                            companyData['charge_type'] = 0
                            companyData['charge_amount'] = 0.35
                    returnPost.append(companyData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                if postData['create_twilio_sub']:
                    twil_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_SID)

                    account = twil_client.api.accounts.create(friendly_name=postData['name'])
                    postData['twilio_account_sid'] = str(account.sid)
                    postData['twilio_auth_token'] = str(account.auth_token)
                newRow = simpleUpdateRow(companies, request.json, request.method)

                # WE WANT TO ADD THAT COMPANY TO OUR CURRENT LIST AND TO DO THAT WE
                # WILL ADD A NEW ADMIN ROLE AND ASSIGN IT TO US
                if session['companies']:
                    postData = {
                        'company_id':newRow['id'],
                        'name':'Admin',
                        'display_name':'Admin',
                        'description':'Built In Admin Role',
                        'permissions':[]
                    }
                    roles_col = mongoDB['roles']
                    newRoleRow = simpleUpdateRow(roles_col, postData, request.method)

                    postData = {
                        'user_id':session['user']['user_id'],
                        'role_id':newRoleRow['id']
                    }
                    roles_col = mongoDB['role_user_new']
                    newRoleRow = simpleUpdateRow(roles_col, postData, request.method)

                    companiesList = session['companies']
                    companiesList.append(newRow['id'])
                    session['companies'] = companiesList

            except:
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                print(updateData)
                simpleUpdateRow(companies, updateData, request.method)
                try:
                    billing = updateData['billing']
                    #updateData.pop('billing')
                except:
                    billing = None
                if billing:
                    print('Billing')
                    filterBy = {
                        'company_id':ObjectId(billing['company_id'])
                    }
                    company_billing_col = mongoDB['company_billing']
                    updateRow = company_billing_col.find_one(filterBy)
                    if updateRow:
                        print('Update')
                        simpleUpdateRow(company_billing_col, billing, 'PUT')
                    else:
                        print('Insert')
                        simpleUpdateRow(company_billing_col, billing, 'POST')
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            try:
                returnPost = simpleUpdateRow(companies, request.json, request.method)
                #client.close()
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/company-logo', methods=['POST'])
def companyLogoAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                isthisFile=request.files.get('file')
            except:
                return jsonify({'Message':'Failure'})
            if isthisFile:
                newName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                fileExtention = str(isthisFile.filename).split('.')[1]
                newFileName = newName + '.' + fileExtention
                
                updateData = {
                    'id':request.form['id'],
                    'logo':newFileName
                }
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                simpleUpdateRow(companies_col, updateData, 'PUT')
                isthisFile.save(os.path.join(config.brand_path, newFileName))
                #client.close()
                return jsonify({'Message':'Success'})
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/lead/campaign-summary')
def leadCampaignSummaryAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        filterBy = {}
            
        try:
            if session['user']['company_id']:
                filterBy['company_id'] = ObjectId(session['user']['company_id'])
            else:
                return jsonify({'Message':'Failure'})
        except:
            return jsonify({'Message':'Failure'})
        
        campaigns_col = mongoDB['campaigns']
        campaign_list = []
        
        for campaign in campaigns_col.find(filterBy):
            campaign_list.append(campaign['_id'])
        
        if request.args.get('campaignid'):
            if ObjectId(request.args.get('campaignid')) in campaign_list:
                filterBy = {
                    "campaign_id": ObjectId(request.args.get('campaignid'))
                }
        else:
            filterBy = {
                "campaign_id": {
                    "$in":campaign_list
                }
            }
        summary_col = mongoDB['leads_campaign_summary_daily']
        summary_col_old = mongoDB['leads_campaign_summary_new']
        leads_col = mongoDB['leads']

        #total_leads = leads_col.count_documents(filterBy)
        #total_unactioned = leads_col.count_documents(filterBy)
        returnPost = {
            "calls_made": 0, 
            "call_time": 0, 
            "time_taken": 0, 
            "total_connected": 0, 
            "total_interested": 0, 
            "total_leads": 0, 
            "total_unactioned": 0,
            "campaign_count":len(campaign_list)
        }
        
        if request.args.get('from') and request.args.get('to'):
            filterBy['entry_date'] = {
                '$gte':request.args.get('from'),
                '$lte':request.args.get('to')
            }
        for row in summary_col.find(filterBy):
            returnPost["calls_made"] += row["calls_made"]
            returnPost["call_time"] += row["call_time"]
            returnPost["time_taken"] += row["time_taken"]
            returnPost["total_connected"] += row["total_connected"]
            returnPost["total_interested"] += row["total_interested"]
        for row in summary_col_old.find(filterBy):
            returnPost["total_leads"] += row["total_leads"]
            returnPost["total_unactioned"] += row["total_unactioned"]

        #client.close()
        return jsonify(returnPost)

@apiBlueprint.route('/api/v1/companies/first-time')
def companyFirstTimeAPI():
    try:
        returnPost = {}
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        filterBy = {}
        if session['user']['company_id']:
            filterBy['company_id'] = ObjectId(session['user']['company_id'])
        campaigns = []
        for campaign in campaigns_col.find(filterBy):
            campaignData = convertToJSON(campaign)

            campaignData['leads'] = []

            leads_total_summary_col = mongoDB['leads_total_summary']
            summaryFilterBy = {
                'campaign_id':campaign['_id']
            }
            lead_summary = leads_total_summary_col.find_one(summaryFilterBy)
            try:
                campaignData['total_leads'] = getInt(lead_summary['total_leads'])
                campaignData['remaining_leads'] = getInt(lead_summary['remaining_leads'])
            except:
                campaignData['total_leads'] = 0
                campaignData['remaining_leads'] = 0
            campaigns.append(campaignData)
        returnPost['campaign_length'] = len(campaigns)

        forms = mongoDB['forms']
        filterBy = {}

        try:
            if session['user']['company_id']:
                filterBy['company_id'] = ObjectId(session['user']['company_id'])
        except:
            pass

        if forms.find_one(filterBy):
            returnPost['form_length'] = 1
        else:
            returnPost['form_length'] = 0
        
        leads_col = mongoDB['leads']
        filterBy = {}
        campaignList = []
        try:
            for campaign in campaigns:
                campaignList.append(ObjectId(campaign['id']))
        except:
            return 0
        
        if len(campaignList) > 0:
            filterBy['campaign_id'] = {'$in':campaignList}
            if leads_col.find_one(filterBy):
                returnPost['lead_length'] = 1
            else:
                returnPost['lead_length'] = 0
        else:
            returnPost['lead_length'] = 0
        return jsonify(returnPost)
    except:
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/companies/summary')
def companySummaryAPI():
    try:
        if validateLogin():
            #try:
            filterBy = {}

            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    filterBy['company_id'] = ObjectId(request.args.get('companyid'))
            
            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = ObjectId(session['user']['company_id'])
                else:
                    company_list = []
                    for company in company_list:
                        company_list.append(ObjectId(company))
                    filterBy['company_id'] = {
                        '$in':company_list
                    }
            except:
                pass
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass

            returnPost = {}
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            company_list = []
            
            campaigns_col = mongoDB['campaigns']
            campaign_list = []
            
            for campaign in campaigns_col.find(filterBy):
                campaign_list.append(campaign['_id'])

            companies_col = mongoDB['companies']
            for company in session['companies']:
                company_list.append(ObjectId(company))
            pipeline = []
            company_active_dict = {}
            company_expire_dict = {}

            camp_count_dict = {}
            try:
                if session['user']['company_id']:
                    company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$eq": [ "$_id", session['user']['company_id'] ] } ] } , 1, 0 ]}
                    company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$eq": [ "$_id", session['user']['company_id'] ] } ] } , 1, 0 ]}

                    camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$eq": [ "$company_id", session['user']['company_id'] ] } ] } , 1, 0 ]}
                else:
                    company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}
                    company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}

                    camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$in": [ "$company_id", company_list ] } ] } , 1, 0 ]}
            except:
                company_active_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "active" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}
                company_expire_dict = {"$cond": [ { "$and": [ { "$eq": [ "$status", "license_ex" ] }, { "$in": [ "$_id", company_list ] } ] } , 1, 0 ]}

                camp_count_dict = {"$cond": [ { "$and": [ { "$ne": [ "$status", "completed" ] }, { "$in": [ "$company_id", company_list ] } ] } , 1, 0 ]}
            
            pipeline = [    
                { 
                    "$group": { 
                        "_id": None,
                        "ActiveCounts":{
                            "$sum": company_active_dict
                        },
                        "ExpireCounts":{
                            "$sum": company_expire_dict
                        }
                    }  
                },
                {
                    "$project": {
                        "ActiveCounts": "$ActiveCounts",
                        "ExpireCounts": "$ExpireCounts"
                    }
                }
            ]
            company_aggr = companies_col.aggregate(pipeline)
            for i in company_aggr:
                returnPost['ActiveCompanyCounts'] = getInt(i['ActiveCounts'])
                returnPost['ExpiredCompanyCounts'] = getInt(i['ExpireCounts'])

            pipeline = [    
                { 
                    "$group": { 
                        "_id": "$_id",
                        "CampCounts":{
                            "$sum": camp_count_dict
                        }
                    }  
                },
                {
                    "$project": {
                        "CampCounts": "$CampCounts"
                    }
                }
            ]
            company_aggr = campaigns_col.aggregate(pipeline)
            for i in company_aggr:
                returnPost['CampaignCount'] = getInt(i['CampCounts'])
            returnPost['CompanyCounts'] = len(company_list)

            

            leadFilterBy = {
                "campaign_id": {
                    "$in":campaign_list
                }
            }
            leads_campaign_summary = mongoDB['leads_campaign_summary']
            LeadCount = 0
            CallsMade = 0
            TotalCallLengthSeconds = 0
            TotalInterested = 0
            for lead in leads_campaign_summary.find(leadFilterBy):
                LeadCount += lead['total_leads']
                CallsMade += lead['calls_made']
                TotalCallLengthSeconds += lead['time_taken']
                TotalInterested += lead['interested']
            returnPost['LeadCount'] = LeadCount
            returnPost['CallsMade'] = CallsMade
            returnPost['TotalCallLengthSeconds'] = TotalCallLengthSeconds
            returnPost['TotalInterested'] = TotalInterested

            returnPost['CampaignCount'] = len(campaign_list)
            returnPost['SubscriptionPlans'] = 2

            #client.close()
            return jsonify(returnPost)
    except:
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/email', methods=['GET', 'POST', 'PUT', 'DELETE'])
def emailAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        email_settings = mongoDB['email_settings']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = []

                for email in email_settings.find(filterBy):
                    userData = convertToJSON(email)
                    returnPost.append(userData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        else:
            try:
                returnPost = simpleUpdateRow(email_settings, request.json, request.method)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
    
@apiBlueprint.route('/api/v1/forms', methods=['GET', 'POST', 'PUT', 'DELETE'])
def formsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        forms = mongoDB['forms']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
            
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass

                if request.args.get('formid'):
                    filterBy['_id'] = ObjectId(request.args.get('formid'))
                returnPost = []
                for form in forms.find(filterBy):
                    defaultFields = [
                        {
                            'field_name':'First Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Last Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Company Name',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Website',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Notes',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Email',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Phone No',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Mobile No',
                            'field_enabled':False
                        },
                        {
                            'field_name':'Telephone No',
                            'field_enabled':False
                        }
                    ]
                    fields = []
                    for field in form['fields']:
                        blankField = {
                            'field_name':field['field_name'],
                            'field_enabled':False
                        }
                        if blankField in defaultFields:
                            index = defaultFields.index(blankField)
                            defaultFields[index]['field_enabled'] = True

                        fields.append(convertToJSON(field))

                    #user_col = mongoDB['users']
                    #user = user_col.find_one({'_id':form['created_by']})
                    ##user = Users.query.filter_by(id=form.created_by).first()
                    form = convertToJSON(form)
                    #form['user_first_name'] = user['first_name']
                    #form['user_last_name'] = user['last_name']
                    #form['fields'] = fields
                    form['default_fields'] = defaultFields
                    returnPost.append(form)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            postData = request.json
            if request.method == 'POST':
                postData['company_id'] = session['user']['company_id']
                postData['fields'] = []
            returnPost = simpleUpdateRow(forms, postData, request.method)
            #client.close()
            return jsonify(returnPost)

@apiBlueprint.route('/api/v1/global-settings', methods=['GET', 'PUT'])
def globalSettingsAPI():
    if validateLogin():
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            global_settings_col = mongoDB['global_settings']
            if request.method == 'GET':
                try:
                    if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                        global_settings = global_settings_col.find_one()
                        returnPost = {}
                        if global_settings:
                            returnPost = convertToJSON(global_settings)
                            returnPost['logo'] = '/static/img/brand/'+global_settings['logo']
                        #client.close()
                        return jsonify(returnPost)
                    return jsonify({'Message':'Failure'})
                except:
                    #client.close()
                    return jsonify({'Message':'Failure'})
            else:
                try:
                    data = request.json
                    returnPost = simpleUpdateRow(global_settings_col, data, request.method)
                    #client.close()
                    return jsonify(returnPost)
                except:
                    #client.close()
                    return jsonify({'Message':'Failure'})
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads', methods=['GET', 'POST', 'PUT', 'DELETE'])
def leadsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        if request.method == 'GET':
            try:
                filterBy = {}
                twilio_account_sid = ''
                twilio_auth_token = ''
                if request.args.get('leadid'):
                    filterBy['_id'] = ObjectId(request.args.get('leadid'))
                    campaign_col = mongoDB['campaigns']
                    campaign = campaign_col.find_one({'_id':ObjectId(request.args.get('campaignid'))})

                    company_col = mongoDB['companies']
                    company = company_col.find_one({'_id':campaign['company_id']})
                    twilio_account_sid = company['twilio_account_sid']
                    twilio_auth_token = company['twilio_auth_token']

                campaignList = []
                if request.args.get('campaignid') and request.args.get('campaignid') != '':
                    try:
                        filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))
                    except:
                        pass
                else:
                    try:
                        campaigns = mongoDB['campaigns']
                        for campaign in campaigns.find({'company_id':ObjectId(session['user']['company_id'])}):
                            campaignList.append(campaign['_id'])
                    except:
                        return jsonify({'Message':'Failure'})
                
                
                if request.args.get('from') and request.args.get('to'):
                    filterBy['call_logs.created_at'] = {
                        '$gte' : request.args.get('from'),
                        '$lte' : request.args.get('to'),
                    }

                if request.args.get('status'):
                    filterBy['status'] = request.args.get('status')

                if request.args.get('dnc') == '1':
                    filterBy['dnc'] = True

                if request.args.get('interested') == '1':
                    filterBy['interested'] = 'interested'
                elif request.args.get('interested') == '0':
                    filterBy['interested'] = None
                
                limit = 1000
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                
                skip = 0
                if request.args.get('skip'):
                    try:
                        skip = int(request.args.get('skip'))
                    except:
                        pass
                leads = None
                max_length = 0
                if len(campaignList) > 0:
                    leads_col = mongoDB['leads']
                    filterBy['campaign_id'] = {'$in':campaignList}
                    print(filterBy)
                    leads = leads_col.find(filterBy).skip(skip).limit(limit).sort("updated_at", pymongo.DESCENDING)
                    max_length = leads_col.count_documents(filterBy)
                else:
                    leads_col = mongoDB['leads']
                    print(filterBy)
                    leads = leads_col.find(filterBy).skip(skip).limit(limit).sort("updated_at", pymongo.DESCENDING)
                    max_length = leads_col.count_documents(filterBy)
                returnPost = []
                
                campaignList = {}
                for lead in leads:
                    leadData = convertToJSON(lead)
                    leadData['max_documents'] = max_length
                    leadData['Email'] = None
                    leadData['First_Name'] = None
                    leadData['Last_Name'] = None
                    leadData['Phone_No'] = None
                    leadData['agent_first_name'] = None
                    leadData['agent_last_name'] = None
                    x = 0
                    if request.args.get('leadid'):
                        for call_log in leadData['call_logs']:
                            try:
                                try:
                                    url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Calls/{}/Events.json'.format(twilio_account_sid, call_log['call_id'])
                                    req_call = requests.get(url, auth=ReqHTTPBasicAuth(twilio_account_sid, twilio_auth_token))
                                    req_call_json = req_call.json()
                                    transcriptions = []
                                    transcribe = False
                                    for event in req_call_json['events']:
                                        try:
                                            transcriptions.append('<b>Customer:</b> '+ event['request']['parameters']['speech_result'])
                                            transcribe = True
                                        except:
                                            try:
                                                if event['request']['method'] == 'GET':
                                                    transcriptions.append('<b>AI:</b> '+ str(event['request']['url'])[str(event['request']['url']).rfind('/')+1:-3])
                                                    transcribe = True
                                                #start = str(event['response']['response_body']).index('<Play>')+6
                                                #end = str(event['response']['response_body']).index('</Play>')
                                                #transcriptions.append('<b>AI:</b> '+ str(event['response']['response_body'])[start:end])
                                                #transcribe = True
                                            except:
                                                pass
                                    if transcribe:
                                        leadData['call_logs'][x]['transcription'] = transcriptions
                                except:
                                    pass
                                x += 1
                            except:
                                pass

                    returnPost.append(leadData)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
                zipNames = ['zip', 'zip code', 'postal', 'postal code']
                leads = request.json
                unique_leads = []
                unique_phones = []
                for lead in leads:
                    for lead_data in lead['lead_data']:
                        if str(lead_data['field_name']) in phoneNames:
                            if str(lead_data['field_value']) not in unique_phones:
                                unique_phones.append(str(lead_data['field_value']))
                                unique_leads.append(lead)
                leads = unique_leads
                campaign_id = ObjectId(leads[0]['campaign_id'])
                existingList = []
                goodList = []
                index = 0
                for row in leads_col.find({'campaign_id':campaign_id}):
                    for lead_data in row['lead_data']:
                        try:
                            if str(lead_data['field_name']) in phoneNames:
                                existingList.append(str(lead_data['field_value']))
                        except:
                            pass

                created_at = str(datetime.datetime.utcnow())[:-7]
                postal_codes_col = mongoDB['postal_codes']
                area_codes_col = mongoDB['area_codes']
                for data in leads:
                    data['campaign_id'] = campaign_id
                    refNum = data['reference_number']
                    leads[index]['created_at'] = created_at
                    leads[index]['updated_at'] = created_at
                    leads[index]['call_logs'] = []
                    leads[index]['call_recordings'] = []
                    post_found = False
                    for lead_data in data['lead_data']:
                        if str(lead_data['field_name']) in phoneNames:
                            refNum = ''.join(filter(str.isdigit, lead_data['field_value']))
                            if str(refNum) not in existingList:
                                if len(refNum) == 10:
                                    refNum = '+1'+refNum
                                leads[index]['reference_number'] = str(refNum)
                                goodList.append(data)
                        elif str(lead_data['field_name']) in zipNames:
                            try:
                                search_query = {
                                    "zip":str(lead_data['field_value'])[0:5]
                                }
                                postal = postal_codes_col.find_one(search_query)
                                leads[index]['offset'] = getDecimal(postal['offset'])
                                post_found = True
                            except:
                                pass
                    if post_found == False:
                        for lead_data in data['lead_data']:
                            if str(lead_data['field_name']) in phoneNames:
                                refNum = ''.join(filter(str.isdigit, lead_data['field_value']))
                                area_code = ''
                                if len(refNum) == 10:
                                    area_code = refNum[:3]
                                try:
                                    search_query = {
                                        "area":area_code
                                    }
                                    postal = area_codes_col.find_one(search_query)
                                    leads[index]['offset'] = getDecimal(postal['offset'])
                                    post_found = True
                                except:
                                    pass
                                
                    index+=1
                try: 
                    leads_col.insert_many(goodList)
                    #client.close()
                except:
                    pass
                return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                lead_id = simpleUpdateRow(leads_col, deleteData, 'DELETE')
                print(lead_id)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/leads/generator/<token>', methods=['POST'])
def leadGenerator(token):
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        campaigns_col = mongoDB['campaigns']
        campaign = campaigns_col.find_one({'_id':ObjectId(token)})
        form_col = mongoDB['forms']
        form = form_col.find_one({'_id':campaign['form_id']})
        created_at = str(datetime.datetime.utcnow())[:-7]
        new_lead = {
            "reference_number":None,
            "status":"unactioned",
            "interested":None,
            "appointment_booked":"0",
            "campaign_id":ObjectId(token),
            "email_template_id":None,
            "first_actioned_by":None,
            "last_actioned_by":None,
            "time_taken":None,
            "lead_data":[],
            "call_logs":[],
            "created_at":created_at,
            "updated_at":created_at
        }
        phoneNames = ['Phone','phone','Phone Number','phone number','Phone No.','phone no.','Phone No','phone no','cell phone number','Cell Phone Number','contact number','Contact Number','Contact No.','Mobile','mobile','Mobile No',' mobile no','Mobile Number','mobile number','Customer Number','customer number','Customer number','customer Number', 'Telephone No', 'Telephone', 'telephone no', 'telephone', 'Telephone Number' , 'telephone number']
        refNum = ''
        postData = None
        if form['webhook_type'] == 'JSON':
            postData = request.json
        else:
            postData = {}
            for key in request.form:
                postData[key] = request.form.get(key)

        for field in form['fields']:
            if field['field_name'] in phoneNames:
                refNum = ''.join(filter(str.isdigit, postData[field['webhook_field']]))
                if len(refNum) == 10:
                    refNum = '+1'+refNum
                new_lead['reference_number'] = refNum
            print(postData)
            try:
                new_lead['lead_data'].append({
                    'field_name':field['field_name'],
                    'field_value':postData[field['webhook_field']]
                })
            except:
                pass
        if new_lead['reference_number'] != None:
            lead_col = mongoDB['leads']
            search_query = {
                'reference_number':new_lead['reference_number'],
                'campaign_id':ObjectId(token)
            }
            if not lead_col.find_one(search_query):
                lead_id = simpleUpdateRow(lead_col, new_lead, 'POST')
                new_lead = lead_col.find_one({'_id':ObjectId(lead_id['id'])})
                returnPost = {
                    'message':'success',
                    'data':convertToJSON(new_lead)
                }
                #client.close()
                return jsonify(returnPost)
            else:
                #client.close()
                return jsonify({'Message':'Lead Already Exists'})
        #client.close()
        return jsonify({'Message':'Phone number is required'})
    except:
        #client.close()
        return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads/summary', methods=['GET', 'POST', 'PUT', 'DELETE'])
def leadSummaryAPI():
    if validateLogin():
        if request.method == 'GET':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            try:
                summary = {}
                summary['dispositions'] = []
                leads = None

                total_dict = {}
                time_taken_dict = {}
                interested_dict = {}

                if request.args.get('campaignid'):
                    total_dict = {"$cond": [ {  "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } , 1, 0 ]}
                    time_taken_dict = {"$cond": [ {  "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } , "$time_taken", 0 ]}
                    interested_dict = {"$cond": [ { "$and": [ { "$eq": [ "$interested", "interested" ] }, { "$in": [ "$campaign_id", [ObjectId(request.args.get('campaignid'))] ] } ] } , 1, 0 ]}
                    

                else:
                    campaign_list = []
                    filterBy = {
                        "company_id":ObjectId(session['user']['company_id'])
                    }
                    campaigns_col = mongoDB['campaigns']
                    for campaign in campaigns_col.find(filterBy):
                        campaign_list.append(ObjectId(campaign['_id']))         
                    total_dict = {"$cond": [ {  "$in": [ "$campaign_id", campaign_list ] } , 1, 0 ]}
                    time_taken_dict = {"$cond": [ {  "$in": [ "$campaign_id", campaign_list ] } , "$time_taken", 0 ]}
                    interested_dict = {"$cond": [ { "$and": [ { "$eq": [ "$interested", "interested" ] }, { "$in": [ "$campaign_id", campaign_list ] } ] } , 1, 0 ]}
                    

                pipeline = [    
                    { 
                        "$group": { 
                            "_id": '$status',
                            "total":{
                                "$sum": total_dict
                            },
                            "time_taken":{
                                "$sum": time_taken_dict
                            },
                            "interested":{
                                "$sum": interested_dict
                            }
                        }  
                    },
                    {
                        "$project": {
                            "total": "$total",
                            "time_taken": "$time_taken",
                            "interested": "$interested"
                        }
                    }
                ]
                
                leads_col = mongoDB['leads']
                lead_aggr = leads_col.aggregate(pipeline)
                for lead in lead_aggr:
                    summary['dispositions'].append({
                        'name':lead['_id'],
                        'total':lead['total'],
                        'duration':lead['time_taken']
                    })
                
                summary['dispositions'] = sorted(summary['dispositions'], key = lambda i: (i['name'], i['name']))
                #client.close()
                return jsonify(summary)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads/counts')
def leadCountsAPI():
    if validateLogin():
        try:
            filterBy = {'status':'started'}
            companyID = ''
            if request.args.get('companyid'):
                if validateCompany(request.args.get('companyid')):
                    companyID = request.args.get('companyid')
                    
            try:
                if session['user']['company_id']:
                    filterBy['company_id'] = session['user']['company_id']
                    companyID = session['user']['company_id']
            except:
                pass

            if request.args.get('campaignid'):
                filterBy['campaign_id'] = request.args.get('campaignid')
            
            limit = 10
            if request.args.get('limit'):
                try:
                    limit = int(request.args.get('limit'))
                except:
                    pass
            leads = []
            
            filterBy = {
                "company_id":ObjectId(session['user']['company_id'])
            }
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            campaigns_col = mongoDB['campaigns']
            campaign_list = []
            for campaign in campaigns_col.find(filterBy):
                campaign_list.append(ObjectId(campaign['_id']))  
            
            if request.args.get('from') and request.args.get('to'):
                fromDate = request.args.get('from') + ' 00:00:00'
                toDate = request.args.get('to') + ' 23:59:59'

            else:
                fromDate = '2021-01-01'
                toDate = '2026-01-01'

            pipeline = [
                {
                    "$match":{
                        "updated_at":{
                            "$gte":fromDate,
                            "$lte":toDate
                        }
                    }
                },
                { 
                    "$group": { 
                        "_id": {
                            "month": { 
                                "$month": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                }
                            },
                            "day": { 
                                "$dayOfMonth": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                }
                            },
                            "year": { 
                                "$year": {
                                    "$dateFromString":{
                                        "dateString":"$updated_at",
                                        "format": "%Y-%m-%d %H:%M:%S"
                                    }
                                } 
                            }
                        },
                        "total_leads":{
                            "$sum":{
                                "$cond":[
                                    {
                                        "$and":[
                                        {
                                            "$ne":["$status","unactioned"]
                                        },
                                        {
                                            "$in":["$campaign_id",campaign_list]
                                        }
                                        ]
                                    },
                                    1,0]
                            }
                        }
                    }  
                },
                {
                    "$project": {
                        "total_leads": "$total_leads"
                    }
                },{"$sort":{"_id":1}}
            ]
            print(campaign_list)

            returnPost = []
            leads_col = mongoDB['leads']
            leads_agg_result = leads_col.aggregate(pipeline)
            for d in leads_agg_result:
                returnPost.append({
                    'date':'{}/{}/{}'.format(d['_id']['month'], d['_id']['day'], d['_id']['year']),
                    'full_date':'{}-{}-{}'.format(d['_id']['year'], d['_id']['month'], d['_id']['day']),
                    'count':d['total_leads'],
                    'company_id':companyID
                })
            if len(returnPost) == 1:
                returnPost.append(returnPost[0])
            
            #client.close()
            return jsonify(returnPost)
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads/export')
def leadExportAPI():
    if validateLogin():
        try:
            filterBy = {}
            if request.args.get('campaignid'):
                filterBy['campaign_id'] = ObjectId(request.args.get('campaignid'))
            
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads = mongoDB['leads']

            returnPost = []
            for lead in leads.find(filterBy):
                if lead['lead_data']:
                    newPost = []
                    for x in lead['lead_data']:
                        newPost.append(x['field_value'])
                    returnPost.append(newPost)

            #client.close()
            return jsonify(returnPost)
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads/recycle', methods=['POST'])
def leadRecycleAPI():
    if validateLogin(): 
        try:   
            post_json = request.json

            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']

            search_query = {}
            search_query['campaign_id'] = ObjectId(post_json['campaign_id'])
            search_query['status'] = {
                '$in':post_json['dispos']
            }
            
            update_query = {
                '$set':{
                    'status':'unactioned'
                }
            }
            leads_col.update_many(search_query, update_query)
            return jsonify({'Message':'Success'})
        except:
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/leads/time_summary')
def leadTimeSummaryAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_time_summary_col = mongoDB['leads_time_summary']
        companies_col = mongoDB['companies']
        try:
            campaign_ids = []

            company_filter_by = {}
            if request.args.get('companyid'):
                campaigns_col = mongoDB['campaigns']
                filterBy = {
                    'company_id':ObjectId(request.args.get('companyid'))
                }
                company_filter_by = {
                    '_id':ObjectId(request.args.get('companyid'))
                }
                for campaign in campaigns_col.find(filterBy):
                    campaign_ids.append(campaign['_id'])

            company = companies_col.find_one(company_filter_by)
            company_charge_rate = company['billing']['charge_amount']

            from_date = "2022-01-01"
            to_date = "2122-01-01"
            if request.args.get('from'):
                from_date = request.args.get('from')
            if request.args.get('to'):
                to_date = request.args.get('to')
            filterBy = {
                "entry_date":{
                    "$gte":from_date,
                    "$lt":to_date
                }
            }
            filterBy['campaign_id'] = {
                "$in" : campaign_ids
            }
            return_post = {
                'total_time_taken':0,
                'total_time_rounded_taken':0,
                'total_by_date':{},
                'company_id':request.args.get('companyid'),
                'breakdown':[]
            }
            for lead in leads_time_summary_col.find(filterBy):
                return_post['total_time_taken'] += lead['time_taken']
                return_post['total_time_rounded_taken'] += lead['time_taken_rounded']

                if not return_post['total_by_date'].get(lead['entry_date']):
                    return_post['total_by_date'][lead['entry_date']] = {
                        'time_taken_rounded':lead['time_taken_rounded'],
                        'time_taken':lead['time_taken']
                    }
                else:
                    return_post['total_by_date'][lead['entry_date']]['time_taken'] += lead['time_taken']

                return_post['breakdown'].append({
                    'entry_date':lead['entry_date'],
                    'campaign_id':str(lead['campaign_id']),
                    'time_taken':lead['time_taken'],
                    'time_taken_rounded':lead['time_taken_rounded'],
                })
            return_post['total_charge'] = getDecimal(getDecimal(company_charge_rate)*getDecimal(return_post['total_time_rounded_taken']))
            return jsonify(return_post)
        except:
            return jsonify({"Message":"Failure"})

@apiBlueprint.route('/api/v1/roles', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rolesAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        roles = mongoDB['roles']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('roleid'):
                    filterBy['_id'] = ObjectId(request.args.get('roleid'))
                
                filterBy['company_id'] = None
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                if filterBy['company_id'] == None:
                    filterBy.pop('company_id')
                    company_list = []
                    for company in session['companies']:
                        company_list.append(ObjectId(company))
                    filterBy['company_id'] = {
                        "$in" : company_list
                    }
                returnPost = []
                companies = {}
                for role in roles.find(filterBy):
                    companyName = None
                    if role['company_id'] not in companies:
                        company_col = mongoDB['companies']
                        company = company_col.find_one({'_id':role['company_id']})
                        if company:
                                companyName = company['name']
                                companies[role['company_id']] = {"name":company['name']}
                    else:
                        companyName = companies[role['company_id']]['name']
                    roleData = convertToJSON(role)
                    roleData['company_name'] = companyName
                    returnPost.append(roleData)
                returnPost = sorted(returnPost, key = lambda i: i['company_name'])
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                postData['permissions'] = []
                role_id = simpleUpdateRow(roles, postData, 'POST')
                new_lead = roles.find_one({'_id':ObjectId(role_id['id'])})
                returnPost = {
                    'message':'success',
                    'data':convertToJSON(new_lead)
                }
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            return jsonify(returnPost)
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    permissions = updateData['permissions']
                    updateData.pop('permissions')
                except:
                    permissions = None
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                simpleUpdateRow(roles, updateData, 'PUT')
                roleID = ObjectId(updateData['id'])
                if permissions:
                    for permission in permissions:
                        search_query = {
                            "_id":roleID,
                            "permissions._id":ObjectId(permission['id'])
                        }
                        role = roles.find_one(search_query)
                        if role == None:
                            if permission['enabled'] == True:
                                permission.pop('enabled')
                                permission['_id'] = ObjectId(permission['id'])
                                permission['description'] = None
                                permission.pop('id')
                                permission.pop('role_id')
                                search_query = {
                                    "_id":roleID
                                }
                                update_query = {
                                    "$push":{
                                        "permissions":permission
                                    }
                                }
                                print(update_query)
                                roles.update_one(search_query, update_query)
                        else:
                            if permission['enabled'] == False:
                                print("Remove")

                #client.close()
                return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                role_id = simpleUpdateRow(roles, deleteData, 'DELETE')
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/subscription-plans', methods=['GET', 'POST', 'PUT', 'DELETE'])
def subscriptionPlansAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        plans = mongoDB['subscription_plans']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('subid'):
                    filterBy['id'] = request.args.get('subid')
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for plan in plans.find(filterBy):
                    returnPost.append(convertToJSON(plan))
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                data = request.json
                returnPost = simpleUpdateRow(plans, data, request.method)
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/sales-members', methods=['GET', 'POST', 'PUT', 'DELETE'])
def salesMembersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        salesMembers = mongoDB['sales_members']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('userid'):
                    filterBy['id'] = request.args.get('userid')

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = request.args.get('companyid')
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = session['user']['company_id']
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []

                for user in salesMembers.find(filterBy):
                    userData = convertToJSON(user)
                    returnPost.append(userData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        else:
            try:
                data = request.json
                returnPost = simpleUpdateRow(salesMembers, data, request.method)
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio', methods=['GET', 'POST', 'PUT', 'DELETE'])
def twilioAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        twilioSettings = mongoDB['twilio_numbers']
        if request.method == 'GET':
            try:
                filterBy = {}

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass

                returnPost = []
                userData = {}
                for twilio in twilioSettings.find(filterBy):
                    userData = convertToJSON(twilio)
                filterBy['_id'] = ObjectId(filterBy['company_id'])
                filterBy.pop('company_id')

                companyTwilioSettings_col = mongoDB['companies']
                companyTwilioSettings = companyTwilioSettings_col.find_one(filterBy)
                userData['twilio_enabled'] = companyTwilioSettings['twilio_enabled'],
                userData['twilio_account_sid'] = companyTwilioSettings['twilio_account_sid'],
                userData['twilio_auth_token'] = companyTwilioSettings['twilio_auth_token'],
                userData['twilio_application_sid'] = companyTwilioSettings['twilio_application_sid']
                returnPost.append(userData)
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

        elif request.method == 'POST':
            try:
                postData = request.json
                if postData['id'] == '':
                    simpleUpdateRow(twilioSettings, postData, 'POST')
                else:
                    simpleUpdateRow(twilioSettings, postData, 'PUT')
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

        elif request.method == 'PUT':
            try:
                updateData = request.json
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                #updateRow = TwilioNumbers.query.filter_by(id=updateData['id']).update(dict(**updateData))
                #db.session.commit()
            except:
                return jsonify({'Message':'Failure'})
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/twilio/test_call', methods=['GET','POST'])
def twilioTestCallAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                twil_client = Client(str(session['call_testing']['twilio_account_sid']), str(session['call_testing']['twilio_auth_token']))
                call = twil_client.calls(str(session['call_testing']['call_id'])).fetch()
                return jsonify({'Status':str(call.status)})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']

                # GRAB COMPANY FOR TWILIO TOKENS
                companies_col = mongoDB['companies']
                filter_by = {
                    "_id":ObjectId(session['company']['id'])
                }
                company = companies_col.find_one(filter_by)

                # GRAB CAMPAIGN FOR VIRTUAL AGENT
                post_data = request.json
                campaigns_col = mongoDB['campaigns']
                filter_by = {
                    "_id":ObjectId(post_data['campaign_id'])
                }
                campaign = campaigns_col.find_one(filter_by)

                # GRAB CALLER ID
                company_caller_ids_col = mongoDB['company_caller_ids']
                filter_by = {
                    "_id":ObjectId(campaign['caller_id'])
                }
                caller_id = company_caller_ids_col.find_one(filter_by)

                # GRAB VIRTUAL AGENT FOR APP ID
                virtual_agent_col = mongoDB['virtual_agents']
                filter_by = {
                    "_id":ObjectId(campaign['virtual_agent_id'])
                }
                virtual_agent = virtual_agent_col.find_one(filter_by)

                twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])

                call = twil_client.calls.create(
                                        timeout=28,
                                        application_sid=virtual_agent['app_id'],
                                        to=post_data['reference_number'],
                                        from_=virtual_agent['phone'],
                                        caller_id=caller_id['caller_id']
                                )
                session['call_testing'] = {
                    'twilio_account_sid':company['twilio_account_sid'],
                    'twilio_auth_token':company['twilio_auth_token'],
                    'status':'calling',
                    'call_id':str(call.sid)
                }
                return jsonify({
                    'Message':'Success',
                    'data':{
                        'twilio_account_sid':company['twilio_account_sid'],
                        'twilio_auth_token':company['twilio_auth_token'],
                        'status':'calling',
                        'call_id':str(call.sid)
                    }
                })
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/available_numbers', methods=['GET', 'POST', 'PUT', 'DELETE'])
def twilioAvailableNumbersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies_col = mongoDB['companies']
        filter_by = {
            "_id":ObjectId(session['company']['id'])
        }
        company = companies_col.find_one(filter_by)
        twilio_available_numbers_col = mongoDB['twilio_available_numbers']
        if request.method == 'GET':
            try:
                if request.args.get('phoneid'):
                    filter_by = {
                        "company_id":ObjectId(session['company']['id']),
                        "_id":ObjectId(request.args.get('phoneid'))
                    }
                    number = twilio_available_numbers_col.find_one(filter_by)
                    return jsonify(convertToJSON(number))
                else:
                    return_data = {
                        "purchasable_numbers":[],
                        "available_numbers":[]
                    }
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    available_numbers = None
                    if request.args.get('areacode'):
                        if str(request.args.get('areacode'))[:1] == '8':
                            available_numbers = twil_client.available_phone_numbers('US').toll_free.list(area_code=request.args.get('areacode'),limit=20)
                        else:
                            available_numbers = twil_client.available_phone_numbers('US').local.list(area_code=request.args.get('areacode'),limit=20)

                    else:
                        available_numbers = twil_client.available_phone_numbers('US').local.list(limit=20)
                    
                    for number in available_numbers:
                        return_data['purchasable_numbers'].append({
                            "phone_number":number.phone_number
                        })

                    filter_by = {
                        "company_id":ObjectId(session['company']['id'])
                    }
                    for number in twilio_available_numbers_col.find(filter_by):
                        return_data['available_numbers'].append(convertToJSON(number))

                    return jsonify(return_data)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                post_data = request.json
                twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                incoming_phone_number = twil_client.incoming_phone_numbers.create(phone_number=post_data['phone_number'])
                
                # INSERT CALLER ID DATA
                insert_data = {
                    "company_id":ObjectId(session['company']['id']),
                    "caller_id":str(post_data['phone_number'])[2:],
                    "verified":True
                }
                caller_id_col = mongoDB['company_caller_ids']
                caller_id_data = simpleUpdateRow(caller_id_col, insert_data, 'POST')

                # INSERT TWILIO NUMBER
                insert_data = {
                    "company_id":ObjectId(session['company']['id']),
                    "phone_number":post_data['phone_number'],
                    "phone_sid":str(incoming_phone_number.sid),
                    "caller_id":ObjectId(caller_id_data['id'])
                }
                simpleUpdateRow(twilio_available_numbers_col, insert_data, 'POST')
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            try:
                post_data = request.json
                try:
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    virtual_agent_col = mongoDB['virtual_agents']
                    virtual_agent = virtual_agent_col.find_one({"_id":ObjectId(post_data['virtual_agent_id'])})
                    incoming_phone_number = twil_client.incoming_phone_numbers(post_data['phone_sid']).update(voice_application_sid=virtual_agent['app_id'])
                except:
                    pass
                simpleUpdateRow(twilio_available_numbers_col, post_data, 'PUT')
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'DELETE':
            try:
                delete_data = request.json
                try:
                    twil_client = Client(company['twilio_account_sid'], company['twilio_auth_token'])
                    incoming_phone_number = twil_client.incoming_phone_numbers(delete_data['phone_sid']).delete()
                except:
                    return jsonify({"Message":"Failure"})
                
                twilio_available_numbers_col = mongoDB['twilio_available_numbers']
                twilio_number = twilio_available_numbers_col.find_one({"_id":ObjectId(delete_data['id'])})
                caller_id_col = mongoDB['company_caller_ids']
                caller_id_col.delete_one({"_id":twilio_number['caller_id']})
                simpleUpdateRow(twilio_available_numbers_col, delete_data, 'DELETE')
                return jsonify({"Message":"Success"})
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/usage', methods=['GET'])
def twilioUsageAPI():
    if validateLogin():
        if request.method == 'GET':
            #try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            companies_col = mongoDB['companies']
            filter_by = { 
                'twilio_account_sid' : { 
                    '$ne':None  
                } 
            }

            if request.args.get('companyid'):
                filter_by['_id'] = ObjectId(request.args.get('companyid'))

            return_post = {
                'company_summary_breakdown':{},
                'cost_breakdown':{
                    'Progammable_Voice':0,
                    'Phone_Numbers':0,
                    'Answering_Machine_Detection':0
                },
                'company_breakdown':{}
            }
            twilio_accounts = []
            
            earnings_col = mongoDB['company_wallet_earnings']
            for company in companies_col.find(filter_by):
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                if twilio_account_sid not in twilio_accounts:
                    twilio_accounts.append(twilio_account_sid)
                    twil_client = Client(twilio_account_sid, twilio_auth_token)

                    company_details = {
                        "Progammable_Voice":{
                            "Speech_Recognition":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Twilio_Client_Minutes":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Recordings":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Amazon_Polly_Characters":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Conference_Minutes":{
                                "count": 0.0, 
                                "count_unit": "", 
                                "end_date": "", 
                                "price": 0.0, 
                                "price_unit": "usd", 
                                "start_date": ""
                            },
                            "Voice_Minutes":{
                                "Inbound_Voice_Minutes":{
                                    "Inbound_Local_Calls":{
                                        "count": 0.0, 
                                        "count_unit": "", 
                                        "end_date": "", 
                                        "price": 0.0, 
                                        "price_unit": "usd", 
                                        "start_date": ""
                                    }
                                },
                                "Outbound_Voice_Minutes":{
                                    "count": 0.0, 
                                    "count_unit": "", 
                                    "end_date": "", 
                                    "price": 0.0, 
                                    "price_unit": "usd", 
                                    "start_date": ""
                                }
                            }
                        },
                        "Phone_Numbers":{
                            "Phone_Numbers":{
                                "Local_PhoneNumbers":{
                                    "count": 0.0, 
                                    "count_unit": "", 
                                    "end_date": "", 
                                    "price": 0.0, 
                                    "price_unit": "usd", 
                                    "start_date": ""
                                }
                            }
                        },
                        "Answering_Machine_Detection":{
                            "count": 0.0, 
                            "count_unit": "", 
                            "end_date": "", 
                            "price": 0.0, 
                            "price_unit": "usd", 
                            "start_date": ""
                        },
                        "Earnings":{
                            "paid_amount":0,
                            "charge_amount":0
                        }
                    }
                    # A list of record objects with the properties described above  
                    records = []

                    earning_search_query = {}
                    from_date = '2022-01-01'
                    to_date = '2022-01-31'
                    if request.args.get('type') == 'this_month':
                        records = twil_client.usage.records.this_month.list()
                        from_date = '2022-01-01'
                        to_date = '2022-01-31'
                                
                    elif request.args.get('type') == 'all_time':
                        records = twil_client.usage.records.all_time.list()
                        from_date = '2019-01-01'
                        to_date = '2122-01-31'
                                
                    elif request.args.get('type') == 'daily':
                        records = twil_client.usage.records.daily.list()
                        from_date = '2022-01-06'
                        to_date = '2022-01-06'
                                
                    elif request.args.get('type') == 'last_month':
                        records = twil_client.usage.records.last_month.list()
                        from_date = '2021-12-01'
                        to_date = '2021-12-31'
                                
                    elif request.args.get('type') == 'monthly':
                        records = twil_client.usage.records.monthly.list()
                                
                    elif request.args.get('type') == 'today':
                        records = twil_client.usage.records.today.list()
                        from_date = '2022-01-06'
                        to_date = '2022-01-06'
                                
                    elif request.args.get('type') == 'yearly':
                        records = twil_client.usage.records.yearly.list()
                                
                    elif request.args.get('type') == 'yesterday':
                        records = twil_client.usage.records.yesterday.list()

                    earning_search_query = {
                        "$and":[
                            {
                                'entry_date' : {
                                    '$gte' : from_date
                                }
                            },
                            {
                                'entry_date' : {
                                    '$lte' : to_date
                                }
                            },
                            {
                                'company_id':company['_id']
                            }
                        ]
                    }
                    print(earning_search_query)

                    earnings = earnings_col.find(earning_search_query)
                    total_paid = 0
                    total_charge = 0
                    for earning in earnings:
                        total_paid += getDecimal(earning['paid_amount'])
                        total_charge += getDecimal(earning['charge_amount'])
                    company_details['Earnings']['paid_amount'] = total_paid
                    company_details['Earnings']['charge_amount'] = total_charge

                    total = 0
                    for record in records:
                        if getDecimal(record.price) > 0 and record.category != 'totalprice':
                            if record.category == 'speech-recognition':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Speech_Recognition'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-client':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Twilio_Client_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-recordings' or record.category == 'recordings':
                                #total += getDecimal(record.price)
                                company_details['Progammable_Voice']['Recordings'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-text-to-speech':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Amazon_Polly_Characters'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-globalconference':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Conference_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-inbound':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Voice_Minutes']['Inbound_Voice_Minutes']['Inbound_Local_Calls'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'calls-outbound':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Progammable_Voice'] += getDecimal(record.price)
                                company_details['Progammable_Voice']['Voice_Minutes']['Outbound Voice_Minutes'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'phonenumbers-local':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Phone_Numbers'] += getDecimal(record.price)
                                company_details['Phone_Numbers']['Phone_Numbers']['Local_PhoneNumbers'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                            elif record.category == 'answering-machine-detection':
                                total += getDecimal(record.price)
                                return_post['cost_breakdown']['Answering_Machine_Detection'] += getDecimal(record.price)
                                company_details['Answering_Machine_Detection'] = {
                                    'start_date':record.start_date, 
                                    'end_date':record.end_date, 
                                    'count':getDecimal(record.count),
                                    'count_unit':record.count_unit, 
                                    'price':getDecimal(record.price), 
                                    'price_unit':record.price_unit
                                }
                    return_post['company_summary_breakdown'][str(company['_id'])] = {}
                    return_post['company_summary_breakdown'][str(company['_id'])]['billing'] = company_details
                    return_post['company_summary_breakdown'][str(company['_id'])]['details'] = {
                        'company_name':str(company['name']),
                        'company_id':str(company['_id']),
                        'total_cost':total
                    }

                    return_post['company_breakdown'][str(company['_id'])] = {
                        'company_name':str(company['name']),
                        'company_id':str(company['_id']),
                        'total_cost':total
                    }

                    #return_post['total_summary'][str(company['_id'])] = {
                    #    'company_name':str(company['name']),
                    #    'total':total
                    #}
            #return_post['company_breakdown']['summary'] = summary
            #client.close()
            return jsonify(return_post)
            #except:
            #    return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/usage/details', methods=['GET'])
def twilioUsageDetailsAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                companies_col = mongoDB['companies']
                filter_by = {}
                if request.args.get('companyid'):
                    filter_by['_id'] = ObjectId(request.args.get('companyid'))
                else:
                    return jsonify({'Message':'Failure'})

                company = companies_col.find_one(filter_by)
                twilio_account_sid = company['twilio_account_sid']
                twilio_auth_token = company['twilio_auth_token']
                #client.close()
                twil_client = Client(twilio_account_sid, twilio_auth_token)

                return_post = []
                # A list of record objects with the properties described above
                records = []
                            
                if request.args.get('type') == 'this_month':
                    records = twil_client.usage.records.this_month.list()
                            
                elif request.args.get('type') == 'all_time':
                    records = twil_client.usage.records.all_time.list()
                            
                elif request.args.get('type') == 'daily':
                    records = twil_client.usage.records.daily.list()
                            
                elif request.args.get('type') == 'last_month':
                    records = twil_client.usage.records.last_month.list()
                            
                elif request.args.get('type') == 'monthly':
                    records = twil_client.usage.records.monthly.list()
                            
                elif request.args.get('type') == 'this_month':
                    records = twil_client.usage.records.this_month.list()
                            
                elif request.args.get('type') == 'today':
                    records = twil_client.usage.records.today.list()
                            
                elif request.args.get('type') == 'yearly':
                    records = twil_client.usage.records.yearly.list()
                            
                elif request.args.get('type') == 'yesterday':
                    records = twil_client.usage.records.yesterday.list()

                for record in records:
                    if getDecimal(record.price) > 0:
                        return_post.append({
                            'start_date':record.start_date, 
                            'end_date':record.end_date, 
                            'category':record.category, 
                            'count':getDecimal(record.count),
                            'count_unit':record.count_unit, 
                            'price':getDecimal(record.price), 
                            'price_unit':record.price_unit
                        })
                return jsonify(return_post)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/twilio/sandbox/make_call', methods=['GET', 'POST', 'PUT'])
def twilioSandboxMakeCallAPI():
    if request.method == 'GET':
        search_query = {}
        if request.args.get('call_id'):
            search_query['call_sid'] = request.args.get('call_id')
        else:
            return jsonify({"Message":"Failure"})

        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        conversation = sandbox_conversations_col.find_one(search_query)
        return jsonify(convertToJSON(conversation))

    elif request.method == 'POST':
        post_data = request.json
        account_sid = 'ACfd0cb9bd7808a4ca590e7f163756b193'
        auth_token = '9e6c4679120eece07dde538b789a0e91'
        client = Client(account_sid, auth_token)
        application_sid = 'AP8d1aacbdf952e716245856fbff05377e'
        if post_data['campaign'] == 'obamacare':
            application_sid = 'APb142896caf09f76966a28da49b23467c'

        call = client.calls.create(
                timeout=28,
                application_sid=application_sid,
                to=post_data['phone_number'],
                from_='+17723616669',
                caller_id='+17723616669',
                record=True,
                recording_status_callback='{}recording/callback'.format(config.webhooks),
                recording_status_callback_method='POST'
        )
        insert_data = {
            'call_sid':str(call.sid),
            'conversation':[]
        }
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        sandbox_conversations_col.insert_one(insert_data)
        #session['sandbox_call_sid'] = str(call.sid)
        print(str(call.sid))
        return jsonify({"Message":"Success", "call_sid":str(call.sid)})

    elif request.method == 'PUT':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        sandbox_conversations_col = mongoDB['sandbox_conversations']
        post_data = request.json
        search_query = {
            'call_sid':post_data['CallSid']
        }
        update_query = {
            '$push':{
                'conversation':{
                    "owner":"client",
                    "message":post_data['user_message']
                }
            }
        }
        sandbox_conversations_col.update_one(search_query, update_query)
        for message in post_data['message']:
            update_query = {
                '$push':{
                    'conversation':{
                        "owner":"ai",
                        "message":message['text']
                    }
                }
            }
            sandbox_conversations_col.update_one(search_query, update_query)
        return jsonify({"Message":"Success"})

@apiBlueprint.route('/api/v1/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def usersAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        users = mongoDB['users']
        if request.method == 'GET':
            try:
                company_list = []
                filterBy = {}
                roleFilterBy = {}
                roleUserFilter = {}
                if request.args.get('userid'):
                    filterBy['_id'] = ObjectId(request.args.get('userid'))
                    roleUserFilter['user_id'] = ObjectId(request.args.get('userid'))

                if request.args.get('superadmin'):
                    if request.args.get('superadmin') == '1':
                        filterBy['super_admin'] = True
                    elif request.args.get('superadmin') == '0':
                        filterBy['super_admin'] = False

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        roleFilterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        return jsonify({'Message':'Failure'})
                
                try:
                    if session['user']['company_id']:
                        roleFilterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                    
                try:
                    if session['user']['user_id'] != '613b8a785a2cd24ac1a33bc0':
                        if session['user']['company_id']:
                            roleFilterBy['company_id'] = ObjectId(session['user']['company_id'])
                        else:
                            for company in session['companies']:
                                company_list.append(ObjectId(company))
                            roleFilterBy['company_id'] = {
                                "$in" : company_list
                            }
                except:
                    pass
                
                limit = 100
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass

                returnPost = {}
                returnPost['users'] = []
                roles = mongoDB['roles']
                user_ids = []
                for role in roles.find(roleFilterBy):
                    role_users = mongoDB['role_user_new']
                    roleUserFilter['role_id'] = role['_id']
                    for user in role_users.find(roleUserFilter):
                        if session['user']['user_id'] == '613b8a785a2cd24ac1a33bc0':
                            user_ids.append(user['user_id'])
                        else:
                            if str(user['user_id']) != '613b8a785a2cd24ac1a33bc0':
                                user_ids.append(user['user_id'])

                filterBy["_id"] = {"$in":user_ids}
                for user in users.find(filterBy):
                    roles = []
                    userData = convertToJSON(user)
                    userData['roles'] = []
                    roleUsers = mongoDB['role_user_new']
                    for roleUser in roleUsers.find({'user_id' : ObjectId(user['_id'])}):
                        filterBy = {
                            '_id':roleUser['role_id']
                        }
                        roles_col = mongoDB['roles']
                        role = roles_col.find_one(filterBy)
                        if role:
                            role_dict = convertToJSON(role)
                            role_dict.pop('permissions')
                            userData['roles'].append(role_dict)
                    returnPost['users'].append(userData)
                    
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'POST':
            try:
                postData = request.json
                try:
                    userRoles = postData['roles']
                    postData.pop('roles')
                except:
                    userRoles = None

                try:
                    if not postData['company_id']:
                        print('Added')
                        postData['company_id'] = session['user']['company_id']
                except:
                    try:
                        postData['company_id'] = session['user']['company_id']
                    except:
                        pass
                postData['image'] = None
                postData['status'] = 'disabled'
                password = bytes(postData['password'], 'utf-8')
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password, salt)
                postData['password'] = str(hashed)[2:]
                postData['password'] = str(postData['password'])[:-1]
                newRow = simpleUpdateRow(users, postData, 'POST')
                userID = newRow['id']
                if userRoles:
                    for role in userRoles:
                        role['user_id'] = userID
                        role_user_col = mongoDB['role_user_new']
                        simpleUpdateRow(role_user_col, role, 'POST')
                #client.close()
                return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            try:
                updateData = request.json
                try:
                    userRoles = updateData['roles']
                    updateData.pop('roles')
                    clearRoles = updateData['clear_roles']
                    updateData.pop('clear_roles')
                except:
                    userRoles = None
                    clearRoles = False
                try:
                    password = bytes(updateData['password'], 'utf-8')
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(password, salt)
                    updateData['password'] = str(hashed)[2:]
                    updateData['password'] = str(updateData['password'])[:-1]
                except:
                    try:
                        updateData.pop('password')
                    except:
                        pass
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                simpleUpdateRow(users, updateData, 'PUT')
                userID = updateData['id']
                if userRoles:
                    role_user_col = mongoDB['role_user_new']
                    if clearRoles:
                        role_user_col.delete_many({'user_id':ObjectId(userID)})
                        for role in userRoles:
                            role['user_id'] = userID
                            filterBy = {
                                'user_id':ObjectId(role['user_id']),
                                'role_id':ObjectId(role['role_id'])
                            }
                            if not role_user_col.find_one(filterBy):
                                simpleUpdateRow(role_user_col, filterBy, 'POST')
                    else:
                        for role in userRoles:
                            role['user_id'] = userID
                            filterBy = {
                                'user_id':ObjectId(role['user_id']),
                                'role_id':ObjectId(role['role_id'])
                            }
                            
                            if role_user_col.find_one(filterBy) and role['enabled'] == False:
                                simpleUpdateRow(role_user_col, filterBy, 'DELETE')
                            elif not role_user_col.find_one(filterBy) and role['enabled']:
                                simpleUpdateRow(role_user_col, filterBy, 'POST')
            except:
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})
        elif request.method == 'DELETE':
            try:
                deleteData = request.json
                simpleUpdateRow(users, deleteData, 'DELETE')
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/users/signup', methods=['POST'])
def userSignupAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                updateData = request.json
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                users_col = mongoDB['users']

                user = users_col.find_one({'_id':ObjectId(updateData['user_id'])})
                if user['status'] != 'enabled':
                    signup_tokens_col = mongoDB['signup_tokens']
                    return_row = simpleUpdateRow(signup_tokens_col, updateData, 'POST')

                    ## EMAIL THE TOKEN #####
                    s = smtplib.SMTP(host='smtp.office365.com', port=587)
                    s.starttls()
                    s.login("info@puretalk.ai", config.SMTP_PASSWORD)

                    msg = MIMEMultipart()
                    msg['Subject'] = 'Invite Request'
                    msg['From'] = "info@puretalk.ai"
                    msg['To'] = user['email']
                    #msg['To'] = 'shawnhasten@gmail.com'
                    text_message = "Puretalk Invite Link\nhttps://dashboard.puretalk.ai/user-sign-up?token={}".format(return_row['id'])
                    html_message = """
                    <html>
                    <body>
                    <a href='https://dashboard.puretalk.ai/user-sign-up/{}'>
                    <body>
                    </html>
                    """.format(return_row['id'])

                    # Record the MIME types of both parts - text/plain and text/html.
                    part1 = MIMEText(text_message, 'plain')
                    part2 = MIMEText(html_message, 'html')

                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    msg.attach(part1)
                    msg.attach(part2)
                    s.send_message(msg)
                    s.quit()
                #except:
                #    pass
            except:
                return jsonify({'Message':'Failure'})
    return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/users-tour', methods=['POST'])
def usersTourAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        users = mongoDB['users']
        try:
            search_query = {
                "_id":ObjectId(session['user']['user_id'])
            }
            update_query = {
                "$set":{
                    "tour_complete":True
                }
            }
            users.update_one(search_query, update_query)
            #client.close()
            return jsonify({'Message':'Success'})
        except:
            #client.close()
            return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/user-img', methods=['POST'])
def userImageAPI():
    if validateLogin():
        if request.method == 'POST':
            try:
                try:
                    isthisFile=request.files.get('file')
                except:
                    return jsonify({'Message':'Failure'})
                if isthisFile:
                    newName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
                    fileExtention = str(isthisFile.filename).split('.')[1]
                    newFileName = newName + '.' + fileExtention

                    #client = app.mongo_client
                    mongoDB = app.mongo_client['jamesbon']
                    user_col = mongoDB['users']
                    
                    search_query = {
                        "_id":ObjectId(request.form['id'])
                    }
                    update_query = {
                        "$set": {
                            'image':newFileName
                        }
                    }
                    isthisFile.save(os.path.join(config.profile_path, newFileName))
                    user_col.update_one(search_query, update_query)
                    #client.close()
                    session['user']['image'] = newFileName
                    return jsonify({'Message':'Success'})
            except:
                return jsonify({'Message':'Failure'})
        return jsonify({'Message':'Failure'})
      
@apiBlueprint.route('/api/v1/roles-details', methods=['GET', 'POST', 'PUT', 'DELETE'])
def roleDetailsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('roleid'):
                    filterBy['_id'] = ObjectId(request.args.get('roleid'))
                
                try:
                    if session['user']['company_id']:
                        filterBy['company_id'] = ObjectId(session['user']['company_id'])
                except:
                    pass
                
                roles = mongoDB['roles']
                permissions = mongoDB['permissions']
                permissionList = []
                for permission in permissions.find():
                    permissionList.append({
                        'id':str(permission['_id']),
                        'name':permission['name'],
                        'display_name':permission['display_name'],
                        'allowed':False
                    })

                returnPost = []
                for role in roles.find(filterBy):
                    roleDict = convertToJSON(role)
                    allowed_permissions = roleDict['permissions']
                    roleDict['permissions'] = permissionList
                    for permission in allowed_permissions:
                        permissionDict = {
                            'id':str(permission['_id']),
                            'name':permission['name'],
                            'display_name':permission['display_name'],
                            'allowed':False
                        }
                        try:
                            indexOf = roleDict['permissions'].index(permissionDict)
                            permissionDict['allowed'] = True
                            roleDict['permissions'][indexOf] = permissionDict
                        except:
                            pass
                    returnPost.append(roleDict)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
    
@apiBlueprint.route('/api/v1/wallet/twilio', methods=['GET'])
def twilioBillingAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        companies = mongoDB['companies']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    filterBy['_id'] = ObjectId(request.args.get('companyid'))
                company = companies.find_one(filterBy)
                twilio_sub_sid = company['twilio_account_sid']
                #twilio_auth_token = company['twilio_auth_token']
                #client.close()
                #twilio_sub_sid = 'ACaec0a651b05932d0d648203e24366cfa'
                twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_SID, twilio_sub_sid)
                calls = twilio_client.calls.list(start_time_after=datetime.datetime(2021, 12, 6, 0, 0, 0), limit=4000)

                return_post = []
                for call in calls:
                    return_post.append({
                        'created_at':call.date_created,
                        'direction':call.direction,
                        'duration':call.duration,
                        'from':call.from_formatted,
                        'price':call.price,
                        'status':call.status,
                        'to_formatted':call.to_formatted,
                    })
                return jsonify(return_post)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
                    
@apiBlueprint.route('/api/v1/wallet', methods=['GET', 'POST', 'PUT'])
def walletAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        transactions = mongoDB['wallet_transactions']
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('userid'):
                    filterBy['last_actioned_by'] = ObjectId(request.args.get('userid'))

                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        return jsonify({'Message':'Failure'})
                else:
                    try:
                        if session['user']['company_id']:
                            filterBy['company_id'] = ObjectId(session['user']['company_id'])
                    except:
                        return jsonify({'Message':'Failure'})
                    
                if request.args.get('from') and request.args.get('to'):
                    filterBy['updated_at'] = {
                        "$gte":request.args.get('from') + ' 00:00:00.000',
                        "$lte":request.args.get('to')+' 23:59:59.999'
                    }

                if request.args.get('type'):
                    filterBy['type'] = request.args.get('type')
                    
                limit = 1000
                if request.args.get('limit'):
                    try:
                        limit = int(request.args.get('limit'))
                    except:
                        pass
                returnPost = []
                print(filterBy)
                for transaction in transactions.find(filterBy).sort([("created_at",pymongo.DESCENDING)]):
                    tranData = convertToJSON(transaction)
                    returnPost.append(tranData)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        else:
            try:
                updateData = request.json
                #updateData['amount'] = getDecimal(updateData['amount'])
                try:
                    if session['user']['user_id']:
                        updateData['last_actioned_by'] = session['user']['user_id']
                except:
                    pass
                updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                returnPost = simpleUpdateRow(transactions, updateData, request.method)
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/balance', methods=['GET'])
def walletBalanceAPI():
    if validateLogin():
        if request.method == 'GET':
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = request.args.get('companyid')
                    else:
                        return jsonify({'Message':'Failure'})
                else:
                    try:
                        if session['user']['company_id']:
                            filterBy['company_id'] = session['user']['company_id']
                    except:
                        pass
                
                company_wallet_balance_col = mongoDB['company_wallet_balance']
                company_wallet_balance = company_wallet_balance_col.find_one({'company_id':ObjectId(filterBy['company_id'])})
                returnBalance = {
                    "company_id":filterBy['company_id'],
                    "paid_balance":getDecimal(0),
                    "voided_balance":getDecimal(0),
                    "refunded_balance":getDecimal(0),
                    "charged_balance":getDecimal(0),
                    "balance":getDecimal(0)
                }
                if company_wallet_balance:
                    returnBalance = {
                        "company_id":str(company_wallet_balance['_id']),
                        "paid_balance":getDecimal(company_wallet_balance['paid_amount']),
                        "voided_balance":getDecimal(company_wallet_balance['voided_amount']),
                        "refunded_balance":getDecimal(company_wallet_balance['refunded_amount']),
                        "charged_balance":getDecimal(company_wallet_balance['charge_amount'])
                    }
                returnBalance['balance'] = returnBalance['paid_balance'] - returnBalance['refunded_balance'] - returnBalance['charged_balance']
                #client.close()
                return jsonify(returnBalance)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})

@apiBlueprint.route('/api/v1/wallet/earnings', methods=['GET'])
def walletEarningsAPI():
    if validateLogin():
        if request.method == 'GET':
            try:
                filterBy = {}
                if request.args.get('companyid'):
                    if validateCompany(request.args.get('companyid')):
                        filterBy['company_id'] = ObjectId(request.args.get('companyid'))
                    else:
                        company_list = []
                        for company in session['companies']:
                            company_list.append(ObjectId(company))
                        filterBy['company_id'] = {
                            "$in" : company_list
                        }
                if request.args.get('from') and request.args.get('to'):
                    filterBy['entry_date'] = {
                        "$gte":request.args.get('from'),
                        "$lte":request.args.get('to')
                    }
                #client = app.mongo_client
                mongoDB = app.mongo_client['jamesbon']
                company_wallet_earnings = mongoDB['company_wallet_earnings']
                returnBalance = {}
                for earning in company_wallet_earnings.find(filterBy).sort([("entry_date",pymongo.ASCENDING)]):
                    if not returnBalance.get(earning['entry_date']):
                        returnBalance[earning['entry_date']] = {
                            "company_id":str(earning['company_id']),
                            "entry_date":earning['entry_date'],
                            "paid_balance":getDecimal(earning['paid_amount']),
                            "voided_balance":getDecimal(earning['voided_amount']),
                            "refunded_balance":getDecimal(earning['refunded_amount']),
                            "charge_amount":getDecimal(earning['charge_amount'])
                        }
                    else:
                        returnBalance[earning['entry_date']]['paid_balance']+=getDecimal(earning['paid_amount'])
                        returnBalance[earning['entry_date']]['voided_balance']+=getDecimal(earning['voided_amount'])
                        returnBalance[earning['entry_date']]['refunded_balance']+=getDecimal(earning['refunded_amount'])
                        returnBalance[earning['entry_date']]['charge_amount']+=getDecimal(earning['charge_amount'])
                returnPost = []
                for key in returnBalance:
                    returnPost.append(returnBalance[key])
                #client.close()
                return jsonify(returnPost)
            except:
                return jsonify({'Message':'Failure'})
                
@apiBlueprint.route('/api/v1/payment-settings', methods=['GET', 'PUT'])
def paySettingsAPI():
    if validateLogin():
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        payment_gateway_settings = mongoDB['payment_gateway_settings']
        if request.method == 'GET':
            try:
                gateway = payment_gateway_settings.find_one()
                returnPost = {}

                if gateway:
                    returnPost = convertToJSON(gateway)
                
                #client.close()
                return jsonify(returnPost)
            except:
                #client.close()
                return jsonify({'Message':'Failure'})
        elif request.method == 'PUT':
            updateData = request.json
            updateQuery = {
                "$set":{}
            }
            for key in updateData:
                updateQuery["$set"][key] = updateData[key]
            payment_gateway_settings.update_one({}, updateQuery)
            #client.close()
            return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/calls/inbound', methods=['POST'])
def callInboundNewAPI():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/api/v1/calls/gathering', method='POST')
    response.append(gather)
    print(str(response))

    return Response(str(response), mimetype="text/xml")

@apiBlueprint.route('/api/v1/calls/gathering', methods=['POST'])
def callInboundGather():
    print(str(request.form))
    return jsonify({'Message':'Success'})

@apiBlueprint.route('/api/v1/calls/inbound/<sid>', methods=['GET', 'POST'])
def callInboundAPI(sid):
    try:
        logger.debug('Got Inbound Call: {}'.format(str(request.form)))
        print('INBOUND CALL')
        filterBy = {
            'phone':request.form['To']
        }
        logger.debug('\t Grabbing Virtual Agent Info: {}'.format(str(filterBy)))
        agent = VirtualAgents.query.filter_by(**filterBy).first()
        print(agent)
        logger.debug('\t Connecting to studio: {}'.format(agent.studio_name))
        response = VoiceResponse()
        connect = Connect(action='{}calls/events'.format(config.hostname))
        connect.virtual_agent(
            connector_name=agent.studio_name, language='en-US', status_callback='{}calls/events'.format(config.hostname)
        )
        response.append(connect)
        logger.debug('\t Studio Connected: {}'.format(agent.studio_name))
        return str(response)
    except:
        logger.debug('NO INBOUND DATA')

    return jsonify({"Message":"Failure"})

@apiBlueprint.route('/recording/callback', methods=['POST'])
def upload_recording():
    try:
        logger.debug('Got Call Back: {}'.format(str(request.form)))
        recording_url = request.form['RecordingUrl']
        logger.debug('\t Recording URL: {}'.format(str(recording_url)))

        call_id = request.form['CallSid']
        logger.debug('\t Call SID Recording: {}'.format(str(call_id)))

        recording_sid = request.form['RecordingSid']
        logger.debug('\t Recording SID: {}'.format(str(recording_sid)))

        updateData = {
            'recording_id':recording_sid,
            'recording_link':recording_url
        }
        logger.debug('\t Update Data: {}'.format(str(updateData)))
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            leads_col = mongoDB['leads']
            search_query = {
                "call_logs.call_id":call_id
            }
            update_query = {
                "$set": {
                    "call_logs.$.recording_id": recording_sid,
                    "call_logs.$.recording_link": recording_url
                }
            }
            lead = leads_col.find_one(search_query)
            leads_col.update_one(search_query, update_query)
            logger.debug('\t Committed Data')
            #client.close()
            try:
                recording_status = request.form['RecordingStatus']
                if lead['status'] == 'voicemail':
                    recording_status = 'voicemail'
                call_event = {
                    'CallStatus':recording_status,
                    'ParentCallSid':request.form['CallSid'],
                    'CallSid':request.form['CallSid'],
                    'CallDuration':request.form['RecordingDuration'],
                }
                url = '{}calls/events'.format(config.webhooks)
                requests.post(url, data=call_event)
            except:
                pass
        except:
            pass
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/events', methods=['POST'])
def updateStatus():
    try:
        logger.debug('Call Events Data: {}'.format(str(request.form)))
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        campaigns_col = mongoDB['campaigns']
        company_billing_col = mongoDB['company_billing']
        wallet_transactions_col = mongoDB['wallet_transactions']
        try:

            try:
                call_status = request.form['CallStatus']
                logger.debug('\t Call Status: {}'.format(str(call_status)))
            except:
                return jsonify({"Message":"Success"}) 

            call_id_child = request.form['CallSid']
            logger.debug('\t CHILD Call SID: {}'.format(str(call_id_child)))

            try:
                call_id = request.form['ParentCallSid']
                logger.debug('\t Call SID: {}'.format(str(call_id)))
            except:
                call_id = request.form['CallSid']
                logger.debug('\t CHILD Call SID: {}'.format(str(call_id)))
            
            search_query = {
                "call_logs.call_id":call_id
            }
            logger.debug('\t Search Query: {}'.format(str(search_query)))
            update_query = {
                "$set": {
                    'call_logs.$.call_id_child':call_id_child
                }
            }
            logger.debug('\t Update Data: {}'.format(str(update_query)))
            logger.debug('\t Stage Data')
            leads_col.update_one(search_query, update_query)
            logger.debug('\t Committed Data')

            leadRow = leads_col.find_one(search_query)
            logger.debug('\t Grabbed Lead Row')

            logger.debug('\t Lead ID: {}'.format(str(leadRow['_id'])))
            update_query = {
                "$set": {}
            }
            try:
                print(call_status)
            except:
                logger.error('\t\t Failed Getting call_status')
            try:
                print(str(datetime.datetime.utcnow())[:-7])
            except:
                logger.error('\t\t Failed Getting DATETIME')
            try:
                if leadRow['call_logs'][len(leadRow['call_logs'])-1]['status'] != 'voicemail':
                    update_query = {
                        "$set": {
                            'call_logs.$.status':call_status,
                            'call_logs.$.updated_at':str(datetime.datetime.utcnow())[:-7],
                            'updated_at':str(datetime.datetime.utcnow())[:-7],
                            'status':call_status
                        }
                    }
                else:
                    update_query = {
                        "$set": {
                            'call_logs.$.updated_at':str(datetime.datetime.utcnow())[:-7],
                            'updated_at':str(datetime.datetime.utcnow())[:-7],
                            'status':call_status
                        }
                    }
            except:
                logger.error('\t\t Failed Writing update query')
            try:
                update_query["$set"]["call_logs.$.time_taken"] = getInt(request.form['CallDuration'])
                update_query["$set"]["time_taken"] = getInt(request.form['CallDuration'])
            except:
                pass
            if call_status == 'completed' or call_status == 'voicemail':
                logger.debug('\t\t Call Finished Need to charge them')
                #try:
                #    time_taken = getInt(leadRow['time_taken'])
                #except:
                #    time_taken = 0
                #update_query["$set"]["time_taken"] = getInt(time_taken)+getInt(request.form['CallDuration'])
                campaign_id = leadRow['campaign_id']
                logger.debug('\t\t Need to charge {}'.format(str(campaign_id)))
                campaignRow = campaigns_col.find_one({'_id':campaign_id})
                company_id = campaignRow['company_id']
                logger.debug('\t\t With company id {}'.format(str(company_id)))
                billing = company_billing_col.find_one({'company_id':company_id})
                if billing:
                    if call_status != 'voicemail':
                        logger.debug('\t\t Biller Found')
                        charge_amount = getDecimal(billing['charge_amount'])
                        logger.debug('\t\t Charge Amount: {}'.format(str(charge_amount)))

                        charge_type = getInt(billing['charge_type'])
                        logger.debug('\t\t Charge Type: {}'.format(str(charge_type)))
                        walletData = {}
                        call_duration = getInt(request.form['CallDuration'])
                        if charge_type == 0:
                            logger.debug('\t\t Call Duration: {}'.format(str(call_duration)))
                            if call_duration != 0:
                                minutes = getDecimal(math.ceil(call_duration/60))
                                logger.debug('\t\t Call Duration Rounded: {}'.format(str(minutes)))
                                total_charge = getDecimal(charge_amount*minutes)
                                logger.debug('\t\t Total Charge: {}'.format(str(total_charge)))
                                walletData = {
                                    'company_id':company_id,
                                    'type':'charged',
                                    'amount':getDecimal(total_charge)
                                }
                        else:
                            if call_duration > 3:
                                total_charge = getDecimal(charge_amount)
                                logger.debug('\t\t Total Charge: {}'.format(str(total_charge)))
                                walletData = {
                                    'company_id':company_id,
                                    'type':'charged',
                                    'amount':getDecimal(total_charge)
                                }

                        try:
                            walletData['memo'] = 'Campaign ID: {} calling: {}'.format(str(campaign_id), str(leadRow['reference_number']))
                        except:
                            pass
                        logger.debug('\t\t Wallet Data: {}'.format(str(walletData)))
                        simpleUpdateRow(wallet_transactions_col, walletData, 'POST')
                        logger.debug('\t\t Stage Data')
                        logger.debug('\t\t Committed Data')
                else:
                    logger.error('\t\t Cannot Find Billing')
            #elif call_status == 'answered':
            #    logger.debug('\t Set the call to answered: {}'.format(str(update_query)))
            #    search_query = {
            #        "call_logs.call_id":call_id
            #    }
            #    logger.debug('\t Search Query: {}'.format(str(search_query)))
            #    update_query = {
            #        "$set": {
            #            'call_logs.$.answered':True
            #        }
            #    }
            #    logger.debug('\t Update Data: {}'.format(str(update_query)))
            #    logger.debug('\t Stage Data')
            #    leads_col.update_one(search_query, update_query)

            logger.debug('\t Search Query: {}'.format(str(search_query)))
            logger.debug('\t Lead Update Data: {}'.format(str(update_query)))
            leads_col.update_one(search_query, update_query)
        except:
            pass
        #client.close()
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/amd', methods=['POST'])
def updateAMD():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        logger.debug('AMD Data: {}'.format(str(request.form)))
        if request.form['AnsweredBy'] != 'human':
            call_id = request.form['CallSid']
            search_query = {
                "call_logs.call_id":call_id
            }
            lead_row = leads_col.find_one(search_query)
            campaigns_col = mongoDB['campaigns']
            campaign = campaigns_col.find_one({'_id':lead_row['campaign_id']})
            companies_col = mongoDB['companies']
            company = companies_col.find_one({'_id':campaign['company_id']})
            account_sid = company['twilio_account_sid']
            auth_token = company['twilio_auth_token']
            try:
                twilClient = Client(account_sid, auth_token)
                logger.debug('\t Call To Hang Up: {}'.format(str(call_id)))

                logger.debug('\t Attempting To Hang Up Call')
                thisCall = twilClient.calls(call_id).update(twiml='<Response><Hangup/></Response>')
                logger.debug('\t Call Hung Up')
            except:
                pass

            logger.debug('\t Grabbing Lead Info')
            search_query = {
                "call_logs.call_id":str(call_id)
            }
            update_query = {
                "$set": {
                    'call_logs.$.status':'voicemail',
                    'status':'voicemail'
                }
            }
            logger.debug('\t Search Query: {}'.format(str(search_query)))
            logger.debug('\t Lead Update Data: {}'.format(str(update_query)))
            leads_col.update_one(search_query, update_query)
            #leadCall = LeadCalls.query.filter(or_(LeadCalls.call_id == call_id, LeadCalls.call_id_child == call_id)).first()
            #leadID = leadCall.lead_id
            #logger.debug('\t Lead ID: {}'.format(leadID))
            #
            #updateData = {
            #    'status':'voicemail'
            #}
            #updateData['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            #logger.debug('\t Lead Update Data: {}'.format(str(updateData)))
            #updateRow = Leads.query.filter_by(id=leadID).update(dict(**updateData))
            #logger.debug('\t Stage Data')
            #db.session.commit()
            logger.debug('\t Committed Data')
        #client.close()
    except:
        pass
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/calls/interested', methods=['POST'])
def updateInterest():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('Interest Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as interested
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            '$set':{
                'interested':'interested'
            }
        }
        leads_col.update_one(search_query,update_query)
        
        # Check for webhook to transfer lead data
        lead = leads_col.find_one(search_query)
        campaigns_col = mongoDB['campaigns']
        campaign = campaigns_col.find_one({'_id':lead['campaign_id']})

        logger.debug('\t Stop recording')
        companies_col = mongoDB['companies']
        company = companies_col.find_one({'_id':campaign['company_id']})
        try:
            try:
                twilio_account_sid = company['twilio_account_sid']
                logger.debug('\t\t Account SID: {}'.format(twilio_account_sid))
            except:
                logger.error('\t\t Failed Grabbing Account SID')
            try:
                twilio_auth_token = company['twilio_auth_token']
                logger.debug('\t\t Auth Token: {}'.format(twilio_auth_token))
            except:
                logger.error('\t\t Failed Grabbing Auth Token')
            try:
                twil_client = Client(twilio_account_sid, twilio_auth_token)
                logger.debug('\t\t Created Twil Client')
            except:
                logger.error('\t\t Failed Creating Twil Client')
            try:
                logger.debug('\t\t Find Recording Using: {}'.format(str(post_data['CallSid'])))
                recording = twil_client.calls(str(post_data['CallSid'])).recordings.list(limit=1)
                try:
                    logger.debug('\t\t Find Total Of {} Recordings'.format(str(len(recording))))
                except:
                    pass
                recording_id = str(recording[0].sid)
                logger.debug('\t\t Recording ID: {}'.format(recording_id))
            except:
                logger.error('\t\t Failed Grabbing Recording ID')
            try:
                twil_client.calls(str(post_data['CallSid'])).recordings(recording_id).update(status='stopped')
                logger.debug('\t Stop Record Successful')
            except:
                logger.error('\t\t Failed Sending Stop Request')
        except:
            logger.error('\t Failed to stop recording')
        try:
            ## DO TRANSFER WEBHOOK STUFF #########
            webhook_url = campaign['xfer_url']
            webhook_data = {}
            for data in lead['lead_data']:
                try:
                    webhook_data[data['field_name']] = data['field_value']
                except:
                    pass
            requests.post(webhook_url, json=webhook_data)
        except:
            pass
        #client.close()
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/calls/dnc', methods=['POST'])
def updateLeadDNC():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('DNC Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as Do Not Call
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            '$set':{
                'dnc':True
            }
        }
        leads_col.update_one(search_query,update_query)
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/calls/voicemail', methods=['POST'])
def updateLeadVoicemail():
    try:
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        post_data = request.json
        logger.debug('Voicemail Data: {}'.format(str(request.json)))
        leads_col = mongoDB['leads']

        # Update Lead as Do Not Call
        search_query = {
            "call_logs.call_id":post_data['CallSid']
        }
        update_query = {
            "$set": {
                'status':'voicemail',
                'call_logs.$.status':'voicemail'
            }
        }
        leads_col.update_one(search_query,update_query)
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/calls/dial_call_back', methods=['POST'])
def callDialBack():
    try:
        print(str(request.form))
        logger.debug('DIAL BACK DATA: {}'.format(str(request.form)))
    except:
        print(str(request.json))
        logger.debug('DIAL BACK DATA: {}'.format(str(request.json)))
    return jsonify({'Message':'Success'})

@apiBlueprint.route('/calls/hangup/<call_sid>', methods=['GET', 'POST'])
def callHangup(call_sid):
    try:
        logger.debug('Hangup Data')
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        leads_col = mongoDB['leads']
        search_query = {
            "call_logs.call_id":call_sid
        }
        lead = leads_col.find_one(search_query)
        campaigns_col = mongoDB['campaigns']
        campaign = campaigns_col.find_one({'_id':lead['campaign_id']})

        logger.debug('\t Stop recording')
        companies_col = mongoDB['companies']
        company = companies_col.find_one({'_id':campaign['company_id']})
        try:
            try:
                twilio_account_sid = company['twilio_account_sid']
                logger.debug('\t\t Account SID: {}'.format(twilio_account_sid))
            except:
                logger.error('\t\t Failed Grabbing Account SID')
            try:
                twilio_auth_token = company['twilio_auth_token']
                logger.debug('\t\t Auth Token: {}'.format(twilio_auth_token))
            except:
                logger.error('\t\t Failed Grabbing Auth Token')
            try:
                twil_client = Client(twilio_account_sid, twilio_auth_token)
                logger.debug('\t\t Created Twil Client')
            except:
                logger.error('\t\t Failed Creating Twil Client')
            try:
                logger.debug('\t\t Find Recording Using: {}'.format(str(call_sid)))
                recording = twil_client.calls(str(call_sid)).recordings.list(limit=1)
                try:
                    logger.debug('\t\t Find Total Of {} Recordings'.format(str(len(recording))))
                except:
                    pass
                recording_id = str(recording[0].sid)
                logger.debug('\t\t Recording ID: {}'.format(recording_id))
            except:
                logger.error('\t\t Failed Grabbing Recording ID')
            try:
                twil_client.calls(str(call_sid)).recordings(recording_id).update(status='stopped')
                logger.debug('\t Stop Record Successful')
            except:
                logger.error('\t\t Failed Sending Stop Request')
        except:
            logger.error('\t Failed to stop recording')
        #client.close()
        return jsonify({"Message":"Success"})
    except:
        return jsonify({"Message":"Failure"})

@apiBlueprint.route('/agent/hooks', methods=['GET'])
def localAgentHookGet():
    if request.method == 'GET':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        lead_hooks_col = mongoDB['lead_hooks']
        search_query = {
            "campaign_id":session['agent-campaign'],
            "checked":False
        }
        lead_hook = lead_hooks_col.find_one(search_query)
        if lead_hook:
            search_query = {
                "_id":ObjectId(lead_hook['_id'])
            }
            update_query = {
                "$set":{
                    "checked":True
                }
            }
            lead_hooks_col.update_one(search_query, update_query)
            return jsonify({"Message":"Success", "details":convertToJSON(lead_hook)})
    return jsonify({"Message":"Failure"})

@apiBlueprint.route('/agent/hooks/<token>', methods=['POST'])
def localAgentHookPost(token):
    if request.method == 'POST':
        try:
            #client = app.mongo_client
            mongoDB = app.mongo_client['jamesbon']
            post_data = request.json
            logger.debug('Local Agent Hook Data: {}'.format(str(request.json)))

            try:
                ## DO TRANSFER WEBHOOK STUFF #########
                lead_hooks_col = mongoDB['lead_hooks']
                insert_query = {
                    "checked":False,
                    "details":post_data,
                    "campaign_id":token,
                    "created_at":str(datetime.datetime.utcnow())[:-3],
                    "updated_at":str(datetime.datetime.utcnow())[:-3]
                }
                lead_hooks_col.insert_one(insert_query)
            except:
                pass
            #client.close()
            return jsonify({"Message":"Success"})
        except:
            return jsonify({"Message":"Failure"})

@apiBlueprint.route('/api/v1/calls/status/<sid>', methods=['POST'])
def callStatusAPI(sid):
    logger.debug('\t Hang Up Form Data: {}'.format(str(request.form)))
    try:
        call_id = request.form['CallSid']
        ## THE AI PASSES WHETHER THERE WAS A LIVE AGENT HAND OFF
        interested = request.form['LiveAgentHandOff']
        logger.debug('\t Call Transfered: {}'.format(str(interested)))
        if not interested:
            ## WE TAKE THE TIMESTAMP THIS HAPPENED AND COMPARE TO OUR
            ## UNFORTUNATELY THE CALLSID ON THE AI AGENT IS DIFFERENT THAN OUR CALL
            ## SO WE TAKE THE REFERENCE NUMBER AND OUR CURRENT TIME TO TRY
            ## AND FIND THE LEAD ID FROM LEAD_CALLS AND SET THE AGENT CALL SID
            time_stamp = request.form['Timestamp']
            dt = datetime.datetime.strptime(time_stamp[:16], "%Y-%m-%dT%H:%M")
            delta = datetime.timedelta(minutes=30)
            newDT = dt-delta
            account_sid = 'ACa6902364cdd0dd9f9b4ea4a86498f71a'
            auth_token = 'efa74a9aa01c33e162fc793aa5d46a30'
            client = Client(account_sid, auth_token)

            call = client.calls(call_id).fetch()
            ref_num = call.forwarded_from
            ref_num = ''.join(filter(str.isdigit, ref_num))
            if len(ref_num) == 10:
                ref_num = '+1'+ref_num
            logger.debug('\t Reference Number: {}'.format(str(ref_num)))

            leadCall = LeadCalls.query.filter_by(agent_call_id=call_id).first()
            lead_id = None
            if leadCall:
                lead_id = leadCall.lead_id
                logger.debug('\t Our lead_id to update: {}'.format(str(lead_id)))
            else:
                qry = '''
                SELECT id as id, lead_id as lead_id FROM lead_calls lc 
                WHERE updated_at BETWEEN :fromTime and :toTime and reference_number = :ref and agent_call_id is NULL
                '''
                leadCalls = db.engine.execute(text(qry), fromTime=newDT, toTime=dt, ref=ref_num)
                for leadCall in leadCalls:
                    lead_call_id = leadCall.id
                    lead_id = leadCall.lead_id
                    logger.debug('\t Our lead_id to update: {}'.format(str(lead_id)))
                    logger.debug('\t Our lead_call_id to update: {}'.format(str(lead_call_id)))
                    updateData = {
                        'agent_call_id':call_id
                    }
                    logger.debug('\t Update Data: {}'.format(str(updateData)))
                    updateRow = LeadCalls.query.filter_by(id=lead_call_id).update(dict(**updateData))
                    logger.debug('\t Staged Data: {}'.format(str(updateData)))
                    db.session.commit()
                    logger.debug('\t Committed Data: {}'.format(str(updateData)))
            updateData = {
                'interested':True
            }
            logger.debug('\t Update Data: {}'.format(str(updateData)))
            updateRow = Leads.query.filter_by(id=lead_id).update(dict(**updateData))
            logger.debug('\t Staged Data: {}'.format(str(updateData)))
            db.session.commit()
            logger.debug('\t Committed Data: {}'.format(str(updateData)))
        
    except:
        pass
    logger.debug('\t Call SID Hang Up: {}'.format(str(call_id)))
    return jsonify({"Message":"Success"})

@apiBlueprint.route('/api/v1/stripe/charge', methods=['POST'])
def make_stripe_charge():
    if request.method == 'POST':
        #client = app.mongo_client
        mongoDB = app.mongo_client['jamesbon']
        transactions = mongoDB['wallet_transactions']

        post_data = request.json
        try:
            company_id = post_data['company_id']
        except:
            try:
                company_id = session['company']['id']
            except:
                return jsonify({'Message':'Failure'})
        type = post_data['type']
        customer_name = post_data['customer_name']
        customer_email = post_data['customer_email']
        #customer_address = post_data['customer_address']
        #customer_city = post_data['customer_city']
        #customer_state = post_data['customer_state']
        #customer_zip = post_data['customer_zip']
        #customer_country = post_data['customer_country']

        card_number = post_data['card_number']
        card_exp_month = post_data['card_exp_month']
        card_exp_year = post_data['card_exp_year']
        card_cvc = post_data['card_cvc']

        amount = post_data['amount']
        customer_memo = post_data['memo']

        stripe.api_key = "sk_test_51JegctKAR6Ijtm4HWZnH2WM2eHgbTroDNlU0fn1apFsStYw2e0HeHYWXqRQMvpwLIMnnTKjwl57DbwlP6JOc4BFX00ZftJ7zJN"
        try:
            card_token = stripe.Token.create(
                card={
                    "number": card_number,
                    "exp_month": getInt(card_exp_month),
                    "exp_year": getInt(card_exp_year),
                    "cvc": card_cvc,
                }
            )
        except:
            return jsonify({'Message':'Card number was not valid!'})

        print("Attempting charge...")

        try:
            resp = stripe.Charge.create(
                amount=getInt(amount)*100,
                currency="usd",
                card=card_token,
                description=customer_email,
            )
        except:
            return jsonify({'Message':'Charge failed!'})

        if resp['status'] == 'succeeded':
            updateData = {
                'company_id':company_id,
                'type':'paid',
                'amount':getDecimal(post_data['amount']),
                'created_at':str(datetime.datetime.utcnow())[:-3],
                'updated_at':str(datetime.datetime.utcnow())[:-3],
                'memo':customer_memo
            }
            try:
                updateData['payment_method_details'] = resp['payment_method_details']
            except:
                pass
            try:
                if session['user']['user_id']:
                    updateData['last_actioned_by'] = session['user']['user_id']
            except:
                pass
            returnPost = simpleUpdateRow(transactions, updateData, 'POST')
            #client.close()
            return jsonify(returnPost)

        #client.close()
        return jsonify({'Message':'Charge failed!'})

@apiBlueprint.route('/scheduler/hopper', methods=['GET'])
def schedulerCron():
    campaignId = request.args.get('campaignid')
    limit = request.args.get('limit')
    filterBy = {
        'campaign_id':campaignId,
        'status':'unactioned'
    }
    leadData = Leads.query.filter_by(**filterBy).limit(limit).all()

    leadReturn = []
    for lead in leadData:
        leadReturn.append({
            'id':lead.id,
            'lead_data':formatStringToJSON(lead.lead_data)
        })
    return jsonify(leadReturn)

def formatDate(myDate):
    return myDate.strftime("%Y/%m/%d")
    
def formatNiceDate(myDate):
    return myDate.strftime("%m/%d/%Y")

def formatDateStd(myDate):
    return myDate.strftime("%Y-%m-%d")

def getDecimal(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return float(x)

def getInt(x):
    try:
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)
    except:
        x = 0
        #return Decimal(x.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
        return int(x)

def formatStringToJSON(x):
    x = str((x).decode("utf-8"))
    leadData = None
    try:
        leadData = json.loads(x)
        print('Properly Loaded')
        return json.loads(leadData)
    except:
        try:
            leadData = str(x).replace("'\"", "'\\\"")
            leadData = str(leadData).replace("\"'", "\\\"'")
            leadData = str(leadData).replace("'", '"')
            return json.loads(leadData)
        except:
            leadData = str(x).replace("'\"", "'\\\"")
            leadData = str(leadData).replace("\"'", "\\\"'")
            leadData = str(leadData).replace("'", '"')
    return None

@apiBlueprint.route('/api/v1/calls/outbound', methods=['POST'])
def make_outbound_call():
    req = get('{}getPhoneNumbers?campaignid=74'.format(config.hostname))
    data = req.json()
    for x in data:
        account_sid = 'ACa6902364cdd0dd9f9b4ea4a86498f71a'
        auth_token = 'efa74a9aa01c33e162fc793aa5d46a30'
        client = Client(account_sid, auth_token)

        call = client.calls.create(
                                to='+12392208726',
                                from_='+19144264849',
                                url='{}/api/bot'.format(config.webhooks)
                        )
        postData = {
            'lead_id':x['lead_id'],
            'call_id':str(call.sid)
        }
        newRow = LeadCalls(**postData)
        db.session.add(newRow)
        db.session.commit()
    return str(call.sid)

def simpleUpdateRow(collection, data, post_type):
    if post_type == 'POST':
        try:
            if isinstance(data, list):
                for x in data:
                    for key in x:
                        if '_id' in key:
                            try:
                                x[key] = ObjectId(x[key])
                            except:
                                x[key] = x[key]
                        else:
                            x[key] = x[key]
                    x['created_at'] = str(datetime.datetime.utcnow())[:-3]
                    x['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                    _id = collection.insert(x)
            else:
                for key in data:
                    if '_id' in key:
                        try:
                            data[key] = ObjectId(data[key])
                        except:
                            data[key] = data[key]
                data['created_at'] = str(datetime.datetime.utcnow())[:-3]
                data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
                _id = collection.insert(data)
            return {
                'Message':'Success',
                'id':str(_id)
            }
        except:
            return {'Message':'Failure'}
    elif post_type == 'PUT':
        try:
            try:
                if data['updated_at'] == None:
                    data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            except:
                data['updated_at'] = str(datetime.datetime.utcnow())[:-3]
            updateQuery = {
                "$set":{}
            }
            for key in data:
                if '_id' in key:
                    try:
                        updateQuery["$set"][key]  = ObjectId(data[key])
                    except:
                        updateQuery["$set"][key]  = data[key]
                elif key != 'id':
                    updateQuery["$set"][key] = data[key]
                else:
                    updateQuery["$set"][key] = data[key]
            search_query = {
                "_id":ObjectId(data['id'])
            }
            collection.update_one(search_query, updateQuery)
            return {
                'Message':'Success',
                'id':data['id']
            }
        except:
            return {'Message':'Failure'}
    elif post_type == 'DELETE':
        try:
            collection.delete_one({"_id":ObjectId(data['id'])})
            return {
                'Message':'Success',
                'id':data['id']
            }
        except:
            return {'Message':'Failure'}
    return {'Message':'Failure'}

def convertToJSON(obj):
    objData = {}
    for key in obj:
        if key != 'password':
            if isinstance(obj[key], list):
                objData[key] = []
                thisList = []
                for x in range(0, len(obj[key])):
                    thisDict = {}
                    for listKey in obj[key][x]:
                        if isinstance(obj[key][x][listKey], str):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], bytes):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], bool):
                            thisDict[listKey] = obj[key][x][listKey]
                        elif isinstance(obj[key][x][listKey], int):
                            thisDict[listKey] = getInt(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], float):
                            thisDict[listKey] = getDecimal(obj[key][x][listKey])
                        elif isinstance(obj[key][x][listKey], ObjectId):
                            thisDict[listKey] = str(obj[key][x][listKey])
                        else:
                            thisDict[listKey] = obj[key][x][listKey]
                    thisList.append(thisDict)
                
                objData[key] = thisList

            else:
                if isinstance(obj[key], str):
                    objData[key] = str(obj[key])
                elif isinstance(obj[key], bytes):
                    objData[key] = str(obj[key])
                elif isinstance(obj[key], bool):
                    objData[key] = obj[key]
                elif isinstance(obj[key], int):
                    objData[key] = getInt(obj[key])
                elif isinstance(obj[key], float):
                    objData[key] = getDecimal(obj[key])
                elif isinstance(obj[key], ObjectId):
                    objData[key] = str(obj[key])
                else:
                    objData[key] = obj[key]
    try:
        objData['id'] = objData['_id']
        objData.pop('_id')
    except:
        pass
    return objData

def tz_diff(home):
    utcnow = pytz.timezone('utc').localize(datetime.datetime.utcnow()) # generic time
    here = utcnow.astimezone(pytz.timezone(home)).replace(tzinfo=None)
    there = utcnow.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)

    offset = relativedelta(there,here)
    return(offset.hours)

## THIS FUNCTION WORKS BY REFERENCING TWO DICTIONARIES WE HAVE SAVED 
## ONE IS FOR STORING ALL AREA CODES AND WHICH TIMEZONE AND STATE THEY BELONG TO
## THE OTHER IS FOR STORING STATE LAWS ABOUT AUTO DIAL TIMES
## WE GRAB THE PHONE NUMBER AND TAKE THE AREA CODE OUT OF THAT
## THEN WE FIND WHAT STATE IT BELONGS TO
## LASTLY WE CHECK THE LAWS FOR WHAT TIME WE CAN CALL FOR THAT STATE AND WHAT DAY IT IS NOW IN THAT TIMEZONE
## WE RETURN TRUE OR FALSE OF WHETHER OR NOT WE CAN MAKE THE CALL
def phone_tz_check(phoneNumber):
    try:
        utcnow = pytz.timezone('utc').localize(datetime.datetime.utcnow()) # generic time

        areaCode = phoneNumber[2:5]
        state = None
        tz = None
        startTime = None
        endTime = None
        for area in areaCodeTZ:
            if str(area['area_code']) == areaCode:
                state = area['state']
                tz = area['time_zone']
                break
        here = utcnow.astimezone(pytz.timezone(tz)).replace(tzinfo=None)
        day = here.weekday()
        for law in stateLaws:
            if law['State'] == state:
                enabled = law['days'][day]['allowed']
                startTime = law['days'][day]['start_full']
                endTime = law['days'][day]['end_full']
                break

        if enabled == 0:
            return False

        startHour = startTime.split(':')[0]
        startMin = startTime.split(':')[1]

        endHour = endTime.split(':')[0]
        endMin = endTime.split(':')[1]
        startTime = here.replace(hour=int(startHour), minute=int(startMin))
        endTime = here.replace(hour=int(endHour), minute=int(endMin))

        if here >= startTime and here < endTime:
            return True
        return False
    except:
        return True