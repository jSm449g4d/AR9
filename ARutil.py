#utility version:0.0.7
#9th

import os
import time
import io

def mkdiring(input):
    arr=input.split("/");input=""
    for inp in arr:
        if not os.path.exists(input+inp+"/"):os.mkdir(input+inp)
        input+=inp+"/"
    return input.rstrip("/")

def outYurl(output,url):
    if output=="":return url.translate(str.maketrans('*:/?\"\'\\','________'))
    return output+"/"+url.translate(str.maketrans('*:/?\"\'\\','________'))

def rootYrel(root,rel):#like as os.path.join
    root=root.rstrip("/")
    rel=rel.lstrip("/")
    if root=="":return rel
    if rel=="":return root
    return root+"/"+rel

def ffzk(input_dir):#Relative directory for all existing files
    imgname_array=[]
    input_dir=input_dir.rstrip("\"").lstrip("\"").maketranse("\\","/")
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
