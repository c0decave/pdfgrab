#!/usr/bin/env python3
#####################
# yay - old tool adjusted for python3, using googlesearch now
# and not some self crafted f00
#
# new features, new layout, new new :>
# by dash at the end of September 2019
# 
# TODO
# * add complete path in output as well as url where pdf came from
# -> if url not exist like -F mode, then the local path
# * clean up code
# * fine tune google search
# * add random timeout for new requests
# -> maybe not necessary, gs has it ...
# -> sort of necessary, on the other hand use proxychains man
# * uh oh some fancy c0l0rs
# * add thread support
# * add scrape mode, to search for pdfs at the website itself
# * add current error conditions to logfile
#
# Done
# * add url list to output
# * queues added, but no thread support yet
# * json file output
# * txt file output
# * outfilename hardcoded
# * add decryption routine
# * catch ssl exceptions
# * add random useragent for google and website pdf gathering
# * set option for certificate verification, default is true
# * catch conn refused connections
# * catch filename to long thingy

import os
import sys
import json
import queue
import urllib
import argparse
import requests

# remove somewhen ;)
from IPython import embed

from PyPDF2 import pdf
import PyPDF2
from Crypto.Hash import SHA256
from collections import deque

# googlesearch library
import googlesearch as gs

# some variables in regard of the tool itself
name 		= 'pdfgrab'
version 	= '0.4.4'
author		= 'dash'
date		= '2019'

# queues for processing
# this queue holds the URL locations of files to download
url_q = queue.Queue()
url_d = {}

# this queue holds the paths of files to analyse
pdf_q = queue.Queue()

# this is the analysis queue, keeping the data for further processing
ana_q = queue.Queue()

def create_sha256(hdata):
	''' introduced to create hashes of filenames, to have a uniqid
		of course hashes of the file itself will be the next topic
	'''
	hobject = SHA256.new(data=hdata.encode())
	return (hobject.hexdigest())

def process_queue_data(filename,data,queue_type):
	''' main function for processing gathered data
		i use this central function for it, so it is at *one* place
		and it is easy to change the data handling at a later step without
		deconstructing the who code
	'''
	ana_dict = {}
	url_dict = {}

	if queue_type=='doc_info':
		print('[v] Queue DocInfo Data %s' % (filename))
		name = find_name(filename)
		path = filename

		# create a hash over the file path
		# hm, removed for now
		#path_hash = create_sha256(path)

		# order data in dict for analyse queue
		ana_dict = {path : {'filename':name,'data':data}}
#		print(data)
#		print(ana_dict)

		# add the data to queue
		add_queue(ana_q,ana_dict)

	elif queue_type=='url':
		# prepare queue entry
		print('[v] Url Queue %s' % (data))
		url_dict = {'url':data,'filename':filename}
		sha256=create_sha256(data)
		url_d[sha256]=url_dict

		# add dict to queue
		add_queue(url_q,url_dict)

	else:
		print('[-] Sorry, unknown queue. DEBUG!')
		return False
	
	return True

def add_queue(tqueue, data):
	''' wrapper function for adding easy data to
		created queues. otherwise the functions will be scattered with
		endless queue commands ;)
	'''

	tqueue.put(data)
	#d=tqueue.get()
	#print(d)
	return True

def url_strip(url):
	url = url.rstrip("\n")
	url = url.rstrip("\r")
	return url

def get_random_agent():
	return (gs.get_random_user_agent())

def get_DocInfo(filename, filehandle):
	''' the easy way to extract metadata
		
		indirectObjects...
		there is an interesting situation, some pdfs seem to have the same information stored 
		in different places, or things are overwritten or whatever
		this sometimes results in an extract output with indirect objects ... this is ugly

		{'/Title': IndirectObject(111, 0), '/Producer': IndirectObject(112, 0), '/Creator': IndirectObject(113, 0), '/CreationDate': IndirectObject(114, 0), '/ModDate': IndirectObject(114, 0), '/Keywords': IndirectObject(115, 0), '/AAPL:Keywords': IndirectObject(116, 0)}

		normally getObject() is the method to use, to fix this, however this was not working in the particular case.
		this thing might even bring up some more nasty things, as a (probably weak) defense and workaround
		the pdfobject is not used anymore after this function, data is converted to strings...
		bad example:
	'''

	err_dict = {}
	real_extract = {}

	fh = filehandle

	try:
		extract = fh.documentInfo

	except pdf.utils.PdfReadError as e:
		print('Error: %s' % e)
		err_dict={'error':str(e)}
		return -1

	except PyPDF2.utils.PdfReadError as e:
		print('Error: %s' % e)
		err_dict={'error':str(e)}
		return -1

	finally:
		process_queue_data(filename,err_dict,'doc_info')

	print('-'*80)
	print('File: %s' % filename)
