import mysql.connector
from tkinter import *

class Objekt:
	#die Attribute von Objekt sind nummer und name
	def __init__(self,name,nummer):
		self.name=name
		self.nummer=nummer

class Person:
	#die Attribute von Person sind vorname, name, strasse, wohnort, nummer
	def __init__(self,vorname,nachname,strasse,wohnort,kundennummer):
		self.vorname=vorname
		self.name=nachname
		self.strasse=strasse
		self.wohnort = wohnort
		self.nummer = kundennummer

	#Ausgabe der Daten einer Person
	def to_string(self):
		ausgabe =""
		if(self.vorname != ""):
			ausgabe = ausgabe + "Vorname: " + self.vorname
		if(self.name != ""):
			ausgabe = ausgabe + " Nachname: " + self.name
		if(self.strasse != ""):
			ausgabe = ausgabe + " Strasse: " + self.strasse
		if(self.wohnort != ""):
			ausgabe = ausgabe + " Wohnort: " + self.wohnort
		if(self.nummer != ""):
			ausgabe = ausgabe + " Kundennummer: " + self.nummer 
		return ausgabe

class Artikel:
	#die Attribute von Artikel sind name, nummer und preis 
	def __init__(self,artikelname,artikelnummer,preis):
		self.name=artikelname
		self.nummer=artikelnummer
		self.preis=preis
	
	#Daten eines Artikels werden ausgegeben
	def to_string(self):
		ausgabe=""
		if(self.name != ""):
			ausgabe = ausgabe + "Name: " + self.name
		if(self.nummer != ""):
			ausgabe = ausgabe + " Artikelnr.: " + self.nummer
		if(self.preis != ""):
			ausgabe = ausgabe + " Preis: " + str(self.preis)
		return ausgabe 
	

class Person_speichern_fenster:
	#diese Klasse enthaelt ein Fenster, in das man Vorname, Nachname, Strasse, Wohnort und Kundennummer eingeben kann
	#Nach Drücken des Knopfes "Speichern" werden diese Werte in eine Datenbank geschrieben
	def daten_speichern(self):
		try:
			#Verbindung zu mysql herstellen
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			
			#die Daten, die in das Fenster fenster eingegeben wurden, werden in die Tabelle personen_db geschrieben
			sp=("insert into personen_db (vorname,nachname,strasse,wohnort,kundennummer) values (%s,%s,%s,%s,%s)")
	
			sp_values=(self.vorname_text.get(),self.nachname_text.get(),self.strasse_text.get(),self.wohnort_text.get(),self.kundennummer_text.get())
			cursor.execute(sp,sp_values)
			#Veraenderungen an der Datenbank werden vorgenommen
			conn.commit()
			
			#Eingabefelder werden geleert
			self.vorname_text.delete(0,END)
			self.nachname_text.delete(0,END)
			self.strasse_text.delete(0,END)
			self.wohnort_text.delete(0,END)
			self.kundennummer_text.delete(0,END)

			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#Falls ein Fehler bei mysql auftritt, wird er hier ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster, in das die Personendaten eingegeben werden
		self.fenster = fenster
		#Titel des Fensters
		fenster.title("Person speichern")
	
		#Beschriftungen und Textfelder, in die die Personendaten eingegeben werden koennen, werden angelegt
		self.ueberschrift_label = Label(fenster,text="Personendaten eingeben:")
		self.vorname_label = Label(fenster,text="Vorname:")
		self.vorname_text = Entry(fenster,bd=5,width=40)
		
		self.nachname_label = Label(fenster,text="Nachname:")
		self.nachname_text = Entry(fenster,bd=5,width=40)
	
		self.strasse_label = Label(fenster,text="Strasse:")
		self.strasse_text = Entry(fenster,bd=5,width=40)
	
		self.wohnort_label = Label(fenster,text="Wohnort:")
		self.wohnort_text = Entry(fenster,bd=5,width=40)
	
		self.kundennummer_label = Label(fenster,text="Kundennummer:")
		self.kundennummer_text = Entry(fenster,bd=5,width=40)
		#wenn der Knopf bestaetigung_button gedrueckt wird, wird die Funktion daten_speichern ausgefuehrt,
		#in der die eingegebenen Personendaten in eine Datenbank geschrieben werden 
		self.bestaetigung_button = Button(fenster,text="Speichern",command=self.daten_speichern)

		#Beschriftungen, Knoepfe und Textfelder werden zum Fenster hinzugefuegt
		self.ueberschrift_label.pack()
		self.vorname_label.pack()
		self.vorname_text.pack()
		self.nachname_label.pack()
		self.nachname_text.pack()
		self.strasse_label.pack()
		self.strasse_text.pack()
		self.wohnort_label.pack()
		self.wohnort_text.pack()
		self.kundennummer_label.pack()
		self.kundennummer_text.pack()
		self.bestaetigung_button.pack()
	
		#fenster wartet auf die Eingabe eines Benutzers
		fenster.mainloop()



