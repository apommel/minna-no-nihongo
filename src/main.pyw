from tkinter import *
from random import randint, sample, shuffle
import sqlite3
import scripts
import netclient

class Interface (Frame) :
    global numeroLecon, entreeRechercher, bdd, curseur

    def __init__(self, fenetre, vocabulaire, perso):
        self.vocabulaire=vocabulaire
        self.curseur=self.vocabulaire.cursor()
        self.perso=perso
        self.curseurPerso=self.perso.cursor()
        
        Frame.__init__(self, fenetre, bg="white")
        fenetre["bg"]="white"
        icone = PhotoImage(file="Data/img/icone.gif")
        fenetre.call('wm', 'iconphoto', fenetre._w, icone)
        fenetre["width"]=650
        fenetre["height"]=500
        self.place(anchor="c", relx=.5, rely=.5)

        self.texte1 = Label(self, text="Vocabulaire", bg="white")
        self.texte1.grid(row=0, columnspan=2, pady=10)

        self.entreeRechercher = Entry(self)
        self.entreeRechercher.bind("<Return>", self.Rechercher)
        self.entreeRechercher.grid(row=1, column=0, pady=5, padx=2, sticky="e")

        self.boutonRechercher = Button(self, text="Rechercher", bg="red", fg="white", command=self.bRechercher)
        self.boutonRechercher.grid(row=1, column=1, pady=5, padx=2, sticky="w")

        self.numeroLecon = Listbox(self, bd=0)
        self.listeVoc=list()
        self.listeAffichage=list()
        self.creerListe(self.curseur)
        self.limite=self.numeroLecon.size()-1
        self.creerListe(self.curseurPerso)
        self.numeroLecon.grid(row=2, columnspan=2, pady=5)

        self.boutonAbonnement = Button(self, text="Abonnement", command=self.Abonnement, bg="red", fg="white")
        self.boutonAbonnement.grid(row=3, column=0, padx=5, pady=10)

        self.boutonAcceder = Button(self, text="Accéder ->", command=self.Acceder, bg="red", fg="white")
        self.boutonAcceder.grid(row=3, column=1, padx=5, pady=10)

        self.boutonRetour = Button(self, text="Retour", bg="red", fg="white", command=self.Retour)

    def creerListe(self, curseur):
        curseur.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence';")
        for name in (curseur.fetchall()):
            self.listeVoc.append(name[0])
            curseur.execute("SELECT DISTINCT liste FROM {}".format(name[0]))
            affichage=curseur.fetchone()[0]
            self.listeAffichage.append(affichage)
            self.numeroLecon.insert(END, affichage+"   "+str(int(scripts.pourcentageLecon(name[0])))+"%")

    def Abonnement(self):
        self.numeroLecon.destroy()
        self.boutonAcceder.destroy()
        self.entreeRechercher.destroy()
        self.boutonRechercher.destroy()
        self.boutonAbonnement.destroy()
        if netclient.internetOn():
            self.texte1["text"]="Abonnement"

            self.persoBox = Listbox(self, bd=0)
            self.listesPerso = netclient.parsePerso()
            for liste in self.listesPerso:
                self.persoBox.insert(END, liste)
            self.persoBox.grid(row=1, columnspan=2, pady=20)

            self.boutonVoir = Button (self, text="Voir", command=self.voir, bg="red", fg="white")
            self.boutonVoir.grid(row=2, column=1, padx=5, pady=0)
        else:
            self.texte1["text"]="Problème de de connexion au serveur"
        self.boutonRetour.grid(row=2, column=0, padx=5, pady=0)

    def voir(self):
        self.ID=int(self.persoBox.curselection()[0])
        self.texte1["text"]=self.listesPerso[self.ID]
        self.persoBox.destroy()
        self.boutonVoir.destroy()
        self.boutonRetour.grid_forget()
        self.texte2 = Label(self, text="Erreur", bg="white")
        self.boutonRetour2 = Button(self, text="Retour", bg="red", fg="white", command=self.Retour2)
        self.boutonRetour2.grid(row=3, column=0, pady=5)
        self.boutonDesabonner = Button(self, text="Se désabonner", bg="red", fg="white", command=self.Desabonner)
        self.boutonAbonner = Button(self, text="S'abonner", bg="red", fg="white", command=self.Abonner)
        if scripts.Existe(self.listesPerso[self.ID]):
            self.boutonDesabonner.grid(row=3, column=1, pady=5)
        else:
            self.boutonAbonner.grid(row=3, column=1, pady=5)
        self.apercu = Text(self, bg="white", bd=0)
        url="http://minnanihongo.toile-libre.org/listesperso/"+scripts.norm2(self.listesPerso[self.ID])+".html"
        affichage=netclient.parseTable(url)
        for i in range (0, len(affichage), 3):
            self.apercu.insert(END, affichage[i])
            if affichage[i] != affichage[i+1]:
                self.apercu.insert(END, " / " + affichage[i+1])
            self.apercu.insert(END, " : " + affichage[i+2])
            if i != len(affichage)-3:
                self.apercu.insert(END, "\n")
        self.apercu.grid(row=1, columnspan=2, pady=5)
        self.apercu.config(state=DISABLED)

    def Desabonner(self):
        file=scripts.norm2(self.listesPerso[self.ID])
        self.texte2["text"]=scripts.unsubscribe(file)
        self.texte2.grid(row=2, columnspan=2, pady=5)
        self.boutonDesabonner.grid_forget()
        self.boutonAbonner.grid(row=3, column=1, pady=5)

    def Abonner(self):
        file=scripts.norm2(self.listesPerso[self.ID])
        liste=netclient.downloadListe("http://minnanihongo.toile-libre.org/listesperso/files/"+file)
        self.texte2["text"]=scripts.importer(liste, netclient.getNom(file))
        self.texte2.grid(row=2, columnspan=2, pady=5)
        self.boutonAbonner.grid_forget()
        self.boutonDesabonner.grid(row=3, column=1, pady=5)

    def Retour2(self):
        self.boutonAbonner.destroy()
        self.boutonDesabonner.destroy()
        self.texte2.destroy()
        self.apercu.destroy()
        self.boutonRetour2.destroy()
        self.Abonnement()
                
    def Rechercher(self, event):
        self.bRechercher()

    def recherche(self, curseur, inf, sup):
        for k in range (inf, sup):
                jpKanji=[]
                jpKana=[]
                trad=[]
                curseur.execute("SELECT MAX(id) FROM {}".format(self.listeVoc[k]))
                longueur=curseur.fetchone()[0]+1
                curseur.execute("SELECT jpKanji, jpKana, trad FROM {}".format(self.listeVoc[k]))
                for i in range (0, longueur):
                    data=curseur.fetchone()
                    jpKanji.append(data[0])
                    jpKana.append(data[1])
                    trad.append(data[2])
                for k2 in range (0, len(trad)):
                    if self.entreeRechercher.get() in jpKanji[k2] or self.entreeRechercher.get() in jpKana[k2] or scripts.norm(self.entreeRechercher.get()) in scripts.norm(trad[k2]):
                        self.affichageRecherche.insert(END, "[{}] ".format(self.listeAffichage[k]) + jpKanji[k2])
                        if jpKanji[k2] != jpKana[k2]:
                            self.affichageRecherche.insert(END, " / " + jpKana[k2])
                        self.affichageRecherche.insert(END, "  :  " + trad[k2]+"   "+str(int(scripts.pourcentageMot(k2, self.listeVoc[k])))+"%")
                        if k2 != len(trad)-1:
                            self.affichageRecherche.insert(END, "\n")

    def bRechercher(self):
        self.boutonAbonnement.destroy()
        self.texte1["text"]="Recherche"
        self.numeroLecon.destroy()
        self.boutonAcceder.destroy()
        self.affichageRecherche = Text(self, bg="white", bd=0)
        if self.entreeRechercher.get() == "" or self.entreeRechercher.get() == " ":
            self.affichageRecherche.insert(END, "Veuillez entrer un mot")
        else:
            self.recherche(self.curseur, 0, self.limite+1)
            self.recherche(self.curseurPerso, self.limite+1, len(self.listeVoc))
        if self.affichageRecherche.get("1.0", 'end-1c') == "":
            self.affichageRecherche.insert(END, "Aucun résultat")
        self.affichageRecherche.config(state=DISABLED)
        self.affichageRecherche.grid(row=2, columnspan=2, pady=5)
        self.boutonRetour.grid(row=3, columnspan=2, pady=10)
        
    def frtojp(self, reponse):
        global score
        self.augmentationTotal[num]+=1
        if var_kanji.get()== 0:
            if reponse == jpKanji[num] or reponse == jpKana[num]:
                message2 = "Correct !"
                score+=1
                self.augmentationScore[num]+=1
            else:
                message2 = "Faux, la réponse est : " + jpKanji[num]
                if jpKanji[num] != jpKana[num]:
                    message2 = message2 + " / " + jpKana[num]
        if var_kanji.get() == 1:
            if reponse == jpKanji[num]:
                message2 = "Correct !"
                score+=1
                self.augmentationScore[num]+=1
            else:
                message2 = "Faux, la reponse est : " + jpKanji[num]
        return message2

    def jptofr(self, reponse):
        global score
        self.augmentationTotal[num]+=1
        if reponse == trad[num]:
            message2 = "Correct !"
            score+=1
            self.augmentationScore[num]+=1
        else:
            message2 = "Faux, la réponse est : " + trad[num]
        return message2

    def Acceder(self):
        global jpKanji, jpKana, trad, pourcentage
        jpKanji=[]
        jpKana=[]
        trad=[]
        pourcentage=[]
        self.numLecon = int(self.numeroLecon.curselection()[0])
        self.table=self.listeVoc[self.numLecon]
        self.boutonAbonnement.destroy()
        perso=0
        if self.numLecon>self.limite:
            self.curseurPerso.execute("SELECT MAX(id) FROM {}".format(self.listeVoc[self.numLecon]))
            longueur=self.curseurPerso.fetchone()[0]+1
            self.curseurPerso.execute("SELECT jpKanji, jpKana, trad FROM {}".format(self.listeVoc[self.numLecon]))
            for i in range (0, longueur):
                data=self.curseurPerso.fetchone()
                jpKanji.append(data[0])
                jpKana.append(data[1])
                trad.append(data[2])
                pourcentage.append(scripts.pourcentageMot(i, self.table))
        else:
            self.curseur.execute("SELECT MAX(id) FROM {}".format(self.table))
            longueur=self.curseur.fetchone()[0]+1
            self.curseur.execute("SELECT jpKanji, jpKana, trad FROM {}".format(self.table))
            for i in range (0, longueur):
                data=self.curseur.fetchone()
                jpKanji.append(data[0])
                jpKana.append(data[1])
                trad.append(data[2])
                pourcentage.append(scripts.pourcentageMot(i, self.table))

        self.numeroLecon.destroy()
        self.boutonAcceder.destroy()
        self.entreeRechercher.destroy()
        self.boutonRechercher.destroy()

        self.texte1["text"]=self.listeAffichage[self.numLecon]

        self.boutonTest = Button(self, text="Test", bg="red", fg="white", command=self.Test)
        self.boutonTest.grid(row=1, columnspan=2, pady=5)
        
        self.listeVoc = Text(self, bg="white", bd=0)
        for k in range (0, len(trad)):
            self.listeVoc.insert(END, jpKanji[k])
            if jpKanji[k] != jpKana[k]:
                self.listeVoc.insert(END, " / " + jpKana[k])
            self.listeVoc.insert(END, " : " + trad[k] + "     " + str(int(pourcentage[k]))+"%")
            if k != len(trad)-1:
                self.listeVoc.insert(END, "\n")
        self.listeVoc.grid(row=3, columnspan=2, pady=5)
        self.listeVoc.config(state=DISABLED)

        self.boutonRetour.grid(row=4, columnspan=2, pady=5)

    def Test(self):
        global var_kanji, testType
        self.boutonTest.destroy()
        self.listeVoc.destroy()
        self.boutonRetour.grid_forget()

        var_kanji = IntVar()
        self.caseKanji = Checkbutton(self, text="Mode Kanji seulement (si disponible)", variable=var_kanji, bg="white")
        self.caseKanji.grid(row=1, columnspan=2, pady=5)

        self.augmentationScore=[0]*len(jpKanji)
        self.augmentationTotal=[0]*len(jpKanji)

        testType = IntVar()
        self.testType_frtojp = Radiobutton(self, text="Français vers japonais", variable=testType, value=0, bg="white")
        self.testType_jptofr = Radiobutton(self, text="Japonais vers français (QCM)", variable=testType, value=1, bg="white")
        self.testType_frtojp.grid(row=2, column=0)
        self.testType_jptofr.grid(row=2, column=1)

        self.boutonDemarrer = Button(self, text="Démarrer", command=self.Demarrer, bg="red", fg="white")
        self.boutonDemarrer.grid(row=3, column=1, pady=10)
        self.boutonRetour.grid(row=3, column=0, pady=10)

    def Demarrer(self):
        global compteur, score, entree, var_QCM
        compteur, score= 0, 0
        self.testType_jptofr.destroy()
        self.testType_frtojp.destroy()
        self.caseKanji.destroy()
        self.boutonDemarrer.destroy()
        self.boutonRetour.grid_forget()
        self.boutonValider1 = Button(self, text="Valider", command=self.bValider1, bg="red", fg="white")
        self.boutonSuivant = Button(self, text="Suivant ->", command=self.pageSuivante, bg="red", fg="white")
        self.boutonValider = Button(self, text="Valider", command=self.bValider, bg="red", fg="white")
        entree = Entry(self)
        var_QCM = StringVar()
        self.QCM1 = Radiobutton(self, variable=var_QCM, bg="white")
        self.QCM2 = Radiobutton(self, variable=var_QCM, bg="white")
        self.QCM3 = Radiobutton(self, variable=var_QCM, bg="white")
        self.QCM4 = Radiobutton(self, variable=var_QCM, bg="white")
        self.texte2 = Label(self, bg="white")
        self.pageSuivante()

    def pageSuivante(self):
        global num, compteur
        self.boutonSuivant.grid_forget()
        entree.delete(0, 'end')
        self.texte2.grid_forget()
        if compteur < 10 :
            if testType.get() == 0:
                entree.bind("<Return>", self.valider)
                entree.grid(row=1, columnspan=2, pady=5)
                self.boutonValider1.grid(row=6, column=1, pady=15, padx=15)
                num = randint(0, len(trad)-1)
                while pourcentage[num]>randint(20, 120):
                      num = randint(0, len(trad)-1)
                self.texte1["text"] = trad[num]
            if testType.get() == 1:
                num = randint(0, len(trad)-1)
                while pourcentage[num]>randint(20, 120):
                      num = randint(0, len(trad)-1)
                self.texte1["text"] = jpKanji[num]
                if var_kanji.get() == 0 and jpKanji[num] != jpKana[num]:
                    self.texte1["text"] = jpKanji[num] + " / " + jpKana[num]
                trad2=list(trad)
                del trad2[num]
                if len(trad2)>2:
                    repQCM = sample(trad2, 3)
                else:
                    repQCM = list(trad2)
                repQCM.append(trad[num])
                shuffle(repQCM)
                self.QCM1["text"]=repQCM[0]
                self.QCM1["value"]=repQCM[0]
                try:
                    self.QCM2["text"]=repQCM[1]
                    self.QCM2["value"]=repQCM[1]
                    self.QCM3["text"]=repQCM[2]
                    self.QCM3["value"]=repQCM[2]
                    self.QCM4["text"]=repQCM[3]
                    self.QCM4["value"]=repQCM[3]
                except:
                    pass
                if self.QCM1["text"]!="":
                    self.QCM1.grid(row=1, columnspan=2, pady=5)
                if self.QCM2["text"]!="":
                    self.QCM2.grid(row=2, columnspan=2, pady=5)
                if self.QCM3["text"]!="":
                    self.QCM3.grid(row=3, columnspan=2, pady=5)
                if self.QCM4["text"]!="":
                    self.QCM4.grid(row=4, columnspan=2, pady=5)
                self.boutonValider.grid(row=6, column=1, pady=10, padx=10)
            compteur+=1
            self.boutonRetour.grid(row=6, column=0, pady=15, padx=15)
        else:
            entree.grid_forget()
            self.boutonRetour.forget()
            self.QCM1.grid_forget()
            self.QCM2.grid_forget()
            self.QCM3.grid_forget()
            self.QCM4.grid_forget()
            scripts.augmenterTotal(self.table, self.augmentationTotal)
            scripts.augmenterScore(self.table, self.augmentationScore)
            self.texte1["text"] = "Votre score est de {}/10".format(score)
            self.boutonRetour.grid(row=3, columnspan=2, pady=10)

    def valider (self, event):
        self.bValider1()

    def bValider1 (self):
        self.boutonValider1.grid_forget()
        reponse = entree.get()
        self.texte2["text"] = self.frtojp(reponse)
        entree.unbind("<Return>")
        self.texte2.grid(row=2, columnspan=2, pady=5)
        self.boutonSuivant.grid(row=6, column=1, pady=15, padx=15)

    def bValider (self):
        self.boutonValider.grid_forget()
        self.texte2["text"] = self.jptofr(var_QCM.get())
        self.texte2.grid(row=5, columnspan=2, pady=5)
        self.boutonSuivant.grid(row=6, column=1, pady=10, padx=10)

    def Retour(self):
        self.destroy()
        self.__init__(fenetre, self.vocabulaire, self.perso)

if netclient.checkTime():
    if netclient.internetOn():
        netclient.checkBDD()
vocabulaire=sqlite3.connect("Data/vocabulaire.db")
perso=sqlite3.connect("Data/perso.db")
fenetre = Tk()
fenetre.title("MinnaのNihongo")
fenetre.pack_propagate(False)
fenetre.resizable(width=False, height=False)

interface = Interface(fenetre, vocabulaire, perso)

interface.mainloop()
