
__author__ = 'Vosteen'
import xml.etree.ElementTree as ET
import sys, re, os
import time, datetime
import shutil

class arcsightXMLParser():
    def prepFile(self, vfilname):
        varBadTicketFolder = "/opt/arcsight/manager/archive/template/badxml/"
        varExportFolder = "/opt/arcsight/manager/archive/exports/"
        # from lxml import etree

        try:
            tree = ET.parse(vfilname)
        except:
            sys.exit("Could not open XML file")

        root = tree.getroot()


        # Search XML for header case list
        casehead = root.findall("./ArchiveCreationParameters/include/list/*")

        def pullCaseNotesInfo(caseid):
            casedetails = root.findall("./Case[@id='" + caseid + "']/hasNote/list/*")
            caselist = []
            for cases in casedetails:
                if caselist is not None:
                    caselist.append(cases.attrib['id'])
            return caselist

        if casehead is None:
            shutil.move(vfilname, varBadTicketFolder)
        numcases = 0

        for caselist in casehead:
            numcases = numcases + 1
            tree2update = ET.parse(vfilname)
            root2update = tree2update.getroot()
            cases = pullCaseNotesInfo(caselist.attrib['id'])
            if cases is not None:

                today = datetime.datetime.today()

                ntr = ET.Element('archive')
                ntr.set("buildTime", today.strftime('%m-%d-%Y_h:M:s'))
                ntr.set("buildVersion", "6.8.0.1896.0")
                ntr.set("createTime", today.strftime('%m-%d-%Y_h:M:s'))
                ntr0 = ET.SubElement(ntr, "ArchiveCreationParameters")
                ntr1 = ET.SubElement(ntr0, "action")
                ntr1.text = "insert"
                ntr2 = ET.SubElement(ntr0, "format")
                ntr2.text = "xml.external.case"
                ntr3 = ET.SubElement(ntr0, "include")
                ntr4 = ET.SubElement(ntr3, "list")
                ntr5 = ET.SubElement(ntr4, "ref")
                ntr5.set("id", caselist.attrib['id'])
                ntr5.set("type", caselist.attrib['type'])
                ntr5.set("uri", caselist.attrib['uri'])

                for elem in root2update.findall("./Case"):
                    if elem.attrib['id'] == caselist.attrib['id']:
                        ntr.append(elem)

                # for elem in root2update.findall("./Note"):
                #     if elem.attrib['id'] in cases:
                #         ntr.append(elem)

                ra = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \r\n<!DOCTYPE archive SYSTEM \"../../schema/xml/archive/arcsight-archive.dtd\"> \r\n" + ET.tostring(ntr)
                with open(varExportFolder + 'ExternalEventTrackingData-c' + caselist.attrib['id'] + '.xml', 'w') as f:
                    f.write(ra)

                # ra1 = etree.fromstring(ra)
                # ri = ET.ElementTree(ra1)  # ET.tostring(ntr)  # ET.ElementTree(ET.fromstring(ra))
                # ra1.write(varExportFolder + 'ExternalEventTrackingData-c' + caselist.attrib['id'] + '.xml', encoding='UTF-8', xml_declaration=True, doctype='<!DOCTYPE archive SYSTEM "../../schema/xml/archive/arcsight-archive.dtd">')

        os.remove(vfilname)
