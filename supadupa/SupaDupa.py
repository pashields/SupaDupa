#!/usr/bin/env python

import sys
import json
import ObjCWriter
import argparse

def handleJsonString(jsonStr, lang):
    return jsonDictToClasses(json.loads(jsonStr), {}, lang)

def jsonDictToClasses(json, objColl, lang):
    writer = writerForLang(lang)
    for k,v in json.iteritems():
        if isinstance(v, dict):
            addClassFromJson(v, objColl, k, writer)
        else:
            print "Bad formatting: Top level should be a JSON object containing the classes to convert"
            sys.exit(1)
    return writer.writeClasses(objColl)

def addClassFromJson(json, objColl, className, writer):
    objColl[className] = {}
    for k,v in json.iteritems():
        if isinstance(v, dict):
            objColl[className][k] = unicode(k)
            addClassFromJson(v, objColl, k)
        elif isinstance(v, list):
            objColl[className][k] = unicode(writer.defaultClassTypes[str(list)])
        elif writer.defaultClassTypes.has_key(str(type(v))):
            objColl[className][k] = unicode(writer.defaultClassTypes[str(type(v))])
        else:
            raise Exception("Unknown class type: %s" % str(type(v)))
    return objColl

def writerForLang(lang):
    if lang == "objc":
        return ObjCWriter
    else:
        print "Unknown language: {}".format(lang)
        sys.exit(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert json structures into classes.")
    parser.add_argument("file", nargs=1, help="Path to the json file that you wish to base your class on. The top level structure should be a JSON object where each key is the name of a class you wish to generate and the corresponding value is an instance of that class.")
    parser.add_argument("output_lang", nargs=1, help="The output language that should be used. Current options are [objc].")
    args = vars(parser.parse_args())

    jsonFileName = args["file"][0]
    
    jsonFile = file(jsonFileName, 'r')
    jsonStr = jsonFile.read()

    lang = args["output_lang"][0]

    print handleJsonString(jsonStr, lang)