class Person_suchen_fenster:
	#Personen_suchen_fenster beinhaltet ein Fenster, in das man den Vornamen und den Nachnamen einer Person eingeben kann
	#Nach Drücken des Knopfes "Suchen" werden dann Personen mit diesem Vornamen oder Nachnamen in einer Datenbank gesucht
	def person_suchen(self):
		try:
			#Verbindung zu mysql wird hergestellt
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			#das Textfeld, das die Suchergebnisse enthaelt, wird fuer eine neue Suchanfrage geleert
			self.ausgabe.delete('1.0',END)

			#Wenn Vorname und Nachname einer Person eingegeben wurden, werden in der Tabelle personen_db alle Personen
			#gesucht, die diesen Nachnamen und diesen Vornamen hat
			if(self.vorname_text.get() != "" and self.nachname_text.get() != ""):
				sup = ("Select vorname,nachname,strasse,wohnort,kundennummer from personen_db where vorname = %s and nachname = %s")
				sup_values=(self.vorname_text.get(),self.nachname_text.get())
				result = cursor.execute(sup,sup_values)
				rows = cursor.fetchall()

				for (vorname,nachname,strasse,wohnort,kundennummer) in rows:
					#Ausgabe der Suchergebnisse
					p = Person(vorname,nachname,strasse,wohnort,kundennummer)
					self.ausgabe.insert(INSERT,p.to_string() +"\n")
			
			#Wenn nur der Vorname eingegeben wurde, werden alle Personen in personen_db mit diesem Vornamen gesucht
			if(self.vorname_text.get() != "" and self.nachname_text.get() == ""):
				sup = ("Select vorname,nachname,strasse,wohnort,kundennummer from personen_db where vorname = '{}'".format(self.vorname_text.get()))
				result = cursor.execute(sup)
				rows = cursor.fetchall()

				for (vorname,nachname,strasse,wohnort,kundennummer) in rows:
					p = Person(vorname,nachname,strasse,wohnort,kundennummer)
					self.ausgabe.insert(INSERT,p.to_string() +"\n")
			
			#Wenn nur der Nachname eingegeben wurde, werden alle Personen in personen_db mit diesem Nachnamen gesucht
			if(self.vorname_text.get() == "" and self.nachname_text.get() != ""):
				sup = ("Select vorname,nachname,strasse,wohnort,kundennummer from personen_db where nachname = '{}'".format(self.nachname_text.get()))
				result = cursor.execute(sup)
				rows = cursor.fetchall()

				for (vorname,nachname,strasse,wohnort,kundennummer) in rows:
					p = Person(vorname,nachname,strasse,wohnort,kundennummer)
					self.ausgabe.insert(INSERT,p.to_string() +"\n")
			
			#Wenn weder Vorname noch Nachname eingegeben wurde, werden alle Personen aus personen_db ausgegeben
			if(self.vorname_text.get() == "" and self.nachname_text.get() == ""):
				sup = ("Select vorname,nachname,strasse,wohnort,kundennummer from personen_db")
				result = cursor.execute(sup)
				rows = cursor.fetchall()

				for (vorname,nachname,strasse,wohnort,kundennummer) in rows:
					p = Person(vorname,nachname,strasse,wohnort,kundennummer)
					self.ausgabe.insert(INSERT,p.to_string() +"\n")
					



			
			#Textfelder werden geleert
			self.vorname_text.delete(0,END)
			self.nachname_text.delete(0,END)
			
			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster, in das Vorname und Nachname einer Person eigegeben werden koennen
		self.fenster = fenster
		fenster.title("Person suchen")
		
		#Knopf, Schriftzuege und Textfelder werden fuer fenster angelegt
		self.ueberschrift_label = Label(fenster,text="Personendaten eingeben:")
		self.vorname_label = Label(fenster,text="Vorname:")
		self.vorname_text = Entry(fenster,bd=5,width=40)
		
		self.nachname_label = Label(fenster,text="Nachname:")
		self.nachname_text = Entry(fenster,bd=5,width=40)
		
		self.ausgabe = Text(fenster)
		self.scrollBar = Scrollbar(fenster)
		self.scrollBar.config(command=self.ausgabe.yview)
		self.ausgabe.config(yscrollcommand=self.scrollBar.set)
		
	
		#wenn bestaetigung_button gedrueckt wird, wird die Funktin person_suchen ausgefuehrt 
		self.bestaetigung_button = Button(fenster,text="Suchen",command=self.person_suchen)

		#Knopf, Schriftzuege und Textfelder werden zu fenster hinzugefuegt
		self.ueberschrift_label.pack()
		self.vorname_label.pack()
		self.vorname_text.pack()
		self.nachname_label.pack()
		self.nachname_text.pack()
		self.bestaetigung_button.pack()
		self.ausgabe.pack(expand=Y)
		self.scrollBar.pack(side=RIGHT, fill=Y)
	
		#fenster wartet auf Benutzereingabe
		fenster.mainloop()



