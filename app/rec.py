import os
import pickle
import signal
import subprocess


def rec_video(name):
    rstp_server = 'rtsp://admin@192.168.31.56/0/av0'
    path = '/home/aymeric/Documents/video/'
    file_name = name + '.mp4'
    cmdbase = 'cvlc -I dummy ' + rstp_server + ' --sout="#transcode{vcodec=h264,acodec=mp3,vb=500,fps=30.0}:std{mux=mp4,dst=' + path + '' + file_name + ',access=file}"'
    process = subprocess.Popen(cmdbase, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    pid = os.getpgid(process.pid)
    f = open('/home/aymeric/Documents/save/out.ser', "wb")
    pickler = pickle.Pickler(f, pickle.HIGHEST_PROTOCOL)
    pickler.dump(pid)
    f.close()
    return pid


def unrec_video():
    f = open('/home/aymeric/Documents/save/out.ser', "rb")
    unpickler = pickle.Unpickler(f)
    pid = unpickler.load()
    f.close()
    os.killpg(pid, signal.SIGTERM)
    return pid
