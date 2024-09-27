import sqlite3

# Funkcija tabulu izveidei (ja datubāze tiek sākta atsevišķā failā)
def create_tables_test():
    conn = sqlite3.connect('receptes.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
    tables = [table[0] for table in cursor.fetchall()]
    
    expected_tables = ['kategorijas', 'sastavdalas', 'receptes', 'receptes_sastavdalas']

    # Pārbaudām, vai visas tabulas ir izveidotas
    if set(expected_tables).issubset(set(tables)):
        print("Test - Tabulu izveide: Izdevās!")
    else:
        print("Test - Tabulu izveide: Neizdevās!")
    
    conn.close()

# Funkcija receptes pievienošanai
def pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas):
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO receptes (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id) VALUES (?, ?, ?, ?)",
                   (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id))
    recepte_id = cursor.lastrowid
    
    for sastavdala in sastavdalas:
        nosaukums, mervieniba, daudzums = sastavdala
        cursor.execute("INSERT INTO sastavdalas (nosaukums, mervieniba) VALUES (?, ?)", (nosaukums, mervieniba))
        sastavdala_id = cursor.lastrowid
        cursor.execute("INSERT INTO receptes_sastavdalas (recepte_id, sastavdala_id, daudzums) VALUES (?, ?, ?)",
                       (recepte_id, sastavdala_id, daudzums))
    
    conn.commit()

# Testa funkcija receptes pievienošanai
def test_add_recipe():
    conn = sqlite3.connect('receptes.db')
    
    # Pievienojam kategoriju (piemēram, 1 - Brokastis)
    cursor = conn.cursor()
    
    nosaukums = "Omlete"
    instrukcijas = "Saputo olas un cep uz pannas."
    gatavosanas_laiks = "10 minūtes"
    sastavdalas = [("Olas", "gab", "3")]
    kategorija_id = 1  # Brokastu kategorija jau pievienota

    pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas)
    
    # Pārbaudām, vai recepte tika pievienota
    cursor.execute("SELECT * FROM receptes WHERE nosaukums = ?", (nosaukums,))
    recipe = cursor.fetchone()
    
    if recipe:
        print("Test - Receptes pievienošana: Izdevās!")
    else:
        print("Test - Receptes pievienošana: Neizdevās!")
    
    conn.close()

# Testa funkcija sastāvdaļas pievienošanai
def test_add_ingredient():
    conn = sqlite3.connect('receptes.db')
    cursor = conn.cursor()
    
    # Pievienojam sastāvdaļu
    sastavdala = "Tomāts"
    mervieniba = "gab"
    cursor.execute("INSERT INTO sastavdalas (nosaukums, mervieniba) VALUES (?, ?)", (sastavdala, mervieniba))
    conn.commit()
    
    # Pārbaudām, vai sastāvdaļa tika pievienota
    cursor.execute("SELECT * FROM sastavdalas WHERE nosaukums = ?", (sastavdala,))
    ingredient = cursor.fetchone()
    
    if ingredient:
        print("Test - Sastāvdaļas pievienošana: Izdevās!")
    else:
        print("Test - Sastāvdaļas pievienošana: Neizdevās!")
    
    conn.close()

# Veicam testus
create_tables_test()    # Pārbauda tabulu izveidi
test_add_recipe()       # Pārbauda receptes pievienošanu
test_add_ingredient()   # Pārbauda sastāvdaļas pievienošanu
