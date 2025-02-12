# Recommendation System Using Vector Databases

[![en](https://img.shields.io/badge/lang-en-red.svg)](./Readme.md) [![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](./docs/Readme.pt-br.md)

## Use Case

An e-commerce platform with a large product catalog and user analytics data wants to implement a recommendation system so that users can obtain a list of the most relevant items based on previously viewed products.  

## Considerations  

1. Only **the last three viewed items** are taken into account.  
2. The number of events is not considered.  
3. Other types of events are not considered.  

## Step-by-Step  

1. The server receives a request with a user identifier.  
2. The application retrieves the last three products viewed by that user.  
3. It concatenates information such as the name and categories of all these products, forming a single search text.  
4. The application performs the embedding process on this search text, transforming it into a vector.  
5. Then, the application searches for the five most relevant items in the vector database. To achieve this, the kNN algorithm - K-nearest neighbors, or simply K-nearest neighbors, is used.  
6. The result is then mapped to a format that makes sense for the client and returned.  

## Possibilities  

There are some modifications that can be made to achieve greater robustness in the solution.  

1. Consider other user events. Example:  
    - Product purchases  
    - Adding products to the cart  
2. Consider the number of events per product within a given time period. Example:  
    - The five most viewed products by a specific user in the last seven days.  
3. Consider events related to the recommended products. Example:  
    - The ten most purchased products by users  
    - The ten most viewed products in the last seven days  

## Running the Project  

1. Start the necessary containers for the application 

```bash
docker-compose up -d
```

2. Install and run a virtual environment

```bash
pip3 install virtualenv
python3.8 -m venv venv
venv\Scripts\activate
```

3. Install the project dependencies

```bash
pip install redis redis-om scikit-learn flask transformers torche
```

4. Run the application using the command

```bash
python server.py
```

5. Make a request to the service and obtain recommendations

```bash
curl --request GET
    --url 'http://localhost:5000/search?userId=123e4567-e89b-12d3-a456-426614174007'
```