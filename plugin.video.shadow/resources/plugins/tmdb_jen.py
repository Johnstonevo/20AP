from resources.modules import public
import logging
addDir3=public.addDir3

def run(url,lang,icon,fanart,plot,name):
    url=url.replace('movies','movie').replace('tv/today','tv/airing_today')
    
    id=''
    if 'year/movie' in url:
        url2='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%(lang,url.split('year/movie/')[1])
        mode=14
    elif 'company/movie/' in url:
        split_url = url.split("/")
        if len(split_url) == 3:
            
            split_url.append(1)
       
        company_id = split_url[-2]
        url2='https://api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&with_companies={0}&language={1}&sort_by=popularity.desc&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(company_id,lang)
        mode=14
    elif 'keyword' in url:
        split_url = url.split("/")
        if len(split_url) == 3:
            
            split_url.append(1)
        
        keyword_id = split_url[-2]
        media = split_url[-3]
        if media == "movie":
            s_type='movie'
        else:
            s_type='tv'
        
        url2='http://api.themoviedb.org/3/discover/%s?with_keywords=%s&api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(s_type,keyword_id,lang)
        mode=14
    elif 'collection/' in url:
        split_url = url.split("/")
        id = split_url[-1]
        url2='http://api.themoviedb.org/3/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(url,lang)
        mode=179
    elif 'network' in url:
        split_url = url.split("/")
        if len(split_url) == 3:
            
            split_url.append(1)
        
        network_id = split_url[-2]
        
        url2='https://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&with_networks={0}&language={1}&sort_by=popularity.desc&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(network_id,lang)
        mode=14
    elif 'genre' in url:
        split_url = url.split("/")
        if len(split_url) == 3:
            
            split_url.append(1)
       
        genre_id = split_url[-2]
        media = split_url[-3]
        if media == "movie":
            s_type='movie'
        else:
            s_type='tv'
        url2='http://api.themoviedb.org/3/discover/%s?api_key=34142515d9d23817496eeb4ff1d223d0&sort_by=popularity.desc&with_genres=%s&language=%s&page=1'%(s_type,genre_id,lang)
        mode=14
    elif 'list/' in url:
        id = url.split("/")[-1]
        url2='http://api.themoviedb.org/3/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(url,lang)
        mode=192
    elif 'people/popular' in url:
        url2='www'
        mode=72
    elif 'person' in url:
        split_url = url.split("/")
        url2 = split_url[-1]
        plot = split_url[-2]
        mode=73
    elif 'trailer/' in url:
        id = url.split("/")[-1]
        url2='movie'
        mode=25
        plot='play_now'
    elif 'search' in url:
        mode=5
        url2='www'
    else:
        url2='http://api.themoviedb.org/3/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=%s&page=1'%(url,lang)
        mode=14
    
    return addDir3(name,url2,mode,icon,fanart,plot,id=id)
    