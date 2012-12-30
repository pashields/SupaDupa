#!/usr/bin/env python

import sys
import json
import ObjCWriter
import argparse

def handleJsonString(jsonStr, lang, keymap):
    return jsonDictToClasses(json.loads(jsonStr), {}, lang, keymap)

def jsonDictToClasses(json, objColl, lang, keymap):
    writer = writerForLang(lang)
    for k,v in json.iteritems():
        if isinstance(v, dict):
            addClassFromJson(v, objColl, k, writer, keymap)
        else:
            print "Bad formatting: Top level should be a JSON object containing the classes to convert"
            sys.exit(1)
    return writer.writeClasses(objColl)

def addClassFromJson(json, objColl, className, writer, keymap):
    className = mapIfMatch(className, keymap)
    objColl[className] = {}
    for k,v in json.iteritems():
        k = mapIfMatch(k, keymap)
        if isinstance(v, dict):
            objColl[className][k] = unicode(k)
            addClassFromJson(v, objColl, k, keymap)
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

def mapIfMatch(key, keymap):
    if key in keymap:
        return keymap[key]
    return key

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert json structures into classes.")
    parser.add_argument("file", nargs=1, help="Path to the json file that you wish to base your class on. The top level structure should be a JSON object where each key is the name of a class you wish to generate and the corresponding value is an instance of that class.")
    parser.add_argument("output_lang", nargs=1, help="The output language that should be used. Current options are [objc].")
    parser.add_argument("--key_conversion_map", dest="keymap", default={}, help="A JSON object representing a mapping of key names. Use this to override key names at the language level. Example: {\"int\":\"anInt\"} will change an instances of \"int\" as a class or property name to \"anInt\".")
    args = vars(parser.parse_args())

    jsonFileName = args["file"][0]
    
    jsonFile = file(jsonFileName, 'r')
    jsonStr = jsonFile.read()

    lang = args["output_lang"][0]

    keymap = json.loads(args["keymap"])

    print handleJsonString(jsonStr, lang, keymap)
