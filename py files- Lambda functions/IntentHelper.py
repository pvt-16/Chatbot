# This contains definitions for all the intent format functions. Pass your responses to these functions and get an ouput in the format that Lex can read.
#Generic functions for Lex
#Handler : lambda_function.lambda_handler
#File Name : IntentHelper.py
#Function : AuroLambda


currentIntent = 'currentIntent'
slots = 'slots'

def getSlots(intent):
    return intent[currentIntent][slots]
    

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
def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }
    
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                         "contentType": "PlainText",
                         "content": message
                     }

        }
    }
    
    
    
def invocationSource(intent_request):
    return intent_request['invocationSource']
    