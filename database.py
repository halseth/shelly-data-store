import psycopg2
from config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
       """
        CREATE TABLE device_status (
            id SERIAL PRIMARY KEY,
            device_id TEXT NOT NULL,
            device_name TEXT NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL default CURRENT_TIMESTAMP,
            payload JSONB NOT NULL
        )
        """,

   )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def insert_device_status(pg_config, device_id, device_name, status_json):
        """ Insert a new device status into the status table """

        sql = """INSERT INTO device_status(device_id, device_name, payload) 
                VALUES(%s, %s, %s) RETURNING id;"""

       # print("sql:", sql)
       # print("inserting", device_id, device_name, status_json)

        _id = None
        config = pg_config

        try:
            with  psycopg2.connect(**config) as conn:
                with  conn.cursor() as cur:
                    # execute the INSERT statement
                    cur.execute(sql, (device_id, device_name, status_json, ))

                    # get the generated id back
                    rows = cur.fetchone()
                    if rows:
                        _id = rows[0]

                    # commit the changes to the database
                    conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return _id

if __name__ == '__main__':
    create_tables()