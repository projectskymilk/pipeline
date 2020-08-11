import mgrs
import simplekml
import math

def outputPolygon(lat,lon):
    leftSideLon = (lon+0.005)
    rightSideLon = (lon-0.005)
    topSideLat = (lat-0.005)
    bottomSideLat = (lat+0.005)

    return ([(leftSideLon,topSideLat),(rightSideLon,topSideLat),(rightSideLon,bottomSideLat),(leftSideLon,bottomSideLat)])


#TODO have to adjust based on precision provided!

def exportToKML(coords):
    kml = simplekml.Kml()
    pol = kml.newpolygon(name=designator)
    pol.outerboundaryis = coords
    kml.save(designator+'.kml')


def segmentedDesignator(fullAddress,precision): #precision in meters
    for char in fullAddress:
        if char.isalpha():
            gzdIndex=fullAddress.find(char)
            break

    gzdAndID = fullAddress[0:gzdIndex+3]
    easting = fullAddress[gzdIndex+3:9]
    northing = fullAddress[9:15]

    if (precision == 100000):
        return [gzdAndID]
    elif (precision == 0):
        return gzdAndID[0:gzdIndex+1]
    else: #(precision=truncate) = 10000=1 1000=2 100=3 10=4 1=5
        truncate = int(5-math.log(precision,10))
        easting = easting[0:truncate]
        northing = northing[0:truncate]
    return [gzdAndID,easting,northing]

latitude = 28.459629
longitude = -81.627454

m = mgrs.MGRS()

designator = "4QFJ1234567890" #(m.toMGRS(latitude,longitude))

coords = outputPolygon(latitude,longitude)

print (segmentedDesignator(designator,0))


