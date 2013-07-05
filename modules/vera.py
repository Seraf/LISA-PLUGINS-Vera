# -*- coding: UTF-8 -*-
import urllib, json, os, inspect
from pymongo import MongoClient
from lisa import configuration
import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='vera', localedir=path, languages=[configuration['lang']]).ugettext

class Vera:
    def __init__(self):
        self.configuration_lisa = configuration
        mongo = MongoClient(self.configuration_lisa['database']['server'],
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
                    return json.dumps({"plugin": "vera","method": "getTemperature",
                                       "body": _('temperature_show') % state['value']})