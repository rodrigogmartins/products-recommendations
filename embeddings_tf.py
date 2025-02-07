import json

import numpy as np
from redis import Redis
from redis.commands.search.field import TagField, VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from sklearn.feature_extraction.text import TfidfVectorizer

def load_and_process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products_data = []
    descriptions = []

    for item in data:
        description = f"O produto {item['name']} possui as seguintes categorias: {', '.join(item['categories'])}."
        product_data = {
            "id": f"{item['id']}",
            "name": item['name'],
            "price": f"{item['price']}",
            "categories": f"{', '.join(item['categories'])}",
            "description": description
        }
        descriptions.append(description)
        products_data.append(product_data)

    return products_data, descriptions

def generate_tfidf_embeddings(documents):
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(documents)

def save_to_redis(redis_client, products_data, embeddings):
    index_name = "products_items_index"
    dimension = embeddings.shape[1]

    try:
        redis_client.ft(index_name).dropindex(delete_documents=False)
    except:
        print(f"Creating index {index_name}")

    redis_client.ft(index_name).create_index([
        TagField("id"),
        TextField("name"),
        VectorField("embedding", "FLAT", {
            "TYPE": "FLOAT32",
            "DIM": dimension,
            "DISTANCE_METRIC": "COSINE"
        })
    ], definition=IndexDefinition(prefix=["products:items:"], index_type=IndexType.HASH))

    for i, product in enumerate(products_data):
        vector = embeddings[i].toarray().astype(np.float32).flatten()
        redis_client.hset(
            f"products:items:{product['id']}",
            mapping={
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "categories": product["categories"],
                "description": product["description"],
                "embedding": vector.tobytes()
            }
        )

def mock_embeddings(redis_client):
    if redis_client.exists("embeddings_saved"):
        return
    
    products_data, descriptions = load_and_process_json("ProductsToRecommend.json")
    embeddings = generate_tfidf_embeddings(descriptions)
    save_to_redis(redis_client, products_data, embeddings)
    redis_client.set("embeddings_saved", "1")
    print("Embeddings saved successfully!")
