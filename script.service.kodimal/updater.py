#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

import xbmc, xbmcgui, xbmcaddon, os, sys, itertools, math
import xml.etree.ElementTree as et
from operator import itemgetter

__settings__    = xbmcaddon.Addon(id='script.service.kodimal')
__cwd__         = __settings__.getAddonInfo('path')
__icon__        = os.path.join(__cwd__, "icon.png")
__configFile__  = xbmc.translatePath('special://profile/addon_data/script.service.kodimal/config.xml')
__scriptname__    = "KodiMAL"

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join(__cwd__, 'resources', 'lib' ) )
sys.path.append(BASE_RESOURCE_PATH)

import myanimelist, kodimal

class MAL():
    def __init__(self):
        self.config = kodimal.XML()
        self.server = kodimal.server()
        self.output = kodimal.output()

    def fullUpdate(self):
        """ Performs a full update of MAL listings """
        repeat = False
        a.init_session()
        csrf_redone = 0
        while(a.csrf_token is 0 and csrf_redone < 10):
            a.end_session()
            a.init_session()
            csrf_redone += 1
        self.output.notify(__settings__.getLocalizedString(300))
        showCount = 0;
        allanime = self.config.parseConfig()
        #Get current MAL list (dictionary of dictionaries)
        malList = a.list()
        if malList is False:
            self.output.notify(__settings__.getLocalizedString(202))
            return False
        malListIDs = malList.keys()
        tvshows = self.server.getXBMCshows()
        for tvshow in tvshows:
            for season in tvshow['seasons']:
                showUpdate = False
                if season is 0:
                    continue #Don't do "season 0"
                item = self.config.showInConfig(tvshow['tvshowid'], season)
                if item is False:
                    continue
                if item in allanime:
                    allanime.remove(item)
                malID = item.attrib['malID']
                offset = item.attrib['offset']
                if (malID == -1 or malID == '%skip%' or malID is False):
                    continue #move on...
                malID = int(malID)
                count = 0
                if season in tvshow['seasonwatched']:
                    count = tvshow['seasonwatched'][season]
                else:
                    count = 0
                epCount = 0
                if malID not in malListIDs:
                    mal.output.log("Trying to add plan", xbmc.LOGNOTICE)
                    if a.add({'anime_id':malID, 'status':6, 'episodes':0, 'rewatch':0}) is False:
                        self.output.notify(__settings__.getLocalizedString(202))
                        return False
                    repeat = True
                    continue #it takes a while for MAL to update animelist, so we'll wait a few seconds after finishing this run through and then run again
                if malList[malID]['episodes'] is not None:
                    epCount = int(malList[malID]['episodes'])
                else:
                    epCount = 0
                if malList[malID]['watched_episodes'] is not None:
                    malCount = int(malList[malID]['watched_episodes'])
                else:
                    malCount = 0
                mal.output.log(tvshow['name'] + " " + str(epCount) + " " + str(count), xbmc.LOGNOTICE)
                if offset == "NaN":
                    rewatch = a.rewatch(malID)
                    offset = rewatch - count
                    self.config.remove(item)
                    self.config.add(str(tvshow['tvshowid']), str(season), tvshow['name'], str(item.attrib['malID']), item.attrib['malTitle'], item.attrib['malEpisodes'], str(offset))
                else:
                    rewatch = int(offset) + int(tvshow['rewatch'][season])
                if malList[malID]['watched_status'] == u'completed' and rewatch != a.rewatch(malID) :
                    if a.rewatch(malID) > rewatch:
                        #if rewatch on MAL is higher than the calculated rewatch (user updated manually) update offset
                        MALRewatch = a.rewatch(malID)
                        if MALRewatch is False:
                            offset = 'NaN'
                        else:
                            offset = max(0,MALRewatch - int(tvshow['rewatch'][season]))
                        self.config.remove(item)
                        self.config.add(str(tvshow['tvshowid']), str(season), tvshow['name'], str(item.attrib['malID']), item.attrib['malTitle'], item.attrib['malEpisodes'], str(offset))
                        mal.output.log("trying to update to " + str(offset), xbmc.LOGNOTICE)
                        continue #just updated offset with current values, update would do nothing
                    mal.output.log("Trying to update rewatch count", xbmc.LOGNOTICE)
                    if a.update(malID, {'status':2, 'episodes':epCount, 'rewatch':rewatch}) is False:
                        self.output.notify(__settings__.getLocalizedString(202))
                        return False
                    showUpdate = True
                elif(malList[malID]['watched_status'] == u'watching' or malList[malID]['watched_status'] == u'plan to watch'):
                    if count == epCount and epCount != 0:
                        #XBMC Log can't handle unicode, need workaround
                        #self.output.log(malList[malID]['title'].encode('ascii','ignore') + " " + __settings__.getLocalizedString(302), xbmc.LOGNOTICE)
                        mal.output.log("Trying to update completed", xbmc.LOGNOTICE)
                        if a.update(malID, {'status':2, 'episodes':count, 'rewatch':rewatch}) is False:
                            self.output.notify(__settings__.getLocalizedString(202))
                            return False
                        showUpdate = True
                    elif (count != 0 and (epCount is 0 or epCount > count) and malCount < count):
                        #self.output.log(malList[malID]['title'].encode('ascii', 'ignore') + " " + __settings__.getLocalizedString(303) + " " + str(count), xbmc.LOGNOTICE)
                        mal.output.log("Trying to update watching", xbmc.LOGNOTICE)
                        if a.update(malID, {'status':1, 'episodes':count, 'rewatch':rewatch}) is False:
                            self.output.notify(__settings__.getLocalizedString(202))
                            return False
                        showUpdate = True
                if showUpdate == True:
                    showCount += 1
        for movie in allanime:
            showUpdate = False
            json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"VideoLibrary.GetMovieDetails","params":{"movieid":'+ str(movie.attrib['xbmcID']) + ', "properties":["playcount"] }, "id":0}')
            json_query = unicode(json_query, 'utf-8', errors='ignore')
            json_response = json.loads(json_query)
            if 'result' not in json_response:
                continue
            count = json_response['result']['moviedetails']['playcount']
            mal.output.log("Movie " + movie.attrib['malTitle'] + " watched " + str(count) + " times", xbmc.LOGNOTICE)
            malID = movie.attrib['malID']
            offset = movie.attrib['offset']
            if (malID == -1 or malID == '%skip%' or malID is False):
                continue #move on...
            malID = int(malID)
            if offset == "NaN":
                rewatch = int(a.rewatch(malID))
                offset = rewatch - (int(count) - 1)
                self.config.remove(movie)
                self.config.add(str(movie.attrib['xbmcID']), str(season), movie.attrib['xbmcTitle'], str(movie.attrib['malID']), movie.attrib['malTitle'], movie.attrib['malEpisodes'], str(offset))
            else:
                rewatch = int(offset) + int(count) - 1
            if malID not in malListIDs:
                if count == 0:
                    mal.output.log("Trying to add plan to watch " + movie.attrib['malTitle'], xbmc.LOGNOTICE)
                    if a.add({'anime_id':malID, 'status':6, 'episodes':0, 'rewatch':0}) is False:
                        self.output.notify(__settings__.getLocalizedString(202))
                        return False
                else:
                    mal.output.log("Trying to add completed " + movie.attrib['malTitle'], xbmc.LOGNOTICE)
                    if a.add({'anime_id':malID, 'status':2, 'episodes':1, 'rewatch':rewatch}) is False:
                        self.output.notify(__settings__.getLocalizedString(202))
                        return False
                showCount += 1
                continue
            if (count > 1 and rewatch != a.rewatch(malID)) or (count == 1 and malList[malID]['watched_status'] == u'plan to watch') :
                if a.rewatch(malID) > rewatch:
                    #if rewatch on MAL is higher than the calculated rewatch (user updated manually) update offset
                    MALRewatch = a.rewatch(malID)
                    if MALRewatch is False:
                        offset = 'NaN'
                    else:
                        offset = max(0,MALRewatch - (int(count) - 1))
                    self.config.remove(movie)
                    self.config.add(str(movie.attrib['xbmcID']), str(season), movie.attrib['xbmcTitle'], str(movie.attrib['malID']), movie.attrib['malTitle'], movie.attrib['malEpisodes'], str(offset))
                    mal.output.log("trying to update to " + str(offset), xbmc.LOGNOTICE)
                    continue #just updated offset with current values, update would do nothing
                mal.output.log("Trying to update rewatch count", xbmc.LOGNOTICE)
                if a.update(malID, {'status':2, 'episodes':1, 'rewatch':rewatch}) is False:
                    self.output.notify(__settings__.getLocalizedString(202))
                    return False
                showUpdate = True
            if showUpdate == True:
                showCount += 1
        a.end_session()
        self.config.writeConfig()
        self.output.notify(str(showCount) + " " + __settings__.getLocalizedString(301))
        if repeat:
            xbmc.sleep(10000)
            self.fullUpdate()


