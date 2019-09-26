#!/usr/bin/env python3
#####################
# yay - old tool adjusted for python3, using googlesearch now
# and not some self crafted f00
#
# new features, new layout, new new :>
# dash in end of September 2019
# 
#
# TODO
# * json output
# * txt output
# * catch conn refused connections
# * set option for certificate verification, default is false
# * complete analyse.txt and seperated
# * clean up code
# * do more testing
# * add random useragent for google and website pdf gathering
#
# Done
# * add decryption routine
# * catch ssl exceptions

import os
import sys
import argparse
import requests

from IPython import embed

from PyPDF2 import pdf
import googlesearch as gs

_name_ 		= 'pdfgrab'
_version_ 	= '0.3'
_author_	= 'dash'
_date_		= '2019'

def url_strip(url):
	url = url.rstrip("\n")
	url = url.rstrip("\r")
	return url


def get_DocInfo(filename, filehandle):

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

def download_pdf(url, header_data):
	''' downloading the pdfile for later analysis '''
	try:
		req = requests.get(url,headers=header_data,verify=True)
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
	''' storing the downloaded pdf data '''
	name = find_name(url)
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

	check_encryption(filename)
	return True

	print('[+] Opening %s' % filename)
	pdfile = open(filename,'rb')

	try:
		h = pdf.PdfFileReader(pdfile)
	except pdf.utils.PdfReadError as e:
		print('[-] Error: %s' % (e))
		return
	
	return pdfile


def parse_single_pdf(filename):
	''' single parse function '''
	return 123

def grab_url(url, outdir):
	''' function keeping all the steps for the user call of grabbing 
		just one pdf and analysing it
	'''
	data = download_pdf(url,None)
	if data != -1:
		savepath = store_pdf(url, data, outdir)
		_parse_pdf(savepath)

	return

def seek_and_analyse(search,sargs,outdir):
	''' function for keeping all the steps of searching for pdfs and analysing
		them together
	'''
	urls = search_pdf(search,sargs)
	for url in urls:
		grab_url(url,outdir)

def search_pdf(search, sargs):
	''' the function where googlesearch from mario vilas
		is called
	'''

	query='%s filetype:pdf' % search
	#print(query)
	urls = []
	for url in gs.search(query,num=20,stop=sargs):
		print(url)
		urls.append(url)
	
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
		grab_url(url, outdir)

	elif args.file_single:
		pdffile = args.file_single
		print('[+] Parsing %s' % (pdffile))
		_parse_pdf(pdffile)

	elif args.search:
		search = args.search
		sargs = args.search_stop
		#print(args)
		print('[+] Seek and de...erm...analysing %s' % (search))
		seek_and_analyse(search,sargs,outdir)
	
	elif args.files_dir:
		directory = args.files_dir
		print('[+] Analyse pdfs in directory %s' % (directory))
		files = os.listdir(directory)
		for f in files:
			fpath = '%s/%s' % (directory,f)
			_parse_pdf(fpath)


		

	else:
		print('[-] Dunno what to do, bro.')
	#logfile = "%s/%s.txt" % (out,out)
	#flog = open(logfile,"w")

def main():
	parser_desc = "%s %s %s" % (_name_,_version_,_author_)
	parser = argparse.ArgumentParser(prog = __name__, description=parser_desc)
	parser.add_argument('-o','--outdir',action='store',dest='outdir',required=False,help="define the outdirectory for downloaded files and analysis output",default='pdfgrab')
	parser.add_argument('-u','--url',action='store',dest='url_single',required=False,help="grab pdf from specified url for analysis",default=None)
	parser.add_argument('-f','--file',action='store',dest='file_single',required=False,help="specify local path of pdf for analysis",default=None)
	parser.add_argument('-F','--files-dir',action='store',dest='files_dir',required=False,help="specify local path of *directory* with pdf *files* for analysis",default=None)
	parser.add_argument('-s','--search',action='store',dest='search',required=False,help="specify domain or tld to scrape for pdf-files",default=None)
	parser.add_argument('-sn','--search-number',action='store',dest='search_stop',required=False,help="specify how many files are searched",default=10,type=int)

	args = parser.parse_args()
	run(args)

if __name__ == "__main__":
	main()
