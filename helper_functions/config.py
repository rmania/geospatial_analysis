#!/usr/bin/python
import pandas as pd
import configparser
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import sys
sys.path.insert(0, '../')
 
def config(config_path = '../', filename='config.ini', section='postgresql'):
    # create a parser.
    parser = configparser.ConfigParser()
    # read config file
    parser.read(config_path + filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

def postgres_engine_pandas(config_full_path, db_config_name):
    """
    Pandas uses SQLalchemy, this is the config wrapper to insert config parameters in to_sql queries.
    Args:
      1. config_full_path: location of the config.ini file including the name of the file, for example authentication/config.ini
      2. db_config_name: dev or docker to get the ip user/password and port values.
    Returns:
        The postgres pandas engine to do sql queries with.
    """
    config = configparser.RawConfigParser()
    config.read(config_full_path)

    postgres_url = URL(
        drivername='postgresql',
        username=config.get(db_config_name, 'user'),
        password=config.get(db_config_name, 'password'),
        host=config.get(db_config_name, 'host'),
        port=config.get(db_config_name, 'port'),
        database=config.get(db_config_name, 'dbname')
    )

    engine = create_engine(postgres_url)
    return engine


def psycopg_connection_string(config_full_path, db_config_name):
    """
    Postgres connection string for psycopg2.
    Args:
      1. config_full_path: location of the config.ini file including the name of the file, for example authentication/config.ini
      2. db_config_name: dev or docker to get the ip user/password and port values.
    Returns:
        Returns the psycopg required connection string: 'PG:host= port= user= dbname= password='
    """

    config = configparser.RawConfigParser()
    config.read(config_full_path)

   
    print(db_config_name)
    host = config.get(db_config_name,'host')
    port = config.get(db_config_name,'port')
    user = config.get(db_config_name,'user')
    dbname = config.get(db_config_name,'dbname')
    password = config.get(db_config_name,'password')

    return 'host={} port={} user={} dbname={} password={}'.format(
        host, port, user, dbname, password
    )


# load csv to PostgreSQL database, write to 'OSM' schema
def load_csv_to_postgres(datadir, filename, table_name, schema,
                         config_path, config_name, all_csv=None):
    """
    Load csv into postgres for single & multiple files
    Args:
        datadir: data directory where file to be uploaded is stored. f.i. data/
        filename: name of the csv
        table_name: table_name in the Postgres db (needs to be present!)
        schema: the schema in postgreSQL where data file should land
        config_path: path to the config file. f.i. auth/config.ini
        config_name: name of the databse config. f.i. 'postgresql'
        all_csv = default false. If True will upload all the csv files in the datadir.
        """
    
    df = pd.read_csv(datadir + filename)
        
    if all_csv:
        csv_files = [glob.glob(x) for x in [datadir + '*.csv']]
        for csv_file in csv_files:
            df = pd.read_csv(datadir + csv_file)
        
    # establish engine
    engine = postgres_engine_pandas(config_path, config_name)
    print (engine)
    
    table_name = table_name
    
    df.to_sql(table_name, engine, schema = schema,
              if_exists='replace', 
              index=True, 
              index_label='idx')  