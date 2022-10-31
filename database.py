# ********************************************************************
# * Project Name : prog_tech_lr3									*
# * File Name : database.py											*
# * Programmer : Katin Georgy , Kozlov Vladislav					*
# * Modifyed By : Katin Georgy , Kozlov Vladislav					*
# * Created : 12 / 10 / 22											*
# * Last Revision : 22 / 10 / 21									*
# ********************************************************************
import psycopg2
from psycopg2 import OperationalError
import pandas as pd
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from sqlalchemy import create_engine


def make_df():
    connection = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    type_leisure_df = pd.read_sql_table('type_leisure', connection)
    type_event_df = pd.read_sql_table('type_event', connection)
    event_information_df = pd.read_sql_table('event_information', connection)

    return type_leisure_df, type_event_df, event_information_df

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Функция, осуществляющая подключение к базе данных"""

    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError:
        print('Подключение осуществленно успешно')
    return connection

def execute_query(query):
    """
    Функция, осуществляющая введение запроса в БД через переменную query.
    :param query: запрос в PostrgeSQL
    :return: None
    """
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except OperationalError:
        print('An OperationalError occurred')