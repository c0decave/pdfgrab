import googlesearch as gs
import urllib
from libs.libhelper import *

def get_random_agent():
    return (gs.get_random_user_agent())

def search_pdf(search, args):
    ''' the function where googlesearch from mario vilas
		is called
	'''

    search_stop = args.search_stop

    query = '%s filetype:pdf' % search
    # print(query)
    urls = []

    try:
        for url in gs.search(query, num=20, stop=search_stop, user_agent=gs.get_random_user_agent()):
            #print(url)
            urls.append(url)

    except urllib.error.HTTPError as e:
        print('Error: %s' % e)
        return -1


    return urls

