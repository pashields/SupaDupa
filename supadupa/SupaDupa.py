#!/usr/bin/env python

import sys
import json
import ObjCWriter
import argparse

def handleJsonString(jsonStr):
    return jsonDictToClasses(json.loads(jsonStr), {})

def jsonDictToClasses(json, objColl):
    for k,v in json.iteritems():
        if isinstance(v, dict):
            addClassFromJson(v, objColl, k)
        else:
            print "Bad formatting: Top level should be dictionary of classes"
    return ObjCWriter.writeClasses(objColl)

def addClassFromJson(json, objColl, className):
    objColl[className] = {}
    for k,v in json.iteritems():
        if isinstance(v, dict):
            objColl[className][k] = unicode(k)
            addClassFromJson(v, objColl, k)
        elif isinstance(v, list):
            objColl[className][k] = unicode(ObjCWriter.defaultClassTypes[str(list)])
        elif ObjCWriter.defaultClassTypes.has_key(str(type(v))):
            objColl[className][k] = unicode(ObjCWriter.defaultClassTypes[str(type(v))])
        else:
            raise Exception("Unknown class type: %s" % str(type(v)))
    return objColl

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert json structures into classes.")
    parser.add_argument("file", nargs=1)
    args = vars(parser.parse_args())

    jsonFileName = args["file"][0]
    
    jsonFile = file(jsonFileName, 'r')
    jsonStr = jsonFile.read()
    
    print handleJsonString(jsonStr)
