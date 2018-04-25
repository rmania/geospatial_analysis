from shapely.geometry import Polygon, mapping

def df_to_geojson(df, properties):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'MultiPolygon',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [mapping(row['geometry'])]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        geojson['features'].append(feature)
    return geojson