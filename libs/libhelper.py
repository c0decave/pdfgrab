import os
import sys
from Crypto.Hash import SHA256

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

    # find the name of the file
    name = pdf.split("/")
    a = len(name)
    name = name[a - 1]
    # print(name)

    return name

