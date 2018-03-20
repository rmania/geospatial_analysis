## geospatial conversions
## =====================================================
# Latitude/Longitude to/from Web Mercator
import math
from pyproj import Proj, transform
import numpy as np
#from cartopy import crs
 


inProj = Proj(init='epsg:4326')
outProj = Proj(init = 'epsg:3857')

def towgs84(row):
    """
    convert lon_lat epsg:4326 to WebMercator epsg:3857 on Pandas Series
    """
    return pd.Series(transform(inProj, outProj, row['longitude'], row['latitude']))


def transform_coords(df):
    df = df.copy()
    lons = np.array(df['longitude'])
    lats = np.array(df['latitude'])
    coords = crs.GOOGLE_MERCATOR.transform_points(crs.PlateCarree(), lons, lats)
    df['longitude'] = coords[:, 0]
    df['latitude']  = coords[:, 1]
    return df

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

def lonlat_to_meters(df, lon_column, lat_column):
    """
    function 1 to convert to WebMercator format
    Convert longitude, latitude GPS coordinates into meters west and north of Greenwich (Web Mercator format). This makes it easier to overlay those with tiles from map providers.
    args:
        df: pandas Dataframe
        lon_name: dataframe column where the longitude coordinates are stored
        lat_name: dataframe column where the latitude coordinates are stored
    example:
        lonlat_to_meters(df, 'lon', 'lat')
    returns:
        df with converted coordinates
    """
    lat = df[lat_column]
    lon = df[lon_column]
    df.loc[:, ('x')] = df.loc[:, (lat_column)]
    df.loc[:, ('y')] = df.loc[:, (lon_column)]
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    df.loc[:, 'x'] = mx
    df.loc[:, 'y'] = my
    
    return df
