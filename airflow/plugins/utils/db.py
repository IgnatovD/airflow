import csv
from io import StringIO
import pandas as pd
import psycopg2
from airflow.hooks.base import BaseHook



def _get_db_url(connector: str) -> str:
    connection = BaseHook.get_connection(connector)
    return f'user={connection.login} password={connection.password} host={connection.host} ' \
           f'port={connection.port} dbname={connection.schema}'


def load_data_to_db(connector: str, df: pd.DataFrame, table_name: str) -> None:

    buffer = StringIO()
    df.to_csv(buffer, index=False, sep='|', na_rep='NUL', quoting=csv.QUOTE_MINIMAL,
              header=False, float_format='%.8f', doublequote=False, escapechar='\\')
    buffer.seek(0)

    copy_query = f"""
        COPY {table_name}({','.join(df.columns)})
        FROM STDIN
        DELIMITER '|'
        NULL 'NUL'
    """

    conn = psycopg2.connect(dsn=_get_db_url(connector))
    with conn.cursor() as cursor:
        cursor.copy_expert(copy_query, buffer)

    conn.commit()
    conn.close()