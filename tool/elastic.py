import os
import configparser
import psycopg2
import json
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read(r'search_engine_v1.1\data\example.ini')


class SyncData:
    """
    A class to synchronize data between PostgreSQL and Elasticsearch.
    """

    def __init__(self) -> None:
        """Initializes the Elasticsearch and PostgreSQL connections and sets relevant configurations."""
        self.es = Elasticsearch([{'host': '172.20.0.1', 'port': 9200, 'scheme': 'http'}])

        # PostgreSQL connection details
        self.db_connection = psycopg2.connect(
            database="trangvv",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"  # Default port of PostgreSQL
        )
        self.db_cursor = self.db_connection.cursor()
        self.postgresql_table_name = "data"
        self.elasticsearch_index_name = "demo"

    def return_path(self) -> str:
        """Returns the current working directory with forward slashes."""
        return os.getcwd().replace("\\", "/")

    def sync(self) -> dict:
        """
        Sync data from PostgreSQL to Elasticsearch.

        Returns:
            dict: Response from Elasticsearch bulk operation.
        """
        bulk_data = []
        self.db_cursor.execute(f"SELECT * FROM {self.postgresql_table_name}")

        for record in self.db_cursor.fetchall():
            bulk_data.append({
                "index": {
                    "_index": self.index_name,
                    "_id": str(record[0])
                }
            })
            bulk_data.append({
                "id": str(record[0]),
                "name": record[1],
                "label": record[2],
                "vector": record[3],
                # Add other fields if necessary
            })

        response = self.es.bulk(body=bulk_data,
                                refresh=True)
        return response

    def delete_data(self):
        self.es.delete(index=self.elasticsearch_index_name,
                       id=self.elasticsearch_index_name,
                       ignore=[404])

    def create_data(self):
        paths = self.return_path() + "/elasticsearch/mapping.json"
        with open(paths, 'r') as file:
            data = json.load(file)
        self.es.indices.create(index=self.elasticsearch_index_name,
                               body=data,
                               ignore=[400])

    def __call__(self):
        """Syncs the data and prints the status of the synchronization."""
        response = self.sync()

        # Check the results
        if response["errors"]:
            for item in response["items"]:
                if "index" in item and item["index"]["status"] != 201:
                    print(f"Failed to index document with ID {item['index']['id']}")
        else:
            print("Bulk indexing completed successfully.")
