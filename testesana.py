import sqlite3

# Funkcija receptes pievienošanai ar vienkāršu validāciju
def pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas):
    cursor = conn.cursor()

    # Validācija: pārbaudām vai ievades lauki ir aizpildīti
    if not nosaukums or not instrukcijas or not gatavosanas_laiks:
        raise ValueError("Nosaukums, instrukcijas un gatavošanas laiks ir obligāti aizpildāmi lauki!")
    
    if not isinstance(kategorija_id, int):
        raise TypeError("Kategorijas ID jābūt skaitlim!")

    cursor.execute("INSERT INTO receptes (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id) VALUES (?, ?, ?, ?)",
                   (nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id))
    recepte_id = cursor.lastrowid

    # Pievienojam sastāvdaļas
    for sastavdala in sastavdalas:
        nosaukums, mervieniba, daudzums = sastavdala
        cursor.execute("INSERT INTO sastavdalas (nosaukums, mervieniba) VALUES (?, ?)", (nosaukums, mervieniba))
        sastavdala_id = cursor.lastrowid
        cursor.execute("INSERT INTO receptes_sastavdalas (recepte_id, sastavdala_id, daudzums) VALUES (?, ?, ?)",
                       (recepte_id, sastavdala_id, daudzums))
    
    conn.commit()
    print("Recepte veiksmīgi pievienota!")

######### Testa funkcija ar assert pārbaudēm######
def test_pievienot_recepti():
    conn = sqlite3.connect('receptes.db')

    #######1. Testējam veiksmīgu pievienošanu#######
    try:
        nosaukums = "Omlete"
        instrukcijas = "Saputo olas un cep uz pannas."
        gatavosanas_laiks = "10 minūtes"
        kategorija_id = 1  # Kategorija ID (Brokastis)
        sastavdalas = [("Olas", "gab", "3")]

        pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas)
        print("Test - Veiksmīga pievienošana: Izdevās!")
    except Exception as e:
        assert False, f"Test - Veiksmīga pievienošana neizdevās: {e}"

    ####### 2. Testējam, ja ir recepte bez nosaukuma(nav ievadīts) (būtu jāizraisa ValueError)
    try:
        nosaukums = ""
        instrukcijas = "Saputo olas un cep uz pannas."
        gatavosanas_laiks = "10 minūtes"
        kategorija_id = 1
        sastavdalas = [("Olas", "gab", "3")]

        pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas)
        assert False, "Test - Tukšs nosaukums neizdevās, vajadzēja izraisīt ValueError"
    
    except ValueError as ve:
        assert str(ve) == "Nosaukums, instrukcijas un gatavošanas laiks ir obligāti aizpildāmi lauki!", f"Kļūda: {ve}"
        print("Test - Tukšs nosaukums: Izdevās!")

    ######## 3. Testējam nederīgu kategorija_id (būtu jāizraisa TypeError)
    try:
        nosaukums = "Omlete"
        instrukcijas = "Saputo olas un cep uz pannas."
        gatavosanas_laiks = "10 minūtes"
        kategorija_id = "brokastis"  # Šeit būtu jābūt skaitlim, bet ir ievadīts teksts
        sastavdalas = [("Olas", "gab", "3")]

        pievienot_recepti(conn, nosaukums, instrukcijas, gatavosanas_laiks, kategorija_id, sastavdalas)
        assert False, "Test - Nederīgs kategorija_id neizdevās, vajadzēja izraisīt TypeError"
    
    except TypeError as te:
        assert str(te) == "Kategorijas ID jābūt skaitlim!", f"Kļūda: {te}"
        print("Test - Nederīgs kategorija_id: Izdevās!")

    conn.close()

########## Testa funkcija
test_pievienot_recepti()
