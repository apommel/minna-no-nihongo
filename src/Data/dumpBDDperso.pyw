from tkinter import *
import sqlite3
import pickle
from os import mkdir

jpKanji = []
jpKana = []
trad = []

conn = sqlite3.connect('perso.db')

def norm(chaine):
        ASCII=['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        sortie=str()
        for k in range (0, len(chaine)):
                caractere=chaine[k].lower()
                if caractere=="à" or caractere=="â" or caractere=="ä":
                        caractere="a"
                elif caractere=="œ":
                        caractere="oe"
                elif caractere=="é" or caractere=="è" or caractere=="ê" or caractere=="ë":
                        caractere="e"
                elif caractere=="î" or caractere=="ï" or caractere=="ì":
                        caractere="i"
                elif caractere=="ç":
                        caractere="c"
                elif caractere=="ô" or caractere=="ö" or caractere=="ò":
                        caractere="o"
                elif caractere=="ù" or caractere=="û" or caractere=="ü":
                        caractere="u"
                elif caractere=="ÿ":
                        caractere="y"
                elif caractere not in ASCII:
                        caractere=""
                sortie=sortie+caractere
        return sortie

def makeDir():
        try:
                mkdir("files/")
        except:
                pass
                

def createHTML(filename, jpKanji, jpKana, trad):
        html="""
<meta charset="UTF-8">
<link rel="stylesheet" href="files/table.css" />
<h1>Liste : {}</h1>
<br/>
<a href="files/{}">Télécharger</a><br/>
<br/>
<table>
   <tr>
       <th>Kanji</th>
       <th>Kana</th>
       <th>Traduction</th>
   </tr>""".format(filename, norm(filename))
        for i in range (0, len(jpKanji)):
                html=html+"""
   <tr>
       <td>{}</td>
       <td>{}</td>
       <td>{}</td>
   </tr>""".format(jpKanji[i], jpKana[i], trad[i])
        html=html+"""
</table>"""
        makeDir()
        fichier=open("files/{}.html".format(norm(filename)), 'w', encoding='utf8')
        fichier.write(html)
        fichier.close()

def createFile(filename, jpKanji, jpKana, trad):
        makeDir()
        fichier=open("files/"+norm(filename), 'wb')
        pickle.dump(jpKanji, fichier)
        pickle.dump(jpKana, fichier)
        pickle.dump(trad, fichier)
        fichier.close()
                
class Interface (Frame) :

    def __init__(self, fenetre, conn):
        global entreeNomFichier, entreeKanji, entreeKana, entreeTrad
        Frame.__init__(self, fenetre, bg="white")
        fenetre["bg"]="white"
        fenetre["width"]=400
        fenetre["height"]=300
        self.place(anchor="c", relx=.5, rely=.5)
        
        self.conn=conn
        self.cursor=self.conn.cursor()

        self.texte1 = Label(self, text="Nom de la liste", bg="white")
        self.texte1.grid(row=0, columnspan=2, pady=10)
        self.texte2 = Label()

        entreeNomFichier = Entry (self)
        entreeNomFichier.bind("<Return>", self.Demarrer)
        entreeNomFichier.grid(row=2, columnspan=2, pady=5)

        entreeKanji = Entry (self)
        entreeKana = Entry (self)
        entreeTrad = Entry (self)

        self.texteKanji = Label(self, text="Kanji", bg="white")
        self.texteKana = Label(self, text="Kana", bg="white")
        self.texteTrad = Label(self, text="Traduction", bg="white")

        self.boutonDemarrer = Button(self, text="Démarrer", command=self.bDemarrer, bg="blue", fg="white")
        self.boutonDemarrer.grid(row=4, columnspan=2, pady=10)

        self.boutonSuivant = Button(self, text="Suivant", command=self.pageSuivante, bg="blue", fg="white")
        self.boutonTerminer = Button(self, text="Terminer", command=self.terminer, bg="blue", fg="white")

    def Demarrer (self, event):
        self.bDemarrer()

    def bDemarrer(self):
        self.filename = entreeNomFichier.get()
        self.texte1["text"]="Expression {}".format(str(len(jpKanji)+1))
        check=sqlite3.connect("vocabulaire.db")
        curseurCheck=check.cursor()
        curseurCheck.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence';")
        liste1=curseurCheck.fetchall()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence';")
        liste2=self.cursor.fetchall()
        existe=False
        for i in range (0, len(liste1)):
                if norm(self.filename) in liste1[i]:
                        existe=True
        for i in range (0, len(liste2)):
                if norm(self.filename) in liste2[i]:
                        existe=True
        if existe==True:
                self.texte2 = Label(self, text="Nom déjà utilisé", bg="white")
                self.texte2.grid(row=3, columnspan=2, pady=10)
        else:
                self.boutonDemarrer.destroy()
                entreeNomFichier.destroy()
                self.texte2.grid_forget()
                self.texte2.destroy()
                self.texteKanji.grid(row=2, column=0, pady=10, padx=5)
                entreeKanji.grid(row=2, column=1, pady=10, padx=5)
                self.texteKana.grid(row=3, column=0, pady=10, padx=5)
                entreeKana.grid(row=3, column=1, pady=10, padx=5)
                self.texteTrad.grid(row=4, column=0, pady=10, padx=5)
                entreeTrad.grid(row=4, column=1, pady=10, padx=5)
                self.boutonSuivant.grid (row=5, column=0, pady=15)
                self.boutonTerminer.grid(row=5, column=1, pady=15)
        
    def pageSuivante(self):
        global jpKanji, jpKana, trad
        if not entreeKanji.get():
            jpKanji.append(entreeKana.get())
        else:
            jpKanji.append(entreeKanji.get())
        jpKana.append(entreeKana.get())
        trad.append(entreeTrad.get())
        entreeKanji.delete(0, 'end')
        entreeKana.delete(0, 'end')
        entreeTrad.delete(0, 'end')
        self.texte1["text"]="Expression {}".format(str(len(jpKanji)+1))

    def non(self):
            self.texte2.destroy()
            self.boutonOui.destroy()
            self.boutonNon.destroy()
            self.texte1["text"]="Terminé"

    def oui(self):
            createHTML(self.filename, jpKanji, jpKana, trad)
            createFile(self.filename, jpKanji, jpKana, trad)
            self.texte2.destroy()
            self.boutonOui.destroy()
            self.boutonNon.destroy()
            self.texte1["text"]="Fichiers générés dans Data/files/.\nTransmettez-les à aurelien.pommel@gmail.com\npour les rendre disponible sur le portail."

    def terminer (self):
        global jpKanji, jpKana, trad
        if not entreeKanji.get():
                jpKanji.append(entreeKana.get())
        else:
                jpKanji.append(entreeKanji.get())
        jpKana.append(entreeKana.get())
        trad.append(entreeTrad.get())

        self.boutonSuivant.destroy()
        self.boutonTerminer.destroy()
        self.texteKanji.destroy()
        self.texteKana.destroy()
        self.texteTrad.destroy()
        entreeKanji.destroy()
        entreeKana.destroy()
        entreeTrad.destroy()

        if len(jpKanji) != len(jpKana) or len(jpKanji) != len(trad) or len(jpKana) != len(trad):
            self.texte1["text"]="Impossible de créer le fichier vocabulaire\nles listes ne possèdent pas le même nombre d'éléments"
        else:
                self.cursor.execute("""
CREATE TABLE IF NOT EXISTS {}(
id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
liste TEXT,
jpKanji TEXT,
jpKana TEXT,
trad TEXT
)
""".format(norm(self.filename)))
                self.conn.commit()
                i=0
                while i<len(jpKana) :
                        self.cursor.execute("""
			INSERT INTO {}(id, liste, jpKanji, jpKana, trad) VALUES(?, ?, ?, ?, ?)""".format(norm(self.filename)), (i, self.filename, jpKanji[i], jpKana[i], trad[i]))
                        i=i+1
                self.conn.commit()
                self.texte1["text"]="Importation dans la base de donnée réussie"
                self.texte2=Label(self, text="Voulez-vous enregistrer cette liste dans un\nfichier et créer une page web en vue de les partager ?", bg="white")
                self.texte2.grid(row=2, columnspan=2, pady=10)
                self.boutonOui = Button(self, text="Oui", command=self.oui, bg="blue", fg="white")
                self.boutonNon = Button(self, text="Non", command=self.non, bg="blue", fg="white")
                self.boutonOui.grid(row=3, column=0, pady=10, padx=5)
                self.boutonNon.grid(row=3, column=1, pady=10, padx=5)
                

fenetre = Tk()
fenetre.title("dumpBDDperso")
interface = Interface(fenetre, conn)

interface.mainloop()
