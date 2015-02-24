# -*- coding: utf-8 -*-
"""
Created on 2015-2-24 15:22

@author: vespa
"""

import urllib
import shutil
import urllib2
import re
import time
import os

def GetRE(content,regexp):
    return re.findall(regexp, content)

def getURLContent(url):
    while True:
        flag = 1;
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(url = url,headers = headers);
            content = urllib2.urlopen(req,timeout = 10).read();
        except:
            print "get content Error:",url
            flag = 0;
            time.sleep(5)
        if flag == 1:
            break;
    time.sleep(1)
    return content.decode('gbk').encode('utf8')

def GetPageNum(content,url):
    result = GetRE(content,r'Pages: \( 1/(\d+) total \)')
    try:
        return int(result[0])
    except:
        print "GetPageNum Error:\nurl:%s\n"%(url)
        return 0

def GetDayInfo(content,url):
    regexp = r'Posted: (\d+-\d+-\d+)'
    result = GetRE(content,regexp)
    try:
        return result[0]
    except:
        print "GetDayInfo Error:\nurl:%s\n"%(url)
        return "1000-01-01"

def SaveNews(url, DateInfo, title):
    URL = "http://rmrbw.info/"+url
    content = getURLContent(URL)
    regexp = '<div class="tpc_content" id="read_tpc">\s+(.*?)\s+(?=<\/div>)'
    result = re.findall(regexp,content,re.S)
    try:
        newsContent = result[0].strip().replace('<br />','\n')
        day = GetDayInfo(content,URL)
        print 'Creating file:%s %s'%(day,title)
        fid = open('./%s/%s %s.txt'%(DateInfo,day,title),'w+')
        fid.write(newsContent)
        fid.close()
    except:
        print "SaveNews Error:\nurl:%s\nDateInfo:%s\ntitle:%s\n"%(url,DateInfo,title)

def ScrapPage(url, DateInfo):
    content = getURLContent(url)
    regexp = r'<h3><a href=\"(read\.php\?tid=\d+)[^>]*>([^<]*)</a></h3>'
    result = GetRE(content,regexp)
    for (pageurl,title) in result:
        SaveNews(pageurl,DateInfo,title)

def SolvePage(url, DateInfo):
    path = './%s/'%DateInfo
    if not os.path.exists(path):
        os.makedirs(path)
    print DateInfo
    URL = "http://rmrbw.info/" + url
    content = getURLContent(URL)
    pageNum = GetPageNum(content,url)
    for page in range(1,pageNum+1):
        url = "%s&page=%d"%(URL,page)
        print 'page:%d   %s'%(page,url)
        ScrapPage(url,DateInfo)

if __name__ == "__main__":
    rootURL = "http://rmrbw.info/index.php"
    content = getURLContent(rootURL)
    regexp = r'<a href=\"(thread\.php\?fid=\d+)\" class=\"fnamecolor\">([^<]*)'
    result = GetRE(content,regexp)
    for (url, DateInfo) in result:
        SolvePage(url, DateInfo)