class Artikel_speichern_fenster:
	#Artikel_speichern_fenster beinhaltet ein Fenster fenster, in das Artikelname, Artikelnummer und der Preis eines Artikel 
	#eingegeben werden koennen. Diese Artikeldaten werden nach Druecken auf den Knopf "Speichern" zu einer Datenbank hinzugefuegt
	def daten_speichern(self):
		try:
			#Verbindung zu mysql wird hergestellt
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			#die Werte, die man in das Fenster fenster eingeben kann, werden
			#in die Tabelle artikel_db geschrieben 
			sp=("insert into artikel_db (name,nummer,preis) values (%s,%s,%s)")
	
			sp_values=(self.name_text.get(),self.nummer_text.get(),self.preis_text.get())
			cursor.execute(sp,sp_values)
			#Veraenderungen an der Datenbank werden ausgefuehrt
			conn.commit()
			
			#Textfelder werden geleeert
			self.name_text.delete(0,END)
			self.nummer_text.delete(0,END)
			self.preis_text.delete(0,END)

			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#falls ein Fehler bei mysql auftritt, wird eine Fehlermeldung ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster fenster wird angelegt
		self.fenster = fenster
		fenster.title("Artikel speichern")
	
		#Knopf, Schriftzuege und Textfelder fuer fenster werden angelegt
		self.ueberschrift_label = Label(fenster,text="Artikeldaten eingeben:")
		self.name_label = Label(fenster,text="Artikelname:")
		self.name_text = Entry(fenster,bd=5,width=40)
		
		self.nummer_label = Label(fenster,text="Artikelnummer:")
		self.nummer_text = Entry(fenster,bd=5,width=40)
	
		self.preis_label = Label(fenster,text="Preis:")
		self.preis_text = Entry(fenster,bd=5,width=40)
	
		#falls bestaetigung_button gedrueckt wird, wird die Funktion daten_speichern ausgefuehrt
		self.bestaetigung_button = Button(fenster,text="Speichern",command=self.daten_speichern)


		#Knopf, Schriftzuege und Textfelder werden zu fenster hinzugefuegt
		self.ueberschrift_label.pack()
		self.name_label.pack()
		self.name_text.pack()
		self.nummer_label.pack()
		self.nummer_text.pack()
		self.preis_label.pack()
		self.preis_text.pack()
		self.bestaetigung_button.pack()
	
		#fenster wartet auf Benutzereingaben
		fenster.mainloop()

