# -*- coding:utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Author:      Diamond Takeshi
# Created:     20/11/2015
# Copyright:   (c) Diamond Takeshi 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pygame.midi

class QtMainClass(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        pygame.midi.init()
        self.player=pygame.midi.Output(1)
        self.player.set_instrument(0, 0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TakeClassic ver.0.4")
        layout=QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        #キーボードの設定
        self.key_sets=[]
        self.key_sets.append(QtCore.Qt.Key_A)	#60
        self.key_sets.append(QtCore.Qt.Key_W)	#61

        self.key_sets.append(QtCore.Qt.Key_S)	#62
        self.key_sets.append(QtCore.Qt.Key_E)	#63

        self.key_sets.append(QtCore.Qt.Key_D)	#64
        self.key_sets.append(QtCore.Qt.Key_F)	#65

        self.key_sets.append(QtCore.Qt.Key_T)	#66
        self.key_sets.append(QtCore.Qt.Key_G)	#67

        self.key_sets.append(QtCore.Qt.Key_Y)	#68
        self.key_sets.append(QtCore.Qt.Key_H)	#69

        self.key_sets.append(QtCore.Qt.Key_U)	#70
        self.key_sets.append(QtCore.Qt.Key_J)	#71

        self.key_sets.append(QtCore.Qt.Key_K)	#72
        self.key_sets.append(QtCore.Qt.Key_O)	#73

        self.key_sets.append(QtCore.Qt.Key_L)
        self.key_sets.append(QtCore.Qt.Key_P)

        #self.key_sets.append(QtCore.Qt.Key_L)
	    #self.key_sets.append(QtCore.Qt.Key_P)

        #ピアノキーのセット
        self.piano_keys=[]
        i=0
        key_color=["w", "b", "w", "b", "w", "w", "b", "w", "b", "w", "b", "w"]
        for key in self.key_sets:
        	kc=key_color[i%len(key_color)]
        	self.piano_keys.append(PianoKey(Note_No=i+60, volume=60, Key_Set=key, Key_Color=kc, parent=self))
        	layout.addWidget(self.piano_keys[i])
        	i+=1

        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.setLayout(layout)
        key_num=len(self.key_sets)  #キーの個数
        self.height=self.piano_keys[0].height
        self.width=self.piano_keys[0].width*key_num
        self.resize(self.width, self.height)
        self.maximumWidth=self.width
        self.maximumHeight=self.height
        self.minimumWidth=self.width
        self.minimumHeight=self.height
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.move(230,340)

        self.show()

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            for i in xrange(len(self.key_sets)):
                if event.key()==self.key_sets[i]: self.piano_keys[i].play_sound()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            for i in xrange(len(self.key_sets)):
                if event.key()==self.key_sets[i]: self.piano_keys[i].stop_sound()

def note2code(note):
	code=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	return code[note%len(code)]

class PianoKey(QtGui.QPushButton):
    def __init__(self, Note_No=69, volume=127, Key_Set=QtCore.Qt.Key_A, Key_Color="w",parent=None):
        super(PianoKey, self).__init__()
        #パラメータ
        self.Note_No=Note_No
        self.volume=volume
        self.Key_Set=Key_Set
        self.parent=parent
        self.setText(note2code(self.Note_No))
        self.setFont(QtGui.QFont("Times", pointSize=22,italic=True))
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.width=1
        self.height=280
        self.maximumWidth=30
        self.maximumHeight=self.height
        self.minimumWidth=30
        self.minimumHeight=self.height
        self.Key_Color=Key_Color
        #シグナル/スロット設定
        self.pressed.connect(self.play_sound)
        self.released.connect(self.stop_sound)

        #スタイルの設定
        self.on_style="""
        				QPushButton{background-color: rgba(255, 255, 127, 200);
        							border-color	: rgba(52, 52, 52, 200);
        							color			: red;
        							}"""
        self.off_style_white="""
        				QPushButton{background-color:   white;
        							border-color	:   rgba(100,100,100, 200);
        							color			:	black;
        							}"""
        self.off_style_black="""
        				QPushButton{background-color:	rgba(15, 15, 15, 220);
        							border-color	:	rgba(0, 0, 0, 200);
        							color			:	white;
        							}"""
        if self.Key_Color=="w":
            self.off_style=self.off_style_white
        if self.Key_Color=="b":
            self.off_style=self.off_style_black
        self.setStyleSheet(self.off_style)

    #サウンドのオンオフ/スロット設定
    def play_sound(self):
        self.setStyleSheet(self.on_style)
        self.parent.player.note_on(self.Note_No, self.volume)

    def stop_sound(self):
        self.setStyleSheet(self.off_style)
        self.parent.player.note_off(self.Note_No, self.volume)


def main():
    app=QtGui.QApplication(sys.argv)
    main_class=QtMainClass()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()