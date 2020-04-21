#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

import xbmc, xbmcgui, xbmcaddon
import os, sys, itertools, math
import xml.etree.ElementTree as et
from operator import itemgetter

__settings__    = xbmcaddon.Addon(id='script.service.kodimal')
__cwd__         = __settings__.getAddonInfo('path')
__icon__        = os.path.join(__cwd__, "icon.png")
__scriptname__  = "KodiMAL"
__configFile__  = xbmc.translatePath('special://profile/addon_data/script.service.kodimal/config.xml')
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join(__cwd__, 'resources', 'lib' ) )
sys.path.append(BASE_RESOURCE_PATH)

import myanimelist

class XML():
    def __init__(self, xmlFile=__configFile__):
        self.xmlFile = xmlFile
        self.tree = et.ElementTree()

    def parseConfig(self):
        """ Parses the configuration XML File, returns a list of XML Elements corresponding to the shows or an empty list"""
        try:
            self.tree.parse(self.xmlFile)
        except IOError:
            self.tree._setroot(et.Element('shows'))
            return []

        return self.tree.findall('show')

    def showInConfig(self, showid, season):
        """ Checks to see if a show is in the config file, based on show id and season, returns the appropriate mal id or false. """
        if self.tree.findall('show') == []:
            return False
        try:
            for item in self.tree.iterfind('show'):
                if (item.attrib['xbmcID'] == str(showid)) and (item.attrib['season'] == str(season)):
                    return item
        except:
            for item in self.tree.findall('show'):
                if (item.attrib['xbmcID'] == str(showid)) and (item.attrib['season'] == str(season)):
                    return item
        return False

    def replace(self, oldItem, location, item):
        """ Replaces the item with the given id with the given item, returns list of XML Elements """
        self.tree.getroot().remove(oldItem)
        self.tree.getroot().insert(location,item)
        return self.tree.findall('show')

    def add(self, showid, season, title, malid, maltitle, malepisodes, offset):
        """ Adds an item to the config file, returns a list of xml elements """
        et.SubElement(self.tree.getroot(), 'show', attrib={'malID':str(malid), 'malTitle':maltitle, 'malEpisodes':str(malepisodes), 'xbmcID':str(showid), 'season':str(season), 'xbmcTitle':title, 'offset':offset})
        return self.tree.findall('show')

    def remove(self, item):
        self.tree.getroot().remove(item)

    def writeConfig(self):
        """ Writes the configuration xml file."""
        o = output()
        o.log(__settings__.getLocalizedString(413), xbmc.LOGNOTICE)
        #Python 2.7
        try:
            self.tree.write(self.xmlFile, encoding="UTF-8", xml_declaration=True)
        except:
            self.tree.write(self.xmlFile, encoding="UTF-8")

class MAL():
    def __init__(self):
        self.mal = myanimelist.MAL((str(__settings__.getSetting("malUser")), str(__settings__.getSetting("malPass"))))
        self.mal.init_anime()
        self.a = self.mal.anime

class server():
    def __init__(self):
        pass

    def getXBMCshows(self):
        """ Gets all of the TV Shows from the XBMC library. Returns a list of shows if successful, empty list if not."""
        json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"VideoLibrary.GetEpisodes","params":{"properties":["tvshowid","season","showtitle","playcount"], "sort": {"method":"episode"} }, "id":0}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = json.loads(json_query)['result']

        gen_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"VideoLibrary.GetTVShows","params":{"properties":["genre"]}, "id":1}')
        gen_query = unicode(gen_query, 'utf-8', errors='ignore')
        gen_response = json.loads(gen_query)['result']['tvshows']
        genres = {}
        for genre in gen_response:
            genres[genre['tvshowid']] = genre['genre']

        if json_response.has_key('episodes'):
            json_response = json_response['episodes']
            tvshows = [list(group) for key,group in itertools.groupby(sorted(json_response,key=itemgetter('tvshowid')),key=itemgetter('tvshowid'))]

            tvshowdetails = []

            for tvshow in tvshows :
                seasons = [list(group) for key,group in itertools.groupby(sorted(tvshow, key=itemgetter('season')), key=itemgetter('season'))]
                tvshowdetail = {"name":tvshow[0]['showtitle'],"tvshowid":tvshow[0]['tvshowid'],"seasons":[],"seasonall":{},"total":len(tvshow),"watched":0,"seasonwatched":{}, "genre":genres[tvshow[0]['tvshowid']], "rewatch":{}}
                for season in seasons :
                    tvshowdetail['seasons'].append(season[0]['season'])
                    tvshowdetail['seasonall'][season[0]['season']] = len(season)
                    rewatch = season[0]['playcount']
                    for ep in season:
                        if ep['playcount'] < rewatch:
                            rewatch = ep['playcount']
                        if ep['playcount'] > 0:
                            tvshowdetail['watched'] += 1
                            if ep['season'] in tvshowdetail['seasonwatched']:
                                tvshowdetail['seasonwatched'][ep['season']] += 1
                            else:
                                tvshowdetail['seasonwatched'][ep['season']] = 1
                    if rewatch > 0:
                        rewatch -= 1
                    tvshowdetail['rewatch'][season[0]['season']] = rewatch
                tvshowdetails.append(tvshowdetail)
        else:
            tvshowdetails = []

        return tvshowdetails

class output():
    def __init__(self):
        pass

    def notify(self, notice):
        """ Sends a notification to XBMC """
        xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,notice,10,__icon__))

    def log(self, msg, loglevel):
        """ Logs into the xbmc.log file """
        if type(msg).__name__ == 'unicode':
            msg = msg.encode('utf-8')
        xbmc.log("### [%s] - %s" %(__scriptname__,msg), level=loglevel)