class Artikel_suchen_fenster:
	#Artikel_suchen_fenster beinhaltet ein Fenster fenster, in das ein Artikelname eingegeben werden kann.
	#Nach Drücken auf den Knopf "Suchen" werden in einer Datenbank alle Artikel gesucht, die diesen Artikelnamen haben
	def suchen(self):
		try:
			#Verbindung zu mysql wird hergestellt
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			#das Textfeld ausgabe wird geleert fuer die neue Suchanfrage
			self.ausgabe.delete('1.0',END)

			#Wenn ein Artikelname eingegeben wurde, werden alle Artikel in der Tabelle artikel_db gesucht, die
			#diesen Artikelname haben
			if(self.name_text.get() != ""):
				sup = ("Select name,nummer,preis from artikel_db where name = '{}'".format(self.name_text.get()))
				result = cursor.execute(sup)
				rows = cursor.fetchall()

				for (name,nummer,preis) in rows:
					#Ausgabe der Ergebnisse
					a = Artikel(name,nummer,preis)
					self.ausgabe.insert(INSERT,a.to_string() +"\n")
			
			#Wenn kein Artikelname eingegeben wurde, werden alle Artikel in der Tabelle artikel_db ausgegeben
			else:
				sup = ("Select name,nummer,preis from artikel_db")
				result = cursor.execute(sup)
				rows = cursor.fetchall()

				for (name,nummer,preis) in rows:
					a = Artikel(name,nummer,preis)
					self.ausgabe.insert(INSERT,a.to_string() +"\n")


			
			#Textfeld wird geleert
			self.name_text.delete(0,END)
			
			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#falls ein Fehler bei mysql auftritt, wird dieser hier ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster fenster wird angelegt
		self.fenster = fenster
		
		#Titel, Schriftzuege und Textfelder fuer fenster werden angelegt
		fenster.title("Artikel suchen")
		
		
		self.ueberschrift_label = Label(fenster,text="Artikeldaten eingeben:")
		self.name_label = Label(fenster,text="Artikelname:")
		self.name_text = Entry(fenster,bd=5,width=40)
		
		
		self.ausgabe = Text(fenster)
		self.scrollBar = Scrollbar(fenster)
		self.scrollBar.config(command=self.ausgabe.yview)
		self.ausgabe.config(yscrollcommand=self.scrollBar.set)
		
		#wenn bestaetigung_button gedrueckt wird, wird die Funktion suchen ausgefuehrt
		self.bestaetigung_button = Button(fenster,text="Suchen",command=self.suchen)

		#Schriftzuege und Textfelder werden zu fenster hinzugefuegt
		self.ueberschrift_label.pack()
		self.name_label.pack()
		self.name_text.pack()
		self.bestaetigung_button.pack()
		self.ausgabe.pack(expand=Y)
		self.scrollBar.pack(side=RIGHT, fill=Y)
	
		#fenster wartet auf Benutzereingabe
		fenster.mainloop()


class Bestellung_speichern_fenster:
	#Bestellung_speichern_fenster beinhaltet ein Fenster fenster, in das die Kundennummer von der Person, die bestellt,
	#die Artikelnummer des Artikels, der bestellt wird, und
	#die Anzahl, wie oft der Artikel mit dieser Artikelnummer bestellt werden soll, eingegeben werden koennen
	#nach Druecken des Knopfes "Speichern" wird die Besetellung in einer Datenbank gespeichert 
	def daten_speichern(self):
		try:
			#Verbindung mit mysql herstellen
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			#Kundennummer, Artikelnummer und Anzahl, die in fenster eingegeben wurden, werden in einer 
			#Datenbank gespeichert
			sp=("insert into bestellungen_db (kundennummer,artikelnummer,anzahl) values (%s,%s,%s)")
	
			sp_values=(self.knr_text.get(),self.anr_text.get(),self.anzahl_text.get())
			cursor.execute(sp,sp_values)
			#Veraenderung an der Datenbank werden vorgenommen
			conn.commit()
			
			#Textfelder werden geleert
			self.knr_text.delete(0,END)
			self.anr_text.delete(0,END)
			self.anzahl_text.delete(0,END)

			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#Fehler, die bei mysql auftreten, werden hier ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster fenster wird angelegt
		self.fenster = fenster
		fenster.title("Bestellung speichern")
	
		#Schriftzuege und Textfelder fuer fenster werden angelegt
	
		self.ueberschrift_label = Label(fenster,text="Daten einer Bestellung eingeben:")
		self.knr_label = Label(fenster,text="Kundennummer:")
		self.knr_text = Entry(fenster,bd=5,width=40)
		
		self.anr_label = Label(fenster,text="Artikelnummer:")
		self.anr_text = Entry(fenster,bd=5,width=40)
	
		self.anzahl_label = Label(fenster,text="Anzahl:")
		self.anzahl_text = Entry(fenster,bd=5,width=40)
	
		#wenn bestaetingung_button gedrueckt wird, wird die Funktion daten_speichern ausgefuehrt
		self.bestaetigung_button = Button(fenster,text="Speichern",command=self.daten_speichern)

		self.ueberschrift_label.pack()
		self.knr_label.pack()
		self.knr_text.pack()
		self.anr_label.pack()
		self.anr_text.pack()
		self.anzahl_label.pack()
		self.anzahl_text.pack()
		self.bestaetigung_button.pack()
	
		#fenster wartet auf Benutzereingabe
		fenster.mainloop()

