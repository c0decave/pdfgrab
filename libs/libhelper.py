import os
import sys
from Crypto.Hash import SHA256

def check_file_size(filename):
    ''' simply check if byte size is bigger than 0 bytes
    '''
    fstat = os.stat(filename)
    if fstat.st_size == 0:
        return False
    return True

def make_directory(outdir):
    ''' naive mkdir function '''
    try:
        os.mkdir(outdir)
    except:
        # print("[W] mkdir, some error, directory probably exists")
        pass

def url_strip(url):
    url = url.rstrip("\n")
    url = url.rstrip("\r")
    return url

def create_sha256(hdata):
    ''' introduced to create hashes of filenames, to have a uniqid
		of course hashes of the file itself will be the next topic
	'''
    hobject = SHA256.new(data=hdata.encode())
    return (hobject.hexdigest())

def find_name(pdf):
    ''' simply parses the urlencoded name and extracts the storage name
		i would not be surprised this naive approach can lead to fuckups
	'''

    name = ''
    # find the name of the file
    # 
    name_list = pdf.split("/")
    len_list = len(name)
    # ugly magic ;-)
    # what happens is, that files can also be behind urls like:
    # http://host/pdf/
    # so splitting up the url and always going with the last item after slash
    # can result in that case in an empty name, so we go another field in the list back
    # and use this as the name
    if name_list[len_list - 1] == '':
        name = name_list[len_list - 2]
    else:
        name = name_list[len_list - 1]

    return name

