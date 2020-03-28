
import requests
import random
import json
tmdbKey='aa28550e5a65f567fc512bd0290ce6fb'
def get_NetFlix_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=213&language=en'
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

def get_HBO_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=49&language=en'
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

def get_CBS_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=16&language=en'
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

def get_SyFy_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=77&language=en'
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
 
 
def get_CW_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=71&language=en'
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
 
 
def get_ABC_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=2&language=en'
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


def get_NBC_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=6&language=en'
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


def get_AMAZON_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=1024&language=enB'
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


def get_Hulu_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=453&language=en'
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


def get_Youtube_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key='+tmdbKey+'&with_networks=1436&language=en'
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