class Bestellung_person_suchen_fenster:
	#Bestellungen_person_suchen_fenster beinhaltet ein Fenster fenster, in das die Kundennummer einer Person eingegeben werden kann
	#Wenn der Knopf "Suchen" gedrueckt wird, werden alle Bestellungen gesucht, die die Person mit dieser Kundennummer bestellt hat
	def suchen(self):
		try:
			#Verbindung mit mysql wird hergestellt
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			#Textfeld fuer die ausgabe wird geleert fuer die neue Suchanfrage
			self.ausgabe.delete('1.0',END)

			#Wenn eine Kundennummer eingegeben wurde, werden alle Bestellungen, die die Person mit dieser Kundennummer bestellt hat,
			# mit Angabe des Artikels, Anzahl und Gesamtpreis angezeigt
			if(self.knr_text.get() != ""):
				finde_bestellung = """select artikel_db.name, artikel_db.preis, bestellungen_db.anzahl, 
						round(artikel_db.preis*bestellungen_db.anzahl,2) as gesamtpreis from artikel_db left outer join bestellungen_db on 
	 					bestellungen_db.artikelnummer = artikel_db.nummer where bestellungen_db.kundennummer = '{}'
						order by artikel_db.name""".format(self.knr_text.get())
				result = cursor.execute(finde_bestellung)
				rows = cursor.fetchall()
				
				#in summe wird der Preis fuer alle gefundenen Bestellungen gespeichert
				summe=0

				for (name,preis,anzahl,gesamtpreis) in rows:
					#gesamtpreis enthaelt den Gesamtpreis einer Bestellung
					summe += gesamtpreis
					self.ausgabe.insert(INSERT,"Name: " + name + " Einzelpreis: " + str(preis) + " Anzahl: " + str(anzahl) + " Gesamtpreis: " +
					str(gesamtpreis) +"\n")
				self.ausgabe.insert(INSERT,"Summe: " + str(format(summe,'.2f')))
			
			else:
				print("Es wurde keine Kundennummer eingegeben")


			
			#Textfeld wird geleert
			self.knr_text.delete(0,END)
			
			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#mysql-Fehler werden hier ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster fenster wird angelegt
		self.fenster = fenster
		fenster.title("Bestellungen einer Person suchen")
		
		#Textfelder und Schriftzuege fuer fenster werden angelegt
		self.ueberschrift_label = Label(fenster,text="Kundennummer einer Person eingeben:")
		self.knr_label = Label(fenster,text="Kundennummer:")
		self.knr_text = Entry(fenster,bd=5,width=40)
		
		
		self.ausgabe = Text(fenster)
		self.scrollBar = Scrollbar(fenster)
		self.scrollBar.config(command=self.ausgabe.yview)
		self.ausgabe.config(yscrollcommand=self.scrollBar.set)
		
	
		#wenn bestaetigung_button gedrueckt wird, dann wird die Funktion suchen ausgefuehrt
		self.bestaetigung_button = Button(fenster,text="Suchen",command=self.suchen)

		#Knopf, Textfelder und Schriftzuege werden zu fenster hinzugefuegt
		self.ueberschrift_label.pack()
		self.knr_label.pack()
		self.knr_text.pack()
		self.bestaetigung_button.pack()
		self.ausgabe.pack(expand=Y)
		self.scrollBar.pack(side=RIGHT, fill=Y)
	
		#fenster wartet auf eine Benutzerangabe
		fenster.mainloop()

