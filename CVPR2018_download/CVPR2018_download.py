#!/usr/bin/python
# coding:utf-8

import urllib
import re

def getHtmlContent(url):
    page = urllib.urlopen(url)
    return page.read()

def getBlock(html):
    re_block = r"<dt class=\"ptitle\"><br><a(.*?)</div>\n</div>\n</dd>"
    re_title = r'html">(.*?)</a></dt>'
    re_paper = r'</dd>\n<dd>\n\[<a href="(.*?)">pdf</a>\]'
    re_supp = r'>pdf</a>]\n\[<a href="(.*?)">supp</a>\]'
    block = re.compile(re_block, re.S)
    blocks = re.findall(block, html)
    msg = []
    for temp in blocks:
        title = re.findall(re.compile(re_title, re.S), temp)[0].replace('/', ' ')
        title = title.replace(':', '')
        title = title.replace(',', '')
        paper = 'http://openaccess.thecvf.com/'+re.findall(re.compile(re_paper, re.S), temp)[0]
        if re.findall(re.compile(re_supp, re.S), temp):
            supp = 'http://openaccess.thecvf.com/'+re.findall(re.compile(re_supp, re.S), temp)[0]
        else:
            supp = ''
        sub_msg=[]
        sub_msg.append(title)
        sub_msg.append(paper)
        sub_msg.append(supp)
        msg.append(sub_msg)
    return msg

def download(url, fileName):
    urllib.urlretrieve(url, fileName)

def batchDownload(blocks, path):
    count = 1
    for block in blocks:
        download(block[1], ''.join([path, '{0}.pdf'.format(block[0])]))
        if block[2]:
            download(block[2], ''.join([path, '{0}.pdf'.format(block[0]+'(supp)')]))
        print 'downloading No.'+str(count)+'/'+str(len(blocks))
        count = count + 1

url = 'http://openaccess.thecvf.com/CVPR2018.py'
html = getHtmlContent(url)
blocks = getBlock(html)
batchDownload(blocks, './')

