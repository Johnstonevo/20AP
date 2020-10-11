import requests
import random
import json
tmdbKey='aa28550e5a65f567fc512bd0290ce6fb'
def get_latest_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/movie/now_playing?api_key='+tmdbKey+'&language=en-GB&include_adult=false'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img

def get_modern_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/43994?api_key='+tmdbKey+'&language=en-GB'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img

def get_not_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/79502?api_key='+tmdbKey+'&language=en-GB'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img

def get_classics_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/47126?api_key='+tmdbKey+'&language=en-GB'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img


def get_popular_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/3/movie/popular?api_key='+tmdbKey+'&language=en-GB&sort_by=vote_average.desc'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img

def get_trending_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/3/trending/movie/week?api_key='+tmdbKey+'&language=en-GB'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan='https://image.tmdb.org/t/p/original'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan='https://image.tmdb.org/t/p/original'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img


