# Copyright (C) 2016-2018, Dylan Grandmont

import math
import numpy as np
import xml.etree.ElementTree as ET

from constants import IONWC_HOME
from utilities import km_per_degree_lat_lng

pi = math.pi 

class UWIToLatLng:

  def __init__(self):
    print 'Initializing UWIToLatLng'
    self.twpToLatLong = {}
    namespace = "{http://www.opengis.net/kml/2.2}"

    tree = ET.parse(IONWC_HOME + '/data/gis/dls_grd_n83_polygon.kml')
    root = tree.getroot()
    placemarks = root.findall(".//" + namespace + "Placemark")

    for placemark in placemarks:
      extendedData = placemark.find(".//" + namespace + "ExtendedData")
      schemaData = extendedData.find(".//" + namespace + "SchemaData")
      twp = '%03d' % int(schemaData.findall(".//" + namespace + "SimpleData[@name='TWP']")[0].text)
      rng = '%02d' % int(schemaData.findall(".//" + namespace + "SimpleData[@name='RGE']")[0].text)
      mer = schemaData.findall(".//" + namespace + "SimpleData[@name='MERIDIAN']")[0].text
      coordinates = placemark.find(".//" + namespace + "Polygon/" + namespace + "outerBoundaryIs/" + namespace + "LinearRing/" + namespace + "coordinates").text
      coordinates = coordinates.split()
      NW = [0, 0]
      NE = [-200, 0]
      SE = [-200, 90]
      SW = [0, 90]

      tol = 5e-4

      for coordinate in coordinates:
        coordinate = coordinate.split(',')
        lonCoordinate = float(coordinate[0])
        latCoordinate = float(coordinate[1])
        if lonCoordinate < NW[0]+tol and latCoordinate > NW[1]-tol:
          NW[0] = lonCoordinate
          NW[1] = latCoordinate
        if lonCoordinate > NE[0]-tol and latCoordinate > NE[1]-tol:
          NE[0] = lonCoordinate
          NE[1] = latCoordinate     
        if lonCoordinate > SE[0]-tol and latCoordinate < SE[1]+tol:
          SE[0] = lonCoordinate
          SE[1] = latCoordinate
        if lonCoordinate < SW[0]+tol and latCoordinate < SW[1]+tol:
          SW[0] = lonCoordinate
          SW[1] = latCoordinate

      self.twpToLatLong[twp+'-'+rng+mer] = [SE, SW, NW, NE]


  def convert(self, uwi, grid = "DLS", position = "center"):
    """ Map legal coordinates to Geographic coordinates (lat,long) 
    Expecting uwi in format like 00/03-22-015-13W4/0 (LSD - Section - Township - Range W Meridian /0
    Reference: http://www.fekete.com/SAN/WebHelp/Piper/WebHelp/c-te-GIStheory.htm
    """

    if position=="center":
       positionFactorX = 2.0
       positionFactorY = 2.0
    elif position=="nw":
       positionFactorX = 1.0
       positionFactorY = 1.0
    elif position=="se":
       positionFactorX = 1e9
       positionFactorY = 1e9
    elif position=="ne":
       positionFactorX = 1e9
       positionFactorY = 1.0
    elif position=="sw":
       positionFactorX = 1.0
       positionFactorY = 1e9
    else: raise ValueError("Invalid position parameter set")

    if grid=="DLS":
       uwi = uwi.split("-")                                                                                                                     
       mer = int(uwi[-1][3])        
       twp = int(uwi[2])                   
       sec = int(uwi[1])                   
       lsd = int(uwi[0].split("/")[-1])    
       rng = int(uwi[-1][0:2])             

       # create set of township lines which are baselines                                                                        
       bls = range(1, 128, 4)
       # find the nearest baseline                                                                    
       near_bl = bls[(np.abs(np.array(bls) - (twp + 1))).argmin()]
       # estimate latitude of nearest baseline                                                                          
       near_bl_lat = 49.0 + 11.0*((near_bl-1)/126.0)
       deg_lat, deg_lon = km_per_degree_lat_lng(near_bl_lat)

       x_offset, y_offset = 0, 0

       # handle the section E/W offset                                                                                 
       if ((sec-1)/6)%2==1: column=6-(sec-1)%6-1
       else:                column=(sec-1)%6
       x_offset += column*1.6294666666666666
       # handle the lsd E/W offset, place in middle of lsd                                                                
       if ((lsd-1)/4)%2==1: column=4-(lsd-1)%4-1
       else:                column=(lsd-1)%4
       x_offset += column*0.40736666666666665 + 0.40736666666666665/positionFactorX
       
       # determine offset from nearest baseline                                                                           
       #y_offset +=  twpToLatLong[uwi[2] + '-' + uwi[-1][0:4]][0][1]#(twp - near_bl)*9.7164
       # handle the section N/S offset                                                                                      
       row = (sec-1)/6
       y_offset += row*1.6194
       # handle the lsd N/S offset                                                                                       
       row = (lsd-1)/4
       y_offset += row*0.40485 + 0.40485/positionFactorY

       # of the form twp - rng W mer
       latlngIndex = str(twp).zfill(3) + '-' + str(rng).zfill(2) + uwi[-1][2:4]
       
       lat =  self.twpToLatLong[latlngIndex][0][1]
       lon = -1.0 * self.twpToLatLong[latlngIndex][0][0]

       #lat=near_bl_lat
       lat+=y_offset/deg_lat
       lon+=x_offset/deg_lon

    elif grid=="NTS":
       #e.g. 200B077D094H0300
       sheet_n=uwi[12:14]
       sheet_a=uwi[11]    #letter
       series=uwi[8:11]   #number
       block=uwi[7]       #block letter
       unit=uwi[4:7]      #block number
       quart=uwi[3]       #quarter units

       if   series[2]=="2": lat=48.0
       elif series[2]=="3": lat=52.0
       elif series[2]=="4": lat=56.0
       elif series[2]=="5": lat=60.0
       else: raise Exception("ERROR: Invalid series", series)

       if   series[1]=="9": lon=120.0
       elif series[1]=="8": lon=112.0
       elif series[1]=="0": lon=128.0

       if   sheet_a=="E" or sheet_a=="F" or sheet_a=="G" or sheet_a=="H": lat+=1.0
       elif sheet_a=="L" or sheet_a=="K" or sheet_a=="J" or sheet_a=="I": lat+=2.0
       elif sheet_a=="M" or sheet_a=="N" or sheet_a=="O" or sheet_a=="P": lat+=3.0

       if   sheet_a=="B" or sheet_a=="G" or sheet_a=="J" or sheet_a=="O": lon+=2.0
       elif sheet_a=="C" or sheet_a=="F" or sheet_a=="K" or sheet_a=="N": lon+=4.0
       elif sheet_a=="D" or sheet_a=="E" or sheet_a=="L" or sheet_a=="M": lon+=6.0

       # NTS Sheet
       # Each sheet is 0.25 lat by 0.5 lon degrees       
       if   sheet_n=="05" or sheet_n=="06" or sheet_n=="07" or sheet_n=="08": lat+=0.25
       elif sheet_n=="09" or sheet_n=="10" or sheet_n=="11" or sheet_n=="12": lat+=0.5
       elif sheet_n=="13" or sheet_n=="14" or sheet_n=="15" or sheet_n=="16": lat+=0.75

       if   sheet_n=="02" or sheet_n=="07" or sheet_n=="10" or sheet_n=="15": lon+=0.5
       elif sheet_n=="03" or sheet_n=="06" or sheet_n=="11" or sheet_n=="14": lon+=1.0
       elif sheet_n=="04" or sheet_n=="05" or sheet_n=="12" or sheet_n=="13": lon+=1.5

       # NTS Block
       # Each Block is 0.08333333333 lat degress by 0.5/4 degrees
       if   block=="E" or block=="F" or block=="G" or block=="H": lat+=(0.25/3.0)
       elif block=="L" or block=="K" or block=="J" or block=="I": lat+=2.0*(0.25/3.0)

       if   block=="B" or block=="G" or block=="J": lon+=(0.5/4.0)
       elif block=="C" or block=="F" or block=="K": lon+=2.0*(0.5/4.0)
       elif block=="D" or block=="E" or block=="L": lon+=3.0*(0.5/4.0)

       # Unit
       # Each unit is 0.25/3.0/10 lat by 0.5/4.0/10 long degrees
       lat+=float((int(unit)-1)/10) * (0.25/30.0)
       lon+=float((int(unit)-1)%10) * 0.0125

       #Quarter Unit
       # Each quarter is 0.25/30/2 lat by 0.025 long degrees
       if quart=="C" or quart=="D": lat += (0.25 / 60.0)
       if quart=="B" or quart=="C": lon += (0.0125 / 2.0)

       lat += (0.25 / 60.0) / positionFactorY
       lon += (0.0125 / 2.0) / positionFactorX

    lon=-lon
    return lat, lon

uwiToLatLng = UWIToLatLng()