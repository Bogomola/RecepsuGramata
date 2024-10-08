from datubaze import *
from testesana import *

import sqlite3


conn = sqlite3.connect('receptes.db')
cursor = conn.cursor()

############## Funkcija, lai parādītu sākotnēju izvēlni#######################
def izvelne():
    while True:
        print()
        print("🍒🍏🍌🍎"*7)
        print("🍏"+" " * 15 + "🍽️  Recepšuu gramāta  🍽️"+" "*15+"🍌")
        print("🍌 "+"="*50+" 🍏")
        print("🍎  1. Pievienot jaunu recepti ➕"+" "*21+"🍒")
        print("🍌  2. Apskatīt visas receptes 👁"+" "*22+"🍎")
        print("🍒  3. Iziet✌️"+" "*41+"🍌")
        print("🍏🍌🍎🍒"*7)
        izvele = input("\nIevadi izvēles numuru: ")
        
        if izvele == '1':
            pievienot_recepti()
        elif izvele == '2':
            paradi_receptes()
        elif izvele == '3':
            print("Programma beidzas.")
            print("🍒🍏🍌🍎"*10)
            break
        else:
            print("Nepareiza izvēle. Mēģiniet vēlreiz!")

##################### Funkcija, lai pievienotu jaunu recepti###############################
def pievienot_recepti():
    nosaukums = input("Ievadi receptes nosaukumu: ").strip()
    if not nosaukums:
        print("Kļūda: Nosaukums nedrīkst būt tukšs!")
        nosaukums = input("Ievadi receptes nosaukumu: ").strip()
    instrukcijas = input("Ievadi receptes instrukcijas: ").strip()
    if not instrukcijas:
        print("Kļūda: Instrukcijas nedrīkst būt tukšas!")
        instrukcijas = input("Ievadi receptes instrukcijas: ").strip()
    
    gatavosanas_laiks = input("Ievadi gatavošanas laiku (piemēram, '30 minūtes'): ").strip()
    if not gatavosanas_laiks:
        print("Kļūda: Gatavošanas laiks nedrīkst būt tukšs!")
        gatavosanas_laiks = input("Ievadi gatavošanas laiku (piemēram, '30 minūtes'): ").strip()

    # Parādīt kategoriju opcijas un izvēlēties
    cursor.execute("SELECT * FROM kategorijas")
    kategorijas = cursor.fetchall()
    print("Izvēlies kategoriju:")
    for kategorija in kategorijas:
        print(f"{kategorija[0]}. {kategorija[1]}")
    
    kategorija_id = input("Ievadi kategorijas ID vai '0', lai pievienotu jaunu kategoriju: ").strip()

    if kategorija_id == '0':  # Lietotājs pievieno jaunu kategoriju
        jauna_kategorija = input("Ievadi jaunās kategorijas nosaukumu: ").strip()
        if not jauna_kategorija:
            print("Kļūda: Kategorijas nosaukums nedrīkst būt tukšs!")
            jauna_kategorija = input("Ievadi jaunās kategorijas nosaukumu: ").strip()
        cursor.execute("INSERT INTO kategorijas (nosaukums) VALUES (?)", (jauna_kategorija,))
        conn.commit()
        kategorija_id = cursor.lastrowid
        print(f"Kategorija '{jauna_kategorija}' pievienota!")
    else:
        try:
            kategorija_id = int(kategorija_id)  # Pārbaudām, vai tas ir derīgs skaitlis
            if kategorija_id <= 0:
                print("Kļūda: Kategorijas ID jābūt pozitīvam skaitlim!")
                return
        except ValueError:
            print("Kļūda: Kategorijas ID jābūt derīgam skaitlim!")
            return

    # Ievadām receptes informāciju datubāzē
    if nosaukums and instrukcijas and gatavosanas_laiks:
        cursor.execute('''
        INSERT INTO receptes (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id) 
        VALUES (?, ?, ?, ?)
        ''', (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id))
        conn.commit()
        # print(f"Recepte '{nosaukums}' veiksmīgi pievienota!\n")
        
        # Iegūstam jaunās receptes ID
        recepte_id = cursor.lastrowid
        
        # Pievienojam sastāvdaļas šai receptei
        while True:
            sastavdala = input("Ievadi sastāvdaļas nosaukumu (vai 'beigt', lai pārtrauktu): ").capitalize()
            if sastavdala.lower() == 'beigt':
                break
            cursor.execute("SELECT * FROM sastavdalas WHERE nosaukums = ?", (sastavdala,))
            atrasta_sastavdala = cursor.fetchone()

            if atrasta_sastavdala:
                sastavdala_id = atrasta_sastavdala[0]
                print(f"Sastāvdaļa '{sastavdala}' ir atrasta satavdaļu datubāzē!")
            else:
                mervieniba = input(f"Ievadi sastāvdaļas '{sastavdala}' mērvienību (piemēram, 'g', 'ml', 'gab'): ")
                cursor.execute("INSERT INTO sastavdalas (nosaukums, mervieniba) VALUES (?, ?)", (sastavdala, mervieniba))
                conn.commit()
                sastavdala_id = cursor.lastrowid
                print(f"Sastāvdaļa '{sastavdala}' pievienota datubāzei!")
            
            daudzums = input(f"Ievadi cik '{sastavdala}' vajag receptei '{nosaukums}' (piemēram, '200'): ")

            # Pievienojam sastāvdaļu receptei ar daudzumu starptabulā
            cursor.execute('''
            INSERT INTO receptes_sastavdalas (recepte_id, sastavdala_id, daudzums)
            VALUES (?, ?, ?)
            ''', (recepte_id, sastavdala_id, daudzums))
            conn.commit()
            print(f"Sastāvdaļa '{sastavdala}' veiksmīgi pievienota receptei '{nosaukums}'!\n")
    else:
        print("Lūdzu, aizpildiet visus laukus pareizi!\n")

# Funkcija, lai izvadītu visas receptes un to sastāvdaļas
def paradi_receptes():
    cursor.execute('''
    SELECT receptes.id, receptes.nosaukums, receptes.instrukcijas, receptes.gatavosanas_laiks, kategorijas.nosaukums
    FROM receptes
    JOIN kategorijas ON receptes.kategorija_id = kategorijas.id
    ''')
    receptes = cursor.fetchall()
    
    if not receptes:
        print("Nav pievienotas nevienas receptes.\n")
    else:
        for recepte in receptes:
            print(f"ID: {recepte[0]}")
            print(f"Nosaukums: {recepte[1]}")
            print(f"Instrukcijas: {recepte[2]}")
            print(f"Gatavošanas laiks: {recepte[3]}")
            print(f"Kategorija: {recepte[4]}")

            # Izvadām receptes sastāvdaļas
            cursor.execute('''
            SELECT sastavdalas.nosaukums, sastavdalas.mervieniba, receptes_sastavdalas.daudzums
            FROM receptes_sastavdalas
            JOIN sastavdalas ON receptes_sastavdalas.sastavdala_id = sastavdalas.id
            WHERE receptes_sastavdalas.recepte_id = ?
            ''', (recepte[0],))
            sastavdalas = cursor.fetchall()
            for sastavdala in sastavdalas:
                print(f"  - {sastavdala[0]}: {sastavdala[2]} {sastavdala[1]}")
            print("-" * 40)

# Sākam ar izvēlni
izvelne()

# Aizveram savienojumu, kad viss darīts
conn.close()
