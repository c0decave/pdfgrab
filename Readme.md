# pdfgrab

## What is it?

This is a reborn tool, used during the epoche dinosaurs were traipsing the earth. 
Basically it analyses PDF files for Metadata. You can direct it to a file or directory with pdfs. 
You can show it the url of a pdf or use the integrated googlesearch (thanx to mario vilas) class
to search for pdfs at target site, download and analyse them

## What information can be gathered?

This depends on the software used to create the pdf. And if it has been cleaned. 
However, common are the following things:

* Producer
* Creator
* CreationDate
* ModificationDate
* Author
* Title
* Subject

and some more :)

## How does it work?

Every more complex filetype above .txt or alike uses metadata for convinience, customer support or only to spread it has been used.
There is a lot information about metadata in different sort of files like pictures, documents, videos, music online. This tool
focuses on pdf only. 
If you are new to that term have a look here:
https://en.wikipedia.org/wiki/Metadata

## Download

```
git clone https://github.com/c0decave/pdfgrab
cd pdfgrab
python3 pdfgrab.py -h
```

## Usage

Those are your options major options:
* grab pdf from url and analyse
* search site for pdfs via google, grab and analyse
* analyse a local pdf
* analyse a local directory with pdfs in it

### Single Url Mode

```
# ./pdfgrab.py -u https://www.kernel.org/doc/mirror/ols2004v2.pdf
```
Result:
```
[+] Grabbing https://www.kernel.org/doc/mirror/ols2004v2.pdf
[+] Written 3893173 bytes for File: pdfgrab/ols2004v2.pdf
[+] Opening pdfgrab/ols2004v2.pdf
--------------------------------------------------------------------------------
File: pdfgrab/ols2004v2.pdf
/Producer pdfTeX-0.14h
/Creator TeX
/CreationDate D:20040714015300
--------------------------------------------------------------------------------
```
### Single File Mode

```
# ./pdfgrab.py -f pdfgrab/ols2004v2.pdf 
```
Result:
```
[+] Parsing pdfgrab/ols2004v2.pdf
[+] Opening pdfgrab/ols2004v2.pdf
--------------------------------------------------------------------------------
File: pdfgrab/ols2004v2.pdf
/Producer pdfTeX-0.14h
/Creator TeX
/CreationDate D:20040714015300
--------------------------------------------------------------------------------
```

### Directory Mode

```
./pdfgrab.py -F pdfgrab/
```
Will analyse all pdf's in that directory


### Google Search Mode
```
# ./pdfgrab.py -s site:kernel.org
```
Result:
```
[+] Seek and analysing site:kernel.org
http://vger.kernel.org/lpc_bpf2018_talks/bpf_global_data_and_static_keys.pdf
http://vger.kernel.org/netconf2018_files/JiriPirko_netconf2018.pdf
http://vger.kernel.org/netconf2018_files/PaoloAbeni_netconf2018.pdf
http://vger.kernel.org/lpc_net2018_talks/LPC_XDP_Shirokov_paper_v1.pdf
http://vger.kernel.org/netconf2018_files/FlorianFainelli_netconf2018.pdf
http://vger.kernel.org/lpc_net2018_talks/tc_sw_paper.pdf
https://www.kernel.org/doc/mirror/ols2009.pdf
https://www.kernel.org/doc/mirror/ols2004v2.pdf
http://vger.kernel.org/lpc_net2018_talks/ktls_bpf.pdf
http://vger.kernel.org/lpc_net2018_talks/ktls_bpf_paper.pdf

[+] Written 211391 bytes for File: pdfgrab/bpf_global_data_and_static_keys.pdf
[+] Opening pdfgrab/bpf_global_data_and_static_keys.pdf
--------------------------------------------------------------------------------
File: pdfgrab/bpf_global_data_and_static_keys.pdf
/Author 
/Title 
/Subject 
/Creator LaTeX with Beamer class version 3.36
/Producer pdfTeX-1.40.17
/Keywords 
/CreationDate D:20181102231821+01'00'
/ModDate D:20181102231821+01'00'
/Trapped /False
/PTEX.Fullbanner This is pdfTeX, Version 3.14159265-2.6-1.40.17 (TeX Live 2016) kpathsea version 6.2.2
```

## TODO
* json file-output
* txt file-output
* catch conn refused connections
* ~~set option for certificate verification, default is true~~
* complete analyse.txt and seperated
* clean up code
* do more testing
* ~~add random useragent for google and website pdf gathering~~
* ~~add decryption routine~~
* ~~catch ssl exceptions~~



## Google

* Search: filetype:pdf site:com
* Results: 264.000.000

## Disclaimer

Have fun!