#	embed()
	# there are situations when documentinfo does not return anything
	# and extract is None
	if extract==None:
		err_dict={'error':'getDocumentInfo() returns None'}
		process_queue_data(filename,err_dict,'doc_info')
		return -1


	try:
		for k in extract.keys():
			key = str(k)
			value = str(extract[k])
			edata = '%s %s' % (key,value)
			print(edata)
			print
			real_extract[key]=value
		print('-'*80)

	except PyPDF2.utils.PdfReadError as e:
		print('Error: %s' % e)
		err_dict={'error':str(e)}
		process_queue_data(filename,err_dict,'doc_info')
		return -1


	process_queue_data(filename,real_extract,'doc_info')


def decrypt_empty_pdf(filename):
	''' this function simply tries to decrypt the pdf with the null password
		this does work, as long as no real password has been set
		if a complex password has been set -> john
	'''

	fr = pdf.PdfFileReader(open(filename,"rb"))
	try:
		fr.decrypt('')

	except NotImplementedError as e:
		#print('Error: %s' % (e))
		print('Error: File: %s encrypted. %s' % (filename,str(e)))
		return -1
	return fr
	

def check_encryption(filename):
	''' basic function to check if file is encrypted 
	'''

#	print(filename)
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
		status_code = req.status_code

	except requests.exceptions.SSLError as e:
		print('Error: %s' % e)
		return -1

	except:
		print('Error: Probably something wrong with remote server')
		return -1

	if status_code == 403:
		print('%s http/403 Forbidden' % (url))
		return -1

	#print(len(data))
	return data

def store_pdf(url,data,outdir):
	''' storing the downloaded pdf data 
	'''
	print('[v] store_pdf')
	name = find_name(url)

	# only allow stored file a name with 50 chars
	if len(name)>50:
		name = name[:49] + '.pdf'
	#print(len(name))

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
	search_pdf(search,args)
	#urls = search_pdf(search,args)


	# *if* we get an answer
	if url_q.empty()==False:
	#if urls != -1:
		# process through the list and get the pdfs
		while url_q.empty()==False:
			item=url_q.get()
			#print(item)
			url = item['url']
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
			#print(url)
			# parse out the name of the file in the url	
			filename=find_name(url)
			# add the file to queue
			process_queue_data(filename,url,'url')
			urls.append(url)
	
	except urllib.error.HTTPError as e:
		print('Error: %s' % e)
		return -1
	#return urls

def run(args):

	# outfile name
	if args.outfile:
		out_filename = args.outfile
	else:
		out_filename = 'pdfgrab_analysis'

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
		try:
			files = os.listdir(directory)
		except:
			print('Error')
			return False

		for f in files:
			# naive filter function, later usage of filemagic possible
			if f.find('.pdf')!=-1:
				fpath = '%s/%s' % (directory,f)
				_parse_pdf(fpath)

	else:
		print('[-] Dunno what to do, bro.')
	
	# move analysis dictionary in queue back to dictionary
	analysis_dict = {}
	while ana_q.empty()==False:
		item = ana_q.get()
		#print('item ', item)
		analysis_dict.update(item)
	
	# ana_q is empty now

	# create txt output
	sep = '-'*80 + '\n'
	txtout = "%s/%s.txt" % (outdir,out_filename)
	fwtxt = open(txtout,'w')
	#print(analysis_dict)
	for k in analysis_dict.keys():
		fwtxt.write(sep)
		fname = 'File: %s\n' % (analysis_dict[k]['filename'])
		ddata = analysis_dict[k]['data']
		fwtxt.write(fname)
		for kdata in ddata.keys():
			metatxt = '%s:%s\n' % (kdata,ddata[kdata])
			fwtxt.write(metatxt)
		fwtxt.write(sep)
	fwtxt.close()
	
	# create json output
	jsonout = "%s/%s.json" % (outdir,out_filename)
	fwjson = open(jsonout,'w')
	#for k in analysis_dict.keys():
		#print(analysis_dict[k])
	#	jdata = json.dumps(analysis_dict[k])

	#print(analysis_dict)
	jdata = json.dumps(analysis_dict)
	fwjson.write(jdata)
	fwjson.close()

	# create url savefile
	#print('url_d: ', url_d)
	jsonurlout = "%s/%s_url.json" % (outdir,out_filename)
	fwjson = open(jsonurlout,'w')
	jdata = json.dumps(url_d)
	fwjson.write(jdata)
	fwjson.close()


	txtout = "%s/%s_url.txt" % (outdir,out_filename)
	fwtxt = open(txtout,'w')
	for k in url_d.keys():
		ddata = url_d[k]
		metatxt = '%s:%s\n' % (ddata['url'], ddata['filename'])
		fwtxt.write(metatxt)
	fwtxt.close()

	return 42
	# This is the end my friend.

def main():
	parser_desc = "%s %s %s in %s" % (name,version,author,date)
	parser = argparse.ArgumentParser(prog = name, description=parser_desc)
	parser.add_argument('-O','--outdir',action='store',dest='outdir',required=False,help="define the outdirectory for downloaded files and analysis output",default='pdfgrab')
	parser.add_argument('-o','--outfile',action='store',dest='outfile',required=False,help="define file with analysis output, if no parameter given it is outdir/pdfgrab_analysis, please note outfile is *always* written to output directory so do not add the dir as extra path")
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
