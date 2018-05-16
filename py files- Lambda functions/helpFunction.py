# helpFunction is the Lambda function name. Aurobot calls helpFunction but it's handler determines the filename and function.
# here it was originally : lambda_function.lambda_handler. If you rename the default lambda_function file, you will have to rename the handler to file_name.lambda_handler.

#Handler : lambda_function.lambda_handler
#File Name : lambda_function.py
#Function : helpFunction


import math
import dateutil.parser
import datetime
import time
import os
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

FORMNAME="Form"
HELPAREA="HelpArea"

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }   
    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def validate_help_request(formName, helpArea):
    return {
        'isValid': 'false',
        'violatedSlot': 'helpArea',
        'message': {'contentType': 'PlainText', 'content': ''}
    }

def helpPage(intent_request):
    formName = get_slots(intent_request)[FORMNAME]
    helpArea = get_slots(intent_request)[HELPAREA]
    
    validation_result = validate_help_request(formName, helpArea)
               
    if formName == 'Budget Estimates':
        if(helpArea == 'create a record'):
            url = createHelpUrl('mergedProjects/BudgetManagement_Estimator_Forecasts/Budget_Management/Budget_Estimates/Creating_a_Budget_Estimate_FS.htm');
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        else:    
            url=createHelpUrl('Enterprise/Enterprise_Home_FS.htm')
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
            
    elif formName == 'Global Fund List':
        if(helpArea == 'create a record'):
            url = createHelpUrl('Fund_Management/Global_Fund_Sources/Creating_Global_Fund_Sources_FS.htm');
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        elif helpArea == 'perform workflow action':
            url = createHelpUrl('Fund_Management/Global_Fund_Sources/Global_Fund_Source_Workflow_Stages_FS.htm');
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        else:    
            url=createHelpUrl('Fund_Management/Global_Fund_Sources/Global_Fund_List_FS.htm')
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))        
        
    elif formName == 'Daily Progress Report':
        if(helpArea == 'create a record'):
            url = createHelpUrl('mergedProjects/Contract%20Management/Construction_Contract/Daily_Progress_Report/Creating_a_Daily_Progress_Report.htm');
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        
        elif helpArea == 'perform workflow action':
            url = createHelpUrl('mergedProjects/Contract%20Management/Construction_Contract/Daily_Progress_Report/Daily_Progress_Report_Workflow_Stages.htm');
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        else:    
            url=createHelpUrl('mergedProjects/Contract%20Management/Construction_Contract/Daily_Progress_Report/Daily_Progress_Report1.htm')
            intent_request['sessionAttributes']["url"] = url 
            return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
        
    else:
        #url = createHelpUrl('Enterprise/Enterprise_Home_FS.htm');
        #intent_request['sessionAttributes']["url"] = url 
        return delegate(intent_request['sessionAttributes'], get_slots(intent_request))
    
def createHelpUrl(trailingURL):
    baseUrl = 'Modules/WEBHELP/Index.htm#';
    formPage = baseUrl + trailingURL ;
    return formPage

def dispatch(intent_request):
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    intent_name = intent_request['currentIntent']['name']
    #if intent_name == 'PerformWF':
    return helpPage(intent_request)
    
def lambda_handler(event, context):
    print "hello1"
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)