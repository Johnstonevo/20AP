
"""
        <dir>
            <title>Subreddit title</title>
            <twitch>t/channel id</twitch>
        </dir>

        headers = {
    'Client-ID': '4sna7678i382czpacc0h7hrskoxvu3',
}

response = requests.get('https://api.twitch.tv/helix/users?client_id=4sna7678i382czpacc0h7hrskoxvu3?id=%s', headers=headers) % (url)

                response = requests.get('https://api.twitch.tv/helix/users?client_id=4sna7678i382czpacc0h7hrskoxvu3?id=%s', headers=headers) % (url)
                json.loads(response)
                twit_thumb = response.get('profile_image_url')

"""

import __builtin__
import base64,time
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
#from importlib import reload
import os

import sys

twitch_headers = {
    'Client-ID': '4sna7678i382czpacc0h7hrskoxvu3',
}


CACHE_TIME = 30 # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')


class TwiTch(Plugin):
    name = "twitch"
    priority = 200

    def process_item(self, item_xml):
        if "<twitch>" in item_xml:
            item = JenItem(item_xml)
            if "t/" in item.get("twitch", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "TwiTch",
                    'url': item.get("twitch", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
            }
                
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Overwatch Plugin Cache?"):
            koding.Remove_Table("twitch_com_plugin")

@route(mode='TwiTch', args=["url"])
def get_TwiTch(url):
        url = url.replace('t/', '') 
        twitch_url = 'https://api.twitch.tv/helix/users?id=%s' % (url)
        html = requests.get(twitch_url, headers=twitch_headers).content

        xml = fetch_from_db(url)
        if not xml:
            xml = ""
            try:
                xml += "<plugin>"\
                        "    <title>[B][COLORff6441a5]Live Twitch[/COLOR][/B]</title>"\
                        "    <link>plugin://plugin.video.twitch/?use_player=True&channel_id=%s&mode=play</link>"\
                        "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                        "    <summary></summary>"\
                        "</plugin>" % (url)
                xml += "<plugin>"\
                        "    <title>[B][COLORff6441a5]Twitch Past Broadcasts[/COLOR][/B]</title>"\
                        "    <link>plugin://plugin.video.twitch/?broadcast_type=highlight&amp;channel_id=%s&amp;game=None&amp;mode=channel_video_list</link>"\
                        "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                        "    <summary></summary>"\
                        "</plugin>" % (url)
                xml += "<plugin>"\
                        "    <title>[B][COLORff6441a5]Twitch Uploads[/COLOR][/B]</title>"\
                        "    <link>plugin://plugin.video.twitch/?broadcast_type=upload&amp;channel_id=%s&amp;game=None&amp;mode=channel_video_list</link>"\
                        "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                        "    <summary></summary>"\
                        "</plugin>" % (url)
                xml += "<plugin>"\
                        "    <title>[B][COLORff6441a5]Twitch Video Highlights[/COLOR][/B]</title>"\
                        "    <link>plugin://plugin.video.twitch/?broadcast_type=highlight&amp;channel_id=%s&amp;game=None&amp;mode=channel_video_list</link>"\
                        "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                        "    <summary></summary>"\
                        "</plugin>" % (url)
                xml += "<plugin>"\
                        "    <title>[B][COLORff6441a5]Twitch Collections[/COLOR][/B]</title>"\
                        "    <link>plugin://plugin.video.twitch/?channel_id=%s&amp;mode=collections</link>"\
                        "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                        "    <summary></summary>"\
                        "</plugin>" % (url)



            except:
                return


            save_to_db(xml, url)

        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())




def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "twitch_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("twitch_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    docuh_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("twitch_com_plugin", docuh_plugin_spec)
    match = koding.Get_From_Table(
        "twitch_com_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                result = base64.b64decode(match_item)
            except:
                return None
            return result
        else:
            return None
    else:
        return None


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = txt.replace("&quot;", "\"").replace("&amp;", "&")
    txt = txt.replace('&#8216;','\'').replace('&#8217;','\'').replace('&#038;','&').replace('&#8230;','....')
    txt = txt.strip()
    return txt


def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A')
    except:
        pass
    return unidecode(text)

