# listRetrievalFunction is the Lambda function name. Aurobot calls listRetrievalFunction but it's handler determines the filename and function.
# here it was originally : lambda_function.lambda_handler. If you rename the default lambda_function file, you will have to rename the handler to file_name.lambda_handler.
#Handler : lambda_function.lambda_handler
#File Name : listRetrieval.py
#Function : ListRetrievalFunction

BaseURL="http://9e5783d1.ngrok.io/"
from botocore.vendored import requests
import json
import masterworks as Masterworks
import IntentHelper as Lamda

def listRetrieval(intent_request):
    print "hello3"
    dataFilter={}
    dataFilter['username']='Akhila'
    dataFilter['password']='aurigo'
        #intent_request['currentIntent']['slots']['slotTwo']
    dataFilter['c']=''
    dataFilter['role']='Administrator'
    
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    pageName=intent_request['currentIntent']['slots']['Form']
    parentInfo=intent_request['currentIntent']['slots']['Project']
    contractInfo=intent_request['currentIntent']['slots']['Contract']
    filterCriteria=intent_request['currentIntent']['slots']['ConditionA']
    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':
        print "hello4"
        pageNames = ["Global Fund List", "Budget Estimates", "Daily Progress Report"]
        if pageName is not None and pageName not in pageNames:
            validation_result= Lamda.build_validation_result(False,
                                           'Form',
                                           'Please select Valid Form')
            if not validation_result['isValid']:
                #intent_request['currentIntent']['slots']['validation_result']['violatedSlot'] = None
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                                   intent_request['currentIntent']['name'],
                                   intent_request['currentIntent']['slots'],
                                   "ConditionA",
                                   {'contentType': 'PlainText', 'content': '<href Please enter http://masterworks.qa.aurigoblr.com/Modules/USRMGMT/Login.aspx Project Name of {} />'.format(pageName)},)
                                       
        if(pageName=='Global Fund List'):
            intent_request['currentIntent']['slots']['Project']='Nan'
        if(pageName=='Budget Estimates' or pageName=='Global Fund List'):
            intent_request['currentIntent']['slots']['Contract']='Nan'
        if(pageName is not None and filterCriteria is None ):
            if(pageName=='Budget'):
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
    if(pageName is not None and parentInfo is not None and contractInfo is not None and filterCriteria is not None):
        #masterworkshelper = http_helper("http://781bcb8c.ngrok.io/")
        '''
        response=requests.post(BaseURL+"api/Login", json=json.dumps(dataFilter))
        print response.status_code
        print json.loads(response.content)['Token']
        print 'Hello5'
        #http://vtrans.aurigo.net/
        #response = requests.post('http://localhost:59874/api/ListFilterManager/AddCurrentFilter',data=dataFilter)
        print 'Hello56'
        headers={'Authorization-Token':json.loads(response.content)['Token']},
        '''
        filterData={}
        filterData['formName']=intent_request['currentIntent']['slots']['Form']
        filterData['projectName']=intent_request['currentIntent']['slots']['Project']
        filterData['contractName']=intent_request['currentIntent']['slots']['Contract']
        filterData['filterCondition']=intent_request['currentIntent']['slots']['ConditionA']
        #filterData['UID']=json.loads(response.content)['UID']
        responseFilter=requests.post(BaseURL+"api/ListFilterManager/AddCurrentFilterUsingLex", json=json.dumps(filterData))
        print json.loads(responseFilter.content)
        #print json.loads(responseFilter.content)['FilterName']
        if(responseFilter.status_code==200):
            moduleID=Masterworks.GetModuleId(pageName)
            pID,parentID=Masterworks.GetPIDParentIdForModule(moduleID,parentInfo,contractInfo)
            UrlValue=buildURL(moduleID,pID,parentID,json.loads(responseFilter.content)["Code"])
            intent_request["sessionAttributes"]['url']=UrlValue
            return Lamda.close(output_session_attributes,"Fulfilled","{0} is added to list page".format(json.loads(responseFilter.content)["FilterName"]))
        return  Lamda.elicit_slot(
                    output_session_attributes,
                    intent_request['currentIntent']['name'],
                    intent_request['currentIntent']['slots'],
                    'ConditionA',
                    {'contentType': 'PlainText', 'content': ' {}'.format(json.loads(responseFilter.content))},
                    )
    return Lamda.delegate(output_session_attributes,intent_request['currentIntent']['slots'])
    
def buildURL(moduleId, pid, parentId,fltrCode):
    # baseUrl = Masterworks.baseUrl
    formPage = "Default.aspx#/Common/BrixListPage.aspx?xContext="+str(moduleId)+"&PID="+str(pid)+"&ParentID="+str(parentId)+"&fltrCode="+str(fltrCode)
    return formPage
