# -*- coding: UTF-8 -*-
import urllib, json
from pymongo import MongoClient
from lisa import configuration

class Vera:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'], \
                            self.configuration_lisa['database']['port'])
        self.configuration = mongo.lisa.plugins.find_one({"name": "Vera"})

    def getTemperature(self, args):
        for device in self.configuration['configuration']['temperature']:
            url = "http://" + self.configuration['ip'] + ":" + self.configuration['port'] + \
                  "/data_request?id=status&output_format=json&DeviceNum=" + device['device_id']
            veraResponse = urllib.urlopen(url)
            states = json.load(veraResponse)['Device_Num_'+device['device_id']]['states']
        for state in states:
            for variable in device['variables']:
                if state['variable'] == variable['name']:
                    return json.dumps({"plugin": "vera","method": "getTemperature", \
                                       "body": u"Il fait "+state['value']+u" degrés"})