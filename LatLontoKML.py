#input latitude/longitude and desired precision, output KML file titled after MGRS designator
import mgrs
import simplekml
import math

def outputPolygon(lat,lon,designator):
    offsetter = 5
    if len(designator[1]) == 0: #100km or 6x8 degree precision
        if len(designator[0]) >= 4: #100km
            offsetter /= 10
        else:
            pass #never gonna need this level of imprecision, 6x8 degrees lat/lon
    else:
        offsetter /= 10**(len(designator[1])+1)

    leftSideLon = (lon+offsetter)
    rightSideLon = (lon-offsetter)
    topSideLat = (lat-offsetter)
    bottomSideLat = (lat+offsetter)

    coords = ([(leftSideLon,topSideLat),(rightSideLon,topSideLat),(rightSideLon,bottomSideLat),(leftSideLon,bottomSideLat)])

    exportToKML(coords,designator)


def exportToKML(coords,designator):
    mgrsName = ""
    for string in designator:
        mgrsName+=string
    kml = simplekml.Kml()
    pol = kml.newpolygon(name=mgrsName)
    pol.outerboundaryis = coords
    kml.save(mgrsName+'.kml')


def segmentedDesignator(fullAddress,precision): #precision in meters
    for char in fullAddress:
        if char.isalpha():
            gzdIndex=fullAddress.find(char)
            break

    gzdAndID = fullAddress[0:gzdIndex+3]
    easting = fullAddress[gzdIndex+3:10]
    northing = fullAddress[10:15]

    if (precision == 100000):
        easting = ""
        northing = ""
    elif (precision == 0):
        gzdAndID = gzdAndID[0:gzdIndex+1]
        easting = ""
        northing = ""
    else: #(precision=truncate) = 10000=1 1000=2 100=3 10=4 1=5
        truncate = int(5-math.log(precision,10))
        easting = easting[0:truncate]
        northing = northing[0:truncate]
    return [gzdAndID,easting,northing]

#INPUTS
latitude = 28.459629
longitude = -81.627454
precisionDesired = 100000 #in meters

m = mgrs.MGRS()
designator = segmentedDesignator(m.toMGRS(latitude,longitude),precisionDesired)
print (designator)


outputPolygon(latitude,longitude,designator)



