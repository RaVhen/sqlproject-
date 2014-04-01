#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import sqlite3
import datetime as dt,datetime
#
#   Pour passer Ã  python 3 il suffit de changer Tkinter en tkinter.
#   On donne l'alias tk pour qu'il n'y ait rien Ã  modifier ailleurs
#   dans le code.
#
import Tkinter as tk
from Tkinter import *


#
#  Il faudra rajouter des fonctions Ã  sqlite. Elles seront importÃ©es ici.
#  On suppose ici que le fichier s'appelle mes_fonctions.py (il peut
#  prendre n'importe quel nom)
#
#import mes_fonctions

class Horaires_tk(tk.Tk):


    def __init__(self, parent, emplacement):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.configure(bg = 'lightblue')
        self.emplacement = emplacement
        self.createWidgets()
        self.initialize()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.configure(bg = 'lightblue')
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)         
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(0, weight=1)        
    
    def okd(self, variable, event=None):

        if not self.validate():
            return

        self.update_idletasks()
        name = variable
        print name
        result = name.split(", ")
        print result[1]
        if(result[1] != 'All'):
            self.depart.delete(0, END)
            self.depart.insert(0,result[1])
        self.cancel()

    def oka(self, variable, event=None):

        if not self.validate():
            return

        self.update_idletasks()
        name = variable
        print name
        result = name.split(", ")
        print result[1]
        self.arrivee.delete(0, END)
        self.arrivee.insert(0,result[1])
        self.cancel2()

    def cancel(self, event=None):
        self.reset()
        self.recherche()
        self.top.destroy()

    def cancel2(self, event=None):
        self.reset()
        self.recherche()
        self.right.destroy()  
  
    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

    def hide_me(event):
        event.widget.pack_forget()
        
    def ferme_fichier(self, event):
        self.conn.close()

    def initialize(self):
        # Ouverture du fichier sqlite, supposÃ© ici s'appeler vols.sqlite.
        # Noter que si le fichier n'existe pas il n'y aura pas d'erreur
        # Ã  l'ouverture, il sera automatiquement crÃ©Ã©, mais il ne contiendra
        # Ã©videmment rien.
        self.conn = sqlite3.connect(os.path.join(self.emplacement,
                                                 'data.sqlite'))
        #
        #  Ajouter ici les fonctions nÃ©cessaires Ã  sqlite
        #self.conn.create_function("nom dans SQL", nbre_de_parametres, fonction_python)

        # ==========================================================
        # Interface graphique. On crÃ©e une "grille" qui permet
        # de placer ses Ã©lÃ©ments faÃ§on bataille navale, en 
        # spÃ©cifiant ligne et colonne (numÃ©rotÃ©es Ã  partir de 0).
        # On crÃ©e deux "Frames" (conteneurs d'autres Ã©lÃ©ments
        # graphiques), une pour la saisie des donnÃ©es de recherche
        # (formulaire) et l'autre pour afficher la liste qui 
        # contiendra les Ã©lÃ©ments retrouvÃ©s de la base (resultat)
        # ==========================================================
        self.grid()
        #
        # Le premier paramÃ¨tre est le parent (l'Ã©lÃ©ment conteneur)
        # du nouvel Ã©lÃ©ment graphique. padx/pady spÃ©cifient la marge
        # entre la bordure de l'Ã©lÃ©ment graphique et les Ã©lÃ©ments qui
        # sont dedans.
        # On crÃ©e l'Ã©lÃ©ment, puis on le place en invoquant sa mÃ©thode
        # grid(). 
        #
        self.formulaire = tk.Frame(self, padx=5, pady=5)
        self.formulaire.grid(column=0, row=0)
        self.configure(background = 'lightblue')
        self.formulaire.configure(background = 'lightblue')
        #
        #  On attache Ã  l'Ã©vÃ¨nement <Destroy> (fermeture de la
        #  fenÃªtre) la mÃ©thode ferme_fichier() qui, comme son
        #  nom l'indique, ferme proprement le fichier sqlite.
        #  La mÃ©thode est associÃ©e au formulaire plutÃ´t qu'Ã 
        #  la fenÃªtre principale parce que sinon toute fermeture
        #  de fenÃªtre fermerait le fichier, y compris pour une 
        #  fenÃªtre d'erreur que l'on voudrait voir apparaÃ®tre.
        #  Quand le formulaire disparaÃ®t, c'est que le programme
        #  est vraiment terminÃ©.
        # 
        self.formulaire.bind("<Destroy>", self.ferme_fichier)
        resultat = tk.Frame(self, pady=10)
        resultat.grid(column=0, row=1)
        resultat.configure(bg = 'lightblue')

        # -----------------------------------------------------
        # "formulaire" contient sa propre grille. A l'intÃ©rieur,
        # on place des Ã©tiquettes (Label), des zones de saisie (Entry),
        # des boutons (Button). Chaque fois le premier paramÃ¨tre
        # spÃ©cifie l'Ã©lÃ©ment parent.
        #
        tk.Label(self.formulaire, text='De', background = 'lightblue').grid(column=0, row=0)
        self.depart = tk.Entry(self.formulaire)
        self.depart.grid(column=0,row=1)
        tk.Label(self.formulaire, text='A', background = 'lightblue').grid(column=1, row=0)
        self.arrivee = tk.Entry(self.formulaire)
        self.arrivee.grid(column=1,row=1)
    
        #
        # Par dÃ©faut les Ã©lÃ©ments sont centrÃ©s. Le paramÃ¨tre
        # optionnel "sticky" permet de modifier l'alignement,
        # avec des rÃ©fÃ©rences aux points cardinaux. N = vers le haut,
        # S = vers le bas, W = Ã  gauche, E = Ã  droite.
        #
        tk.Label(self.formulaire,
                      text='Départ le ', background = 'lightblue').grid(column=0,
                                              row=2,
                                              sticky=tk.E)
        #
        # Le paramÃ¨tre optionel width limite au nombre de 
        # caractÃ¨res Ã  entrer; font spÃ©cifie la police de caractÃ¨res.
        # Le reste est plus dÃ©licat:
        #   Par dÃ©faut, on met le modÃ¨le de format de date attendu
        # (AAAAMMJJ, on peut choisir autre chose). Pour que l'utilisateur
        # comprenne bien que c'est un modÃ¨le, on le met en gris (paramÃ¨tre
        # 'fg', pour 'ForeGround color'. L'ennui, c'est que l'on voudra
        # revenir au noir quand l'utilisateur tape sa date. On ne peut pas
        # changer la couleur avant que la fenÃªtre soit affichÃ©e. On triche
        # en disant qu'il faut appeler une mÃ©thode Ã  un instant prÃ©cis,
        # et c'est cette mÃ©thode qui fera le boulot; 'validate' prÃ©cise
        # quand la fonction sera appelÃ©e ('focusin' = quand on se positionne
        # dans la zone) et 'validatecommand' quelle est cette fonction.
        #
        self.date_depart = tk.Entry(self.formulaire,
                                         width=8,
                                    
                                         fg='darkgray',
                                         font=("Courier","10"),
                                         validate='focusin',
                                         validatecommand=self.prepare_date)
        # Le format pour aider
        self.date_depart.insert(0, 'AAAAMMJJ')
        self.date_depart.grid(column=1, row=2, sticky=tk.W)

        self.bouton_recherche = tk.Button(self.formulaire,
                                               text="Recherche", 
                                               command= self.recherche)
        self.bouton_recherche.grid(column=0,row=3, padx=10)
        self.bouton_RAZ = tk.Button(self.formulaire,
                                         text="Nouvelle Recherche",
                                         state=tk.DISABLED,
                                         command=self.remise_a_zero)
        self.bouton_RAZ.grid(column=1,row=3, padx=10)

        # -----------------------------------------------------
        # On prÃ©pare l'emplacement des rÃ©sultats, avec un en-tÃªte
        # et une liste que l'on pourra dÃ©rouler
        #
        entete = tk.Label(resultat,
                               text=format(format(' Vol', '6.6s')
                                   + ' ' + format('Départ', '20.20s')
                                   + ' ' + format('Arrivée', '20.20s')
                                   + ' ' + format('Durée', '10.10s')
                                   + ' ' + format('Compagnie Aérienne',
                                                  '20.20s')),
                               anchor='w',
                               font=('Courier', '12', 'bold'),
                               bg='darkred',
                               fg='White') 
        entete.pack(side=tk.TOP)
        #
        #  Pour balayer les resultats
        #
        ascenseur = tk.Scrollbar(resultat)
        ascenseur.pack(side=tk.RIGHT, fill=tk.Y)
        horizon = tk.Scrollbar(resultat)
        #horizon.pack(side=tk.BOTTOM, fill=tk.X)
        #
        #  Pour recevoir le rÃ©sultat de la requÃªte
        #
        self.donnees = tk.StringVar()
        self.liste_de_vols = tk.Listbox(resultat,
                                       yscrollcommand=ascenseur.set,
                                       xscrollcommand=horizon.set,
                                       bg='darkgray',
                                       height=10,
                                       width=75,
                                       
                                       font=("Courier","12"),
                                       listvariable=self.donnees)
        self.liste_de_vols.pack(side=tk.LEFT, fill=tk.BOTH, expand = 1)
        ascenseur.config(command=self.liste_de_vols.yview)
        #horizon.config(command=self.liste_de_vols.xview)
        #
        #   Diverses opÃ©rations dÃ©finissant si l'on peut 
        #  redimensionner la fenÃªtre, etc.
        #
        self.resizable(True,True)
        self.update()
         #self.liste_de_vols.resizable(True,True)
        self.liste_de_vols.update()
        self.geometry(self.geometry())       
        self.depart.focus_set()
        self.depart.selection_range(0, tk.END)
        #self.date_depart.config(fg='black')

    def prepare_date(self):
        #
        # Fonction appelÃ©e quand on se positionne sur la zone
        # oÃ¹ l'on saisit la date de dÃ©part. D'abord on efface
        # le contenu (qui peut n'Ãªtre que le format de date attendu),
        # puis on passe en noir (la zone est crÃ©Ã©e en gris)
        #
        self.date_depart.delete(0, tk.END)
        self.date_depart.config(fg='black')

    def recherche(self):
        #
        #  LA fonction intÃ©ressante ... Evidemment c'est Ã  vous
        #  de l'Ã©crire!
        #  On commencera par rÃ©cupÃ©rer le contenu des champs de
        #  saisie, vÃ©rifier au passage qu'ils sont bien dans le format
        #  attendu (date) ou Ã©ventuellement les transformer pour qu'ils
        #  soient comparables (majuscules/minuscules, etc) Ã  ce qui est
        #  dans les tables (ce genre de transformation se fait au choix 
        #  dans le langage de programmation ou en SQL, c'est un peu
        #  comme on le sent)
        #

        
        date = self.date_depart.get()
        
        if(len(date) >= 8 and date != 'AAAAMMJJ'):
            date = (int)(self.date_depart.get().replace('/',''))
            date = (int)(self.date_depart.get().replace('-',''))
            year = date/10000
            month = date/100 - year*100
            day = date - (year*10000 + month*100)

            stddate = str(year) + str(month) + str(day)
            jourdep = dt.datetime.strptime(stddate, '%Y%m%d').isoweekday()
	
        else:
            stddate = (str)(dt.date.today())
            jourdep = dt.datetime.strptime(stddate, '%Y-%m-%d').isoweekday()

        
        depart = self.depart.get();
        arrivee = self.arrivee.get();
        nbCityd = 0;
        nbCitya = 0;
        All = False
        cur = self.conn.cursor()
        if(len(depart) > 3):
            query = "Select IATA, Name, Country, (select count(City) from usedAirports where UPPER(City)=UPPER(?)) as nb_total, City from usedAirports where UPPER(City)=UPPER(?)"
            cur.execute(query,[depart,depart])
            result = cur.fetchmany()
            if(len(result) > 0):
                nbCityd = result[0][3]
                self.liste_de_vols.insert(tk.END,nbCityd)

        if(nbCityd > 1):
            OPTIONS = []
            
            while len(result) > 0:
                for row in result:
                        OPTIONS.append(row[1] +', '+ row[0]+', '+row[2]) 
                result = cur.fetchmany()
            OPTIONS.append(depart.title()+ ' tous aéroports'+', All')
            
                
            box = Tk()
            self.top = box
            variable = StringVar(box)
            variable.set(OPTIONS[0]) # default value
            w = apply(OptionMenu, (box, variable) + tuple(OPTIONS))
            w.pack()
            w = Button(box, text="OK", width=10, command=lambda: self.okd(variable.get()), default=ACTIVE)
            w.pack(side=LEFT, padx=5, pady=5)
            w = Button(box, text="Cancel", width=10, command=box.destroy)
            w.pack(side=LEFT, padx=5, pady=5)

            
        if(len(arrivee) > 3 and nbCityd <= 1):
            query = "Select IATA, Name, Country, (select count(City) from usedAirports where UPPER(City)=UPPER(?)) as nb_total from usedAirports where UPPER(City)=UPPER(?)"
            cur.execute(query,[arrivee,arrivee])
            result = cur.fetchmany()
            if(len(result) > 0):
                nbCitya = result[0][3]
                self.liste_de_vols.insert(tk.END,nbCitya)

        if(nbCitya > 1 and nbCityd <= 1):
            OPTIONS = []
            
            while len(result) > 0:
                for row in result:
                        OPTIONS.append(row[1] +', '+ row[0]+', '+row[2]) 
                result = cur.fetchmany()
             
            box2 = Tk()
            self.right = box2
            variable = StringVar(box2)
            variable.set(OPTIONS[0]) # default value
            w = apply(OptionMenu, (box2, variable) + tuple(OPTIONS))
            w.pack()
            w = Button(box2, text="OK", width=10, command=lambda: self.oka(variable.get()), default=ACTIVE)
            w.pack(side=LEFT, padx=5, pady=5)
            w = Button(box2, text="Cancel", width=10, command=box2.destroy)
            w.pack(side=LEFT, padx=5, pady=5)
            
            # Test des villes (aéroports avec le même nom de ville mais pas le même IATA
        # Test à la saisie ou test à la recherche ?
        
        if(nbCityd <= 1 and nbCitya <= 1):
            cur = self.conn.cursor()
            query = "SELECT * FROM flights f, usedAirports a1, usedAirports a2 where f.Departure = a1.IATA AND f.Arrival = a2.IATA AND f.Day_op like('%'||?||'%')";
            parameters = []
            parameters.append(jourdep) 
            if (len(depart) > 0 and len(arrivee) > 0):
                if(len(depart) <= 3):
                    query += " AND UPPER(Departure)=UPPER(?)"
                else:
                    query += " AND UPPER(a1.City)=UPPER(?)"
                if(len(arrivee) <= 3):
                    query += " AND UPPER(Arrival)=UPPER(?)"
                else:
                    query += " AND UPPER(a2.City)=UPPER(?)"
                parameters.append(depart)
                parameters.append(arrivee)
            #cur.execute("SELECT * FROM flights f, usedAirports a1, usedAirports a2 where f.Departure = a1.IATA AND f.Arrival = a2.IATA AND Departure=? AND Arrival=?",[depart,arrivee])
            if (len(arrivee) > 0 and len(depart) <= 0):
                if(len(arrivee) <= 3):
                    query += " AND UPPER(Arrival)=UPPER(?)"
                else:
                    query += " AND UPPER(a2.City)=UPPER(?)"
                parameters.append(arrivee)
            #cur.execute("SELECT * FROM flights f, usedAirports a1, usedAirports a2 where f.Departure = a1.IATA AND f.Arrival = a2.IATA AND Arrival=?",[arrivee])
            if (len(depart) > 0 and len(arrivee) <= 0):
                if(len(depart) <= 3):
                    query += " AND UPPER(Departure)=UPPER(?)"
                else:
                    query += " AND UPPER(a1.City)=UPPER(?)"
                parameters.append(depart)
            #cur.execute("SELECT * FROM flights f, usedAirports a1, usedAirports a2 where f.Departure = a1.IATA AND f.Arrival = a2.IATA AND Departure=?",[depart])
    #SELECT f.Departure, a1.City, f.Arrival, a2.City FROM flights f, usedAirports a1, usedAirports a2 where f.Departure = a1.IATA AND f.Arrival = a2.IATA

            if parameters != []:
                cur.execute(query, parameters)
            result = cur.fetchmany()
            found = 0
            display = ''
            while len(result) > 0:
                for row in result:
                    i = 0
                    display = ' '+format(str(row[6]), '4.4s') + ' '+format(str(row[10]), '17.17s') + ' '+format(str(row[17]), '17.17s') + '       '+format(str(row[7]), '10.10s')+ ' '+format(str(row[5]), '10.10s') + ' '
                    #while(i < len(row)):
                     #   display += str(row[i]) + ' ' 
                      #  i+=1
                    self.liste_de_vols.insert(tk.END,display)
                    found += 1
                    result = cur.fetchmany()
            if (found == 0 and nbCityd <= 1):
                self.liste_de_vols.insert(tk.END, '*** No flights found ***')
        
            if(nbCityd <= 1 and nbCitya <= 1):
        #
        #  AprÃ¨s avoir affichÃ©, on rÃ©cupÃ¨re tous les sous-Ã©lÃ©ments
        #  du formulaire pour les dÃ©sactiver. On rÃ©active ensuite
        #  le bouton "Nouvelle Recherche"
        #


                for element in self.formulaire.children.values():
                    element.config(state = tk.DISABLED)
                self.bouton_RAZ.config(state = tk.NORMAL)
        cur.close()


    def remise_a_zero(self):
        # PrÃ©paration pour une nouvelle recherche
        # On efface d'abord le rÃ©sultat prÃ©cÃ©dent.
        self.liste_de_vols.delete(0, tk.END)
        # On rÃ©-active tous les Ã©lÃ©ments du formulaire
        for element in self.formulaire.children.values():
            element.config(state = tk.NORMAL)
        # On efface le contenu des champs, et on remet le format
        # en gris pour la date.
        self.depart.delete(0, tk.END)
        self.arrivee.delete(0, tk.END)
        self.date_depart.delete(0, tk.END)
        self.date_depart.config(fg='darkgray')
        self.date_depart.insert(0, 'AAAAMMJJ')
        # Il faut rÃ©activer ce qui efface le modÃ¨le et
        # passe en noir, cela ne fonctionne qu'une fois
        # sinon.
        self.date_depart.config(validate='focusin')
        self.date_depart.config(validatecommand=self.prepare_date)
        # On dÃ©sactive le bouton "Nouvelle Recherche"
        self.bouton_RAZ.config(state = tk.DISABLED)
        # On positionne dans le champ correspondant Ã 
        # l'aÃ©roport de dÃ©part.
        self.depart.focus_set()
        
    def reset(self):
        # PrÃ©paration pour une nouvelle recherche
        # On efface d'abord le rÃ©sultat prÃ©cÃ©dent.
        self.liste_de_vols.delete(0, tk.END)
        # On rÃ©-active tous les Ã©lÃ©ments du formulaire
        #for element in self.formulaire.children.values():
            #element.config(state = tk.NORMAL)
        # On efface le contenu des champs, et on remet le format
        # en gris pour la date.
        #self.depart.delete(0, tk.END)
        #self.arrivee.delete(0, tk.END)
        #self.date_depart.delete(0, tk.END)
        #self.date_depart.config(fg='darkgray')
        #self.date_depart.insert(0, 'AAAAMMJJ')
        # Il faut rÃ©activer ce qui efface le modÃ¨le et
        # passe en noir, cela ne fonctionne qu'une fois
        # sinon.
        self.date_depart.config(validate='focusin')
        self.date_depart.config(validatecommand=self.prepare_date)
        # On dÃ©sactive le bouton "Nouvelle Recherche"
        self.bouton_RAZ.config(state = tk.DISABLED)
        # On positionne dans le champ correspondant Ã 
        # l'aÃ©roport de dÃ©part.
        self.depart.focus_set()

if __name__ == "__main__":
    #
    #  On suppose que le fichier sqlite est dans le
    #  mÃªme rÃ©pertoire que ce programme.
    #
    emplacement = os.path.dirname(sys.argv[0])
    app = Horaires_tk(None, emplacement)
    app.title('Horaires')
    app.mainloop()

