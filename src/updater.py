import urllib.request
import hashlib
from os import mkdir

url="http://minnanihongo.toile-libre.org/MinnaNihongo/"

def internetOn():
    try:
        response=urllib.request.urlopen('http://minnanihongo.toile-libre.org/',timeout=1)
        return True
    except:
        pass
    return False

def parsehref(path):
    parse=list()
    string=str(urllib.request.urlopen(url+path).read())
    test=True
    k=0
    i=0
    j=0
    while test:
        if i<len(string):
            i=string.find('href="', i, len(string))+6
            if i>j:
                parse.append("")
                while string[i]!='"':
                    parse[k]=parse[k]+string[i]
                    i+=1
                k+=1
            else:
                test=False
            j=i
            i+=1 
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

def identique(path):
    try:
        if sumfile(path)==internetsumfile(url+path):
            print("Fichier a jour")
            return True
        else:
            return False
    except:
        return False

def download(path):
    print("Telechargement de",path,"...")
    fichier=open(path, 'wb')
    fichier.write(urllib.request.urlopen(url+path).read())
    fichier.close()

def parsing(chemin):
    liens=parsehref(chemin)
    for path in liens:
        if path[0]!= "/":
            if path[len(path)-1]=="/":
                try:
                    mkdir(chemin+path)
                    parsing(chemin+path)
                except:
                    parsing(chemin+path)
            else:
                print("/"+chemin+path)
                if not identique(chemin+path):
                    download(chemin+path)
                    print("100%")

print("Mise a jour de MinnaNihongo...")
if internetOn():
    parsing("")
    print("Mise a jour terminee")
else:
    print("Pas d'acces à internet")

input("Appuyez sur une touche pour quitter...")

