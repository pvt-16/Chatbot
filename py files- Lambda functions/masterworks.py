#masterworks.py file name. API for masterworks APIs
#Contains functions that will be used across all intents.

#Handler : lambda_function.lambda_handler
#File Name : masterworks.py
#Function : AuroLambda



# import requests
# from requests.auth import HTTPDigestAuth
from botocore.vendored import requests
import json
import math
import dateutil.parser
import datetime
import time
import os
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# class Masterworks: 
baseUrl = "http://9e5783d1.ngrok.io/" 
ID = "ID"
PROJECT_ID = "projectId"
PARENT_ID = "contractId"
#     __authorizationToken = ""; 
#     # def Login(self, username, password):
#     #     # masterworkshelper = Http_Helper("http://localhost:8081/"); 
#     #     data = {}
#     #     data["username"] = username 
#     #     data['password'] = password
#     #     data["c"] = "" 
#     #     data["role"] = ""
        
#     #     response = requests.post(self.baseUrl + "api/Login" , headers = headers, json = data) 
#     #     jsonResponse = json.loads(response.text)
#     #     self.authorizationToken  = jsonResponse["Token"]; 
    
    
def GetModuleId(formName):
    if(formName == 'Budget Estimates'):
        return 'BDGTEST'
    
    elif(formName == 'Daily Progress Report'):
        return 'CONTDWR'
    
    elif(formName == 'Global Fund List'):
        return 'FNDMGMT'


# change if needed. 
def GetIdentifierFieldForForm(self, formName):
    moduleId = self.GetModuleId(formName)
    
    if(moduleId == "BDGTEST"):
        return "BudgetEstimateName"
        
    elif(moduleId == "CONTDWR"):
        return "Prepared by" 
        
    elif(moduleId == "FNDMGMT"):
        return "FundName"
    
def GetTableName(self, moduleId):
    if(moduleId == "BDGTEST"):
        return "BDGTESTBudgetEstimates"
        
    elif(moduleId == "CONTDWR"):
        return "Prepared by" 
        
    elif(moduleId == "FNDMGMT"):
        return "FundName"
    
    
    
def GetFormInstanceId(moduleId, recordName, projectName = None, contractName = None):
    
    data = {}
    data['moduleId'] = moduleId
    data['projectName'] = projectName
    data['contractName'] = contractName
    data['recordName'] = recordName
    
    url = "api/Auro/GetFormInstanceId"
    
    response = requests.get(baseUrl+url,params = data)
    if(response.ok):
        jsonResponse = json.loads(response.content)
        # print "jsonResponse: "+jsonResponse
        instanceId = jsonResponse[ID]
        pid = jsonResponse[PROJECT_ID]
        parentId = jsonResponse[PARENT_ID]
        return instanceId, pid, parentId
    
    else:
        return None, None, None
        
    
        
        
        # api call
    
    
def GetPIDParentIdForModule(moduleId, projectName = None, contractName = None):
    # api call 
    pid = 0 
    parentId = 0 
    if(moduleId == "FNDMGMT"):
        return pid, parentId
    
    
    if(projectName is None):
        projectName = ''
    elif(contractName is None):
        contractName = ''
    
    data = {}
    data['moduleId'] = moduleId
    data['projectName'] = projectName
    data['contractName'] = contractName
    
    # print "Ravi "
    
    # url = "api/Auro/GetParentIds?moduleId="+moduleId+"&projectName="+projectName+"&contractName="+contractName; 
    url = "api/Auro/GetParentIds"
    response = requests.get(baseUrl+url , params=data)
    if(response.ok):
        jsonResponse = json.loads(response.content)
        pid = jsonResponse[PROJECT_ID]
        parentId = jsonResponse[PARENT_ID]
        return pid , parentId
    else:
        return None, None
    
       
    # def GetWorkflowActionsFromState():
    #     NotImplemented 
        
    
    
     
    