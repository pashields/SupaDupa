defaultClassTypes = {
    str(unicode) : "NSString",
    str(list) : "NSArray",
    str(int) : "NSNumber",
    str(float) : "NSNumber",
    str(bool) : "NSNumber",
    str(None.__class__) : "id"
}

def writeClasses(classDict):
    classDict = dict([(key.capitalize(), val) for key, val in classDict.iteritems()])
    classes = []
    forwardDec = writeForwardDec(classDict.keys())
    for className, props in classDict.iteritems():
        classes.append(writeClass(className, [], props))
    return forwardDec + '\n\n' + '\n\n'.join(classes)
    
def writeForwardDec(classNames):
    return "@class " + ", ".join(classNames) + ";"
    
def writeClass(name, deps, props):
    return writeClassHeader(name, deps, props) + '\n' + writeClassImpl(name)
    
def writeClassHeader(name, deps, props):
    top = "@interface {} : NSObject".format(name)
    bottom = "@end"
    middle = []
    for propName, propType in props.iteritems():
        middle.append("@property(nonatomic,strong){} *{};".format(propType, propName))
    return '\n'.join([top, '\n'.join(middle), bottom])
    
def writeClassImpl(name):
    return "@implementation {}\n@end".format(name)
