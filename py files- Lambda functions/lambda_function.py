#Main function : lambda_function. Used to handle the direction of the intent processing.

#Handler : lambda_function.lambda_handler
#File Name : IntentHelper.py
#Function : AuroLambda


import math
import dateutil.parser
import datetime
import time
import os
import logging
import create as CreateIntent
import update as UpdateIntent
import listRetrieval as ListRetrievalIntent
import navigate as NavigateIntent
import scalarRetrieval as scalarCellRetrievalIntent
# from botocore.vendored import requests
import json
# import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
auth_Token = '111'

# """------------------------------------INTENT NAME------------------------------------------------"""
SCALAR_RETRIEVE = "ScalarCellRetrieval" 
LIST_RETRIEVE = "ListRetrieval"
# WF_ACTION = ""
# HELP_NAVIGATE = ""
# HELP_TICKET = ""
NAVIGATE = "Navigate"
CREATE="Create"
UPDATE = "Update"
# SAVE_TO_WORKSPACE = "" #OPTIONAL : DEPENDS ON IMPLEMENTATION


def close(session_attributes):
    response = {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': "Fulfilled",
            'message': 'Success @ www.youtube.com'
        }
    }

    return response
    
    
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    
    intent_name = intent_request['currentIntent']['name']
    print intent_name
    # # Dispatch to your bot's intent handlers
    if intent_name == SCALAR_RETRIEVE:
        return scalarCellRetrievalIntent.scalarCellRetrieval(intent_request)
    if intent_name == LIST_RETRIEVE:
        return ListRetrievalIntent.listRetrieval(intent_request)
    # elif intent_name == WF_ACTION: 
    #     return perform_wf_action(intent_request)
    # elif intent_name == HELP_NAVIGATE: 
    #     return help_navigate(intent_request)
    # elif intent_name == HELP_TICKET: 
    #     return help_ticket(intent_request) 
    elif intent_name == NAVIGATE: 
         return NavigateIntent.navigate(intent_request) 
    elif intent_name == CREATE: 
        return CreateIntent.create(intent_request) 
    elif intent_name == UPDATE: 
        return UpdateIntent.update(intent_request)
    # elif intent_name == SAVE_TO_WORKSPACE: 
    #     return save_to_workspace(intent_request)
    elif intent_name is None:
        #raise Exception('Intent not found')
        print 'ff'
    else: 
        raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    # os.environ['TZ'] = 'America/New_York'
    # time.tzset()
    # logger.debug('event.bot.name={}'.format(event['bot']['name']))
    if ( hasattr(event['sessionAttributes'],'Authorization-Token') ):
        auth_Token= event['sessionAttributes']['Authorization-Token'];
        
    print context.aws_request_id
    return dispatch(event)
