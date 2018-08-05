#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import xml.etree.ElementTree as ET
from logger_settings import logger

logger = logger()


def get_available_layers_from_wfs(url_wfs):
    """
        Get all layer names in WFS service, print and return them in a list.
    """
    layer_names = []
    parameters = {
        "REQUEST": "GetCapabilities",
        "SERVICE": "WFS"
    }

    getcapabilities = requests.get(url_wfs, params=parameters)
    root = ET.fromstring(getcapabilities.text)

    for neighbor in root.iter('{http://www.opengis.net/wfs/2.0}FeatureType'):
        logger.info("layername: " + neighbor[1].text)
        layer_names.append(neighbor[1].text)
        
    return layer_names


def get_layer_from_wfs(url_wfs, layer_name, crs, outputformat, retry_count=3):
    """
    Get layer from a wfs service.
    Args:
        1. url_wfs: full url of the WFS including https, excluding /?::
            https://map.data.amsterdam.nl/maps/gebieden
        2. layer_name: Title of the layer:: f.i. stadsdeel
        3. crs: coordinate system number, excluding EPSG::
            28992, 4326
        4. outputformat: leave empty to return standard GML (Geographic Markup language),
           otherwise: json, geojson, txt, shapezip
    Returns:
        The layer in the specified output format.
    """ 

    parameters = {
        "REQUEST": "GetFeature",
        "TYPENAME": layer_name,
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        "SRSNAME": "EPSG:{}".format(crs),
        "OUTPUTFORMAT": outputformat
    }

    logger.info("Requesting data from {}, layer: {}".format(
        url_wfs, layer_name))

    retry = 0

    # webrequests sometimes fail..
    while retry < retry_count:
        response = requests.get(url_wfs, params=parameters)
        logger.debug(response)
        if response.status_code == 400:
            logger.info("Incorrect layer name: {}, please correct the layer name".format(layer_name))
            continue
        if response.status_code != 200:
            time.sleep(3)
            # try again..
            retry += 1
        else:
            # status 200. Yeah!.
            break

    if outputformat in ('geojson, json'):
        geojson = response.json()
        logger.info("{} features returned.".format(str(len(geojson["features"]))))
        return geojson
    
    return response