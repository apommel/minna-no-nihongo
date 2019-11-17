import sqlite3

def norm(chaine):
    sortie=str()
    for k in range (0, len(chaine)):
        caractere=chaine[k].lower()
        if caractere=="à" or caractere=="â" or caractere=="ä":
            caractere="a"
        elif caractere=="œ":
            caractere="oe"
        elif caractere=="é" or caractere=="è" or caractere=="ê" or caractere=="ë":
            caractere="e"
        elif caractere=="ç":
            caractere="c"
        elif caractere=="î" or caractere=="ï" or caractere=="ì":
            caractere="i"
        elif caractere=="ô" or caractere=="ö" or caractere=="ò":
            caractere="o"
        elif caractere=="ù" or caractere=="û" or caractere=="ü":
            caractere="u"
        elif caractere=="ÿ":
            caractere="y"
        sortie=sortie+caractere
    return sortie

def norm2(chaine):
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

def importer(liste, nom):
    conn = sqlite3.connect('Data/perso.db')
    curseur=conn.cursor()
    if Existe(nom):
        return("Erreur, une de vos listes a déjà le même nom")
    else:
        curseur.execute("""
CREATE TABLE IF NOT EXISTS {}(
id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
liste TEXT,
jpKanji TEXT,
jpKana TEXT,
trad TEXT
)
""".format(norm2(nom)))
        conn.commit()
        i=0
        while i<len(liste[0]):
            curseur.execute("""
INSERT INTO {}(id, liste, jpKanji, jpKana, trad) VALUES(?, ?, ?, ?, ?)""".format(norm(nom)), (i, nom, liste[0][i], liste[1][i], liste[2][i]))
            i+=1
        conn.commit()
        return("Abonnement validé")

def unsubscribe(liste):
    conn = sqlite3.connect('Data/perso.db')
    c1 = conn.cursor()
    conn2 = sqlite3.connect('Data/log.db')
    c2 = conn2.cursor()
    sortie="Echec du désabonnement"
    try:
        c1.execute("DROP TABLE {}".format(liste))
        conn.commit()
        sortie="Vous vous êtes désabonné"
    except:
        pass
    try:
        c2.execute("DROP TABLE {}".format(liste))
        conn2.commit()
    except:
        pass
    return(sortie)

def Existe(liste):
    conn = sqlite3.connect('Data/perso.db')
    curseur=conn.cursor()
    check=sqlite3.connect("Data/vocabulaire.db")
    curseurCheck=check.cursor()
    curseurCheck.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence';")
    liste1=curseurCheck.fetchall()
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table' and name!='sqlite_sequence';")
    liste2=curseur.fetchall()
    existe=False
    for i in range (0, len(liste1)):
        if norm2(liste) in liste1[i]:
            existe=True
    for i in range (0, len(liste2)):
        if norm2(liste) in liste2[i]:
            existe=True
    return(existe)

def augmenterTotal(liste, augmentationTotal):
    scoreDB=sqlite3.connect("Data/log.db")
    curseurDB=scoreDB.cursor()
    curseurDB.execute("""
CREATE TABLE IF NOT EXISTS {}(
id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
score INTEGER,
total INTEGER
)
""".format(liste))
    curseurDB.execute("SELECT COUNT(id) FROM {}".format(liste))
    i=curseurDB.fetchone()[0]
    while i<len(augmentationTotal):
        curseurDB.execute("INSERT INTO {}(id, score, total) VALUES(?, 0, 0)".format(liste), (i,))
        i+=1
    for ID in range(0, len(augmentationTotal)):
        curseurDB.execute("SELECT total FROM {} where id=?".format(liste), (ID,))
        total=curseurDB.fetchone()[0]+augmentationTotal[ID]
        curseurDB.execute("UPDATE {} SET total=? where id=?".format(liste), (total, ID))
    scoreDB.commit()

def augmenterScore(liste, augmentationScore):
    scoreDB=sqlite3.connect("Data/log.db")
    curseurDB=scoreDB.cursor()
    for ID in range(0, len(augmentationScore)):
        curseurDB.execute("SELECT score FROM {} where id=?".format(liste), (ID,))
        score=curseurDB.fetchone()[0]+augmentationScore[ID]
        curseurDB.execute("UPDATE {} SET score=? where id=?".format(liste), (score, ID))
    scoreDB.commit()

def pourcentageLecon(liste):
    scoreDB=sqlite3.connect("Data/log.db")
    curseurDB=scoreDB.cursor()
    resultat=0
    try:
        curseurDB.execute("SELECT COUNT(id) FROM {}".format(liste))
        total=curseurDB.fetchone()[0]
        for ID in range (0, total):
            resultat=resultat+pourcentageMot(ID, liste)
        resultat=resultat/total
    except:
        pass
    return(resultat)
    

def pourcentageMot(ID, liste):
    scoreDB=sqlite3.connect("Data/log.db")
    curseurDB=scoreDB.cursor()
    try:
        curseurDB.execute("SELECT score, total FROM {} WHERE total!=0 and id=?".format(liste), (ID,))
        resultat=curseurDB.fetchone()
        return(100*resultat[0]/resultat[1])
    except:
        return(0)

    
    

