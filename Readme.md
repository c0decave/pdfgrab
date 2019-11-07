# pdfgrab

* Version 0.4.9

## What is it?

This is a reborn tool, used during the epoche dinosaurs were traipsing the earth. 
Basically it analyses PDF files for Metadata. You can direct it to a file or directory with pdfs. 
You can show it the url of a pdf or use the integrated googlesearch (thanx to mario vilas class)
to search for pdfs at target site, download and analyse them.

## What is new in 0.4.9?

* exported reporting methods to libreport.py
* added optargs for disabling different report methods
* made the html report a bit more shiny
* added function for generating html report after analysis
* exported requests and storing data to new library
* code fixes and more clear error handling
* removed necessary site: parameter at search flag -s
* updated readme
* -s flag now acceppts several domains
* console logging more clean

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

## What is this for anyways?

Well, this can be used for a range of things. However, i will only focus on the 
security part of it. Depending on your target you will get information about:

* used software in company xyz
	* possible version numbers
		* this will help you to identify existing vulnerabilities
	* sometimes pdfs are rendered new, for instance on uploads
		* now you can figure what the rendering engine is and find bugs in it
* who is the author of documents
	* sometimes usernames are users of the OS itself
		* congrats you just found by analysing a pdf an existing username in the domain
		* combine the information with the first part, you know which user uses which software
* passwords ... do i need to say more?

## Is it failproof?

Not at all. Please note that metadata as every other data is just written to that file. So it can be changed before it is uploaded. Said that, the amount of companies really changing that sort of data is maybe at 20%. Also you will recognize if it is empty or alike.

## How does it work?

Every more complex filetype above .txt or alike uses metadata for convinience, customer support or only to spread it has been used.
There is a lot information about metadata in different sort of files like pictures, documents, videos, music online. This tool
focuses on pdf only. 
If you are new to that term have a look here:
* https://en.wikipedia.org/wiki/Metadata

Also, if you are interested in a real pdf analysis, this tool will only do the basics for you. It has not been written to analyse bad, malware or even interesting files. It's purpose is to give you an idea what is used at target xyz. 
If you are looking for more in-depth analysis i recommend the tools of Didier Stevens:
* https://blog.didierstevens.com/programs/pdf-tools/

## Download

```
git clone https://github.com/c0decave/pdfgrab
cd pdfgrab
python3 pdfgrab.py -h
```

## Usage

Those are your major options:
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
# ./pdfgrab.py -s kernel.org
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

### Google Search Mode, several domains
```
# ./pdfgrab.py -s example.com,example.us
```

### Reporting

pdfgrab outputs the information in different formats. If not disabled by one of the reporting flags (see -h) you will
find in the output directory:

* html report
* text report
* text url list
* json data
* json url list

### Logging

pdfgrab creates a logfile in the running directory called "pdfgrab.log"

## Google

* Search: filetype:pdf site:com
* Results: 264.000.000

## Disclaimer

Have fun!
