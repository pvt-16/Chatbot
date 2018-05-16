# Perform workflow intent - works properly
#The lambda function in TestFuncRavi imports this file. 
# [ import performWF as PerformWF]
#Import this to lambda_function.  Looks like lambda_function imports from performWF as well. Check the interdependencies. 

#Handler : lambda_function.lambda_handler
#File Name : performWF.py
#Function : TestFuncRavi

import math
import dateutil.parser
import datetime
import time
import os
import logging
from botocore.vendored import requests
import json
import masterworks as Masterworks
import IntentHelper as Lamda
import lambda_function as LamdaFunction

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MODULENAME="Form"
WF_ACTION="WFAction"
FormInstance="record"

form_uniqueIdentifier_mapping = {
    "Budget Estimate":"Budget Estimate Name",
    "Daily Progress Report":"DPR Number",
    "Global Fund List":"Fund Name"
}

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
    


def perform_wf_action(intent_request):
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    wf_action = get_slots(intent_request)[WF_ACTION]
    module = get_slots(intent_request)[MODULENAME]
    record = get_slots(intent_request)[FormInstance]
    
    
    #rint record,module
    moduleID= Masterworks.GetModuleId(module)
    #print moduleID
   
    
    url=Masterworks.baseUrl
    
    if module is not None and record is None:
        return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "record",
                       {'contentType': 'PlainText', 'content': 'Enter the {0} you want to {1}'.format(form_uniqueIdentifier_mapping[module],wf_action)})
    elif module is None:
        return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Form",
                       {'contentType': 'PlainText', 'content':'Enter the Form you want to take action on'})
                       
    if moduleID=='BDGTEST' or moduleID=='CONTDWR':
        Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Project",
                       {'contentType': 'PlainText', 'content':'Enter the Project Name'})
                       
    if moduleID=='CONTDWR':
        return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Contract",
                       {'contentType': 'PlainText', 'content':'Enter the Contract Name'})
                       
    data={'username': 'pt',
          'password': 'aurigo',
           'role': 'Administrator',
           'c': 'as'
         }
    formInstanceID,pid, contractid = Masterworks.GetFormInstanceId(moduleID,record,get_slots(intent_request)['Project'],get_slots(intent_request)['Contract'])
    #print "form " + formInstanceID
    #print get_slots(intent_request)
        
    data1={'moduleId':str(moduleID),'formInstanceid':str(formInstanceID),'jsonParameters':'{}'}#json.dumps({'pid':pid,'parentid':contractid})
                     
    #print "data --------- " + json.dumps(data1)
    #res = requests.post(url+'api/Login', json=str(data), headers={'content':'application/json'})
    response=requests.post(url+"api/Login", json=json.dumps(data))
    
    req2 = requests.get(url+'api/Workflow/GetActions', params=data1,headers={'Authorization-Token':json.loads(response.content)['Token']})
    
    #print json.loads(req2.content)
    print req2.content
    actionId = GetValueInArray('ActionId',wf_action,json.loads(req2.content))
    performActionParams={'moduleId':moduleID,'formInstanceId':formInstanceID,'actionId':actionId,'actionName':wf_action}
    res3 = requests.post(url+'api/Workflow/PerformAction',json=json.dumps({'pid':pid,'parentid':contractid}),params=performActionParams,headers={'Authorization-Token':json.loads(response.content)['Token']})
    #return Lambda.close(output_session_attributes,"Fulfilled","Done")
    return Lamda.delegate(output_session_attributes,intent_request['currentIntent']['slots'])

def GetValueInArray(propertyName,actionName,array):
    for a in array:
        print a
        if actionName == a["ActionName"]:
            return a[propertyName]
