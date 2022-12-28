import sqlite3

base = sqlite3.connect('music.db')
cur = base.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS music (
music_id INTEGER PRIMARY KEY AUTOINCREMENT,
file_id TEXT,
right_answer TEXT,
wrong_answers TEXT);
""")
base.commit()

cur.execute("""INSERT INTO music (file_id, right_answer, wrong_answers)
VALUES ('PASTE ID HERE', 'F. F. Chopin - Funeral March', 'P.I. Tchaikovsky – Swan Lake, W. A. Mozart - Fantasia No. 3 in D minor'),
       ('', 'F. F. Chopin - Nocturne No. 21 in C minor', 'L. V. Beethoven - Für Elise, L. V. Beethoven - Ode to Joy'),
       ('', 'L. V. Beethoven - Moonlight Sonata', 'W. A. Mozart - Fantasia No. 3 in D minor, L. V. Beethoven - Für Elise'),
       ('', 'W. A. Mozart - Fantasia No. 3 in D minor', 'W. A. Beethoven - Symphony No. 5, W. A. Mozart - Lacrimosa'),
       ('', 'W. A. Mozart - Lacrimosa', 'L. V. Beethoven - Für Elise, W. A. Mozart – Turkish March'),
       ('', 'W. A. Mozart – Turkish March', 'L. V. Beethoven - Moonlight Sonata, P.I. Tchaikovsky – Swan Lake');
""")
base.commit()
