__author__ = 'Vosteen'

class emailout():

    def __init__(self):
        a = "ok"

    def sendEmail(self, vuserIdorEmail, templatetype, incidentnum):
        import smtplib
        import logging
        import arcsightIOInterface
        from email.mime.text import MIMEText
        Files2Proc = arcsightIOInterface.arcsightInterface()


        logger = logging.getLogger('serviceNowInterface')
        emailInt = emailout()
        SMTPServerName = "localhost"
        vfrom = "DL-DARTAnalysis@Company1.com"
        varTemplateFolder = "/opt/arcsight/manager/archive/template/"

        if templatetype == "system":
            if incidentnum == "NOUSERORWORKSTATION":
                vCaseId = Files2Proc.readASCaseId(vuserIdorEmail)
                vsubject = "Attempt to Export ArcSight and Create SystemNow Ticket Failed"
                vbody = "There was a problem processing the ServiceNow incident for ArcSight CaseId: " + vCaseId + ".  \r\n \r\n The case was missing the workstation name or the the userid.  Please correct and re-export the case."
                vemail = vfrom
                msg = MIMEText(vbody)
            elif incidentnum == "MISSINGTEMPLATE":
                vCaseId = Files2Proc.readASCaseId(vuserIdorEmail)
                vsubject = "Attempt to Export ArcSight and Create SystemNow Ticket Failed"
                vbody = "There was a problem processing the ServiceNow incident for ArcSight CaseId: " + vCaseId + ".  \r\n \r\n The case was missing the template information in the Recommended Action field in the case.  Please correct and re-export the case."
                vemail = vfrom
                msg = MIMEText(vbody)
            elif incidentnum == "ERRORCREATINC":
                vCaseId = Files2Proc.readASCaseId(vuserIdorEmail)
                vsubject = "Attempt to Export ArcSight and Create SystemNow Ticket Failed"
                vbody = "There was a problem processing the ServiceNow incident for ArcSight CaseId: " + vCaseId + ".  \r\n \r\n Please review information in the case for any errors.  Please reference the error log for the ArcSight-ServiceNow Integration module for more information on the error."
                vemail = vfrom
                msg = MIMEText(vbody)
            elif incidentnum == "ClosedTicket":
                vCaseId = Files2Proc.readASCaseId(varTemplateFolder + vuserIdorEmail + ".xml")
                vsubject = "ServiceNow Ticket Associated to ArcSight Case has been Closed"
                vbody = "A ticket associated to ArcSight Case Id: " + vCaseId + " has been closed.  The service now incident number is: " + vuserIdorEmail + ".  The information logged in the ServiceNow resolution field is logged in the ArcSight Case.\r\n \r\n Please review information in the case for any errors."
                vemail = vfrom
                msg = MIMEText(vbody)
            elif incidentnum == "ClosedTicketCancelled":
                vCaseId = Files2Proc.readASCaseId(varTemplateFolder + vuserIdorEmail + ".xml")
                vsubject = "ServiceNow Ticket Associated to ArcSight Case has been Closed with a Cancelled Status"
                vbody = "A ticket associated to ArcSight Case Id: " + vCaseId + " has been closed with a Cancel Status.  The service now incident number is: " + vuserIdorEmail + ".  The information logged in the ServiceNow resolution field is logged in the ArcSight Case.\r\n \r\n Please review information in the case for any errors."
                vemail = vfrom
                msg = MIMEText(vbody)
            else:
                return "False"
        else:
            vemail=""
            if "@" in vuserIdorEmail:
                vemail = vuserIdorEmail
            elif vuserIdorEmail != "":
                vemail = vuserIdorEmail + "@Company1.com"

            # Pull Subject
            vsubject = emailInt.getTemplateInfo(templatetype, "subject") + incidentnum
            vbody = emailInt.getTemplateInfo(templatetype, "body")
            # msg = MIMEText()

            fp = open("/opt/arcsight/manager/archive/template/emailtemplates/" + templatetype + ".html", 'rb')
            msg = MIMEText(fp.read(), 'html')


        msg['Subject'] = vsubject
        msg['From'] = vfrom
        vemail = "duy.tran@Company1.com"
        msg['To'] = vemail
        try:
            s = smtplib.SMTP(SMTPServerName)
            s.sendmail(vfrom, [vemail], msg.as_string())
            s.quit()
        except:
            logger.error("Error sending out email.")
    def getTemplateInfo(self, templatetype, templateitem):
        if templatetype == "reimage":
            if templateitem == "subject":
                return "Ticket for Machine Reimage has been created for you - "
            elif templateitem == "body":
                return "Hello,\r\n \r\n By way of introduction, my name is Steven and I am member of Company1's Detection Analysis and Response Team.  Our role is to detect computer viruses, malware and other malicious activity on the Company1 network. \r\n \r\n Our team has identified malware on your system. A re-image of your system is required to rid the malware from your machine. \r\n \r\n A Help Desk ticket (listed above) has been created and routed to Field Support to coordinate your system re-image.  Please note, it is important for the reimage to take place in the timeliest manner possible. Prolonging the reimage places both your personal information and corporate data at risk.  Command-and-control botnet membership, credential theft, and fraud are the risks most commonly associated with malware. \r\n \r\nIf no action is taken, your system may be disconnected from the network. Thank you in advance for your prompt attention to this matter. \r\n \r\n Please let me know if you have any questions."
            else:
                return "False"
        elif templatetype == "scan":
            if templateitem == "subject":
                return "Ticket for Machine Scan has been created for you - "
            elif templateitem == "body":
                return "Hello, \r\n \r\n By way of introduction, my name is Steven and I am member of Company1's Detection Analysis and Response Team.  Our role is to detect computer viruses, malware, and other malicious activity on the Company1 network. \r\n \r\n Our team has identified your system as having connected to a site hosting malicious code that could have compromised your asset.  Due to the severity of this and that your system has connected to a potentially malicious site, a malware scan of your system is the ideal solution to this issue. \r\n \r\n To assist this process I have created the above ticket and routed to Enterprise Service Desk to coordinate with you for the scan of your system at your earliest availability.  It is important for the scan to take place in the timeliest manner possible.  Prolonging the scan places both your personal information and corporate data at risk.  If no action is taken, your system may be disconnected from the network.   Thank you in advance for your prompt attention to this matter. \r\n \r\n Please let me know if you have any questions."
            else:
                return "False"
        elif templatetype == "softwareremoval":
            if templateitem == "subject":
                return "Ticket for Software Removal has been created for you - "
            elif templateitem == "body":
                return "Hello,  \r\n \r\n By way of introduction, my name is Steven and I am member of Company1's Detection Analysis and Response Team.  Our role is to detect computer viruses, malware, unapproved software posing risk, and other malicious activity on the Company1 network.  \r\n \r\n Our team has identified that your system has downloaded unapproved software (please see the link to Company1 policy below).  The software will need to be removed and a malware scan of your system is required.  \r\n \r\n Please help us protect your information and the Company1 network by working with the desktop team to have your machine scanned in the timeliest manner possible.  Prolonging the scan places your personal information, customer data and Company1 proprietary data at risk. A ticket has been created on your behalf and routed to the Enterprise Service Desk to coordinate the removal of unapproved software and a malware scan of your system.   Unfortunately, if prompt action is not taken, your system may be disconnected from the network.   Thank you in advance for your attention to this matter.  \r\n \r\n Company1 Personal Computer Software Ownership and Usage Policy:  \r\n https://worknet.auth.wellpoint.com/resources/OT_Main/default/Intranet_Asset/PW_A061221.pdf  \r\n \r\n Please reference Section 3.2 Software Installation.  \r\n \r\n Please let me know if you have any questions."
            else:
                return "False"
        else:
            return "False"
