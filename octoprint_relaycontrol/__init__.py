# coding=utf-8
from __future__ import absolute_import

__author__ = "Martial Gourde <mgourde@gmail.com>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2020 Shawn Bruce - Released under terms of the AGPLv3 License"

__plugin_name__ = "Relay Control"

import octoprint.plugin
from octoprint.server import user_permission
import time
import subprocess
import threading
import os
from flask import make_response, jsonify
#from relayGPIO import relayGPIO



class RelaycontrolPlugin(octoprint.plugin.StartupPlugin,
                   	    octoprint.plugin.TemplatePlugin,
                   	    octoprint.plugin.AssetPlugin,
                   	    octoprint.plugin.SettingsPlugin,
                   	    octoprint.plugin.SimpleApiPlugin
                        ):
    def __init__(self):
        global relayGPIO
        self.NbRelays = 0
        self.LblR1 = ''
        self.DftR1 = True
        self.Cur1 = False
        self.PinR1 = 0
        self.LblR2 = ''
        self.DftR2 = False
        self.CurR2 = False
        self.PinR2 = 0
        self.LblR3 = ''
        self.DftR3 = False
        self.CurR3 = False
        self.PinR3 = 0
        self.LblR4 = ''
        self.DftR4 = False
        self.CurR4 = False
        self.PinR4 = 0
        self.LblR5 = ''
        self.DftR5 = False
        self.CurR5 = False
        self.PinR5 = 0
        self.LblR6 = ''
        self.DftR6 = False
        self.CurR6 = False
        self.PinR6 = 0
        self.LblR7 = ''
        self.DftR7 = False
        self.CurR7 = False
        self.PinR7 = 0
        self.LblR8 = ''
        self.DftR8 = False
        self.CurR8 = False
        self.PinR8 = 0

    def on_after_startup(self):
        self._logger.info("----= RelayControl: Starting..")    
        NbRelays = self._settings.get(["NbRelays"])
        LblR1 = self._settings.get(["LblR1"])
        DftR1 = self._settings.get_boolean(["DftR1"])
        CurR1 = self._settings.get_boolean(["CurR1"])
        PinR1 = self._settings.get_int(["PinR1"])
        LblR2 = self._settings.get(["LblR2"])
        DftR2 = self._settings.get_boolean(["DftR2"])
        CurR2 = self._settings.get_boolean(["CurR2"])
        PinR2 = self._settings.get_int(["PinR2"])
        LblR3 = self._settings.get(["LblR3"])
        DftR3 = self._settings.get_boolean(["DftR3"])
        CurR3 = self._settings.get_boolean(["CurR3"])
        PinR3 = self._settings.get_int(["PinR3"])
        LblR4 = self._settings.get(["LblR4"])
        DftR4 = self._settings.get_boolean(["DftR4"])
        CurR4 = self._settings.get_boolean(["CurR4"])
        PinR4 = self._settings.get_int(["PinR4"])
        LblR5 = self._settings.get(["LblR5"])
        DftR5 = self._settings.get_boolean(["DftR5"])
        CurR5 = self._settings.get_boolean(["CurR5"])
        PinR5 = self._settings.get_int(["PinR5"])
        LblR6 = self._settings.get(["LblR6"])
        DftR6 = self._settings.get_boolean(["DftR6"])
        CurR6 = self._settings.get_boolean(["CurR6"])
        PinR6 = self._settings.get_int(["PinR6"])
        LblR7 = self._settings.get(["LblR7"])
        DftR7 = self._settings.get_boolean(["DftR7"])
        CurR7 = self._settings.get_boolean(["CurR7"])
        PinR7 = self._settings.get_int(["PinR7"])
        LblR8 = self._settings.get(["LblR8"])
        DftR8 = self._settings.get_boolean(["DftR8"])
        CurR8 = self._settings.get_boolean(["CurR8"])
        PinR8 = self._settings.get_int(["PinR8"])
	
	
	##~~ SettingsPlugin mixin
     # put your plugin's default settings here
    def get_settings_defaults(self):
        return dict(
            NbRelays=6,LblR1="Relay 1",LblR2="Relay 2",LblR3="Relay 3",LblR4="Relay 4"
            ,LblR5="Relay 5",LblR6="Relay 6",LblR7="Relay 7",LblR8="Relay 8"
            ,DftR1=False,DftR2=False,DftR3=False,DftR4=False,DftR5=False,DftR6=False,DftR7=False,DftR8=False
            ,CurR1=False,CurR2=False,CurR3=False,CurR4=False,CurR5=False,CurR6=False,CurR7=False,CurR8=False
            ,PinR1=0,PinR2=0,PinR3=0,PinR4=0,PinR5=0,PinR6=0,PinR7=0,PinR8=0
        )

    def get_template_vars(self):
        return dict(
            NbRelays=self._settings.get(["NbRelays"])
            ,LblR1=self._settings.get(["LblR1"]),LblR2=self._settings.get(["LblR2"])
            ,LblR3=self._settings.get(["LblR3"]),LblR4=self._settings.get(["LblR4"])
            ,LblR5=self._settings.get(["LblR5"]),LblR6=self._settings.get(["LblR6"])
            ,LblR7=self._settings.get(["LblR7"]),LblR8=self._settings.get(["LblR8"])
            ,DftR1=self._settings.get_boolean(["DftR1"]),DftR2=self._settings.get_boolean(["DftR2"])
            ,DftR3=self._settings.get_boolean(["DftR3"]),DftR4=self._settings.get_boolean(["DftR4"])
            ,DftR5=self._settings.get_boolean(["DftR5"]),DftR6=self._settings.get_boolean(["DftR6"])
            ,DftR7=self._settings.get_boolean(["DftR7"]),DftR8=self._settings.get_boolean(["DftR8"])
            ,CurR1=self._settings.get_boolean(["CurR1"]),CurR2=self._settings.get_boolean(["CurR2"])
            ,CurR3=self._settings.get_boolean(["CurR3"]),CurR4=self._settings.get_boolean(["CurR4"])
            ,CurR5=self._settings.get_boolean(["CurR5"]),CurR6=self._settings.get_boolean(["CurR6"])
            ,CurR7=self._settings.get_boolean(["CurR7"]),CurR8=self._settings.get_boolean(["CurR8"])
            ,PinR1=self._settings.get_int(["PinR1"]),PinR2=self._settings.get_int(["PinR2"])
            ,PinR3=self._settings.get_int(["PinR3"]),PinR4=self._settings.get_int(["PinR4"])
            ,PinR5=self._settings.get_int(["PinR5"]),PinR6=self._settings.get_int(["PinR6"])
            ,PinR7=self._settings.get_int(["PinR7"]),PinR8=self._settings.get_int(["PinR8"])
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

	##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/relaycontrol.js"],
            css=["css/relaycontrol.css"],
            less=["less/relaycontrol.less"]
        )

	##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
        return dict(
                relaycontrol=dict(
                displayName="Relay Control Plugin",
                displayVersion=self._plugin_version,

				# version check: github repository
                type="github_release",
                user="mgourde",
                repo="OctoPrint-Relaycontrol",
                current=self._plugin_version,

				# update method: pip
                pip="https://github.com/mgourde/OctoPrint-Relaycontrol/archive/{target_version}.zip"
            )
        )


# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = RelaycontrolPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

