import psycopg2


class PostgreSQLManager:
    """
    A class to manage interactions with a PostgreSQL database.

    Args:
        dbname (str): The name of the database to connect to.
        user (str): The database user to connect with.
        password (str): The password for the database user.
        host (str): The host of the database.
        port (str): The port to use for the connection.

    """

    def __init__(self,
                 dbname,
                 user,
                 password,
                 host,
                 port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def create_table(self,
                     table_name: str) -> None:
        """
        Create a new table in the database.

        Args:
            table_name (str): Name of the table to be created.

        """
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name TEXT,
            label TEXT[],
            vector FLOAT[]
        )
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_data(self,
                    table_name: str,
                    data: tuple) -> None:
        """
        Insert new data into a table.

        Args:
            table_name (str): Name of the table to insert data into.
            data (tuple): Data to be inserted.

        """
        insert_data_query = f"""
        INSERT INTO {table_name} (name, label, vector)
        VALUES (%s, %s, %s)
        """
        self.cur.execute(insert_data_query, data)
        self.conn.commit()

    def delete_data(self,
                    table_name: str,
                    id: int) -> None:
        """
        Delete data from a table based on ID.

        Args:
            table_name (str): Name of the table to delete data from.
            id (int): ID of the data to be deleted.

        """
        delete_data_query = f"""
        DELETE FROM {table_name} WHERE id = %s
        """
        self.cur.execute(delete_data_query, (id,))
        self.conn.commit()

    def drop_table(self,
                   table_name: str) -> None:
        """
        Drop a table from the database.

        Args:
            table_name (str): Name of the table to be dropped.

        """
        drop_table_query = f"""
        DROP TABLE IF EXISTS {table_name}
        """
        self.cur.execute(drop_table_query)
        self.conn.commit()

    def close_connection(self) -> None:
        """
        Close the connection to the database.
        """
        self.cur.close()
        self.conn.close()


# if __name__ == '__main__':
#     db = PostgreSQLManager(
#         dbname="trangvv",
#         user="postgres",
#         password="123456",
#         host="localhost",
#         port="5432"
#     )
#     db.drop_table('data')
#     db.create_table('data')
