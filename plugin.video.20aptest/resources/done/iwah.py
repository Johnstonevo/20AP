# coding: utf-8

############################################################

############### Credit To Gotham Scrapers ##################

############################################################

import requests,re,logging

import xbmc,xbmcaddon

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'

# =======================================================================================================================================
class source:
    domains = ['iwannawatch.is']
    name = 'wannawatch'
   

    def __init__(self):
        self.scraper = cfscrape.create_scraper() # self.scraper.get
        self.base_link = 'https://www.iwannawatch.is'
        self.search = '/wp-admin/admin-ajax.php?action=bunyad_live_search&query='

# =======================================================================================================================================

    
            
            search_id = clean_search(title.lower())
            start_url = '%s%s%s' %(self.base_link,self.search,search_id.replace(' ','+'))
            #print 'Start URL >>> '+start_url
            
            headers = {'User-Agent':User_Agent}
            OPEN = requests.get(start_url,headers=headers,timeout=10).content
            Regex = re.compile('<li>.+?<a href="(.+?)".+?title="(.+?)".+?<a href=.+?>(.+?)<',re.DOTALL).findall(OPEN)
            for item_url,name,release in Regex:
                name = checker.name_clean(name)
                release=release.split('(')[-1].split(')')[0]
                name=name.split('(')[0]
                #print 'Link >>> '+item_url
                #print 'Name >>> '+name
                #print 'Year >>> '+release
                if not year == release:
                    continue
                if clean_title(search_id).lower() == clean_title(name).lower():
                    #print 'Sent Movie To Source >>> ' + item_url + '\n'
                    self.get_source(item_url,title,year,'','',debrid)
            return self.sources2
      

# =======================================================================================================================================

    
    def get_source(self, item_url, title, year, season, episode, debrid):
       
            #debrid = True # REMOVE BEFORE USING SCRAPER IN KODI

            headers = {'User-Agent':User_Agent}
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            quality = re.compile('<div class="cf">.+?class="quality">(.+?)</td>',re.DOTALL).findall(OPEN)
            for quality in quality:
                check_quality = checker.check_quality(quality)

            headers = {'User-Agent':User_Agent}
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            Regex = re.compile('li class=.+?data-href="(.+?)"',re.DOTALL).findall(OPEN)
            for link in Regex:
                if 'http' not in link:
                    link = 'http:'+link
                if 'http' in link:					
                        if debrid is False:
                            host = link.split('//')[1].replace('www.','').split('.')[0].lower()
                            check_site = checker.check_site(host)
                            if 'Resolve' in check_site:
                                hostname = link.split('//')[1].replace('www.','').split('/')[0].split('.')[0].title()
                                self.sources2.append({'source': hostname,'language': 'en', 'quality': check_quality, 'scraper': self.name, 'url': link, 'direct': False, 'debridonly': False})
                                #print '%s | %s | %s | \n'%(link,check_quality,'Resolve')
                        elif debrid is True:
                            host = link.split('//')[1].replace('www.','').split('.')[0].lower()
                            check_site = checker.check_site(host)
                            if 'Resolve' in check_site:
                                hostname = link.split('//')[1].replace('www.','').split('/')[0].split('.')[0].title()
                                self.sources2.append({'source': hostname,'language': 'en', 'quality': check_quality, 'scraper': self.name, 'url': link, 'direct': False, 'debridonly': False})
                                #print '%s | %s | %s | \n'%(link,check_quality,'Resolve')
                            elif 'Debrid' in check_site:
                                hostname = link.split('//')[1].replace('www.','').split('/')[0].split('.')[0].title()
                                self.sources2.append({'source': hostname,'language': 'en', 'quality': check_quality, 'scraper': self.name, 'url': link, 'direct': False, 'debridonly': True})
                                #print '%s | %s | %s | \n'%(link,check_quality,'Debrid')
       

# =======================================================================================================================================

#Scraper15().scrape_movie('hell fest','2018','') # REMOVE BEFORE USING SCRAPER IN KODI