# Used by ScalarCalRetrieval intent  in Auro Bot-??

#Handler : lambda_function.lambda_handler
#File Name : scalarRetrieval.py
#Function : AuroLambda


BaseURL="http://0e9290a0.ngrok.io/"
from botocore.vendored import requests
import json
import masterworks as Masterworks
import IntentHelper as Lamda

def scalarCellRetrieval(intent_request):
    dataFilter={}
    dataFilter['username']='Akhila'
    dataFilter['password']='aurigo'
    dataFilter['c']=''
    dataFilter['role']='Administrator'
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    pageName=intent_request['currentIntent']['slots']['Form']
    #parentInfo=intent_request['currentIntent']['slots']['Project']
    #contractInfo=intent_request['currentIntent']['slots']['Contract']
    columnInfo=intent_request['currentIntent']['slots']['Column']
    recordID=intent_request['currentIntent']['slots']['record']
    source = intent_request['invocationSource']
    
    if source == 'DialogCodeHook':
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
        '''
        if pageName is not None and columnInfo is None:
            return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "Column",
                                   {'contentType': 'PlainText', 'content': 'Enter column of Form'})
        
        if pageName is not None and recordID is None:
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "record",
                                   {'contentType': 'PlainText', 'content': 'Enter Record ID'})
    
    if(pageName is not None and recordID is not None and columnInfo is not None):
        #masterworkshelper = http_helper("http://781bcb8c.ngrok.io/")
        response=requests.post(BaseURL+"api/Login", json=json.dumps(dataFilter))
        print response.status_code
        print json.loads(response.content)['Token']
        print 'Hello5'
        moduleID=Masterworks.GetModuleId(intent_request['currentIntent']['slots']['Form'])
        scalarData={'moduleId':moduleID,'columnName':intent_request['currentIntent']['slots']['Column'],'instanceID':intent_request['currentIntent']['slots']['record']}
        responseFilter=requests.get(BaseURL+"api/Auro/GetScalarCellData", headers={'Authorization-Token':json.loads(response.content)['Token']},params=scalarData)
        print json.loads(responseFilter.content)
        print responseFilter.status_code
        #print json.loads(responseFilter.content)['FilterName']
        if(responseFilter.status_code==200):
            return Lamda.close(output_session_attributes,"Fulfilled","Value is {0}".format(json.loads(responseFilter.content)))
        return Lamda.close(output_session_attributes,"Fulfilled","sorry")
    return Lamda.delegate(output_session_attributes,intent_request['currentIntent']['slots'])
    
    