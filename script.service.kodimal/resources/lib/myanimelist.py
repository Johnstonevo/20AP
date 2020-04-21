# =============================================================================
# lib/myanimelist.py
# This module is made for the MAL API: http://myanimelist.net/api
#
# Copyright (c) 2009 Frank Smit (FSX) (created for http://mal-api.com/)
# License: GPL v3, see the COPYING file for details
#
# Modified 5/21/2012 by Spencer Julian
#          5/04/2014
#
# Reworked for the official API 01/06/2018 by Zvon
#
# =============================================================================

import requests
import xml.etree.ElementTree
import re

host = 'https://myanimelist.net/api/'
series_status = ['currently airing', 'finished airing', 'not yet aired']
my_status = ['watching', 'completed', 'on-hold', 'dropped', 'for some reason this position is skipped', 'plan to watch']

try:
    import json
except ImportError:
    import simplejson as json

class MAL():

    def __init__(self, auth):

        self.auth = auth
        self.user_id = 0

        self.anime = None
        self.manga = None

    def init_anime(self):
        self.verify_user()
        self.anime = Anime(self.auth, self.user_id)

    def init_manga(self):
        pass

    def verify_user(self):
        """Verify user details."""

        credentialsGet = 0
        parseError = True
        while parseError:
            if(credentialsGet > 10) :
                return False
            credentials = requests.get(host + 'account/verify_credentials.xml', auth=self.auth).text
            if credentials == 'Invalid credentials':
                return False
            try:
                e = xml.etree.ElementTree.fromstring(credentials.encode('ascii','ignore'))
                parseError = False
            except Exception:
                parseError = True
                credentialsGet += 1
        self.user_id = e.getchildren()[0].text
        return True

class Anime():

    def __init__(self, auth, id):

        self.auth = auth
        self.user_id = id
        self.session = None
        self.csrf_token = 0

    def init_session(self):
        self.session = requests.Session()
        self.session.head('https://myanimelist.net/animelist/' + self.auth[0] + '?status=2')
        base = self.session.get('https://myanimelist.net')
        self.csrf_token = re.search('csrf.*',str(base.text.encode('ascii','ignore')))
        if self.csrf_token :
            self.csrf_token = self.csrf_token.group()
            self.csrf_token = self.csrf_token.split(' ')[1]
            self.csrf_token = self.csrf_token.split('>')[0]
            self.csrf_token = self.csrf_token.split('\'')[1]
            self.csrf_token = re.match('[a-zA-Z0-9]*', self.csrf_token).group()
        else:
            self.csrf_token = 0
        if len(self.session.cookies.items()) > 1 :
            self.cookie = self.session.cookies.items()[0][0] + '=' + self.session.cookies.items()[0][1] + '; ' + self.session.cookies.items()[1][0] + '=' + self.session.cookies.items()[1][1]
        else:
            self.cookie = ""

    def end_session(self):
        self.session.close()
        self.csrf_token = 0

    def list(self):
        """Fetch/Download anime list from MAL."""

        response = requests.get("https://myanimelist.net/malappinfo.php?u=" + self.auth[0] + "&status=all&type=anime")
        if response.status_code != 200:
            return False
        e = xml.etree.ElementTree.fromstring(response.text.encode('ascii','ignore'))
        children = e.getchildren()
        # info goes into a dict for easier access
        data = {}

        for i in range(1, len(children)) :
            data[int(children[i].getchildren()[0].text)] = {
                'id':               int(children[i].getchildren()[0].text),
                'title':            children[i].getchildren()[1].text,
                'type':             children[i].getchildren()[3].text,             # TV, Movie, OVA, ONA, Special, Music
                'episodes':         int(children[i].getchildren()[4].text),
                'status':           series_status[int(children[i].getchildren()[5].text)-1],           # finished airing, currently airing, not yet aired
                'watched_status':   my_status[int(children[i].getchildren()[14].text)-1],   # watching, completed, on-hold, dropped, plan to watch
                'watched_episodes': int(children[i].getchildren()[10].text),
                'score':            int(children[i].getchildren()[13].text),
                'image':            children[i].getchildren()[8].text
                }

        return data

    def search(self, query):
        """Fetch/Download anime list from MAL."""

        response = requests.get(host + 'anime/search.xml?q=' + query, auth=self.auth)
        if response.status_code != 200:
            return False
        e = xml.etree.ElementTree.fromstring(response.text.encode('ascii','ignore'))
        children = e.getchildren()
        # info goes into a dict for easier access
        data = {}

        for child in children:
            data[int(child.getchildren()[0].text)] = {
                'id':               int(child.getchildren()[0].text),
                'title':            child.getchildren()[1].text,
                'type':             child.getchildren()[6].text,             # TV, Movie, OVA, ONA, Special, Music
                'episodes':         int(child.getchildren()[4].text),
                'status':           child.getchildren()[7].text,
                'members_score':    float(child.getchildren()[5].text),
                'image':            child.getchildren()[11].text
                }

        return data

    def add(self, params):
        """Add anime to list.  params = {anime_id, status, episodes, rewatch}."""

        xml = '<?xml version="1.0" encoding="UTF-8"?><entry><episode>' + str(params['episodes']) + '</episode><status>' + str(params['status']) + '</status><times_rewatched>' + str(params['rewatch']) + '</times_rewatched></entry>'
        response = requests.post(host + 'animelist/add/' + str(params['anime_id']) + '.xml', auth=self.auth, data={'data':xml}).status_code
        if response == 400 :
            return False
        return True

    def update(self, id, params):
        """Update anime in the list.  data = {status, episodes, rewatch}."""

        xml = '<?xml version="1.0" encoding="UTF-8"?><entry><episode>' + str(params['episodes']) + '</episode><status>' + str(params['status']) + '</status><times_rewatched>' + str(params['rewatch']) + '</times_rewatched></entry>'

        response = requests.post(host + 'animelist/update/' + str(id) + '.xml', auth=self.auth, data={'data':xml}).status_code
        if response == 400 :
            return False
        return True

    def delete(self, id):
        """Remove anime from the list."""

        response = requests.post(host + 'animelist/delete/' + str(id) + '.xml', auth=self.auth).status_code

        if response == 400 :
            return False
        return True

    def rewatch(self, id):
        if self.csrf_token == 0:
            return False
        response = self.session.post('https://myanimelist.net/includes/ajax-no-auth.inc.php?t=6',headers={'cookie':self.cookie},data={'color':'1','id':str(id),'memId':str(self.user_id),'type':'anime','csrf_token':self.csrf_token})
        rewatch = re.search('re-watched.*strong> times',str(response.text.encode('ascii','ignore')))
        if not rewatch:
            return 0
        rewatch = rewatch.group()
        rewatch = rewatch.split('strong')[1]
        rewatch = rewatch.split('>')[1]
        rewatch = rewatch.split('<')[0]
        rewatch = int(rewatch)
        return rewatch
