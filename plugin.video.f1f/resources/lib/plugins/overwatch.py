
"""
        <dir>
            <title>Subreddit title</title>
            <overwatch>r/subreddit</overwatch>
        </dir>

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
from resources.lib.modules import praw2
from datetime import datetime
#from importlib import reload
import os

import sys


CACHE_TIME = 10800 # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

reddit = praw2.Reddit(client_id='nza3RQ0hwoEOZA',
                     client_secret='v0nAe9D3PDm4F2tb4k7MriTJjgk',
                     user_agent='Watch Overwatch b /u/My-PiDiaries',
                     username='My-PiDiaries')

reg_items = ['vimeo','dailymotion','rutube','vid.ag','thevideobee','vidzi.tv','drive.google','streamable.com']
unreg_items = ['v.redd.it','myspace','nfb.ca','thevideobee','dotsub','en.musicplayon.com','vkontakte.ru','veehd.com','snagfilms','liveleak.com','imdb.com','disclose.tv','videoweed.es','putlocker','vid.ag','vice.com']
image_items = ['.png','.jpg','.gif']



class OverWatch(Plugin):
    name = "overwatch"
    priority = 200

    def process_item(self, item_xml):
        if "<overwatch>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "OverWatch",
                'url': item.get("overwatch", ""),
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
            result_item['fanart_smday'] = result_item["fanart"]
            return result_item

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Overwatch Plugin Cache?"):
            koding.Remove_Table("overwatch_com_plugin")

@route(mode='OverWatch', args=["url"])
def get_OverWatch(url):
    url = url.replace('r/', '') 
    xml = fetch_from_db(url)
    if any(x in url for x in image_items):
        xbmc.executebuiltin("ShowPicture(%s)" % url)
    elif not xml:
        xml = ""
        try:
            for submission in reddit.subreddit(url).new(limit=200):
                redd_flair = submission.link_flair_text
                redd_title = submission.title
                redd_url = submission.url
                redd_summary = submission.selftext
                redd_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%d-%m-%y')
                try:
                    if 'youtu' in redd_url:
                        if 'playlist' in redd_url:
                            video_id = redd_url.split("=")[-1]
                            redd_url = 'plugin://plugin.video.youtube/playlist/%s/' % video_id
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>Playlists are not working on some Kodi builds, sorry.\n %s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        elif 'attribution_link' in redd_url:
                            redd_url = redd_url.split("a=")[-1]
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        else:
                            redd_url = redd_url.replace("/m.",'')

                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                    
                    elif 'twitch' in redd_url:
                            redd_url = redd_url.replace("https://www.twitch.tv/videos/",'plugin://plugin.video.twitch/?video_id=').replace("https://clips.twitch.tv/",'plugin://plugin.video.twitch/?use_player=True&mode=play&amp;slug=')
                            xml += "<plugin>"\
                                "    <title>[COLORff6441a5]%s [/COLOR]| %s </title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                                "    <summary>Twitch \n%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</plugin>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                        


                    elif any(x in redd_url for x in reg_items):
                            xml += "<item>"\
                                "    <title>[COLORffffff00]%s [/COLOR]| %s</title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail></thumbnail>"\
                                "    <summary%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                    
                    elif any(x in redd_url for x in image_items):
                        xml += "<item>"\
                            "    <title>[COLORwhite]%s [/COLOR]| %s</title>"\
                            "    <reddit>%s</reddit>"\
                            "    <thumbnail>%s</thumbnail>"\
                            "    <summary%s \n\n %s</summary>"\
                            "    <fanart>%s</fanart>"\
                            "    <premiered>%s</premiered>"\
                            "</item>" % (redd_title,redd_date,redd_url,redd_url,redd_flair,redd_summary,redd_url,redd_date)
                    
                    else:
                        continue
                    
                except:
                    continue


            for submission in reddit.subreddit(url).hot(limit=200):
                redd_flair = submission.link_flair_text
                redd_title = submission.title
                redd_url = submission.url
                redd_summary = submission.selftext
                redd_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%d-%m-%y')
                try:
                    if 'youtu' in redd_url:
                        if 'playlist' in redd_url:
                            video_id = redd_url.split("=")[-1]
                            redd_url = 'plugin://plugin.video.youtube/playlist/%s/' % video_id
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>Playlists are not working on some Kodi builds, sorry.\n %s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        elif 'attribution_link' in redd_url:
                            redd_url = redd_url.split("a=")[-1]
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        else:
                            redd_url = redd_url.replace("/m.",'')

                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                    
                    elif 'twitch' in redd_url:
                            redd_url = redd_url.replace("https://www.twitch.tv/videos/",'plugin://plugin.video.twitch/?video_id=').replace("https://clips.twitch.tv/",'plugin://plugin.video.twitch/?use_player=True&mode=play&amp;slug=')
                            xml += "<plugin>"\
                                "    <title>[COLORff6441a5]%s [/COLOR]| %s </title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                                "    <summary>Twitch \n%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</plugin>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                        


                    elif any(x in redd_url for x in reg_items):
                            xml += "<item>"\
                                "    <title>[COLORffffff00]%s [/COLOR]| %s</title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail></thumbnail>"\
                                "    <summary%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                    
                    elif any(x in redd_url for x in image_items):
                        xml += "<item>"\
                            "    <title>[COLORwhite]%s [/COLOR]| %s</title>"\
                            "    <reddit>%s</reddit>"\
                            "    <thumbnail>%s</thumbnail>"\
                            "    <summary%s \n\n %s</summary>"\
                            "    <fanart>%s</fanart>"\
                            "    <premiered>%s</premiered>"\
                            "</item>" % (redd_title,redd_date,redd_url,redd_url,redd_flair,redd_summary,redd_url,redd_date)
                    
                    else:
                        continue
                    
                except:
                    continue

            for submission in reddit.subreddit(url).top(limit=200, time_filter='all'):
                try:
                    redd_flair = submission.link_flair_text
                    redd_title = submission.title
                    redd_url = submission.url
                    redd_summary = submission.selftext
                    redd_date = datetime.utcfromtimestamp(submission.created_utc).strftime('%d-%m-%y')              
                    if 'youtu' in redd_url:
                        if 'playlist' in redd_url:
                            video_id = redd_url.split("=")[-1]
                            redd_url = 'plugin://plugin.video.youtube/playlist/%s/' % video_id
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>Playlists are not working on some Kodi builds, sorry.\n %s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        elif 'attribution_link' in redd_url:
                            redd_url = redd_url.split("a=")[-1]
                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                        
                        else:
                            redd_url = redd_url.replace("/m.",'')

                            xml += "<item>"\
                                    "    <title>[COLORffff0000]%s[/COLOR]|  %s</title>"\
                                    "    <link>%s</link>"\
                                    "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.youtube/icon.png</thumbnail>"\
                                    "    <summary>%s\n%s</summary>"\
                                    "    <premiered>%s<premiered>"\
                                    "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_title,redd_date)
                    
                    elif 'twitch' in redd_url:
                            redd_url = redd_url.replace("https://www.twitch.tv/videos/",'plugin://plugin.video.twitch/?video_id=').replace("https://clips.twitch.tv/",'plugin://plugin.video.twitch/?use_player=True&mode=play&amp;slug=')
                            xml += "<plugin>"\
                                "    <title>[COLORff6441a5]%s [/COLOR]| %s </title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail>http://mirrors.kodi.tv/addons/leia/plugin.video.twitch/icon.png</thumbnail>"\
                                "    <summary>Twitch \n%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</plugin>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                        


                    elif any(x in redd_url for x in reg_items):
                            xml += "<item>"\
                                "    <title>[COLORffffff00]%s [/COLOR]| %s</title>"\
                                "    <link>%s</link>"\
                                "    <thumbnail></thumbnail>"\
                                "    <summary%s \n\n %s</summary>"\
                                "    <premiered>%s</premiered>"\
                                "</item>" % (redd_title,redd_date,redd_url,redd_flair,redd_summary,redd_date)
                    
                    elif any(x in redd_url for x in image_items):
                        xml += "<item>"\
                            "    <title>[COLORwhite]%s [/COLOR]| %s</title>"\
                            "    <reddit>%s</reddit>"\
                            "    <thumbnail>%s</thumbnail>"\
                            "    <summary%s \n\n %s</summary>"\
                            "    <fanart>%s</fanart>"\
                            "    <premiered>%s</premiered>"\
                            "</item>" % (redd_title,redd_date,redd_url,redd_url,redd_flair,redd_summary,redd_url,redd_date)
                    
                    else:
                        continue
                    
                except:
                    continue
        except:
            pass

        save_to_db(xml, url)


    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

    
          
def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "overwatch_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("overwatch_com_plugin",
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
    koding.Create_Table("overwatch_com_plugin", docuh_plugin_spec)
    match = koding.Get_From_Table(
        "overwatch_com_plugin", {"url": url})
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