class XBMCPlayer( xbmc.Player ):
    def __init__(self, *args):
        xbmc.Player.__init__(self)
        self.wasVideo = False
        self.updating = False

    def onPlayBackEnded( self ):
        if self.wasVideo:
            xbmc.sleep(2000)
            if not self.isPlayingVideo() and not self.updating :
                self.updating = True
                mal = MAL()
                mal.fullUpdate()
                self.updating = False

    def onPlayBackStopped( self ):
        if self.wasVideo:
            if not self.updating :
                self.updating = True
                mal = MAL()
                mal.fullUpdate()
                self.updating = False

    def onPlayBackStarted( self ):
        self.wasVideo = False
        if self.isPlayingVideo():
            self.wasVideo = True

    def onPlayBackResumed( self ):
        self.wasVideo = False
        if self.isPlayingVideo():
            self.wasVideo = True

#class XBMCMonitor( xbmc.Monitor ):
#    def __init__(self, *args):
#        pass

#    def onDatabaseUpdated(self, database):
#        xbmc.log("### [%s] - %s" %(__scriptname__,"Database Updated, Updating..."), level=xbmc.LOGNOTICE)
#        mal = MAL()
#        mal.fullUpdate(__configFile__)

#Entry point
player = XBMCPlayer()
#monitor = XBMCMonitor()
mal = MAL()
o = kodimal.output()
if (len(sys.argv) > 1):
    callmal = kodimal.MAL()
else:
    callmal = kodimal.MAL()
a = callmal.a
mal.output.log("created a", xbmc.LOGNOTICE)
if (a == -1 or a is False):
    mal.output.log("fail", xbmc.LOGNOTICE)
    sys.exit(0)
else:
    while not xbmc.abortRequested:
        xbmc.sleep(100)
sys.exit(0)
