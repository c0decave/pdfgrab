import googlesearch as gs
import urllib
from libs.libhelper import *

def get_random_agent():
    return (gs.get_random_user_agent())

def hits_google(search, args):
    ''' the function where googlesearch from mario vilas
		is called
	'''
    s = search.split(',')
    query = 'filetype:pdf'


    try:
        hits = gs.hits(query, domains=s,user_agent=gs.get_random_user_agent())

    except urllib.error.HTTPError as e:
        return False,e

    except urllib.error.URLError as e:
        return False,e

    except IndexError as e:
        return False,e

    return True,hits


def search_google(search, args):
    ''' the function where googlesearch from mario vilas
		is called
	'''

    s = search.split(',')
    search_stop = args.search_stop

    query = 'filetype:pdf'
    #query = 'site:%s filetype:pdf' % search
    # print(query)
    urls = []

    try:
        for url in gs.search(query, num=20, domains=s,stop=search_stop, user_agent=gs.get_random_user_agent()):
            #print(url)
            urls.append(url)

    except urllib.error.HTTPError as e:
        #print('Error: %s' % e)
        return False,e

    except urllib.error.URLError as e:
        return False,e


    return True,urls

