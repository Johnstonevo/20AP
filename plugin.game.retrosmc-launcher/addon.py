"""
    Plugin for Launching programs
"""

# -*- coding: UTF-8 -*-
# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcaddon

# plugin constants
__plugin__ = "retrosmc-launcher"
__author__ = "jcnventura/mcobit"
__url__ = "https://retropie.org.uk"
__git_url__ = "https://github.com/Johnstonevo/retrosmc/"
__credits__ = "mcobit"
__version__ = "0.0.1"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id='plugin.game.retrosmc-launcher')

output=os.popen("/home/$USER/.kodi/addons/plugin.game.retrosmc-launcher/scripts/retropie.sh").read()
#dialog.ok("Starting RetroPie",output)
#print output
