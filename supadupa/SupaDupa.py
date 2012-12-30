#!/usr/bin/env python

import sys
import json
import ObjCWriter
import argparse

def handleJsonString(jsonStr, conf):
    return jsonDictToClasses(json.loads(jsonStr), {}, conf)

def jsonDictToClasses(json, objColl, conf):
    writer = conf.getWriter()
    for k,v in json.iteritems():
        if isinstance(v, dict):
            addClassFromJson(v, objColl, k, conf)
        else:
            print "Bad formatting: Top level should be a JSON object containing the classes to convert"
            sys.exit(1)
    return writer.writeClasses(objColl)

def addClassFromJson(json, objColl, className, conf):
    className = conf.mapKey(className)
    writer = conf.getWriter()
    objColl[className] = {}
    for k,v in json.iteritems():
        k = conf.mapKey(k)
        if conf.classOverrideForProp(k) is not None:
            objColl[className][k] = unicode(conf.classOverrideForProp(k))
        elif isinstance(v, dict):
            objColl[className][k] = unicode(k)
            addClassFromJson(v, objColl, k, conf)
        elif isinstance(v, list):
            objColl[className][k] = unicode(writer.defaultClassTypes[str(list)])
        elif writer.defaultClassTypes.has_key(str(type(v))):
            objColl[className][k] = unicode(writer.defaultClassTypes[str(type(v))])
        else:
            raise Exception("Unknown class type: %s" % str(type(v)))
    return objColl

class SupaDupaConf:
    def __init__(self, lang, keymap, overrides):
        self.lang = lang
        self.keymap = keymap
        self.overrides = overrides
        self.writers = {"objc": ObjCWriter}

        if lang not in self.writers.keys():
            print "Unknown language: {}".format(lang)
            sys.exit(1)

    def mapKey(self, key):
        if key in self.keymap:
            return self.keymap[key]
        return key

    def classOverrideForProp(self, prop):
        if prop in self.overrides:
            return self.overrides[prop]
        return None

    def getWriter(self):
        return self.writers[self.lang]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Convert json structures into classes.")
    parser.add_argument("file", nargs=1, help="Path to the json file that you wish to base your class on. The top level structure should be a JSON object where each key is the name of a class you wish to generate and the corresponding value is an instance of that class.")
    parser.add_argument("output_lang", nargs=1, help="The output language that should be used. Current options are [objc].")
    parser.add_argument("-k", dest="keymap", default="{}", help="A JSON object representing a mapping of key names. Use this to override key names at the language level. Example: {\"int\":\"anInt\"} will change an instances of \"int\" as a class or property name to \"anInt\".")
    parser.add_argument("-p", dest="overrides", default="{}", help="A JSON object representing overrides for class type of certain properties. Use this to prevent the creation of undesired classes or to enforce the use of user classes created outside of the JSON.")
    args = vars(parser.parse_args())

    jsonFileName = args["file"][0]
    
    jsonFile = file(jsonFileName, 'r')
    jsonStr = jsonFile.read()

    conf = SupaDupaConf(args["output_lang"][0], json.loads(args["keymap"]),
                        json.loads(args["overrides"]))

    print handleJsonString(jsonStr, conf)
