#!/bin/sh

wget --user=svcArcSight --password=[Company]@123 --no-check-certificate https://[Company]prod.service-now.com/incident.do\?CSV\&sysparm_query=subcategory=DART\^u_sub_statusANYTHING\^^assignment_group=563bbd7f0fce710039190bcce1050e02^ORassignment_group=c1eea8110f427100ee194b9ce1050e5c\^u_closed_dateRELATIVEGE@dayofweek@ago@2 -O incident_with_close_notes.csv -o wget.log
