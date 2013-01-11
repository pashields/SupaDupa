#!/usr/bin/env python

import sys, os, json, argparse
import SupaDupaResult, ObjCWriter

def handleJsonString(jsonStr, conf):
    return jsonDictToClasses(json.loads(jsonStr), {}, conf)

def jsonDictToClasses(json, objColl, conf):
    for k,v in json.iteritems():
        if isinstance(v, dict):
            addClassFromJson(v, objColl, k, conf)
        else:
            print "Bad formatting: Top level should be a JSON object containing the classes to convert"
            sys.exit(1)
    return conf.getWriter(objColl).getResult()

def addClassFromJson(json, objColl, className, conf):
    className = conf.mapKey(className)
    objColl[className] = {}
    for k,v in json.iteritems():
        k = conf.mapKey(k)
        if conf.classOverrideForProp(k) is not None:
            objColl[className][k] = makeClassName(conf.classOverrideForProp(k))
        elif isinstance(v, dict):
            objColl[className][k] = makeClassName(k)
            addClassFromJson(v, objColl, k, conf)
        elif isinstance(v, list):
            objColl[className][k] = getClassNameFromWriter(list, conf)
            if len(v) > 0:
                addClassFromJson(v[0], objColl, convertNameFromArray(k), conf)
        elif conf.getWriteClass().defaultClassTypes.has_key(str(type(v))):
            objColl[className][k] = getClassNameFromWriter(type(v), conf)
        else:
            raise Exception("Class type '%s' not supported by language '%s'" % (str(type(v)), conf.lang))
    return objColl

def makeClassName(name):
    return unicode(name)

def getClassNameFromWriter(pythonClass, conf):
    return unicode(conf.getWriteClass().defaultClassTypes[str(pythonClass)])

def convertNameFromArray(name):
    if name[-1:] == u's':
        return name[:-1]
    else:
        return name

class SupaDupaConf:
    def __init__(self, lang, keymap, overrides, toFile, outputDir):
        self.lang = lang
        self.keymap = keymap
        self.overrides = overrides
        self.writers = {"objc": ObjCWriter}
        self.toFile = toFile
        self.outputDir = outputDir

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

    def getWriteClass(self):
        return self.writers[self.lang]

    def getWriter(self, classDict):
        writerClass = self.getWriteClass()
        return writerClass.Writer(classDict, conf.getOutputDir())

    def getOutputDir(self):
        if self.outputDir:
            return self.outputDir
        if self.toFile:
            return os.getcwd()
        return None

# Need to-file flag, output dir option, generated methods (and flag), interface for writers
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert json structures into classes.")
    parser.add_argument("file", nargs=1, 
                        help="Path to the json file that you wish to base your class on. The top level structure should be a JSON object where each key is the name of a class you wish to generate and the corresponding value is an instance of that class.")
    parser.add_argument("output_lang", nargs=1, 
                        help="The output language that should be used. Current options are [objc].")
    parser.add_argument("-k", "--keymap", dest="keymap", default="{}", 
                        help="A JSON object representing a mapping of key names. Use this to override key names at the language level. Example: {\"int\":\"anInt\"} will change an instances of \"int\" as a class or property name to \"anInt\".")
    parser.add_argument("-p", "--class-overrides", dest="overrides", default="{}", 
                        help="A JSON object representing overrides for class type of certain properties. Use this to prevent the creation of undesired classes or to enforce the use of user classes created outside of the JSON.")
    parser.add_argument("-f", "--to-files", dest="tofile", action="store_true", default=False, 
                        help="Pass this option to write the output classes to files.")
    parser.add_argument("-o", "--output-dir", dest="outputdir", default=None, 
                        help="Directory to write the output class files to. Only useful with '-f'. Defaults to the current working directory.")
    args = vars(parser.parse_args())

    jsonFileName = args["file"][0]    
    jsonFile = file(jsonFileName, 'r')
    jsonStr = jsonFile.read()

    conf = SupaDupaConf(args["output_lang"][0], json.loads(args["keymap"]),
                        json.loads(args["overrides"]), args["tofile"], 
                        args["outputdir"])

    supaDupaResult = handleJsonString(jsonStr, conf)
    jsonFile.close()

    if conf.getOutputDir():
        supaDupaResult.writeFiles(conf.getOutputDir())
    else:
        supaDupaResult.writeToStdOut()
