# -*- coding: utf-8 -*-
# 作者：LittleCoder
# 来源：知乎

import sys
import threading

import pyaudio
import wave
from PyQt4.QtGui import (
    QApplication, QWidget,
    QVBoxLayout,
    QPushButton)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
RECORDING = False
TIME = 10


def record_thread(fileName, stream, p):
    print('recording')
    waveFile = wave.open(fileName, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    while RECORDING:
        print "."
        waveFile.writeframes(stream.read(CHUNK))
    waveFile.close()
    print('end')


def record_generator(fileName, recordBtn):
    global RECORDING
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
    while 1:
        recordBtn.setText(u'开始录制')
        yield
        recordBtn.setText(u'停止录制')
        RECORDING = True
        t = threading.Thread(target=record_thread, args=(fileName, stream, p))
        t.setDaemon(True)
        t.start()
        yield
        RECORDING = False


app = QApplication(sys.argv)
mainWindow = QWidget()
layout = QVBoxLayout()
btn = QPushButton()

g = record_generator('output.wav', btn)
g.next()
btn.pressed.connect(g.next)
layout.addWidget(btn)
mainWindow.setLayout(layout)
mainWindow.show()
sys.exit(app.exec_())
