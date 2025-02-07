import numpy as np
from redis.commands.search.query import Query

class RecommendationsService:

    def __init__(self, redis_client, vectorizer):
        self.redis_client = redis_client
        self.vectorizer = vectorizer

    def get_user_interested_products(self, user_id):
        products_ids = self.redis_client.zrange(f"products:events:view:users:{user_id}", 0, 2, desc=True)
        recommendations_query = self.__get_recommendations_query(products_ids)
        query_vector_bytes = self.__generate_query_embedding(recommendations_query).tobytes()
        recommended_products = self.__get_recommended_products(query_vector_bytes)
        return self.__map_recommendations_to_response(recommended_products)

    def __get_recommendations_query(self, product_ids):
        products_desc = []

        for product_id in product_ids:
            key = f"products:items:{product_id}"
            product = self.redis_client.hmget(key, ["name", "categories"])

            if not product[0]:
                continue

            products_desc.append(" ".join(product))

        return " ".join(products_desc)

    def __generate_query_embedding(self, query_text):
        return self.vectorizer.transform([query_text]).toarray().astype(np.float32).flatten()

    def __get_recommended_products(self, query_vector_bytes):
        return self.redis_client.ft("products_items_index").search(
            Query("(*)=>[KNN 5 @embedding $query_vector AS score]")
                .sort_by("score")
                .return_fields("score", "id", "name", "categories")
                .dialect(2)
            ,
            { 'query_vector': query_vector_bytes }
        )

    @staticmethod
    def __map_recommendations_to_response(recommended_products):
        return [
            {
                "id": doc.id,
                "name": doc.name,
                "categories": doc.categories.split(", "),
                "score": float(doc.score)
            }
            for doc in recommended_products.docs
        ]