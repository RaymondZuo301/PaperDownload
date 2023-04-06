#!/usr/bin/python
# coding:utf-8

import urllib
import re

def getHtmlContent(url):
    page = urllib.urlopen(url)
    return page.read()

def getBlock(html):
    re_block = r"<dt class=\"ptitle\"><br><a(.*?)</dd>\n<dt"
    re_title = r'html">(.*?)</a></dt>'
    re_paper = r'\[<a href="(.*?)">pdf</a>'
    re_supp = r'\[<a href="(\S+\.pdf)">supp</a>'
    block = re.compile(re_block, re.S)
    blocks = re.findall(block, html)
    msg = []
    for temp in blocks:
        title = re.findall(re.compile(re_title, re.S), temp)[0].replace('/', ' ')
        title = title.replace(':', '')
        title = title.replace(',', '')
	paper_url = re.findall(re.compile(re_paper, re.S), temp)[0]
        paper = 'https://openaccess.thecvf.com/'+paper_url
        if re.findall(re_supp, temp):
            supp = 'https://openaccess.thecvf.com/'+re.findall(re.compile(re_supp, re.S), temp)[0]
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
	#print block[1]
	#print block[2]
        download(block[1], ''.join([path, '{0}.pdf'.format(block[0])]))
        if block[2]:
            download(block[2], ''.join([path, '{0}.pdf'.format(block[0]+'(supp)')]))
        print 'downloading No.'+str(count)+'/'+str(len(blocks))+': '+block[0]
        count = count + 1

url = 'https://openaccess.thecvf.com/WACV2022'
html = getHtmlContent(url)
blocks = getBlock(html)
batchDownload(blocks, './WACV2022/')
