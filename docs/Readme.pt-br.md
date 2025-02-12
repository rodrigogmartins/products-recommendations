# Sistema de recomendações utilizando bases de dados vetoriais

[![en](https://img.shields.io/badge/lang-en-red.svg)](../README.md) [![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](README.pt-br.md)

## Caso de uso

Um e-commerce com um catálogo amplo de produtos e dados analíticos dos usuários deseja implantar um sistema de recomendações de forma que os usuários consigam obter uma lista de itens com maior relevância com base nos itens vistos previamente.

## Considerações

1. Estão sendo levados em conta apenas **os últimos três itens visualizados**.
2. A quantidade de eventos não está sendo levada em consideração.
3. Outros tipos de eventos não estão sendo levados em consideração.

## Passo-a-passo

1. O servidor recebe uma requisição com o identificador de um usuário.
2. A aplicação busca os últimos 3 produtos visualizados por esse usuário.
3. Concatena informações como nome e categorias de todos esses produtos, formando um único texto de busca.
4. Realiza o processo de embedding deste texto de busca, transformando-o em um vetor.
5. Então, a aplicação realiza uma busca dos 5 itens mais relevantes na base vetorial. Para isso, é utilizando o algoritmo kNN - K-nearest neighbors, ou, simplesmente, K-vizinhos mais próximos.
6. O resultado então é mapeado para um formato que faça sentido para o cliente e retornado.

## Possibilidades

Existem algumas altrações que podem ser feitas com o intuito de atingir uma robustez maior da solução.

1. Considerar outros eventos dos usuários. Exemplo:
    - Compra de produtos
    - Adicionar produtos ao carrinho
2. Considerar a quantidade de eventos por produto em determinado período de tempo. Exemplo:
    - Os 5 produtos mais visualizados por determinado usuário nos últimos 7 dias.
3. Considerar eventos dos produtos a serem recomendados. Exemplo:
    - Os 10 produtos mais comprados pelos usuários
    - Os 10 produtos mais vistos nos últimos 7 dias.

## Rodando o Projeto

1. Execute os containers necessários para a aplicação

```bash
docker-compose up -d
```

2. Instale e rode uma virtualenv

```bash
pip3 install virtualenv
python3.8 -m venv venv
venv\Scripts\activate
```

3. Instale as dependências do projeto

```bash
pip install redis redis-om scikit-learn flask transformers torche
```

4. Rode a aplicação através do comando

```bash
python server.py
```

5. Realize uma chamada para o serviço e obtenha as recomendações

```bash
curl --request GET
    --url 'http://localhost:5000/search?userId=123e4567-e89b-12d3-a456-426614174007'
```
