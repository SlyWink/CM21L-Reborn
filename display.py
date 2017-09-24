#!/usr/bin/python
#-*- coding: utf-8 -*-

#import sys
import time
import chardet
from threading import Thread, Lock
from unidecode import unidecode
from lcdshift import *

CHAR_COUNT = 16
LINE_COUNT = 2


def Translit(text):
  if type(text) is unicode:
    l_text = text
  else:
    l_text = text.decode(chardet.detect(text)['encoding'])
  return unidecode(l_text)


class Display(Thread):

  def __init__(self,seconds):
    Thread.__init__(self)
    self.line = ['','']
    self.index = [0,0]
    self.loop = False
    self.lock = Lock()
    self.seconds = seconds
    self.lcd = HD44780(1,2,[5,6,7,4])

  def run(self):
    self.loop = True
    text = ['','']
    while self.loop:
      for linenum in range(0,LINE_COUNT):
        with self.lock:
          if len(self.line[linenum]) > CHAR_COUNT:
            text[linenum] = self.line[linenum][self.index[linenum]:self.index[linenum]+CHAR_COUNT+1]
            self.index[linenum] += 1
            if self.index[linenum] + CHAR_COUNT >= len(self.line[linenum]):
              self.index[linenum] = 0
          else:
            text[linenum] = self.line[linenum]
        self.lcd.display(linenum,text[linenum])
      time.sleep(self.seconds)

  def stop(self):
    self.loop = False

  def setLine(self,num,text):
    with self.lock:
      if text != self.line[num]:
#        self.line[num] = text.decode(chardet.detect(text)['encoding']).encode('ascii','replace')
        self.line[num] = Translit(text)
        self.index[num] = 0

  def setLines(self,text1,text2):
    self.setLine(0,text1)
    self.setLine(1,text2)

  def scrollUp(self,text):
    for linenum in range(0,LINE_COUNT-1):
      self.setLine(linenum,self.line[linenum+1])
    self.setLine(1,text)

  def scrollDown(self,text):
    for linenum in range(LINE_COUNT-1,0,-1):
      self.setLine(1,self.line[linenum-1])
    self.setLine(0,text)
