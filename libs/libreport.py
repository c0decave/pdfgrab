import os
import sys
import json
from json2html import * 
from libs.pdf_png import get_png_base64

def prepare_analysis_dict(ana_queue):
    '''params: ana_queue - queue with collected information
    '''
    # initiate analysis dictionary
    analysis_dict = {}

    # move analysis dictionary in queue back to dictionary
    while ana_queue.empty() == False:
        item = ana_queue.get()
        # print('item ', item)
        analysis_dict.update(item)

    # ana_q is empty now return the newly created dictionary
    return analysis_dict

def create_txt_report(analysis_dict, outdir, out_filename):
    ''' create a txt report in the output directory
    '''

    # draw seperator lines
    sep = '-' * 80 + '\n'

    # create output filepath
    txtout = "%s/%s.txt" % (outdir, out_filename)

    # open the file and return filedescriptor
    fwtxt = open(txtout, 'w')

    # get the keys of the dict
    for k in analysis_dict.keys():
        # write seperator
        fwtxt.write(sep)

        # build entry filename of the pdf
        fname = 'File: %s\n' % (analysis_dict[k]['filename'])

        # build data entry
        ddata = analysis_dict[k]['data']

        # write the filename
        fwtxt.write(fname)

        # write the metadata
        for kdata in ddata.keys():
            metatxt = '%s:%s\n' % (kdata, ddata[kdata])
            fwtxt.write(metatxt)

        # write seperator
        fwtxt.write(sep)

    # close the file
    fwtxt.close()

    return True

def create_json_report(analysis_dict, outdir, out_filename):
    ''' create a jsonfile report in the output directory
    '''

    # build json output name
    jsonout = "%s/%s.json" % (outdir, out_filename)

    # open up json output file
    fwjson = open(jsonout, 'w')

    # convert dictionary to json data
    jdata = json.dumps(analysis_dict)

    # write json data to file 
    fwjson.write(jdata)

    # close file
    fwjson.close()

    return True

def create_html_report(analysis_dict, outdir, out_filename):
    ''' create a html report from json file using json2html in the output directory
    '''

    # build up path for html output file
    htmlout = "%s/%s.html" % (outdir, out_filename)

    # open htmlout filedescriptor
    fwhtml = open(htmlout,'w')

    # some html stuff
    pdfpng=get_png_base64('supply/pdf_base64.png')
    html_style ='<style>.center { display: block; margin-left: auto;margin-right: auto;} table {border-collapse: collapse;} th, td { border: 1px solid black;text-align: left; }</style>\n'
    html_head = '<html><head><title>pdfgrab - {0} item/s</title>{1}</head>\n'.format(len(analysis_dict),html_style)
    html_pdf_png = '<p class="center"><img class="center" src="data:image/jpeg;base64,{0}"><br><center>pdfgrab - grab and analyse pdf files</center><br></p>'.format(pdfpng)
    html_body = '<body>{0}\n'.format(html_pdf_png)
    html_end = '\n<br><br><p align="center"><a href="https://github.com/c0decave/pdfgrab">pdfgrab</a> by <a href="https://twitter.com/User_to_Root">dash</a></p></body></html>\n'

    # some attributes
    attr = 'id="meta-data" class="table table-bordered table-hover", border=1, cellpadding=3 summary="Metadata"'

    # convert dictionary to json data
    # in this mode each finding gets its own table there are other possibilities
    # but now i go with this
    html_out = ''
    for k in analysis_dict.keys():
        trans = analysis_dict[k]
        jdata = json.dumps(trans)
        html = json2html.convert(json = jdata, table_attributes=attr)
        html_out = html_out + html + "\n"
        #html_out = html_out + "<p>" + html + "</p>\n"
    #jdata = json.dumps(analysis_dict)

    # create html
    #html = json2html.convert(json = jdata, table_attributes=attr)

    # write html
    fwhtml.write(html_head)
    fwhtml.write(html_body)
    fwhtml.write(html_out)
    fwhtml.write(html_end)

    # close html file
    fwhtml.close()
    
def create_url_json(url_d, outdir, out_filename):
    ''' create a json url file in output directory
    '''

    # create url savefile
    jsonurlout = "%s/%s_url.json" % (outdir, out_filename)

    # open up file for writting urls down
    fwjson = open(jsonurlout, 'w')

    # convert url dictionary to json
    jdata = json.dumps(url_d)

    # write json data to file
    fwjson.write(jdata)

    # close filedescriptor
    fwjson.close()

    return True

def create_url_txt(url_d, outdir, out_filename):
    ''' create a txt url file in output directory
    '''
    # build up txt out path
    txtout = "%s/%s_url.txt" % (outdir, out_filename)

    # open up our url txtfile
    fwtxt = open(txtout, 'w')

    # iterating through the keys of the url dictionary
    for k in url_d.keys():

        # get the entry
        ddata = url_d[k]

        # create meta data for saving
        metatxt = '%s:%s\n' % (ddata['url'], ddata['filename'])

        # write metadata to file
        fwtxt.write(metatxt)

    # close fd
    fwtxt.close()

    return True
