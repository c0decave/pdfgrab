#!/usr/bin/env python3
#####################
# yay - old tool adjusted for python3, using googlesearch now
# and not some self crafted f00
#
# new features, new layout, new new :>
# by dash at the end of September 2019
# 
# TODO
# * json file output
# * txt file output
# * complete analyse.txt and seperated
# * clean up code
# * do more testing
# * fine tune google search
# * add random timeout for new requests
# -> maybe not necessary, gs has it ...
# -> sort of necessary, on the other hand use proxychains man
# * uh oh some fancy c0l0rs
# * catch filename to long thingy
#
# Done
# * add decryption routine
# * catch ssl exceptions
# * add random useragent for google and website pdf gathering
# * set option for certificate verification, default is true
# * catch conn refused connections

import os
import sys
import argparse
import requests
import urllib

from IPython import embed

from PyPDF2 import pdf
import googlesearch as gs

name 		= 'pdfgrab'
version 	= '0.4'
author		= 'dash'
date		= '2019'

def url_strip(url):
	url = url.rstrip("\n")
	url = url.rstrip("\r")
	return url

def get_random_agent():
	return (gs.get_random_user_agent())

def get_DocInfo(filename, filehandle):
	''' the easy way to extract metadata
	'''

	fh = filehandle
	try:
		extract = fh.documentInfo
	except pdf.utils.PdfReadError as e:
		print('Error: %s' % e)
		return -1

	print('-'*80)
	print('File: %s' % filename)
	for k in extract.keys():
		edata = '%s %s' % (k,extract[k])
		print(edata)
		print
	print('-'*80)


def decrypt_empty_pdf(filename):

	fr = pdf.PdfFileReader(open(filename,"rb"))
	try:
		fr.decrypt('')
	except NotImplementedError as e:
		print('Error: %s' % (e))
		print('Only algorithm code 1 and 2 are supported')
		return -1
	return fr
	

def check_encryption(filename):
	''' basic function to check if file is encrypted 
	'''

	print(filename)
	try:
		fr = pdf.PdfFileReader(open(filename,"rb"))
	except pdf.utils.PdfReadError as e:
		print('Error: %s' % e)
		return -1

	if fr.getIsEncrypted()==True:
		print('[i] File encrypted %s' % filename)
		nfr = decrypt_empty_pdf(filename)
		if nfr != -1:
			get_DocInfo(filename,nfr)

	else:
		get_DocInfo(filename,fr)

	#fr.close()

	return True

def find_name(pdf):
	''' simply parses the urlencoded name and extracts the storage name
		i would not be surprised this naive approach can lead to fuckups
	'''

	#find the name of the file
	name = pdf.split("/")
	a = len(name)
	name = name[a-1]
	#print(name)

	return name

def make_directory(outdir):
	''' naive mkdir function '''
	try:
		os.mkdir(outdir)
	except:
		#print("[W] mkdir, some error, directory probably exists")
		pass

def download_pdf(url, args, header_data):
	''' downloading the pdfile for later analysis '''

	# check the remote tls certificate or not?
	cert_check = args.cert_check

	try:
		req = requests.get(url,headers=header_data,verify=cert_check)
		#req = requests.get(url,headers=header_data,verify=False)
		data = req.content
	except requests.exceptions.SSLError as e:
		print('Error: %s' % e)
		return -1
	except:
		print('Error: Probably something wrong with remote server')
		return -1

	#print(len(data))
	return data

def store_pdf(url,data,outdir):
	''' storing the downloaded pdf data 
	'''
	name = find_name(url)

	# only allow stored file a name with 50 chars
	name = name[:49] + '.pdf'
	print(len(name))
	save = "%s/%s" % (outdir,name)
	try:
		f = open(save,"wb")
	except OSError as e:
		print('Error: %s' % (e))
		return -1

	ret=f.write(data)
	print('[+] Written %d bytes for File: %s' % (ret,save))
	f.close()
	
	# return the savepath
	return save

def _parse_pdf(filename):
	''' the real parsing function '''

	ret = check_encryption(filename)
	return ret

def grab_url(url, args, outdir):
	''' function keeping all the steps for the user call of grabbing 
		just one pdf and analysing it
	'''
	header_data={'User-Agent':get_random_agent()}
	data = download_pdf(url,args, header_data)
	if data != -1:
		savepath = store_pdf(url, data, outdir)
		_parse_pdf(savepath)

	return

def seek_and_analyse(search,args,outdir):
	''' function for keeping all the steps of searching for pdfs and analysing
		them together
	'''
	# use the search function of googlesearch to get the results
	urls = search_pdf(search,args)


	# *if* we get an answer
	if urls != -1:
		# process through the list and get the pdfs
		for url in urls:
			grab_url(url,args,outdir)

def search_pdf(search, args):
	''' the function where googlesearch from mario vilas
		is called
	'''

	search_stop = args.search_stop

	query='%s filetype:pdf' % search
	#print(query)
	urls = []

	try:
		for url in gs.search(query,num=20,stop=search_stop,user_agent=gs.get_random_user_agent()):
			print(url)
			urls.append(url)
	
	except urllib.error.HTTPError as e:
		print('Error: %s' % e)
		return -1
	return urls

def run(args):

	# specify output directory
	outdir = args.outdir

	# create output directory
	make_directory(outdir)

	# lets see what the object is
	if args.url_single:
		url = args.url_single
		print('[+] Grabbing %s' % (url))
		grab_url(url, args,outdir)

	elif args.file_single:
		pdffile = args.file_single
		print('[+] Parsing %s' % (pdffile))
		_parse_pdf(pdffile)

	elif args.search:
		search = args.search
		#print(args)
		print('[+] Seek and de...erm...analysing %s' % (search))
		seek_and_analyse(search,args,outdir)
	
	elif args.files_dir:
		directory = args.files_dir
		print('[+] Analyse pdfs in directory %s' % (directory))
		files = os.listdir(directory)
		for f in files:
			fpath = '%s/%s' % (directory,f)
			_parse_pdf(fpath)

	else:
		print('[-] Dunno what to do, bro.')


	return 42
	# This is the end my friend.

def main():
	parser_desc = "%s %s %s in %s" % (name,version,author,date)
	parser = argparse.ArgumentParser(prog = name, description=parser_desc)
	parser.add_argument('-O','--outdir',action='store',dest='outdir',required=False,help="define the outdirectory for downloaded files and analysis output",default='pdfgrab')
#	parser.add_argument('-o','--outfile',action='store',dest='outfile',required=False,help="define file with analysis output in txt format",default='pdfgrab_analysis.txt')
	parser.add_argument('-u','--url',action='store',dest='url_single',required=False,help="grab pdf from specified url for analysis",default=None)
	#parser.add_argument('-U','--url-list',action='store',dest='urls_many',required=False,help="specify txt file with list of pdf urls to grab",default=None)
#########
	parser.add_argument('-f','--file',action='store',dest='file_single',required=False,help="specify local path of pdf for analysis",default=None)
	parser.add_argument('-F','--files-dir',action='store',dest='files_dir',required=False,help="specify local path of *directory* with pdf *files* for analysis",default=None)
	parser.add_argument('-s','--search',action='store',dest='search',required=False,help="specify domain or tld to scrape for pdf-files",default=None)
	parser.add_argument('-sn','--search-number',action='store',dest='search_stop',required=False,help="specify how many files are searched",default=10,type=int)
	parser.add_argument('-z','--disable-cert-check',action='store_false',dest='cert_check',required=False,help="if the target domain(s) run with old or bad certificates",default=True)

	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
