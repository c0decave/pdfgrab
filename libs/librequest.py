import os
import sys
import json
import socket
import requests

from libs.liblog import logger
from libs.libhelper import *
from libs.libgoogle import get_random_agent

def store_file(url, data, outdir):
    ''' storing the downloaded data to a file
        params: url     - is used to create the filename
                data    - the data of the file
                outdir  - to store in which directory
                returns: dict { "code":<code>, "data":<savepath>,"error":<error>} - the status code, the savepath, the errorcode
    '''

    logger.info('Store file {0}'.format(url))
    name = find_name(url)

    # only allow stored file a name with 50 chars
    if len(name) > 50:
        name = name[:49]

    # build up the save path
    save = "%s/%s" % (outdir, name)

    try:
        f = open(save, "wb")

    except OSError as e:
        logger.warning('store_file {0}'.format(e))
        # return ret_dict
        return {"code":False,"data":save,"error":e}

    # write the data and return the written bytes
    ret = f.write(data)

    # check if bytes are zero
    if ret == 0:
        logger.warning('Written {0} bytes for file: {1}'.format(ret,save))

    else:
        # log to info that bytes and file has been written
        logger.info('Written {0} bytes for file: {1}'.format(ret,save))

    # close file descriptor
    f.close()

    # return ret_dict
    return {"code":True,"data":save,"error":False}


def download_file(url, args, header_data):
    ''' downloading the file for later analysis 
        params: url         - the url
                args        - argparse args namespace
                header_data - pre-defined header data
        returns: ret_dict
    '''

    # check the remote tls certificate or not?
    cert_check = args.cert_check

    # run our try catch routine
    try:
        # request the url and save the response in req
        # give header data and set verify as delivered by args.cert_check
        req = requests.get(url, headers=header_data, verify=cert_check)

    except requests.exceptions.SSLError as e:
        logger.warning('download file {0}{1}'.format(url,e))

        # return retdict
        return {"code":False,"data":req,"error":e}

    except requests.exceptions.InvalidSchema as e:
        logger.warning('download file {0}{1}'.format(url,e))

        # return retdict
        return {"code":False,"data":False,"error":e}

    except socket.gaierror as e:
        logger.warning('download file, host not known {0} {1}'.format(url,e))
        return {"code":False,"data":False,"error":e}

    except:
        logger.warning('download file, something wrong with remote server? {0}'.format(url))
        # return retdict
        if not req in locals():
            req = False

        return {"code":False,"data":req,"error":True}

    #finally:
        # lets close the socket
        #req.close()

    # return retdict
    return {"code":True,"data":req,"error":False}

def grab_run(url, args, outdir):
    ''' function keeping all the steps for the user call of grabbing
	just one and analysing it
    '''
    header_data = {'User-Agent': get_random_agent()}
    rd_download = download_file(url, args, header_data)
    code_down = rd_download['code']

    # is code True download of file was successfull
    if code_down:
        rd_evaluate = evaluate_response(rd_download)
        code_eval = rd_evaluate['code']
        # if code is True, evaluation was also successful
        if code_eval:
            # get the content from the evaluate dictionary request
            content = rd_evaluate['data'].content

            # call store file 
            rd_store = store_file(url, content, outdir)

            # get the code
            code_store = rd_store['code']

            # get the savepath
            savepath = rd_store['data']

            # if code is True, storing of file was also successfull
            if code_store:
                return {"code":True,"data":savepath,"error":False}

    return {"code":False,"data":False,"error":True}

def evalute_content(ret_dict):
    pass

def evaluate_response(ret_dict):
    ''' this method comes usually after download_file,
        it will evaluate what has happened and if we even have some data to process
        or not
        params: data    - is the req object from the conducted request
        return: {}
        returns: dict { "code":<code>, "data":<savepath>,"error":<error>} - the status code, the savepath, the errorcode
        '''
    # extract data from ret_dict
    req = ret_dict['data']

    # get status code
    url = req.url
    status = req.status_code
    reason = req.reason

    # ahh everything is fine 
    if status == 200:
        logger.info('download file, {0} {1} {2}'.format(url,reason,status))
        return {"code":True,"data":req,"error":False}

    # nah something is not like it should be
    else:
        logger.warning('download file, {0} {1} {2}'.format(url,reason,status))
        return {"code":False,"data":req,"error":True}
