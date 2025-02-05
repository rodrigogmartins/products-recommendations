from sklearn.feature_extraction.text import TfidfVectorizer

class QueryVectorizer:

    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.vectorizer = TfidfVectorizer()

    def get_vectorizer(self):
        keys = self.redis_client.keys("products:items*")
        all_descriptions = [
            self.redis_client.hget(key, "description") for key in keys if self.redis_client.hget(key, "description")
        ]
        self.vectorizer.fit(all_descriptions)

        return self.vectorizer
