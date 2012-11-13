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

import datetime
import math

def normalize(v):
    v = v - math.floor(v);
    if (v < 0):
        v = v + 1;
    return v;
  
def getMoonAge(date = datetime.datetime.now()):
    """
    Return moon's age
    """
    Y = date.year
    M = date.month
    D = date.day

    # calculate the Julian date at 12h UT
    YY = Y - math.floor( ( 12 - M ) / 10 )      
    MM = M + 9 
    if MM >= 12: 
        MM = MM - 12
  
    K1 = math.floor( 365.25 * ( YY + 4712 ) )
    K2 = math.floor( 30.6 * MM + 0.5 )
    K3 = math.floor( math.floor( ( YY / 100 ) + 49 ) * 0.75 ) - 38

    JD = K1 + K2 + D + 59      # for dates in Julian calendar
    if JD > 2299160:
        JD = JD - K3           # for Gregorian calendar

    # calculate moon's age in days
    IP = normalize( ( JD - 2451550.1 ) / 29.530588853 )
    AG = IP * 29.53
    return AG
  
