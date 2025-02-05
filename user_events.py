from redis import Redis

def save_to_redis(redis_client):
    redis_client.zadd(
        "products:events:view:users:123e4567-e89b-12d3-a456-426614174007",
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

def main():
    redis_client = Redis(host="localhost", port=6379, decode_responses=False)
    save_to_redis(redis_client)
    print("Eventos de usuários salvos com sucesso!")

if __name__ == "__main__":
    main()
