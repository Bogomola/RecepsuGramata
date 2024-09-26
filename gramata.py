import sqlite3


conn = sqlite3.connect('receptes.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS receptes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL,
    sastavdalas TEXT NOT NULL,
    daudzums TEXT NOT NULL,
    instrukcijas TEXT NOT NULL
)
''')

# Receptes pievienošana
def pievienot_recepti():
    nosaukums = input("Ievadi receptes nosaukumu: ")
    sastavdalas = input("Ievadi sastāvdaļas, atdalot ar komatu: ")
    daudzums = input("Ievadi daudzumu (tajā pašā secībā kā sastāvdaļas): ")
    instrukcijas = input("Ievadi receptes instrukcijas: ")
    
    if nosaukums and sastavdalas and daudzums and instrukcijas:
        cursor.execute('''
        INSERT INTO receptes (nosaukums, sastavdalas, daudzums, instrukcijas) 
        VALUES (?, ?, ?, ?)
        ''', (nosaukums, sastavdalas, daudzums, instrukcijas))
        conn.commit()
        print(f"Recepte '{nosaukums}' veiksmīgi pievienota!\n")
    else:
        print("Lūdzu, aizpildiet visus laukus!\n")

# Parāda visas receptes no datubāzes
def paradi_receptes():
    cursor.execute('SELECT * FROM receptes')
    receptes = cursor.fetchall()
    
    if not receptes:
        print("Nav pievienotas nevienas receptes.\n")
    else:
        for recepte in receptes:
            print(f"ID: {recepte[0]}")
            print(f"Nosaukums: {recepte[1]}")
            print(f"Sastāvdaļas: {recepte[2]}")
            print(f"Daudzums: {recepte[3]}")
            print(f"Instrukcijas: {recepte[4]}\n")
            print("-" * 40)

# Receptes dzēšana no ID
def dzest_recepti():
    paradi_receptes()
    recepte_id = input("Ievadiet receptes ID, kuru vēlaties dzēst: ")
    
    if recepte_id.isdigit():
        cursor.execute('DELETE FROM receptes WHERE id = ?', (recepte_id,))
        conn.commit()
        print(f"Recepte ar ID {recepte_id} ir dzēsta!\n")
    else:
        print("Nepareizs ID formāts.\n")

# Galvenā izvēlne
def izveleties_darbibu():
    while True:
        print("=" * 50)
        print(" " * 15 + "🍽️  Recepšu gramāta  🍽️")
        print("=" * 50)
        print("Izvēlies darbību:")
        print("1. Pievienot recepti")
        print("2. Parādīt visas receptes")
        print("3. Dzēst recepti")
        print("4. Iziet no programmas\n")
        print("=" * 50)
        izvele = input("\nIevadi izvēles numuru: ")

        if izvele == "1":
            pievienot_recepti()
        elif izvele == "2":
            paradi_receptes()
        elif izvele == "3":
            dzest_recepti()
        elif izvele == "4":
            print("Atā!")
            break
        else:
            print("Nepareiza izvēle, mēģini vēlreiz!\n")


izveleties_darbibu()


conn.close()
