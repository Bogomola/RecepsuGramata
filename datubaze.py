##########Fails, kas atbild par datubāzes izveidošanu ar visām 4 tabulām (Receptes, sastavdalas, kategorijas, receptes_sastavdalas)

import sqlite3

############# Izveidojam savienojumu ar SQLite datubāzi (ja tā neeksistē, tā tiks izveidota)
conn = sqlite3.connect('receptes.db')
cursor = conn.cursor()

############## Izveidojam tabulu kategorijām
cursor.execute('''
CREATE TABLE IF NOT EXISTS kategorijas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL
)
''')

############### Pievienojam kategorijas piemēram brokastis, pusdienas, vakariņas, ja vēl neeksistē
cursor.execute("INSERT OR IGNORE INTO kategorijas (id, nosaukums) VALUES (1, 'Brokastis')")
cursor.execute("INSERT OR IGNORE INTO kategorijas (id, nosaukums) VALUES (2, 'Pusdienas')")
cursor.execute("INSERT OR IGNORE INTO kategorijas (id, nosaukums) VALUES (3, 'Vakariņas')")

############## Izveidojam tabulu receptēm
cursor.execute('''
CREATE TABLE IF NOT EXISTS receptes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL,
    instrukcijas TEXT NOT NULL,
    gatavosanas_laiks TEXT NOT NULL,
    kategorija_id INTEGER,
    FOREIGN KEY (kategorija_id) REFERENCES kategorijas (id)
)
''')

############# Izveidojam tabulu sastāvdaļām
cursor.execute('''
CREATE TABLE IF NOT EXISTS sastavdalas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL,
    mervieniba TEXT NOT NULL
)
''')
############## Pievienojam 15 sastāvdaļas tabulai, lai tabula nebūtu pilnīgi tukša
cursor.execute('''
INSERT OR IGNORE INTO sastavdalas (nosaukums, mervieniba) VALUES 
('Cukurs', 'g'),
('Sāls', 'g'),
('Milti', 'g'),
('Olīveļļa', 'ml'),
('Piens', 'ml'),
('Vistas olas', 'gab'),
('Sviests', 'g'),
('Rīsi', 'g'),
('Makaronu izstrādājumi', 'g'),
('Siers', 'g'),
('Tomāti', 'gab'),
('Burkāni', 'gab'),
('Sīpoli', 'gab'),
('Paprika', 'gab'),
('Šokolāde', 'g')
''')

############# Saglabājam izmaiņas, ja tiek ievadīta jauna sastavdaļa
conn.commit()
print("Sastāvdaļas veiksmīgi pievienotas sastāvdaļu tabulai.")


############ Izveidojam starptabulu, kas saistīs receptes ar sastāvdaļām
cursor.execute('''
CREATE TABLE IF NOT EXISTS receptes_sastavdalas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recepte_id INTEGER,
    sastavdala_id INTEGER,
    daudzums TEXT NOT NULL,
    FOREIGN KEY (recepte_id) REFERENCES receptes (id),
    FOREIGN KEY (sastavdala_id) REFERENCES sastavdalas (id)
)
''')