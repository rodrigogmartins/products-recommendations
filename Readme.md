# Sistema de recomendações utilizando bases de dados vetoriais

## Passo-a-passo

1. O servidor recebe uma requisição com o identificador de um usuário.
2. A aplicação busca os últimos 3 produtos visualizados por esse usuário.
3. Concatena informações como nome e categorias de todos esses produtos, formando um único texto de busca.
4. Realiza o processo de embedding deste texto de busca, transformando-o em um vetor.
5. Então, a aplicação realiza uma busca dos 5 itens mais relevantes na base vetorial. Para isso, é utilizando o algoritmo kNN - K-nearest neighbors, ou, simplesmente, K-vizinhos mais próximos.
6. O resultado então é mapeado para um formato que faça sentido para o cliente e retornado.

## Rodando o Projeto

1 . Execute os containers necessários para a aplicação
```bash
$ docker-compose up -d
```

2. Instale e rode uma virtualenv
```bash
$ pip3 install virtualenv
$ python3.8 -m venv venv
$ venv\Scripts\activate
```

3. Instale as dependências do projeto
```bash
$ pip install redis redis-om scikit-learn flask transformers torche
```

4. Rode o seguinte comando para criar eventos de visualização para o usuário **123e4567-e89b-12d3-a456-426614174007**
```bash
$ python user_events.py
```

5. Rode o seguinte comando para popular a base de dados vetorial
```bash
$ python embeddings_tf.py
```

6. Rode a aplicação através do comando
```bash
$ python server.py
```

7. Realize uma chamada para o serviço e obtenha as recomendações
```bash
$ curl --request GET
    --url 'http://localhost:5000/search?userId=123e4567-e89b-12d3-a456-426614174007'
```
