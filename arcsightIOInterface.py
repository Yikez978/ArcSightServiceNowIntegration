#__author__ = 'Vosteen'
#   arcsightIOInterface.py = defines the ArcSight working environments (export/import/template directories)
#   Reads the Exported XML file for its existence and parses the following
#                   - Verify existence of an Incident # already in SNOW
#                   - Determines what Template to use (0,1,2,3)
#                       * Parses the software is listed in the case (if templates 2,3 are selected)
#                   - Extracts Hostname, CaseID, and UserID from XML
#                   - Sets up an XML replica file inside the ../template/ directory.
#                        * Updates Incident # when SNOW ticket has been created.
#                        * Appends the ticket incident # to the XML and updates case
#                        * Updates XML when CSV provides any closing incident details -->Close Reason & Closing Notes  


class arcsightInterface():
    def __init__(self):
        import logging
        import os
        import sys
        logger = logging.getLogger('serviceNowInterface')
        varExportFolder = "/opt/arcsight/manager/archive/exports"
        varImportFolder = "/opt/arcsight/manager/archive/imports"
        varTemplateFolder = "/opt/arcsight/manager/archive/template"
        varClosedTicketFolder = "/opt/arcsight/manager/archive/template/closed"
        varBadTicketFolder = "/opt/arcsight/manager/archive/template/badxml"

        logger.info("Working ArcSight export folder: " + varExportFolder)
        logger.info("Working ArcSight import folder: " + varImportFolder)
        logger.info("Working ArcSight import-export template folder: " + varTemplateFolder)

        if not os.path.exists("/opt/arcsight/"):
            logger.info("Stopping work - /opt/arcsight/ does not exist - This script needs to run on an ArcSight ESM server. ")
            sys.exit("Stopping work - /opt/arcsight/ does not exist - This script needs to run on an ArcSight ESM server")

        if not os.path.exists(varTemplateFolder):
            try:
                os.makedirs(varTemplateFolder)
                logger.info("First time script has been run on this system - Created template folder: " + varTemplateFolder)
                print "First time script has been run on this system - Created template folder: " + varTemplateFolder
            except:
                logger.info("Error creating the working template folder.")
                logger.info("Error: " + sys.exc_info()[0])
                logger.info("Most likely cause is permissions on the file system.")
                sys.exit("Error creating the working template folder.  Most likely caused by file permissions.  See error in log.")
        if not os.path.exists(varClosedTicketFolder):
            try:
                os.makedirs(varClosedTicketFolder)
                logger.info("Created closed ticket folder: " + varClosedTicketFolder)
                print "Created closed ticket folder: " + varClosedTicketFolder
            except:
                logger.info("Error creating the closed ticket folder: " + varClosedTicketFolder)
                logger.info("Error: " + sys.exc_info()[0])
                logger.info("Most likely cause is permissions on the file system.")
                sys.exit("Error creating the closed ticket folder.  Most likely caused by file permissions. " + varClosedTicketFolder + "  See error in log.")
        if not os.path.exists(varBadTicketFolder):
            try:
                os.makedirs(varBadTicketFolder)
                logger.info("Created bad ticket folder: " + varBadTicketFolder)
                print "Created bad ticket folder: " + varBadTicketFolder
            except:
                logger.info("Error creating the bad ticket folder: " + varBadTicketFolder)
                logger.info("Error: " + sys.exc_info()[0])
                logger.info("Most likely cause is permissions on the file system.")
                sys.exit("Error creating the closed ticket folder.  Most likely caused by file permissions. " + varBadTicketFolder + "  See error in log.")

    def checkFiles2Process(self):
        import logging
        import os
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Checking for files to process...")
        varExportFolder = "/opt/arcsight/manager/archive/exports"
        vFiles2Process = False
        vFileList = ""
        for file in os.listdir(varExportFolder):
            if file.endswith(".xml"):
                vFiles2Process = True
                vFileList += varExportFolder + "/" + file + "||"
                logger.debug("File identified for processing: " + file)

        if not vFiles2Process:
            logger.info("****** No files to process ******")
            return "False"
        else:
            logger.info("File identified for processing: " + vFileList[:-2])
            return vFileList[:-2]

    def readIncNum(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<plannedActions>(\S+)</plannedActions>"
        vtext = open(vFileName).read()
        TicketNum = re.findall(vreg, vtext)

        if TicketNum:
            logger.info("Existing ticket number found in export file: " + ''.join(TicketNum))
            return ''.join(TicketNum)
        else:
            logger.info("No ticket found in export file")
            return "False"

    def readAttackProtocol(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<attackProtocol>(.*?)\:\s+\[.*\].*</attackProtocol>|<attackProtocol>(.*?)\:.*</attackProtocol>|<attackProtocol>(.*?)\:.*"
        #vreg = "<attackProtocol>(.*) \[.*\].*</attackProtocol>|<attackProtocol>(.*)</attackProtocol>"
        vtext = open(vFileName).read()
        AttackProtocol = re.findall(vreg, vtext)

        if AttackProtocol:
            logger.debug("Found Recommended Action in the file: " + ''.join(AttackProtocol[0]))
            return ''.join(AttackProtocol[0])
        else:
            logger.info("No Recommended Action found in the file")
            return "False"

    def readCaseName(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process case name: " + vFileName)

        vreg = ".*\<Case id.* name=\"(.*)\" action.*"
        vtext = open(vFileName).read()
        vCaseName = re.findall(vreg, vtext)

        if vCaseName:
            logger.debug("Case name found in file: " + ''.join(vCaseName[0]))
            return ''.join(vCaseName[0])
        else:
            logger.info("No case name found in the file")
            return "False"

    def readSoftwareName(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<attackProtocol>.*\[(.*)\].*</attackProtocol>|<attackProtocol>.*\[(.*)\].*"
        #vreg = "<attackProtocol>.*\[(.*)\]</attackProtocol>"
        vtext = open(vFileName).read()
        SoftwareName = re.findall(vreg, vtext)

        if SoftwareName:
            try:
                logger.debug("Found software name in the file: " + ''.join(SoftwareName))
                return ''.join(SoftwareName)
            except:
                return "False"
        else:
            logger.info("No Recommended Action found in the file")
            return "False"

    def readHostName(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<vulnerabilitySource>(.*)</vulnerabilitySource>"
        vtext = open(vFileName).read()
        HostName = re.findall(vreg, vtext)

        if HostName:
            logger.debug("Found host name in the file: " + ''.join(HostName))
            return ''.join(HostName)
        else:
            logger.info("No host name found in the file")
            return "False"

    def readASCaseId(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<displayId>(.*)</displayId>"
        vtext = open(vFileName).read()
        CaseId = re.findall(vreg, vtext)

        if CaseId:
            logger.debug("Found ArcSight case id in the file: " + ''.join(CaseId))
            return ''.join(CaseId)
        else:
            logger.info("No ArcSight case id found in the file")
            return "False"

    def readUserId(self, vFileName):
        import logging
        import re
        logger = logging.getLogger('serviceNowInterface')
        logger.info("Reading export file to process: " + vFileName)

        vreg = "<vulnerabilityData>(.*)</vulnerabilityData>"
        vtext = open(vFileName).read()
        UserId = re.findall(vreg, vtext)

        if UserId:
            logger.debug("Found user id in the file: " + ''.join(UserId))
            return ''.join(UserId)
        else:
            logger.info("No user id found in the file")
            return "False"

    def updateTemplate(self, vFileName, vIncNum):
        import logging
        import shutil
        varTemplateFolder = "/opt/arcsight/manager/archive/template/"
        varExportFolder = "/opt/arcsight/manager/archive/exports"
        logger = logging.getLogger('serviceNowInterface')
        try:
            shutil.move(vFileName, varTemplateFolder + vIncNum + ".xml")
        except Exception,e:
            logger.error("Error updating template file: " + str(e))
        logger.info("Updated template folder: " + varTemplateFolder + vIncNum + ".xml")

    def updateTemplateNewIncNum(self, vFileName, vIncNum):
        import logging
        import re
        varImportFolder = "/opt/arcsight/manager/archive/imports"
        logger = logging.getLogger('serviceNowInterface')
        vreg = "<plannedActions>(.*)</plannedActions>|(<plannedActions/>|<plannedActions />)"
        vtext = open(vFileName).read()
        logger.info("Updated file: " + vFileName + " with new ServiceNow Incident Number")
        open(vFileName, mode='w').writelines(re.sub(vreg, "<plannedActions>" + vIncNum + "</plannedActions>", vtext))

    def updateTemplateClosedReason(self, vFileName, vStatus):
        import logging
        import re
        varImportFolder = "/opt/arcsight/manager/archive/imports"
        logger = logging.getLogger('serviceNowInterface')
        vreg = "<sensitivity>(.*)</sensitivity>"
        vtext = open(vFileName).read()
        logger.info("Updated file: " + vFileName + " with new status: " + vStatus)
        open(vFileName, mode='w').writelines(re.sub(vreg, "<sensitivity>" + vStatus + "</sensitivity>", vtext))

    def updateTemplateIncStatus(self, vFileName, vStatus):
        import logging
        import re
        varImportFolder = "/opt/arcsight/manager/archive/imports"
        logger = logging.getLogger('serviceNowInterface')
        vreg = "<stage>(.*)</stage>"
        vtext = open(vFileName).read()
        logger.info("Updated file: " + vFileName + " with new status: " + vStatus)
        open(vFileName, mode='w').writelines(re.sub(vreg, "<stage>" + vStatus + "</stage>", vtext))
        if vStatus == "Closed":
            arcsightInterface.updateTemplateClosedReason(self, vFileName, "Resolved")

    def updateTemplateClosedNotes(self, vFileName, vStatus):
        import logging
        import re
        varImportFolder = "/opt/arcsight/manager/archive/imports"
        logger = logging.getLogger('serviceNowInterface')
        vreg = "<inspectionResults>(.*)</inspectionResults>|(<inspectionResults/>|<inspectionResults />)"
        vtext = open(vFileName).read()
        logger.info("Updated file: " + vFileName + " with new status: " + vStatus)
        open(vFileName, mode='w').writelines(re.sub(vreg, "<inspectionResults>" + vStatus + "</inspectionResults>", vtext))
        if vStatus == "Closed":
            arcsightInterface.updateTemplateClosedReason(self, vFileName, "Resolved")
 
    def updateESMNewIncNum(self, vFileName):
        import logging
        import shutil
        import datetime
        varImportFolder = "/opt/arcsight/manager/archive/imports/"
        logger = logging.getLogger('serviceNowInterface')
        today = datetime.datetime.today()
        try:
            shutil.copy(vFileName, varImportFolder + vFileName.rpartition("/")[2])
        except Exception, e:
            logger.error("Error updating ESM imports folder: " + str(e))
        logger.info("Wrote update file with incident number to: " + varImportFolder + vFileName.rpartition("\\")[2])

    def updateESMNew(self, vFileName, vcount):
        import logging
        import shutil
        import datetime
        varImportFolder = "/opt/arcsight/manager/archive/imports/"
        logger = logging.getLogger('serviceNowInterface')
        today = datetime.datetime.today()

        try:
            shutil.copy(vFileName, varImportFolder + vFileName.rpartition("/")[2])
        except Exception, e:
            logger.error("Error updating ESM imports folder: " + str(e))
        logger.info("Wrote update file with incident number to: " + varImportFolder + "ExternalEventTrackingData-" +today.strftime('%Y%m%d%H%M') + ".xml")

    def updateESMClosed(self, vFileName, vcount):
        import logging
        import shutil
        import datetime
        varImportFolder = "/opt/arcsight/manager/archive/imports/"
        logger = logging.getLogger('serviceNowInterface')
        today = datetime.datetime.today()

        try:
            shutil.copy(vFileName, varImportFolder + "ExternalEventTrackingData-" + today.strftime('%Y%m%d%H%M') + ".xml")
        except Exception, e:
            logger.error("Error updating ESM imports folder: " + str(e))
        logger.info("Wrote update file with incident number to: " + varImportFolder + "/ExternalEventTrackingData-" + vcount + today.strftime('%Y%m%d%H%M') + ".xml")

