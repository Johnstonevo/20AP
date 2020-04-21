
import requests
import random
import json
import datetime
now = datetime.datetime.now()
tmdbKey='aa28550e5a65f567fc512bd0290ce6fb'
def get_Currently_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/47121?api_key='+tmdbKey+'&language=en'
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

def get_Finished_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/47119?api_key='+tmdbKey+'&language=en'
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

def get_Crime_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/4/list/97542?api_key='+tmdbKey+'&language=en'
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

def get_Popular_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/3/tv/popular?api_key='+tmdbKey+'&language=en'
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
 
 
def get_Running_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/tv/on_the_air?api_key='+tmdbKey+'&language=en'
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
 
 
def get_HOT_backdrop():
      all_img=[]
      url='http://api.themoviedb.org/3/trending/tv/week?api_key='+tmdbKey+'&language=en'
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


def get_New_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&language=en-GB&first_air_date_year='+str(now.year)+'&timezone=Europe%2fLondon&include_null_first_air_ates=false&language=en-GB'
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


