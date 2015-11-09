#!/usr/bin/python
#__author__ = 'Vosteen'


import serviceNowConfig
import arcsightIOInterface
import serviceNowInterface
import csv
import os
import logging
import shutil
import emailout

serviceNowConfig.ClientConfig("CSVImport")
logger = logging.getLogger('serviceNowInterface')
logger.info("Started CSV Import")

varCSVFileName = "/opt/arcsight/snow/serviceNowModule/Working/incident_with_close_notes.csv"
varImportFolder = "/opt/arcsight/manager/archive/imports/"
varTemplateFolder = "/opt/arcsight/manager/archive/template/"
varClosedTicketFolder = "/opt/arcsight/manager/archive/template/closed"
Files2Proc = arcsightIOInterface.arcsightInterface()
ServiceNowProc = serviceNowInterface.serviceNowInterface()
sysemail = emailout.emailout()


#try:
vCSVFile = open(varCSVFileName, 'rU')
csvreader = csv.reader(vCSVFile)
vClosedDescription = ""
rcount = 0
count, rcount, vStatus, vIncidentNum = 0, 0,  "", ""
for row in csvreader:
    rcount += 1
    count, vStatus, vIncidentNum, vSubStatus= 0, "", "", ""
    if rcount != 1:
        for column in row:
            if count == 0:
                vIncidentNum = column
                logger.debug(vIncidentNum)
            elif count == 3:
                vStatus = column
                logger.debug(vStatus)
            elif count == 4:
                vSubStatus = column
                logger.debug(vSubStatus)
            elif count == 11:
                vClosedDescription = column
                logger.debug(vClosedDescription)
            count += 1
        if os.path.exists(varTemplateFolder + vIncidentNum + ".xml"):
            # Update the template INC file repository
            if vStatus == "Closed" or vStatus == "Resolved":
                vstatusupdate = "Closed"
            else:
                vstatusupdate = vStatus

            Files2Proc.updateTemplateIncStatus(varTemplateFolder + vIncidentNum + ".xml", vstatusupdate)
            # Update the template INC file with close notes description
            Files2Proc.updateTemplateClosedNotes(varTemplateFolder + vIncidentNum + ".xml", vClosedDescription)
            if vStatus == "Closed":
                # Update the template INC file with close reasons
                vUserId = Files2Proc.readUserId(varTemplateFolder + vIncidentNum + ".xml")
                Files2Proc.updateTemplateClosedReason(varTemplateFolder + vIncidentNum + ".xml", "Resolved")
                if vSubStatus != "Cancelled":
                    sysemail.sendEmail(vIncidentNum, "system", "ClosedTicket")

            if vSubStatus == "Cancelled":
                # Update the template INC file to Escalate if status = cancelled
                Files2Proc.updateTemplateClosedReason(varTemplateFolder + vIncidentNum + ".xml", "Pending")
                sysemail.sendEmail(vIncidentNum, "system", "ClosedTicketCancelled")

            # Update ESM with ticket status
            Files2Proc.updateESMClosed(varTemplateFolder + vIncidentNum + ".xml", rcount)
            # If ticket is closed move the template file to the closed ticket folder
            if vStatus == "Closed":
                try:
                    shutil.move(varTemplateFolder + vIncidentNum + ".xml", varClosedTicketFolder)
                    logger.info("Ticket closed... Moving template file to closed ticket folder: " + varClosedTicketFolder + vIncidentNum + ".xml")
                except:
                    logger.error("Error moving template file to closed ticket folder: " + varClosedTicketFolder + vIncidentNum + ".xml")
        else:
            logger.info("Incident in csv :" + vIncidentNum + " not found in ArcSight Case in template folder: " + varTemplateFolder + vIncidentNum + ".xml")
#except:
#    logger.error("Error opening CSV file.  Verify that it exists.")
#    sys.exit("Error opening CSV file.  Verify that it exists.")




