#!/usr/bin/python
#__author__ = 'Vosteen'
# cron ArcSightServiceNowIntegrator.py to run every 15 minutes
# Initiates the integration process

import serviceNowConfig
import arcsightIOInterface
import serviceNowInterface
import arcsightXMLParser
import sys
import logging
import emailout


serviceNowConfig.ClientConfig('SNIncident')
logger = logging.getLogger('serviceNowInterface')
logger.info("Started ServiceNow Interface")

Files2Proc = arcsightIOInterface.arcsightInterface()
ServiceNowProc = serviceNowInterface.serviceNowInterface()
ASXMLParser = arcsightXMLParser.arcsightXMLParser()
sysemail = emailout.emailout()

#Checks for any files to process
ListFiles2Proc = Files2Proc.checkFiles2Process()

if ListFiles2Proc == "False":
    sys.exit()
else:
    if "||" in ListFiles2Proc:
        for fileName in ListFiles2Proc.split("||"):
            ASXMLParser.prepFile(fileName)
    else:
        ASXMLParser.prepFile(ListFiles2Proc)


# Checks for any files to process

ListFiles2Proc = Files2Proc.checkFiles2Process()

if ListFiles2Proc == "False":
    sys.exit()
else:
    # Checks to see if there's multiple files in the response
    if "||"in ListFiles2Proc:
        print "Multiple files to process: " + ListFiles2Proc
        # Splits the files on delimeter "||", interates through files and searches for incident number
        for fileName in ListFiles2Proc.split("||"):
            vSNIncidentNum = (Files2Proc.readIncNum(fileName))
            if vSNIncidentNum == "False":
                # Creates new Incident
                vnewTicketNum = ServiceNowProc.createIncident(fileName)
                if vnewTicketNum != "False":
                    # Update file with new Incident Number
                    Files2Proc.updateTemplateNewIncNum(fileName, vnewTicketNum)
                    # Update ESM case with new Incident Number - writes to import folder
                    Files2Proc.updateESMNewIncNum(fileName)
                    # Update the template folder
                    Files2Proc.updateTemplate(fileName, vnewTicketNum)
                else:
                    try:
                        sysemail.sendEmail(fileName, "system", "ERRORCREATINC")
                        logger.error("An error creating the incident.  Please review the logs above for the specific error.")
                    except:
                        logger.error("****** Error sending out system notification email showing failure in incident creation. ******")
            else:
                logger.info("Existing incident " + vSNIncidentNum + ".  Updating template file next.")
                # Ticket already created, just update the template folder
                Files2Proc.updateTemplate(fileName, str(vSNIncidentNum))
    else:
        vSNIncidentNum = Files2Proc.readIncNum(ListFiles2Proc)
        if vSNIncidentNum == "False":
                vnewTicketNum = ServiceNowProc.createIncident(ListFiles2Proc)
                if vnewTicketNum != "False":
                    # Update file with new Incident Number
                    Files2Proc.updateTemplateNewIncNum(ListFiles2Proc, vnewTicketNum)
                    # Update ESM case with new Incident Number - writes to import folder
                    Files2Proc.updateESMNewIncNum(ListFiles2Proc)
                    # Update the template folder
                    Files2Proc.updateTemplate(ListFiles2Proc, vnewTicketNum)
                else:
                    try:
                        sysemail.sendEmail(ListFiles2Proc, "system", "ERRORCREATINC")
                        logger.error("An error creating the incident.  Please review the logs above for the specific error.")
                    except:
                        logger.error("****** Error sending out system notification email showing failure in incident creation. ******")
        else:
            logger.info("Existing incident " + str(vSNIncidentNum) + ".  Updating template file next.")
            #  Ticket already created, just update the template folder
            Files2Proc.updateTemplate(ListFiles2Proc, vSNIncidentNum)



