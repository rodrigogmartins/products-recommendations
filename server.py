from flask import Flask, request, jsonify
from redis import Redis

from query_vectorizer import QueryVectorizer
from recommendations_service import RecommendationsService

from user_events import mock_user_events
from embeddings_tf import mock_embeddings

app = Flask(__name__)
app.debug = True

redis_client = Redis(host="localhost", port=6379, decode_responses=True)
mock_user_events(redis_client)
mock_embeddings(redis_client)
query_vectorizer = QueryVectorizer(redis_client)
vectorizer = query_vectorizer.get_vectorizer()
recommendations_service = RecommendationsService(redis_client=redis_client, vectorizer=vectorizer)

@app.route("/search", methods=["GET"])
def search():
    try:
        user_id = request.args.get("userId")

        if not user_id:
            return jsonify({"error": "A 'userId' parameter is required"}), 400

        response = recommendations_service.get_user_interested_products(user_id)

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)