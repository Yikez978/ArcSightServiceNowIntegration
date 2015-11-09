#__author__ = 'Vosteen'
# serviceNowInterface.py = defines the Company1 Service Now Creation templates
# depending on the template, it creates an incident with the appropriate Title & Descriptions and assigns it to the rightful assignment group.
#


class serviceNowInterface():
    def __init__(self):
        r = None

    def getTemplateInfo(self, vattackProtocol, vTemplateField):
        import logging
        logger = logging.getLogger('serviceNowInterface')
        if vattackProtocol == "0":
        #if vattackProtocol == "machine scan":
            if vTemplateField == "title":
                return "Company1 Information Security Request - Please read full description below"
            elif vTemplateField == "description":
                return "System %s has been reaching out to malicious websites. Customer may not be aware of the issue. Please contact customer immediately to schedule a scan and removal of infection for this system using an approved malware removal tool. \r\n \r\nPlease take note of threats found and include in the closing comments. \r\n \r\n If this request is closed for any other reason than successful scan, please contact a member of the DART team via dl-dartanalysis. \r\n \r\n  This ticket has been created on behalf of the listed requester by the DART.  \r\n\r\n Company1 Information Security Team Detection Analysis Response ArcSight case %s"
            elif vTemplateField == "assignedgroup":
                return "Field Support Services"
            else:
                return "False"
        elif vattackProtocol == "1":
        #elif vattackProtocol == "machine reimage":
            if vTemplateField == "title":
                return "Company1 Information Security Request - Please read full description below"
            elif vTemplateField == "description":
                return "Machine %s has been discovered to be infected with malware and is actively attempting to connect to external addresses to receive instructions. Due to the level of infection, this machine will be re-imaged to minimize continued risk to Company1. Customer may not be aware of issue. Please contact customer immediately to schedule a re-image for this system. \r\n \r\n Please ship/deploy a loaner system at the earliest available to minimize impact to the Associate. \r\n \r\n If backing up data, complete both malware and AV scans with approved tools before the backup, restore only what is needed. Do not restore temporary files, executables downloaded and any installation outside approved. \r\n \r\n If this request is closed for any other reason than successful re-image, please contact a member of the DART team via dl-dartanalysis. \r\n \r\n This ticket has been created on behalf of the listed requester by the DART. \r\n \r\n Company1 Information Security Team Detection Analysis Response \r\n \r\n Detection Analysis Response Arcsight case %s"
            elif vTemplateField == "assignedgroup":
                return "ENTERPRISE_SERVICEDESK_ATS"
            else:
                return "False"
        elif vattackProtocol == "2":
        #elif vattackProtocol == "unauthorized file sharing software removal":
            if vTemplateField == "title":
                return "Company1 Information Security Request - Please read full description below"
            elif vTemplateField == "description":
                return "System %s was observed to have unauthorized software %s installed. This type of software is not authorized for installation on Company1 assets and could potentially be used for malicious purposes. Customer may not be aware of the issue. Please contact customer immediately to remove unauthorized software and scan for malware using an approved malware removal tool. \r\n \r\n Please take note of threats found and include in the closing comments. \r\n \r\n If this request is closed for any other reason than successful software removal and scan, please contact a member of the DART team via dl-dartanalysis. \r\n \r\n This ticket has been created on behalf of the listed requester by the DART. Company1 Information Security Team \r\n \r\n Detection Analysis Response \r\n \r\n ArcSight case %s"
            elif vTemplateField == "assignedgroup":
                return "ENTERPRISE_SERVICEDESK_ATS"
            else:
                return "False"
        elif vattackProtocol == "3":
        #elif vattackProtocol == "unauthorized software installed":
            if vTemplateField == "title":
                return "Company1 Information Security Request - Please read full description below"
            elif vTemplateField == "description":
                return "System %s was observed to have unauthorized software %s installed. This type of software is not authorized for installation on Company1 assets and could potentially be used for malicious purposes. Customer may not be aware of the issue. Please contact customer immediately to remove unauthorized software and scan for malware using an approved malware removal tool. \r\n \r\n Please take note of threats found and include in the closing comments. \r\n \r\n If this request is closed for any other reason than successful software removal and scan, please contact a member of the DART team via dl-dartanalysis. \r\n \r\n This ticket has been created on behalf of the listed requester by the DART. Company1 Information Security Team \r\n \r\n Detection Analysis Response \r\n \r\n ArcSight case %s"
            elif vTemplateField == "assignedgroup":
                return "ENTERPRISE_SERVICEDESK_ATS"
            else:
                return "False"
        else:
            return "False"

    def createSNOWIncident(self, params_dict):
        import datetime
        from SOAPpy import SOAPProxy

        # instance to send to
        instance = 'Company1prod'

        # username/password
        username = 'svcArcSight'
        password = 'Company1@123'


        # proxy - NOTE: ALWAYS use https://INSTANCE.service-now.com, not https://www.service-now.com/INSTANCE for web services URL from now on!
        proxy = 'https://%s:%s@%s.service-now.com/incident.do?SOAP' % (username, password, instance)
        namespace = 'http://www.service-now.com/'
        server = SOAPProxy(proxy, namespace)

        # uncomment these for LOTS of debugging output
        # server.config.dumpHeadersIn = 1
        # server.config.dumpHeadersOut = 1
        # server.config.dumpSOAPOut = 1
        # server.config.dumpSOAPIn = 1

        response = server.insert(impact=int(params_dict['impact']), urgency=int(params_dict['urgency']), priority=int(params_dict['priority']), category=params_dict['category'], u_current_location=params_dict['location'], caller_id=params_dict['user'], assignment_group=params_dict['assignment_group'], subcategory=params_dict['subcategory'], short_description=params_dict['short_description'], description=params_dict['description'], u_business_unit=params_dict['business_unit'])

        return response

    def createIncident(self, vfilename):
        import logging
        import datetime
        import arcsightIOInterface
        import re
        import sys
        import os
        import emailout

        return "INC123456"
        logger = logging.getLogger('serviceNowInterface')
        today = datetime.datetime.today()
        Files2Proc = arcsightIOInterface.arcsightInterface()
        vattackProtocol = Files2Proc.readAttackProtocol(vfilename)
        TempLU = serviceNowInterface()
        sysemail = emailout.emailout()

        logger.info("File Recommended Action (used for templates): " + vattackProtocol)
        vAssignedGroup = TempLU.getTemplateInfo(vattackProtocol, "assignedgroup")
        vDescription = TempLU.getTemplateInfo(vattackProtocol, "description")
        vTitle = TempLU.getTemplateInfo(vattackProtocol, "title")
        vUserId = Files2Proc.readUserId(vfilename)
        vWorkstationName = Files2Proc.readHostName(vfilename)
        vReadCaseName = Files2Proc.readCaseName(vfilename)

        # Checks if UserId and Workstation in the ArcSight case send notification email and stop incident creation process
        if vUserId == "False" or vWorkstationName == "False":
            vUserId = ""
            try:
                sysemail.sendEmail(vfilename, "system", "NOUSERORWORKSTATION")
                logger.error("No user id or workstation name present in the ArcSight case.  Workstation Name: " + vWorkstationName + ", User Name: " + vUserId)
            except:
                logger.error("****** Error sending out system notification email showing failure in ServiceNow Incident creation because of missing workstation or user information. ******")
            try:
                os.remove(vfilename)
            except:
                logger.error("Error removing ArcSight export file.")
            sys.exit("No user id or workstation name present in the ArcSight case.  Workstation Name: " + vWorkstationName + ", User Name: " + vUserId)

        # Checks if vattackProtocol (Template) in the ArcSight case is empty or incorrect, if it is send notification email and stop incident creation process
        if vDescription == "False":
            try:
                sysemail.sendEmail(vfilename, "system", "MISSINGTEMPLATE")
                logger.error("No user id or workstation name present in the ArcSight case.  Workstation Name: " + vWorkstationName + ", User Name: " + vUserId)
            except:
                logger.error("****** Error sending out system notification email showing failure in ServiceNow Incident creation because of missing template information. ******")
            try:
                os.remove(vfilename)
            except:
                logger.error("Error removing ArcSight export file.")
            sys.exit("No user id or workstation name present in the ArcSight case.  Workstation Name: " + vWorkstationName + ", User Name: " + vUserId)

        #Send email notification to user
        if vattackProtocol == "0":
            templateid = "scan"
        elif vattackProtocol == "1":
            templateid = "reimage"
        elif vattackProtocol == "2" or vattackProtocol == "3":
            templateid = "softwareremoval"
        else:
            templateid = "scan"

        vSoftwareName = Files2Proc.readSoftwareName(vfilename)
        vASCaseId = Files2Proc.readASCaseId(vfilename)

        logger.debug("Userid from file: " + vUserId)
        logger.debug("Workstation Name from file: " + vWorkstationName)
        logger.debug("Software Name from file: " + vSoftwareName)
        logger.debug("ArcSight Case ID from file: " + vASCaseId)
        logger.debug("Template ticket info, assigned group: " + vAssignedGroup)
        logger.debug("Template ticket info, title: " + vTitle)
        logger.info("Template found.  Assigned group: " + vAssignedGroup)

        if (vattackProtocol == "0" or vattackProtocol == "1") and vAssignedGroup != "False" and vAssignedGroup != "False" and vAssignedGroup != "False":
            vDescClean = vDescription % (vWorkstationName, vASCaseId)
            logger.info("Template ticket info, description: " + vDescClean)
        elif (vattackProtocol == "2" or vattackProtocol == "3") and vAssignedGroup != "False" and vAssignedGroup != "False" and vAssignedGroup != "False":
            logger.info("Template ticket info, description: " + vDescription % (vWorkstationName, vSoftwareName, vASCaseId))
            vDescClean = vDescription % (vWorkstationName, vSoftwareName, vASCaseId)
        else:
            logger.info("Something went wrong pulling all of the template fields: ")
            logger.info("Template ticket info, assigned group: " + vAssignedGroup)
            logger.info("Template ticket info, title: " + vTitle)

        values = {'impact': '3', 'urgency': '2', 'priority': '2', 'category': 'High', 'location': 'XX-UNKNOWN', 'user': vUserId, 'assignment_group': vAssignedGroup, 'subcategory': 'DART', 'short_description': vTitle, 'description': vDescClean + "\r\n \r\n" + vReadCaseName, 'business_unit': 'Corporate'}
        new_incident_sysid=TempLU.createSNOWIncident(values)
        logger.info("****** Incident Created: " + repr(new_incident_sysid) + " *****")
        vreg = "'number': '(.*)'"
        logger.info(''.join(re.findall(vreg, repr(new_incident_sysid))))
        try:
            INCNum =''.join(re.findall(vreg, repr(new_incident_sysid)))
        except:
            INCNum = "False"
            logger.info(repr(new_incident_sysid))
        sysemail.sendEmail(vUserId, templateid, INCNum)
        return INCNum