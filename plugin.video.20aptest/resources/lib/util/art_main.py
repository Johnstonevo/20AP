import requests
import random
import json
tmdbKey='aa28550e5a65f567fc512bd0290ce6fb'
def get_movie_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/movie/now_playing?api_key='+tmdbKey+'&language=en-GB&include_adult=false'
      url2='https://api.themoviedb.org/3/movie/top_rated?api_key='+tmdbKey+'&language=en-GB&&include_adult=false'
      x=requests.get(url,url2).json()
      
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

def get_tv_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/tv/on_the_air?api_key='+tmdbKey+'&language=en-GB'
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


def get_kids_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/tv?api_key=aa28550e5a65f567fc512bd0290ce6fb&certification_country=GB&certification.lte=PG&with_genres=16,10751'
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

      
def get_doc_backdrop():
      all_img=[]
      url='https://api.themoviedb.org/3/discover/movie?api_key='+tmdbKey+'&language=en-GB&with_genres=99&include_adult=false&include_video=false&page=1'
      url2='https://api.themoviedb.org/3/discover/movie?api_key='+tmdbKey+'&language=en-GB&with_genres=99&include_adult=false&include_video=false&page=2'
      x=requests.get(url,url2).json()
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
      
def get_anime_backdrop():
      import random
      all_img=[]
      url='https://api.themoviedb.org/3/keyword/210024/movies?api_key='+tmdbKey+'&language=en-GB&include_adult=false'
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
