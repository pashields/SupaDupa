import SupaDupa
from SupaDupa import SupaDupaConf
import unittest

class SupaDupaConfTest(unittest.TestCase):
    def setUp(self):
        self.conf = SupaDupaConf('objc', {'foo': 'bar'}, {'dicty': 'NSDictionary'}, 
                                 False, None)

    def testKeyMapping(self):
        self.assertEquals(self.conf.mapKey('bar'), 'bar')
        self.assertEquals(self.conf.mapKey('foo'), 'bar')

    def testClassOverride(self):
        self.assertEquals(self.conf.classOverrideForProp('NSDictionary'),
                          None)
        self.assertEquals(self.conf.classOverrideForProp('dicty'),
                          'NSDictionary')

class SupaDupaTest(unittest.TestCase):
    def setUp(self):
        self.conf = SupaDupaConf('objc', {'foo': 'bar', 'zip': 'ping'}, 
                                 {'dicty': 'NSDictionary', 'ping': 'OH NOES'}, 
                                 False, None)

    def testAddClassFromJsonBasic(self):
        basicJson = {'property': u'stringValue'}
        out = SupaDupa.addClassFromJson(basicJson, {}, 'className', self.conf)
        self.assertEquals(len(out), 1)
        classDescr = out['className']
        self.assertEquals(len(classDescr.properties), 1)
        self.assertEquals(classDescr.properties['property'], 'NSString')

    def testAddClassWithKeyMap(self):
        json = {u'foo': 1}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(out[u'x'].properties['bar'], 'NSNumber')
    
    def testAddClassWithFixedPropClass(self):
        json = {u'dicty': 1}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(out[u'x'].properties['dicty'], 'NSDictionary')
        json = {u'dicty': {u'foo', 'bar'}}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(len(out), 1)
        self.assertEquals(out[u'x'].properties['dicty'], 'NSDictionary')
        
    def testMixPropClassAndKeyMap(self):
        json = {u'zip': 1}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(out[u'x'].properties['ping'], 'OH NOES')

    def testNestedClass(self):
        json = {u'inner': {u'stringy': u'xxx'}}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(len(out), 2)
        self.assertEquals(out[u'x'].properties['inner'], 'inner')
        self.assertEquals(out[u'inner'].properties['stringy'], 'NSString')

    def testConvertName(self):
        self.assertEquals(SupaDupa.convertNameFromArray(u'Plans'), u'Plan')
        self.assertEquals(SupaDupa.convertNameFromArray(u'Plan'), u'Plan')

    def testArray(self):
        json = {u'inners': [{u'stringy': u'xxx'}]}
        out = SupaDupa.addClassFromJson(json, {}, u'x', self.conf)
        self.assertEquals(len(out), 2)
        self.assertEquals(out[u'x'].properties[u'inners'], 'NSArray')
        self.assertEquals(out[u'inner'].properties[u'stringy'], 'NSString')
