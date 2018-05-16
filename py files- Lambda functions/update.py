# Update intent - works properly

#Handler : lambda_function.lambda_handler
#File Name : update.py
#Function : AuroLambda

import masterworks as Masterworks
import IntentHelper as Lamda

FORMNAME = "Form" 
PROJECTNAME = "Project"
CONTRACTNAME="Contract"
RECORD = "record"

def update(intent_request):
    formName  = Lamda.getSlots(intent_request)[FORMNAME]
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
        
    # moduleId = Masterworks.GetModuleId(formName); 
    # pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId) 
    moduleId = Masterworks.GetModuleId(str(formName))
    print moduleId
    if moduleId is not None:
        sessionAttributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # pid, parentId = Masterworks.GetPIDParentIdForModule(moduleId)
        
        if recordName is not None:
            
            if(moduleId == "BDGTEST"):
                print projectName
                if projectName != None :
                    instanceId, pid, parentId = Masterworks.GetFormInstanceId(moduleId, recordName, projectName); 
                    if(instanceId is not None and pid is not None and parentId is not None):
                        url = CreateUrl(moduleId, pid, parentId, instanceId)
                        sessionAttributes["url"] = url 
                        return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
                    else:
                         return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           RECORD,
                           {'contentType': 'PlainText', 'content':'Given Record name does not exists.Please specify the correct Record Name'})
                
                else:
                    return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           PROJECTNAME,
                           {'contentType': 'PlainText', 'content':'In which Project would you like to create the'+str(formName) +'record?'})
                           
            elif(moduleId == "CONTDWR"):
                if(projectName is not None and contractName is not None):
                    instanceId, pid, parentId = Masterworks.GetFormInstanceId(moduleId, recordName, projectName, contractName); 
                    if(instanceId is not None and pid is not None and parentId is not None):
                        url = CreateUrl(moduleId, pid, parentId, instanceId)
                        sessionAttributes["url"] = url 
                        return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
                    else:
                         return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           RECORD,
                           {'contentType': 'PlainText', 'content':'Given Record name does not exists. Please specify the correct record name.'})
                
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
                instanceId, pid, parentId = Masterworks.GetFormInstanceId(moduleId, recordName, 0, 0)
                if(instanceId is not None):
                    url = CreateUrl(moduleId, 0, 0, instanceId)
                    sessionAttributes["url"] = url 
                    return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
                else:
                    return Lamda.elicit_slot(intent_request['sessionAttributes'],
                           intent_request['currentIntent']['name'],
                           intent_request['currentIntent']['slots'],
                           RECORD,
                           {'contentType': 'PlainText', 'content':'Given Record name does not exists. Please specify the correct record name.'})
                
        else:
            if(moduleId == "BDGTEST"):
                columnName = "Budget Estimate Name"
            elif(moduleId == "FNDMGMT"):
                columnName = "Fund source name"
            elif(moduleId == "CONTDWR"):
                columnName = "DPR Number"
            return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       RECORD,
                       {'contentType': 'PlainText', 'content':'Please specify the '+columnName+ ' of the record you want to update.'})
            
            
        sessionAttributes["url"] = url 
        return Lamda.delegate(sessionAttributes, Lamda.getSlots(intent_request))
    else:
        return Lamda.elicit_slot(intent_request['sessionAttributes'],
                       intent_request['currentIntent']['name'],
                       intent_request['currentIntent']['slots'],
                       "Form",
                       {'contentType': 'PlainText', 'content':'Enter the Form you want to take action on'})
    # hit api to open url 
    


def CreateUrl(moduleId, pid, parentId, instanceId):
    # baseUrl = Masterworks.baseUrl
    formPage = "Default.aspx#/Common/BrixForm.aspx?Context="+str(moduleId)+"&PID="+str(pid)+"&ParentID="+str(parentId)+"&Mode=Edit&InstanceID="+str(instanceId)
    return formPage
