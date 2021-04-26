import datetime
import os
import pickle
import signal
import subprocess
from pathlib import Path
import sqlite3


def rec_video(name):
    # Déclaration de variable
    ts = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime.now()
    annee = timestamp.strftime('%Y')
    semaine = timestamp.strftime('%V le %m.%y')
    jour = timestamp.strftime('%d-%m-%y %Hh%M')

    # Création dossier
    path = Path('/home/aymeric/Documents/data/' + annee + '/Semaine-' + semaine + '/')
    path.mkdir(parents=True, exist_ok=True)

    # Flux réseau caméra
    rstp_server = 'rtsp://admin@192.168.31.56/0/av0'

    # Nom fichier
    file_directory = '/home/aymeric/Documents/data/' + annee + '/Semaine-' + semaine + '/' + name + ' ' + jour + '.mp4'

    # Démarrage VLC
    cmdbase = 'cvlc -I dummy ' + rstp_server + ' --sout="#transcode{vcodec=h264,acodec=mp3,vb=500,fps=30.0}:std{mux=mp4,dst=' + file_directory + ',access=file}"'
    process = subprocess.Popen(cmdbase, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    pid = os.getpgid(process.pid)
    f = open('/home/aymeric/Documents/data/out.ser', "wb")
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)
    pickler.dump(pid)
    f.close()

    # Mise en BDD
    con = sqlite3.connect("/home/aymeric/Documents/data/bdd/rec_bdd.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS rec(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT,
        time INTEGER,
        status INTEGER
    )''')
    donnees = (name, ts, 1)
    cur.execute("INSERT INTO rec (name, time, status) VALUES (?, ?, ?)", donnees)
    con.commit()
    con.close()

    return pid


def unrec_video():
    f = open('/home/aymeric/Documents/data/out.ser', "rb")
    unpickler = pickle.Unpickler(f)
    pid = unpickler.load()
    f.close()
    os.killpg(pid, signal.SIGTERM)

    con = sqlite3.connect("/home/aymeric/Documents/data/bdd/rec_bdd.db")
    cur = con.cursor()
    cur.execute("UPDATE rec SET status = 0")
    con.commit()
    con.close()

    return pid


def status_rec():
    con = sqlite3.connect("/home/aymeric/Documents/data/bdd/rec_bdd.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM rec WHERE status = 1 ORDER BY id DESC LIMIT 1")
    data = cur.fetchall()

    # true = enregistrement en cours / false = pas d'enregistrement en cours
    if len(data) == 0:
        rec = 'false'
    else:
        rec = 'true'
        rec_id = (','.join(map(str, next(zip(*data)))))

    try:
        return rec, rec_id
    except NameError:
        return rec


def info_rec(rec_id):
    con = sqlite3.connect("/home/aymeric/Documents/data/bdd/rec_bdd.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM rec WHERE id = ?", (rec_id,))
    res = cur.fetchall()
    for row in res:
        rec_id = row[0]
        rec_name = row[1]
        rec_time = row[2]
        if row[3] == 1:
            rec_status = 'true'
        else:
            rec_status = 'false'
    con.close()

    return rec_id, rec_name, rec_time, rec_status
