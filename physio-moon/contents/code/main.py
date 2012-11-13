#!/usr/bin/python
# -*- coding: utf-8 -*-
# **************************************************************************************
#    Copyright (C) 2012 Andrey Volkov <evil.bobby AT YOU KNOW  DELETE THAT gmail.com> 
#                                                                                     
#    This program is free software; you can redistribute it and/or modify             
#    it under the terms of the GNU General Public License as published by           
#    the Free Software Foundation; either version 2 of the License, or     
#    (at your option) any later version.                                  
#                                                                          
#    This program is distributed in the hope that it will be useful,       
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
#    GNU General Public License for more details.                          
#                                                                          
#    You should have received a copy of the GNU General Public License     
#    along with this program; if not, write to the                         
#    Free Software Foundation, Inc.,                                       
#    51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA .        
# **************************************************************************************

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import moonAge
 
class PhysioMoon(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 
    def init(self):
        self.resize(475, 310)
        self.setAspectRatioMode(Plasma.KeepAspectRatio)
        self.theme = Plasma.Svg(self)
        self.setBackgroundHints(Plasma.Applet.NoBackground)
        self.graphY = [-0.4675, -0.4845, -0.442, -0.153, 0.204, 
                      0.459, 0.493, 0.459, 0, -0.3145, 
                      -0.323, -0.272, -0.255, -0.272, -0.391, 
                      -0.408, -0.2635, 0.238, 0.408, 0.4165, 
                      0.272, 0, -0.2295, -0.34, -0.34, 
                      -0.272, -0.255, -0.272, -0.3995, -0.4505 ]
        self.ag = int( moonAge.getMoonAge() )
        self.graph = []
        #self.ag = 30
        self.m1 = QImage(self)
        self.m2 = QImage(self)
        self.m3 = QImage(self)
        self.m4 = QImage(self)
        self.m1.load(self.package().path()+"contents/images/m1.png")
        self.m2.load(self.package().path()+"contents/images/m2.png")
        self.m3.load(self.package().path()+"contents/images/m3.png")
        self.m4.load(self.package().path()+"contents/images/m4.png")
    
    def poly(self, pts):
        return QPolygonF(map(lambda p: QPointF(*p), pts))

    def paintInterface(self, painter, option, rect):
        painter.save()
        # Устанавливаем шрифт
        legendfont = QFont("Sans Serif", 5)
        painter.setFont(legendfont)
        self.width = int(self.applet.geometry().width())
        self.height = int(self.applet.geometry().height())
        # Рассчёт горизонтальных координат вертикальной линии, отображающий текущий лунный день 
        self.vertLineCoord = self.width * 0.96 / 29 * (self.ag-1) + self.width*0.02
        #painter.drawImage(0, 0, self.moonGraph)
        painter.setPen(QColor(0, 255, 0, 125))
        painter.drawLine( self.vertLineCoord, self.height*0.01, self.vertLineCoord, self.height*0.99)
        painter.setPen(QColor(255, 255, 255, 125))
        painter.drawLine( self.width*0.02, self.height/2, self.width*0.98, self.height/2)
        self.graph.append( [0, -0.2])
        # Рисуем координатную сетку и подписи по оси х
        for x in xrange(0, 30):
          # Сетка
          painter.drawLine( self.width*0.02+x*self.width*0.96/29, self.height/2-self.height*0.005, self.width*0.02+x*self.width*0.96/29, self.height/2+self.height*0.005)
          # Подписи
          cords = QRectF(int(self.width*0.02+x*self.width*0.96/29-self.width*0.005), int(self.height/2+self.height*0.04),
                         int(self.width*0.02+x*self.width*0.96/29+self.width*0.005), int(self.height/2+self.height*0.04) )
          painter.drawText(cords, Qt.AlignJustify, QString(str(x+1)))
          # Кривая активации - торможения
          self.graph.append( [ self.width*0.02+x*self.width*0.96/29, self.height/2+self.height*self.graphY[x] ] )
        self.graph.append( [self.width, -0.2])
        painter.setPen(QColor(255, 255, 255, 255))
        gr = self.graph[:]
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPolyline(self.poly(gr))
        painter.drawImage(self.width*0.02+0.5*self.width*0.96/29,self.height/2-self.height*0.1, self.m1)
        painter.drawImage(self.width*0.02+6.5*self.width*0.96/29,self.height/2-self.height*0.1, self.m2)
        painter.drawImage(self.width*0.02+13*self.width*0.96/29,self.height/2-self.height*0.1, self.m3)
        painter.drawImage(self.width*0.02+20.5*self.width*0.96/29,self.height/2-self.height*0.1, self.m4)
        painter.drawImage(self.width*0.02+27.5*self.width*0.96/29,self.height/2-self.height*0.1, self.m1)
        painter.restore()
 
def CreateApplet(parent):
    return PhysioMoon(parent)