class Bestellung_artikel_suchen_fenster:
	# Bestellung_artikel_suchen_fenster enthaelt ein Fenster fenster, in das die Artikelnummer eines Artikels eingegeben werden kann
	#Wenn der Knopf "Suchen" gedrueckt wird, dann werden alle Bestellungen in einer Datenbank gesucht, in welchen der Artikel mit dieser
	#Artikelnummer bestellt wurde
	def suchen(self):
		try:
			#Verbindung zu mysql wird hergestellt
			conn = mysql.connector.connect(user='root',password='',host='localhost',database='Bestellungen')
			cursor = conn.cursor()
			
			#Textfeld fuer die Ausgabe wird fuer die neue Suchanfrage geleert
			self.ausgabe.delete('1.0',END)

			#Wenn eine Artikelnummer eingegeben wurde, werden alle Bestellungen in der Tabelle bestellungen_db gesucht, in welcher
			#dieser Artikel bestellt wurde. Fuer jeder Bestellung wird der Name der Person, welche bestellt hat, die Anzahl und der Gesamtpreis
			#angezeigt
			if(self.anr_text.get() != ""):
				#Preis des ausgewaehlten Artikels wird ermittelt
				finde_preis = "select preis from artikel_db where nummer = '{}'".format(self.anr_text.get())
				result = cursor.execute(finde_preis)
				preis = cursor.fetchall()
				finde_bestellung = """select personen_db.nachname, personen_db.vorname, bestellungen_db.anzahl from personen_db left outer join
						    bestellungen_db on personen_db.kundennummer = bestellungen_db.kundennummer where bestellungen_db.artikelnummer 
						    like '{}'""".format(self.anr_text.get()) 
				result = cursor.execute(finde_bestellung)
				rows = cursor.fetchall()
				
				#in summe wird der Preis aller gefundenen Bestellungen gespeichert
				summe=0
				for (nachname,vorname,anzahl) in rows:
					gesamtpreis = 1
					gesamtpreis = preis[0][0]*anzahl
					summe += gesamtpreis
					self.ausgabe.insert(INSERT,"Name: " + nachname + " " + vorname + " Anzahl: " + str(anzahl) + " Gesamtpreis: " + 
					str(format(gesamtpreis,'.2f')) + "\n")
				self.ausgabe.insert(INSERT,"Summe: " + str(format(summe,'.2f')))
			
			else:
				print("Es wurde keine Kundennummer eingegeben")


			
			#Textfeld wird geleert
			self.anr_text.delete(0,END)
			
			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#mysql-Fehler werden hier ausgegeben
			print("Fehler: {}".format(err))
	

	def __init__(self,fenster):
		#Fenster fenster wird angelegt
		self.fenster = fenster
		fenster.title("Bestellungen eines Artikels suchen")
		
		#Knopf, Beschriftungen und Textfelder fuer fenster werden angelegt
		self.ueberschrift_label = Label(fenster,text="Artikelnummer eines Artikels eingeben:")
		self.anr_label = Label(fenster,text="Artikelnummer:")
		self.anr_text = Entry(fenster,bd=5,width=40)
		
		
		self.ausgabe = Text(fenster)
		self.scrollBar = Scrollbar(fenster)
		self.scrollBar.config(command=self.ausgabe.yview)
		self.ausgabe.config(yscrollcommand=self.scrollBar.set)
		
	
		#wenn bestaetingung_button gedrueckt wird, wird die Funktion suchen ausgefuehrt
		self.bestaetigung_button = Button(fenster,text="Suchen",command=self.suchen)

		self.ueberschrift_label.pack()
		self.anr_label.pack()
		self.anr_text.pack()
		self.bestaetigung_button.pack()
		self.ausgabe.pack(expand=Y)
		self.scrollBar.pack(side=RIGHT, fill=Y)
	
		#fenster wartet auf Benutzereingabe
		fenster.mainloop()

