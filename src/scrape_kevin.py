# Copyright (C) 2011 by Kevin Nam Truong, Daniel Steinberg, Debasish Das, Juan Pineda, Melissa Miranda, and Victoria Pan

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# `THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urllib, re, time
from BeautifulSoup import BeautifulSoup

def sanitize_html(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        tag.hidden = True
    return soup.renderContents()

hexentityMassage = [(re.compile('&#x([^;]+);'), lambda m: '&#%d' % int(m.group(1), 16))]

def convert(html):
    return BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, markupMassage=hexentityMassage).contents[0].string



def scrape(userID):
    invalidChars = re.sub('[-_\\w]', '', userID)
    if (len(userID) < 2 or len(userID) > 15 or len(invalidChars) > 0):
	return -1
    allcomments = []
    allpostID = []
    result = []
    nexturl = 'http://news.ycombinator.com/threads?id=' + userID
    commentfieldre = re.compile('<a href="user\?id=' + userID + '">' + userID + '<(.*?)></td>', re.DOTALL)
    commentre = re.compile('class="comment"><font color=.......>(.*?)</fo', re.DOTALL)
    postIDre = re.compile('<a href="item\?id=(.*)">parent</a> \| on: <a href="item\?id=(\\1)">')
    nexturlre = re.compile('class="title"><a href="(.*)" rel')
    commentIDre = re.compile('<a href="item\?id=([^>]*)">link</a>')
    checkUser = True

    while (nexturl and len(result) < 10):
        content = urllib.urlopen(nexturl).read()
	if (checkUser == True):
	    if (content == 'No such user.'):
		return -1
	    checkUser = False
        allcommentfield = commentfieldre.findall(content)
        for currfield in allcommentfield:
            postID = []
            comment = []
            commentID = []
            postIDmatch = postIDre.search(currfield)
            if postIDmatch:
                postID = postIDmatch.group(1)
            commentmatch = commentre.search(currfield)
            if commentmatch:
                comment = convert(sanitize_html(commentmatch.group(1)))
            commentIDmatch = commentIDre.search(currfield)
            if commentIDmatch:
                commentID = commentIDmatch.group(1)
            if (postID and comment and commentID):
                result.append([postID, comment, commentID]) 
        nexturlmatch = nexturlre.search(content)
        if nexturlmatch:
            nexturlappend = nexturlmatch.group(1)
            nexturl = 'http://news.ycombinator.com/' + nexturlappend[1:]
        else:
            nexturl = []
        time.sleep(.05)
    return result


#commentIdStructure = scrape("pg")
#for elt in commentIdStructure:
#    print elt
#print len(commentIdStructure)
#scrape("icey")
