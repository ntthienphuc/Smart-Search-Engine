from elasticsearch import Elasticsearch
import time

from .database import DatabaseManager


class SearchEngine:
    """
    A class to manage and execute search queries on an Elasticsearch index.
    """

    def __init__(self) -> None:
        pass

    def path(self):
        """
        Return Elasticsearch connection and index name.

        Returns:
            tuple: A tuple containing the Elasticsearch connection and the index name.
        """
        es = Elasticsearch([{'host': '172.20.0.1', 'port': 9200, 'scheme': 'http'}])
        index_name = "demo"
        return es, index_name

    def search(self, search_term: str):
        """
        Execute an Elasticsearch query based on the provided search term.

        Args:
            search_term (str): The term to search for in the Elasticsearch index.

        Returns:
            dict: The response from Elasticsearch.
        """
        es, index_name = self.path()
        time_embed = time.time()
        query_vector = DatabaseManager().vector(search_term)
        print(len(query_vector))
        print('TIME EMBEDDING ', time.time() - time_embed)
        # Elasticsearch query
        query = {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity("
                              "params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
        response = self.es.search(
            index=self.index_name, body={
                "size": 20,
                "query": query}, ignore=[400])
        return response

    def main(self, search_term: str, volumn: float) -> list:
        """
        Retrieve and rank search results based on similarity to the search term.

        Args:
            search_term (str): The term to search for in the Elasticsearch index.
            volumn (float): Minimum similarity score to consider for results.

        Returns:
            list: A list of search results with their associated similarity scores.
        """
        lst = []
        response = self.search(search_term)
        # Sắp xếp kết quả theo độ tương tự giảm dần
        response["hits"]["hits"].sort(key=lambda x: x["_score"], reverse=True)
        for hit in response["hits"]["hits"]:
            _source = hit['_source']
            _name = _source['name']
            if hit['_score'] / 2 > volumn != None:
                lst.append([str(_name).replace('Name image: ', ''),
                            str(hit['_score'] / 2).replace('Score: ', '')])
        return lst
