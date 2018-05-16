# Navigate intent - works properly

#Handler : lambda_function.lambda_handler
#File Name : navigate.py
#Function : AuroLambda

import masterworks as Masterworks
import IntentHelper as Lamda

FORMNAME = "Form" 
PROJECTNAME = "Project"
CONTRACTNAME="Contract"
RECORD = "record"

def navigate(intent_request):
    if(FORMNAME in Lamda.getSlots(intent_request)):
        formName = Lamda.getSlots(intent_request)[FORMNAME]
    else:
        formName = None
    if(PROJECTNAME in Lamda.getSlots(intent_request)):
        projectName = Lamda.getSlots(intent_request)[PROJECTNAME]
    else:
        projectName = None
    if(CONTRACTNAME in Lamda.getSlots(intent_request)):
        contractName = Lamda.getSlots(intent_request)[CONTRACTNAME]
    else:
        contractName = None
    
    if(RECORD in Lamda.getSlots(intent_request)):
        recordName = Lamda.getSlots(intent_request)[RECORD]
    else:
        recordName = None
        
    sessionAttributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {} 
    moduleId = Masterworks.GetModuleId(str(formName))
    print moduleId

    if(intent_request['invocationSource'] == 'DialogCodeHook'):
        if(moduleId is None):
            Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Form",
                       {'contentType': 'PlainText', 'content':'Enter the Form you want to take action on'})
        
        if((moduleId == "BDGTEST" or moduleId== "CONTDWR") and projectName is None):
            return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           PROJECTNAME,
                           {'contentType': 'PlainText', 'content':'In which Project would you like to create the '+str(formName) +' record?'})

        if(moduleId == "CONTDWR" and contractName is None):
             return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           CONTRACTNAME,
                           {'contentType': 'PlainText', 'content':'In which Contract would you like to create the '+str(formName) +' record?'})

    if(recordName is not None): 
        instanceId, pid, parentId = Masterworks.GetFormInstanceId(moduleId, recordName, projectName); 
        if(instanceId is not None and pid is not None and parentId is not None):
            url = CreateFormUrl(moduleId, pid, parentId, instanceId); 
            sessionAttributes["url"] = url
    else:
        pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId, projectName, contractName)
        url = CreateListUrl(moduleId, pid, parentId); 
        sessionAttributes["url"] = url
    
    return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
           

def CreateListUrl(moduleId, pid, parentId):
    listPage = "Default.aspx#/Common/BrixListPage.aspx?xcontext="+str(moduleId)+"&PID="+str(pid)+"&ParentID="+str(parentId)
    return listPage


def CreateFormUrl(moduleId, pid, parentId, instanceId):
    # baseUrl = Masterworks.baseUrl
    formPage = "Default.aspx#/Common/BrixForm.aspx?Context="+str(moduleId)+"&PID="+str(pid)+"&ParentID="+str(parentId)+"&Mode=View&InstanceID="+str(instanceId)
    return formPage
