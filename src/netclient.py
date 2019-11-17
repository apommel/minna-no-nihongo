import urllib.request
import hashlib
import pickle
from time import time

def internetOn():
    try:
        response=urllib.request.urlopen('http://minnanihongo.toile-libre.org/',timeout=1)
        return True
    except:
        pass
    return False

def parsePerso():
    parse=list()
    string=str(urllib.request.urlopen("http://minnanihongo.toile-libre.org/listesperso/").read())
    test=True
    positionListe=0
    positionString=0
    oldPositionString=0
    while test:
        if positionString<len(string):
            positionString=string.find('href="', positionString, len(string))+6
            if positionString>oldPositionString:
                fichier=""
                while string[positionString]!='"':
                    fichier=fichier+string[positionString]
                    positionString+=1
                if fichier[len(fichier)-1]!="/" and fichier[0]!="/":
                    parse.append("")
                    string2=str(urllib.request.urlopen("http://minnanihongo.toile-libre.org/listesperso/"+fichier).read())
                    i=string2.find("<h1>")+12
                    while string2[i]!="<":
                        parse[positionListe]=parse[positionListe]+string2[i]
                        i+=1
                    positionListe+=1
                oldPositionString=positionString
                positionString+=1
            else:
                test=False
    return(parse)

def getNom(file):
    nom=""
    string=str(urllib.request.urlopen("http://minnanihongo.toile-libre.org/listesperso/"+file+".html").read())
    i=string.find("<h1>")+12
    while string[i]!="<":
        nom=nom+string[i]
        i+=1
    return(nom)

def downloadListe(url):
    file=urllib.request.urlopen(url)
    liste0=pickle.load(file)
    liste1=pickle.load(file)
    liste2=pickle.load(file)
    liste=[liste0, liste1, liste2]
    return(liste)

def parseTable(url):
    parse=list()
    string=urllib.request.urlopen(url).read().decode('utf-8')
    test=True
    positionListe=0
    positionString=0
    oldPositionString=0
    while test:
        if positionString<len(string):
            positionString=string.find("<td>", positionString, len(string))+4
            if positionString>oldPositionString:
                parse.append("")
                while string[positionString]!="<":
                    parse[positionListe]=parse[positionListe]+string[positionString]
                    positionString+=1
                positionListe+=1
                oldPositionString=positionString
                positionString+=1
            else:
                test=False
    return(parse)
                    
def internetsumfile(url):
    fileObj = urllib.request.urlopen(url)
    m = hashlib.md5()
    while True:
        d = fileObj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def sumfile(filePath):
    fileObj = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        d = fileObj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def writeTime(path):
    file=open(path, 'wb')
    pickle.dump(time(), file)
    file.close()

def checkTime():
    path="Data/log.p"
    try:
        t=getTime(path)       
    except:
        t=0
    return((abs(time()-t)>86400))

def getTime(path):
    return(pickle.load(open(path, 'rb')))
    
def checkBDD():
    url="http://minnanihongo.toile-libre.org/MinnaNihongo/Data/vocabulaire.db"
    path="Data/log.p"
    bdd=open("Data/vocabulaire.db", 'wb')
    if sumfile("Data/vocabulaire.db")!=internetsumfile(url):
        bdd.write(urllib.request.urlopen(url).read())
        writeTime(path)
        
