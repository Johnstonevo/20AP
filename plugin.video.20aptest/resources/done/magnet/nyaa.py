# -*- coding: utf-8 -*-
# created by Venom for Openscrapers

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    OpenScrapers Project
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['nyaa.si']
		self.base_link = 'https://nyaa.si'
		self.search_link = '/?f=0&c=0_0&q=%s'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url is None:
				return
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if url is None:
				return sources

			if debrid.status() is False:
				return sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
			hdlr2 = 'S%d - %d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

			query = '%s %s' % (title, hdlr)
			query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

			query2 = '%s %s' % (title, hdlr2)
			query2 = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query2)

			urls = []
			url = self.search_link % urllib.quote_plus(query)
			url = urlparse.urljoin(self.base_link, url)
			urls.append(url)
			url2 = self.search_link % urllib.quote_plus(query2)
			url2 = urlparse.urljoin(self.base_link, url2)
			urls.append(url2)

			for url in urls:
				try:
					r = client.request(url)
					if 'magnet' not in r:
						return sources
					links = zip(re.findall('href="(magnet:.+?)"', r, re.DOTALL), re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', r, re.DOTALL))

					for link in links:
						url = link[0].replace('&amp;', '&')
						url = url.split('&tr')[0]

						name = url.split('&dn=')[1]
						name = urllib.unquote_plus(name)

						# if name.startswith('www'):
							# try:
								# name = re.sub(r'www(.*?)\W{2,10}', '', name)
							# except:
								# name = name.split('-.', 1)[1].lstrip()

						if hdlr not in name and hdlr2 not in name:
							continue

						if source_utils.remove_lang(name):
							continue

						if hdlr in name:
							t = name.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and').replace('.US.', '.').replace('.us.', '.')

						if hdlr2 in name:
							t = name.split(hdlr2)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and').replace('.US.', '.').replace('.us.', '.')

						# if cleantitle.get(t) != cleantitle.get(title):
							# continue

						quality, info = source_utils.get_release_quality(name, url)

						try:
							size = link[1]
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except:
							dsize = 0
							pass

						info = ' | '.join(info)

						sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
												'info': info, 'direct': False, 'debridonly': True, 'size': dsize})

				except:
					source_utils.scraper_error('NYAA')
					return sources

			return sources

		except:
			source_utils.scraper_error('NYYAA')
			return sources


	def resolve(self, url):
		return url