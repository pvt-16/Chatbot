# Used by ScalarCellRetrieval intent  in Auro Bot-??

#Handler : lambda_function.lambda_handler
#File Name : scalarRetrieval.py
#Function : pushPak

BaseURL="http://9e5783d1.ngrok.io/"
from botocore.vendored import requests
import json
import masterworks as Masterworks
import IntentHelper as Lamda

def scalarCellRetrieval(intent_request):
    '''
    dataFilter={}
    dataFilter['username']='Akhila'
    dataFilter['password']='aurigo'
    dataFilter['c']=''
    dataFilter['role']='Administrator'
    '''
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    pageName=intent_request['currentIntent']['slots']['Form']
    #parentInfo=intent_request['currentIntent']['slots']['Project']
    #contractInfo=intent_request['currentIntent']['slots']['Contract']
    columnInfo=intent_request['currentIntent']['slots']['Column']
    recordID=intent_request['currentIntent']['slots']['record']
    ws=intent_request['currentIntent']['slots']['ws']
    source = intent_request['invocationSource']
    moduleID=Masterworks.GetModuleId(intent_request['currentIntent']['slots']['Form'])
  
    formInstanceID, pid, parentId = Masterworks.GetFormInstanceId(moduleID, recordID)

    
    #print formInstanceID
    if(source == 'DialogCodeHook'):
        print "hello4"
        pageNames = ["Global Fund List", "Budget Estimates", "Daily Progress Report"]
        '''
        if pageName is not None and pageName not in pageNames:
            validation_result= Lamda.build_validation_result(False,
                                           'Form',
                                           'Please select Valid Form')
            if not validation_result['isValid']:
                #intent_request['currentIntent']['slots']['validation_result']['violatedSlot'] = None
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "Form",
                                   {'contentType': 'PlainText', 'content': 'Enter Valid Form'})
        
        if pageName is not None and columnInfo is None:
            return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "Column",
                                   {'contentType': 'PlainText', 'content': 'Enter column of Form'})
        #return Lamda.delegate(output_session_attributes,intent_request['currentIntent']['slots'])
        '''
        '''
        if pageName is not None and formInstanceID is None:
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "record",
                                   {'contentType': 'PlainText', 'content': 'Enter Record ID'})
        '''
        if(pageName=='Global Fund List'):
            intent_request['currentIntent']['slots']['Project']=0
        if(pageName=='Budget Estimates' or pageName=='Global Fund List'):
            intent_request['currentIntent']['slots']['Contract']=0
        if(pageName is None and recordID is not None):
            if(pageName=='Budget Estimates'):
                return Lamda.elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'Project',
                    {'contentType': 'PlainText', 'content': 'Please enter Project Name of {} '.format(pageName)},
                    )
            elif(pageName=='Daily Progress Report'):
                return Lamda.elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'Contract',
                    {'contentType': 'PlainText', 'content': 'Please enter Contract Name of {}'.format(pageName)},
                    )
            
        print pageName
        print "pusjndjf"
        print formInstanceID
        print columnInfo
        print ws
    if(pageName is not None and formInstanceID is not None and columnInfo is not None and ws is not None):
        scalarData={'moduleId':moduleID,'columnName':intent_request['currentIntent']['slots']['Column'],'instanceID':formInstanceID,'WorkSpaceEnabled':ws}
        responseFilter=requests.get(BaseURL+"api/Auro/GetScalarCellData",params=scalarData)
            #print json.loads(responseFilter.content)
        print responseFilter.status_code
            #print json.loads(responseFilter.content)['FilterName']
        if(responseFilter.status_code==200 or responseFilter.status_code==202):
            return Lamda.close(output_session_attributes,"Fulfilled","{}".format(responseFilter.content))
        return  Lamda.elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'ws',
                    {'contentType': 'PlainText', 'content': 'Want to save in Work Space?'},
                    )
    return Lamda.delegate(output_session_attributes,intent_request['currentIntent']['slots'])
    
    