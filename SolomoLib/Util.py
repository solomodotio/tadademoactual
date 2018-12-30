import os
from flask import request, current_app as app
from simple_salesforce import Salesforce

def load_configuration(fileName):
    fieldMap = {}
    fieldList = []
    fileName = app.config['FIELD_MAP_DIR']+fileName
    with open(fileName, "r") as config_data:
        for line in config_data:
            line = line.strip()
            if not line:  # line is blank
                continue
            if line.startswith("#"):  # comment line
                continue
            (key, val) = line.strip().split('=')
            fieldMap[key] = val
    return fieldMap

def salesforce_login():
    sf_object = Salesforce(
        username=app.config['SALESFORCE_USERNAME'],
        password=app.config['SALESFORCE_PASSWORD'],
        security_token=app.config['SALESFORCE_SECURITY_TOKEN'],
        sandbox=app.config['SALESFORCE_SANDBOX'])

    return sf_object

def solomo_login():
    sf_object = Salesforce(
        username=app.config['SOLOMO_SF_USERNAME'],
        password=app.config['SOLOMO_SF_PASSWORD'],
        security_token=app.config['SOLOMO_SF_SECURITY_TOKEN'],
        sandbox=app.config['SOLOMO_SF_SANDBOX'])

    return sf_object

def process_related(mapfile, data, lu, exid, objectmap):

    #objects holds the map of the nested collections to the sobjects in Salesforce
    objects = util.load_configuration(objectmap)

    #the mapfile is the name of the file holding the fields to be mapped
    fieldmap = util.load_configuration(mapfile)

    #dictionary and list that hold the nested collections
    sobject = {}
    sobjects = []

    """first, determine if there's a corresponding key value.  not all 
       nest collections have a key value, such as when there is only one
       text value"""
    if fieldmap is not None:
        #iterate through each record in the collection
        for record in data:
            if exid is not None:
                sobject[lu.split("\\:")[0]] = dict([(lu.split("\\:")[1], exid)])
                #sobject[lu] = exid
            for origfield in fieldmap.keys():
                sobject[fieldmap[origfield]] = record[origfield]

            sobjects.append(sobject)
            sobject = {}

    if len(fieldmap)==0:
        for record in data:
            if exid is not None:
                sobject[lu] = exid
            sobject['Name'] = record


    return sobjects
