import datetime
import os
import pickle
import signal
import subprocess
from pathlib import Path




def rec_video(name):

    # Déclaration de variable
    timestamp = datetime.datetime.now()
    annee = timestamp.strftime('%Y')
    semaine = timestamp.strftime('%V.%m.%y')
    jour = timestamp.strftime('%d-%m-%Y:%Hh%M')

    # Création dossier
    path = Path('/srv/aeve-rec-session/data/' + annee + '')
    path.mkdir(parents=True, exist_ok=True)
    path = Path('/srv/aeve-rec-session/data/' + annee + '/Semaine-' + semaine + '')
    path.mkdir(parents=True, exist_ok=True)
    path = '/srv/aeve-rec-session/data/' + annee + '/Semaine-' + semaine + ''

    # Flux réseau caméra
    rstp_server = 'rtsp://admin@192.168.31.56/0/av0'

    # Nom fichier
    file_name = name + '' + jour + '.mp4'

    # Démarrage VLC
    cmdbase = 'cvlc -I dummy ' + rstp_server + ' --sout="#transcode{vcodec=h264,acodec=mp3,vb=500,fps=30.0}:std{mux=mp4,dst=' + path + '' + file_name + ',access=file}"'
    process = subprocess.Popen(cmdbase, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    pid = os.getpgid(process.pid)
    f = open('/srv/aeve-rec-session/back/temp_var/out.ser', "wb")
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)
    pickler.dump(pid)
    f.close()

    return pid


def unrec_video():

    f = open('/srv/aeve-rec-session/back/temp_var/out.ser', "rb")
    unpickler = pickle.Unpickler(f)
    pid = unpickler.load()
    f.close()
    os.killpg(pid, signal.SIGTERM)

    return pid
