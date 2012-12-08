import lxml.html
import urllib2
import chardet
import re
import xml.parsers.expat

def unescape(s):
    want_unicode = False
    if isinstance(s, unicode):
        s = s.encode("utf-8")
        want_unicode = True

    # the rest of this assumes that `s` is UTF-8
    list = []

    # create and initialize a parser object
    p = xml.parsers.expat.ParserCreate("utf-8")
    p.buffer_text = True
    p.returns_unicode = want_unicode
    p.CharacterDataHandler = list.append

    # parse the data wrapped in a dummy element
    # (needed so the "document" is well-formed)
    p.Parse("<e>", 0)
    p.Parse(s, 0)
    p.Parse("</e>", 1)

    # join the extracted strings and return
    es = ""
    if want_unicode:
        es = u""
    return es.join(list)

# open file
f = open("gl02-12.txt","w")

# entry parameter
param = [
"2002-2003",
"2003-2004",
"2004-2005",
"2005-2006",
"2006-2007",
"2007-2008",
"2008-2009",
"2009-2010",
"2010-2011",
"2011-2012"]


for item in param:
	print
	# URL
	url =  "http://www.eurofotbal.cz/gambrinus-liga/%s/vysledky-rozlosovani/" % item
	print url
	
	# make HTTP request
	content = urllib2.urlopen(url).read()
	# print "Requesting file " + url + str(param+num)
	# print content

	# decode source code
	encd = chardet.detect(content)['encoding']
	if encd != 'utf-8':
	    content = content.decode(encd, 'replace').encode('utf-8')

	# print content
	# exit()
	    
	# parse to XML tree
	root = lxml.html.fromstring(content.decode('utf-8'), base_url=url)

	# select result tr
	for el in root.cssselect("div.col-center div.in table.matches tr"):
		# convert HtmlElement to string
	    l = lxml.html.tostring(el)
	    # print l
	    # # replace (delete) html markup
	    l = l.replace("<tr><td class=\"date\">","")
	    l = l.replace("<tr class=\"last\"><td class=\"date\">","")
	    l = l.replace("</td><td class=\"time\">",",")
	    l = l.replace("</td><td class=\"teams\"><div class=\"fl\">",",")
	    l = l.replace(" - ",",")
	    l = re.sub(r'</div>.*/\">',",", l)	    
	    l = re.sub(r'</a></td></tr>',"", l)
	    l = item + "," + l + "\n"
	    l = unescape(l)
	    print l
	    # # write line to file
	    f.write(l)


