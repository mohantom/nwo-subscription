# nwo-subscription
A webservice to manage user subscriptions

## Design
1. Serverless (AWS Lambda) is used to as the webservice to handle the REST requests. Lambda can be easily automatically scaled to handle many requests and spike of requests. While the volume is low, lambda will scale down by itself to keep the cost low.
2. Dynamodb is used to store the user subscriptions. "nwo_subscriptions" is used to store current active subscriptions, "nwo_subscriptions_archive" is used to store the archived subscriptions. Dynamodb has a very low latency and can also handle huge amount of data. Cost is low if volume is low. RDBMS can also be used if the subscription volume is not too high, but it comes with constant cost to keep it running.
3. FastAPI is used as the web framework to handle REST requests. It is lightweight and easy to use and scale. It uses Pydantic for type hint and validation.
4. This webservice currently handle GET, POST, PUT, DELETE to manage subscriptions (retrieve, add, update and delete).
5. GitHub actions are used to run build, test and deployment


## Quick start for local development
```commandline
bash install.sh
python main.py
```

You should see Swagger UI here: [Swagger UI](http://localhost:8001/docs)

## Examples
### Add a new subscription
```commandline
curl --location 'http://localhost:8001/api/v1/subscription' \
--header 'Content-Type: application/json' \
--header 'x-api-key;' \
--data-raw '{
  "email": "test@gmail.com",
  "industries": ["Consumer", "Health"],
  "sources": ["News", "Social Media"]
}'
```

### Get a subscription
```commandline
curl --location 'http://localhost:8001/api/v1/subscription?id=648a3f89-d473-4fb6-b8d4-6ed9d5c47516' \
--header 'x-api-key;'
```

### Update a subscription
```commandline
curl --location --request PUT 'http://localhost:8001/api/v1/subscription' \
--header 'Content-Type: application/json' \
--header 'x-api-key;' \
--data-raw '{
    "id": "648a3f89-d473-4fb6-b8d4-6ed9d5c47516",
  "email": "test@gmail.com",
  "industries": ["Consumer", "Health"]
}'
```

### Archive a subscription
```commandline
curl --location --request DELETE 'http://localhost:8001/api/v1/subscription?id=648a3f89-d473-4fb6-b8d4-6ed9d5c47516' \
--header 'x-api-key;'
```