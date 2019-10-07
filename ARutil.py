#utility version:0.0.7
#9th

import os
import sys
import time
import io
import json
from bs4 import BeautifulSoup
import certifi
import urllib3

def mkdiring(input):
    arr=input.split("/");input=""
    for inp in arr:
        if not os.path.exists(input+inp+"/"):os.mkdir(input+inp)
        input+=inp+"/"
    return input.rstrip("/")

def outYurl(output,url):
    if output=="":return url.translate(str.maketrans('*:/?\"\'\\','_______'))
    return output+"/"+url.translate(str.maketrans('*:/?\"\'\\','_______'))

def rootYrel(root,rel):#like as os.path.join
    root=root.rstrip("/")
    rel=rel.lstrip("/")
    if root=="":return rel
    if rel=="":return root
    return root+"/"+rel

def ffzk(input_dir):#Relative directory for all existing files
    imgname_array=[];input_dir=input_dir.strip("\"\'")
    for fd_path, _, sb_file in os.walk(input_dir):
        for fil in sb_file:imgname_array.append(fd_path + '/' + fil)
    if os.path.isfile(input_dir):imgname_array.append(input_dir)
    return imgname_array

#For processing that may stop,such as request
#errorID,interval per process[s],wait time when an error occurs,
#the function,args of the function,params of the function
def tryex(ID,interval,wait,func,*args,**params):
    idnewflg=1;time.sleep(interval)
    while idnewflg:
        try:ret=func(*args,**params)
        except:print("errID:"+str(ID)+" wait...");time.sleep(wait);continue
        idnewflg=0
    return ret

#bonding url ver 0.20
def burl(url_input,*add_string):
    for i in add_string:
        if(url_input[-1:]=="/"):url_input=url_input.rstrip("/")+'?'+i
        else:url_input+='&';url_input+=i
    return url_input

#string organizer
def storer(input):
    if type(input) is not str:return ""
    io_ = io.StringIO() 
    spaceflag=1;sqflag=0;Ynflag=1
    for car in input:
        if car=='<':sqflag=1;continue
        if car=='>':sqflag=0;continue
        if sqflag==1:continue
        if car==' ' and spaceflag==0:io_.write(car);spaceflag=1;continue
        if car=='\n' and Ynflag==0:io_.write(car);Ynflag=1;continue
        if  car=='\n'or car==' 'or car=='\t' or car=='◆' or car=='　'or car=='★'\
            or car=='・' or car=='□'or car==',' or car=='■' or car=='♪' or car=='…'\
            or car=='◇' or car=='※' or car==':' or car =='‥' or car=='↓' or car=='＊'\
            or car=='▼' or car=='◎' or car=='③' or car=='②' or car=='①'\
            or car=='/' or car=='●' or car=='▲'or car=='〇'or car=='☆':continue
        io_.write(car);spaceflag=0;Ynflag=0
    output = io_.getvalue();io_.close()
    return output

#Rough Image Scraper
def RIS(url,output="./RIS_image",interval=3,urlfilter="",last_s_omit=1,minsize=10000,ETI="ETtlId.json",headers={}):
    print("access:",url,"\nThe miminum size is ",minsize,"[Byte]\nThe interval time is ",interval,"[s]")
    if interval<3.0:print('plz set interval time more than 3.0[s]');return
    titles={};output2=outYurl(output,url)
    #index_file_load
    if os.path.isfile(outYurl(output,ETI)):
        with open(outYurl(output,ETI), 'r',encoding='utf-8') as fp:titles.update(json.load(fp))
    if outYurl("",url) in titles:print("arleady exist in index file");titles.clear();return
    #access url
    if 150<len(output2):print("output folder directory is too large(150<len)");return
    mkdiring(output2)
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),headers=headers)
    html=tryex("unable to access url",interval,600,https.request,'GET',url)
    soup = BeautifulSoup(html.data,"html.parser")
    #Image_files_getting
    for link in soup.find_all("img"):
        target=""
        if link.get("src").endswith(".jpg"):target=link.get("src")
        elif link.get("src").endswith(".png"):target=link.get("src")
        else:continue
        if urlfilter not in target:continue
        if last_s_omit:target=target.replace("s.jpg",".jpg").replace("s.png",".png")
        print("downloading:",target);time.sleep(interval)
        try:re=https.request('GET',target)
        except:print("failed!");continue
        if sys.getsizeof(re.data)<minsize:print("size is less than the minimum");continue
        with open(output2+'/'+target.split('/')[-1], 'wb') as f:f.write(re.data)
    #if there is not file in folder.
    if len(ffzk(output2))==0:os.removedirs(output2);print("rm -rf ",output2)
    #index_file_update
    titles[outYurl("",url)]=soup.head.title.text
    with open(outYurl(output,ETI), 'w',encoding='utf-8') as fp:json.dump(titles,fp, ensure_ascii=False)
    titles.clear()
    print("RIS_complete")

#sitemap_loader
def SML(url,interval=3,headers={},recursion=1,fromurl=""):
    ret=[]
    if url.endswith(".xml")==False:return ret
    if fromurl!="":print("from:",fromurl)
    print("access:",url,"\nThe interval time is ",interval,"[s]")
    if interval<3.0:print('plz set interval time more than 3.0[s]');return ret
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),headers=headers)
    html=tryex(0,interval,600,https.request,'GET',url)
    soup = BeautifulSoup(html.data,"html.parser")
    for i in range(len(soup.findAll('loc'))):
        ret.append(soup.findAll('loc')[i].text)
    #recursion
    if recursion:
        for i in ret:ret.extend(SML(i,interval,headers,recursion=1,fromurl=url))
    return ret

def ETM(dir,ETI="ETtlId.json"):
    titles={}
    if os.path.isfile(outYurl(dir,ETI)):
        with open(outYurl(dir,ETI), 'r',encoding='utf-8') as fp:titles.update(json.load(fp))
    fils=ffzk(dir)
    for fil in fils:
        if len(ffzk(fil))==0:os.removedirs(fil);print("rm -rf ",fil)
        if titles not in fil.split("/")[-1]:
            print("erase from index:",fil.split("/")[-1]);titles.pop(fil.split("/")[-1])


    