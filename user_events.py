from redis import Redis

def mock_user_events(redis_client):
    user_mock_key = "products:events:view:users:123e4567-e89b-12d3-a456-426614174007"
    
    if redis_client.exists(user_mock_key):
        return

    redis_client.zadd(
        user_mock_key,
        mapping = {
            1: 1738628288000,
            3: 1738585088000,
            2: 1738577882000,
            36: 1738577522000,
            6: 1738570322000,
            20: 1738563122000,
            7: 1738548722000
        }
    )
    print("User events mocks Embeddings saved successfully!")