class Hauptfenster:
	#Hauptfenster enthaelt ein Menue, mit dem man die anderen Fenster aufrufen kann
	
	#die nachfolgenden Funktionen oeffnen verschiedene Fenster; je nachdem welches Menueelement
	#angeklickt wurde, wird eine dieser Funktionen ausgefuehrt 
	def sup_oeffne_fenster(self):
		fenster = Tk()
		sup_fenster = Person_suchen_fenster(fenster)

	def sp_oeffne_fenster(self):
		fenster = Tk()
		sp_fenster = Person_speichern_fenster(fenster)
	
	def sa_oeffne_fenster(self):
		fenster = Tk()
		sa_fenster = Artikel_speichern_fenster(fenster)
	
	def sua_oeffne_fenster(self):
		fenster = Tk()
		sua_fenster = Artikel_suchen_fenster(fenster)
		
	def sb_oeffne_fenster(self):
		fenster = Tk()
		sb_fenster = Bestellung_speichern_fenster(fenster)
	
	def bp_oeffne_fenster(self):
		fenster = Tk()
		bp_fenster = Bestellung_person_suchen_fenster(fenster)
	
	def ba_oeffne_fenster(self):
		fenster = Tk()
		ba_fenster = Bestellung_artikel_suchen_fenster(fenster)

	def db_anlegen(self):
		try:
			#Verbindung mit mysql herstellen
			conn = mysql.connector.connect(user='root',password='',host='localhost')
			cursor = conn.cursor()
			#Datenbank Bestellungen wird angelegt, falls diese noch nicht vorhanden ist
			cursor.execute("CREATE DATABASE IF NOT EXISTS Bestellungen")
			#Datenbank Bestellungen wird ausgewaehlt
			cursor.execute("use Bestellungen")
	
			#die Tabelle bestellungen_db wird angelegt, falls diese noch nicht existiert
			create_table = """CREATE TABLE IF NOT EXISTS bestellungen_db (
					nr INT AUTO_INCREMENT PRIMARY KEY,
					kundennummer VARCHAR(30),
					artikelnummer VARCHAR(30),
					anzahl FlOAT) """
			cursor.execute(create_table)

			#Tabelle artikel_db wird angelegt, falls diese noch nicht existiert
			create_table = """CREATE TABLE IF NOT EXISTS artikel_db (
					nr INT AUTO_INCREMENT PRIMARY KEY,
					name VARCHAR(30),
					nummer VARCHAR(30),
					preis FLOAT) """
			cursor.execute(create_table)

			#die Tabelle personen_db wird erstellt, falls sie noch nicht existiert
			create_table = """CREATE TABLE IF NOT EXISTS personen_db ( 
					nr INT AUTO_INCREMENT PRIMARY KEY, 
					vorname VARCHAR(30),
					nachname VARCHAR(30),
					strasse VARCHAR(30),
					wohnort VARCHAR(30), 
					kundennummer VARCHAR(30)) """
			cursor.execute(create_table)

			cursor.close()
			conn.close()
		

		except mysql.connector.Error as err:
			#Fehler, die bei mysql auftreten, werden hier ausgegeben
			print("Fehler: {}".format(err))
	



	def __init__(self,fenster):
		#ein Fenster fenster wird erstellt
		self.fenster = fenster
		#Titel des Fensters
		fenster.title("Bestellungen")
		#minimale Groesse von Fenster wird festgestellt
		fenster.minsize(width=500,height=500)

		#Menue mit Menuepunkten fuer fenster wird angelegt
		self.menuleiste = Menu(fenster)

		#je nachdem, welche Menuepunkte ausgewaehlt werden, wird eine der oben definierten Funktionen ausgefuehrt
		self.person_menu = Menu(self.menuleiste,tearoff=0)
		self.person_menu.add_command(label="Person suchen", command=self.sup_oeffne_fenster)
		self.person_menu.add_command(label="Peson speichern",command=self.sp_oeffne_fenster)
		self.person_menu.add_separator()
		self.menuleiste.add_cascade(label="Personen bearbeiten", menu=self.person_menu)

		
		self.artikel_menu = Menu(self.menuleiste,tearoff=0)		
		self.artikel_menu.add_command(label="Artikel suchen", command=self.sua_oeffne_fenster)
		self.artikel_menu.add_command(label="Artikel speichern",command=self.sa_oeffne_fenster)
		self.artikel_menu.add_separator()
		self.menuleiste.add_cascade(label="Artikel bearbeiten", menu=self.artikel_menu)
	
		self.bestellung_menu = Menu(self.menuleiste,tearoff=0)		
		self.bestellung_menu.add_command(label="Bestellung speichern", command=self.sb_oeffne_fenster)
		self.bestellung_menu.add_command(label="Bestellungen einer Person suchen",command=self.bp_oeffne_fenster)
		self.bestellung_menu.add_command(label="Bestellungen eines Artikels suchen",command=self.ba_oeffne_fenster)
		self.bestellung_menu.add_separator()
		self.menuleiste.add_cascade(label="Bestellungen bearbeiten", menu=self.bestellung_menu)

		fenster.config(menu=self.menuleiste)

		self.db_anlegen()

		#in der Ereignisschleife auf Eingabe des Benutzers warten
		fenster.mainloop()

#ein Hauptfenster wird angelegt
fenster = Tk()
hauptfenster = Hauptfenster(fenster)


