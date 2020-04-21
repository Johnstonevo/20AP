#!/usr/bin/env python
import xbmc, xbmcgui, xbmcaddon, os, sys, itertools, math, string
import xml.etree.ElementTree as et
from operator import itemgetter

__settings__    = xbmcaddon.Addon(id='script.service.kodimal')
__cwd__         = __settings__.getAddonInfo('path')
__icon__        = os.path.join(__cwd__, "icon.png")
__configFile__  = xbmc.translatePath('special://profile/addon_data/script.service.kodimal/config.xml')
__scriptname__  = "KodiMAL Setup"
__updaterFile__    = xbmc.translatePath( os.path.join(__cwd__, 'updater.py') )

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join(__cwd__, 'resources', 'lib' ) )
sys.path.append(BASE_RESOURCE_PATH)

import myanimelist, kodimal

class ListGenerator():
    def __init__(self):
        self.config = kodimal.XML()
        self.mal = kodimal.MAL()
        self.server = kodimal.server()
        self.output = kodimal.output()
        self.a = self.mal.a

    def int_to_roman(self, i):
        numeral_map = zip(
            (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
            ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
        )
        result = []
        for integer, numeral in numeral_map:
            count = int(i / integer)
            result.append(numeral * count)
            i -= integer * count
        return ''.join(result)

    def generateList(self, ret):
        """ Generates a list of elements to be mapped """
        returnList = self.config.parseConfig() #returns a list of elements
        item = sys.listitem
        self.a.init_session()
        csrf_redone = 0
        while(self.a.csrf_token == 0 and csrf_redone < 10):
            self.a.end_session()
            self.a.init_session()
            csrf_redone += 1

        label = item.getVideoInfoTag().getTitle().decode('utf-8').encode('ascii','ignore')
        self.output.log("Checking " + label, xbmc.LOGNOTICE)
        rewatch = int(item.getVideoInfoTag().getPlayCount()) - 1
        itemInfo = self.config.showInConfig(item.getVideoInfoTag().getDbId(),1)
        if(ret.iscanceled()):
            return False
        if itemInfo is False:
            if 'Animation' in item.getVideoInfoTag().getGenre() :
                searchResults = self.a.search(label)
            else:
                searchResults = {0:{'id':'%skip%', 'title':__settings__.getLocalizedString(402), 'episodes':0}}
            if (searchResults is False):
                searchResult = [{'id':'%skip%', 'title':__settings__.getLocalizedString(411), 'episodes':0}]
            else:
                searchResult = searchResults.values()
            if len(searchResult) != 0:
                #Time to play the "Let's guess which title is the episode we're looking for" game!
                #Step one: If we only have one result, that's probably it. Good for one-season no-ova cases.
                if len(searchResult) == 1:
                    searchResult = searchResult[0]
                else:
                    #First, super-easy mode: Shortest item is probably the one we're looking for.
                    titleSize = 10000000000
                    for result in searchResult:
                        if len(result['title']) < titleSize:
                            selectedResult = result
                            titleSize = len(result['title'])
                    searchResult = selectedResult
            else:
                searchResult = {'id':'%skip%', 'title':__settings__.getLocalizedString(400), 'episodes':0}
            self.output.log(u" ".join(("My guess:",searchResult['title'])).encode('utf-8'), xbmc.LOGNOTICE)
            MALRewatch = self.a.rewatch(searchResult['id'])
            if MALRewatch is False:
                offset = 'NaN'
            else:
                offset = max(0,MALRewatch - rewatch)
            returnList = self.config.add(str(item.getVideoInfoTag().getDbId()), str(1), label, str(searchResult['id']), searchResult['title'], searchResult['episodes'], str(offset))
        elif itemInfo.attrib['offset'] == 'NaN' and itemInfo.attrib['malID'] != '%skip%':
            MALRewatch = self.a.rewatch(itemInfo.attrib['malID'])
            self.output.log(MALRewatch, xbmc.LOGNOTICE)
            if MALRewatch is False:
                offset = 'NaN'
            else:
                offset = max(0,MALRewatch - rewatch)
            itemID = itemInfo.attrib['malID']
            itemTitle = itemInfo.attrib['malTitle']
            itemEpisodes = itemInfo.attrib['malEpisodes']
            self.config.remove(itemInfo)
            returnList = self.config.add(str(itemInfo.attrib['xbmcID']), str(season), label, str(itemID), itemTitle, itemEpisodes, str(offset))

        self.a.end_session()
        return returnList

    def generateFix(self, item, searchString=False):
        """ generates a list of results to fix a single mapping """
        self.a.init_session()
        rewatch = 'NaN'
        origOffset = item.get('offset')
        if origOffset != 'NaN':
            origMALR = self.a.rewatch(item.get('malID'))
            if origMALR != False:
                rewatch = int(origMALR) - int(origOffset)
        returnList = []
        if searchString is False or searchString == "":
            searchString = item.get('xbmcTitle')
            searchResults = self.a.search(searchString.encode('ascii','ignore'))
        else:
            searchResults = self.a.search(searchString.encode('ascii','ignore'))
        #check if searchResults is not false to prevent error
        if searchResults is not False:
            for result in searchResults.values():
                offset = 'NaN'
                if rewatch != 'NaN':
                    MALRewatch = self.a.rewatch(result['id'])
                    if MALRewatch is False:
                        self.output.log("NAN", xbmc.LOGNOTICE)
                        self.output.log(itemInfo.attrib['malID'], xbmc.LOGNOTICE)
                        self.output.log(self.a.csrf_token, xbmc.LOGNOTICE)
                        offset = 'NaN'
                    else:
                        offset = max(0,int(MALRewatch) - int(rewatch))
                returnList.append(et.Element('show', attrib={'xbmcID':item.get('xbmcID'), 'season':item.get('season'), 'xbmcTitle':item.get('xbmcTitle'), 'malID':str(result['id']), 'malTitle':result['title'], 'malEpisodes':str(result['episodes']), 'offset':str(offset)}))
            returnList.append(et.Element('show', attrib={'xbmcID':item.get('xbmcID'), 'xbmcTitle':item.get('xbmcTitle'), 'season':item.get('season'), 'malID':'%skip%', 'malTitle':__settings__.getLocalizedString(402), 'malEpisodes':"0", 'offset':"0"}))
            self.a.end_session()
            return returnList
        else:
            returnList.append(et.Element('show', attrib={'xbmcID':item.get('xbmcID'), 'xbmcTitle':item.get('xbmcTitle'), 'season':item.get('season'), 'malID':'%skip%', 'malTitle':__settings__.getLocalizedString(402), 'malEpisodes':"0", 'offset':"0"}))
            self.a.end_session()
            return returnList

    def generateSelection(self, mappings, fullList=True):
        """ Takes a list of elements and generates a readable list in the same order. """
        displayStrings = []
        if fullList == True:
            map2 = [x for x in mappings]
            for item in map2:
                if item.get('malTitle') == __settings__.getLocalizedString(402):
                    mappings.remove(item)
                    continue
                displayStrings.append(item.get('xbmcTitle') + " S" + str(item.get('season')) + " -> " + item.get('malTitle'))
            displayStrings.append(__settings__.getLocalizedString(401))
        else:
            for item in mappings:
                displayStrings.append(item.get('malTitle'))
            displayStrings.append(__settings__.getLocalizedString(403))
        return displayStrings


class MainDiag():
    def __init__(self):
        #Generate a progress dialog
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(__settings__.getLocalizedString(408))
        pDialog.update(0, __settings__.getLocalizedString(410))
        #Create the listgenerator
        lg = ListGenerator()
        if (lg.a != False and lg.a != -1): #If lg.a is False, then we can't login to MAL. Exit.
            pDialog.update(0, __settings__.getLocalizedString(404), __settings__.getLocalizedString(405))
            #Generate the XBMC to MAL list
            mappings = lg.generateList(pDialog)
            pDialog.close()
            #if mappings is false, then something went wrong in generateList. Exit.
            if mappings != False:
                mappings.reverse()
                selectedItem = 0
                doWrite = True
                #We're looping until the final selection is made - either "back" or the write command.
                while selectedItem != len(mappings):
                    #Create a new Dialog. Did not want to deal with creating a full window, although a virtual file list might be nice...
                    ListDialog = xbmcgui.Dialog()
                    #Make it a select dialog, and generate a list of strings we can use from the list we got earlier
                    selectedItem = ListDialog.select(__settings__.getLocalizedString(409), lg.generateSelection(mappings))
                    if (selectedItem != len(mappings) and selectedItem != -1): #-1 is back, last item is write
                        #Perform the MAL search for the XBMC title, and create a dialog of all the results.
                        possibleReplacements = lg.generateFix(mappings[selectedItem])
                        #if there's no possible replacement only offer manual search
                        if possibleReplacements is None:
                            while 1:
                                #If it's manual, keep looping until they select something or give up (none or back)
                                possibleReplacements = lg.generateFix(mappings[selectedItem], self.manualSearch())
                                newResult = ListDialog.select(__settings__.getLocalizedString(406) + " " + mappings[selectedItem].get('xbmcTitle'), lg.generateSelection(possibleReplacements, False))
                                if (newResult != len(possibleReplacements) and newResult != -1):
                                    mappings = lg.config.replace(mappings[selectedItem],len(mappings)-1-selectedItem,possibleReplacements[newResult])
                                    mappings.reverse()
                                    break
                                elif (newResult == -1):
                                        break
                        else:
                            newResult = ListDialog.select(__settings__.getLocalizedString(406) + " " + mappings[selectedItem].get('xbmcTitle'), lg.generateSelection(possibleReplacements, False))
                            if (newResult != len(possibleReplacements) and newResult != -1): #-1 is back, last item is manual
                                mappings = lg.config.replace(mappings[selectedItem],len(mappings)-1-selectedItem,possibleReplacements[newResult])
                                mappings.reverse()
                            elif (newResult != -1):
                                while 1:
                                    #If it's manual, keep looping until they select something or give up (none or back)
                                    possibleReplacements = lg.generateFix(mappings[selectedItem], self.manualSearch())
                                    newResult = ListDialog.select(__settings__.getLocalizedString(406) + " " + mappings[selectedItem].get('xbmcTitle'), lg.generateSelection(possibleReplacements, False))
                                    if (newResult != len(possibleReplacements) and newResult != -1):
                                        mappings = lg.config.replace(mappings[selectedItem],len(mappings)-1-selectedItem,possibleReplacements[newResult])
                                        mappings.reverse()
                                        break
                                    elif (newResult == -1):
                                            break
                    if(selectedItem == -1): #In this case, we backed out of the main select dialog
                        doWrite = False
                        break
                if doWrite: #Write the config file
                    pDialog.create(__settings__.getLocalizedString(413))
                    lg.config.writeConfig()
                    pDialog.close()
                xbmc.executebuiltin("XBMC.StopScript(" +  __updaterFile__ + ")")
                xbmc.executebuiltin("XBMC.RunScript(" +  __updaterFile__ + ", True)")#If the main script isn't running, run it now.
                lg.output.notify(__settings__.getLocalizedString(414))
        else:
            pDialog.close() #and we're done!


    def manualSearch(self):
        """ Creates a keyboard for a manual search """
        kb = xbmc.Keyboard()
        kb.setHeading(__settings__.getLocalizedString(412))
        kb.doModal()
        if (kb.isConfirmed()):
            return kb.getText()
        else:
            return False


w = MainDiag()
