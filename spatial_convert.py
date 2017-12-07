## geospatial conversions
## =====================================================
# Latitude/Longitude to/from Web Mercator
import math
from pyproj import Proj, transform
 
def toWGS84(xLon, yLat):
    """ 
    convert WebMercator epsg:3857 to lon_lat epsg:4326 mathematically per point
    """
    #Check if coordinate out of range for Latitude/Longitude 
    if (abs(xLon) < 180) and (abs(yLat) > 90):
        return
 
    # Check if coordinate out of range for Web Mercator
    # 20037508.3427892 is full extent of Web Mercator
    if (abs(xLon) > 20037508.3427892) or (abs(yLat) > 20037508.3427892):
        return
 
    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
 
    latitude = (1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * yLat) / semimajorAxis)))) * (180/math.pi)
    longitude = ((xLon / semimajorAxis) * 57.295779513082323) - ((math.floor((((xLon / semimajorAxis) * 57.295779513082323) + 180.0) / 360.0)) * 360.0)
 
    return [longitude, latitude]
 
def toWebMercator(xLon, yLat):
    """ 
    convert lon_lat epsg:4326 to WebMercator epsg:3857 mathematically per point
    """
    # Check if coordinate out of range for Latitude/Longitude
    if (abs(xLon) > 180) and (abs(yLat) > 90):
        return
 
    semimajorAxis = 6378137.0  # WGS84 spheriod semimajor axis
    east = xLon * 0.017453292519943295
    north = yLat * 0.017453292519943295
 
    northing = 3189068.5 * math.log((1.0 + math.sin(north)) / (1.0 - math.sin(north)))
    easting = semimajorAxis * east
 
    return [easting, northing]


inProj = Proj(init='epsg:4326')
outProj = Proj(init = 'epsg:3857')

def towgs84(row):
    """
    convert lon_lat epsg:4326 to WebMercator epsg:3857 on Pandas Series
    """
    return pd.Series(transform(inProj, outProj, row['longitude'], row['latitude']))

