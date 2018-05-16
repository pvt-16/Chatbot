# Create intent - works properly

#Handler : lambda_function.lambda_handler
#File Name : create.py
#Function : AuroLambda

import masterworks as Masterworks
import IntentHelper as Lamda

FORMNAME = "Form" 
PROJECTNAME = "Project"
CONTRACTNAME="Contract"

def create(intent_request):
    formName  = Lamda.getSlots(intent_request)[FORMNAME]
    if(PROJECTNAME in Lamda.getSlots(intent_request)):
        projectName = Lamda.getSlots(intent_request)[PROJECTNAME]
    else:
        projectName = None
    if(CONTRACTNAME in Lamda.getSlots(intent_request)):
        contractName = Lamda.getSlots(intent_request)[CONTRACTNAME]
    else:
        contractName = None
    # moduleId = Masterworks.GetModuleId(formName); 
    # pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId) 
    moduleId = Masterworks.GetModuleId(str(formName))
    print moduleId
    if moduleId is not None:
        sessionAttributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId)
        
        if(moduleId == "BDGTEST"):
            if(projectName is not None):
                pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId, projectName)
                if(pid is not None and parentId is not None):
                    url = CreateUrl(moduleId, pid, parentId)
                    sessionAttributes["url"] = url 
                    return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
                else:
                    return Lamda.build_validation_result(False,PROJECTNAME,intent_request['currentIntent']['slots'])
                    #   {'contentType': 'PlainText', 'content':'Given Project name does not exists.Please specify the correct Project Name'})
            
            else:
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       PROJECTNAME,
                       {'contentType': 'PlainText', 'content':'In which Project would you like to create the '+str(formName) +' record?'})
        
        
        elif(moduleId == "CONTDWR"):
            if(projectName is not None and contractName is not None):
                pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId, projectName, contractName)
                if(pid is not None and parentId is not None):
                    url = CreateUrl(moduleId, pid, parentId)
                    sessionAttributes["url"] = url 
                    return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
                else:
                    return Lamda.build_validation_result(False,PROJECTNAME,intent_request['currentIntent']['slots'])
                    #  return Lamda.elicit_slot(intent_request['sessionAttributes'],
                    #   intent_request['currentIntent']['name'],
                    #   intent_request['currentIntent']['slots'],
                    #   PROJECTNAME,
                    #   {'contentType': 'PlainText', 'content':'Given Project or Contract name does not exists.Please specify the correct Project or Contract Name'})
            
            elif(projectName is None):
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       PROJECTNAME,
                       {'contentType': 'PlainText', 'content':'In which Project would you like to create the '+str(formName) +' record?'})
        
            elif(contractName is None):
                return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       CONTRACTNAME,
                       {'contentType': 'PlainText', 'content':'In which Contract would you like to create the '+str(formName) +' record?'})

        
        else: 
            url = CreateUrl(moduleId, 0, 0)
            sessionAttributes["url"] = url
            return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
            
        # sessionAttributes["url"] = url 
        # return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
    else:
        return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Form",
                       {'contentType': 'PlainText', 'content':'Enter the Form you want to take action on'})
    # hit api to open url 
    


def CreateUrl(moduleId, pid, parentId):
    # baseUrl = Masterworks.baseUrl
    formPage = "Default.aspx#/Common/BrixForm.aspx?Context="+str(moduleId)+"&PID="+str(pid)+"&ParentID="+str(parentId)+"&Mode=New"
    return formPage
