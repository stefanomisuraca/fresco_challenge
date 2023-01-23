# fresco_challenge
Code challenge for Fresco

## Technologies used

* Python framework -> Django
* REST Api frameWork -> Django Rest Framework (DRF)
* Container system -> Docker and DockerCompose
* Web server -> Nginx + Wgsi

## How to run the project

* Simply run `docker-compose up --build`
* Nginx server is running on port `8000` -> go to `localhost:8000`
* There is a predefined user for token request or admin access:
Username --> `test`
Password --> `test123`

The system will take care of running the migrations and the fixtures automatically

## Request to API

All API endpoints are protected, you need to request a token first

POST `/api-token-auth/` -> returns a new token
All requests must then include the header `Authorization: Token {token}`

- GET `/v1/receipts/` -> return all receipts belonging to the user
- GET `/v1/receipts/{receipt_id}/` -> return specific receipt belonging to the user
- POST `/v1/receipts/` -> create a new receipt
payload example :

```javascript
{
    "name": "Receipt",
    "instructions": [
        {
            "step_number": 1,
            "description": "Boil the pasta for 10 minutes"
        },
        {
            "step_number": 2,
            "description": "Drain the pasta"
        },
        {
            "step_number": 3,
            "description": "Enjoy your meal"
        }
    ],
    "ingredients": [
        {
            "ingredient_name":"pasta",
            "amount": 80,
            "unit": "gr"
        }
    ]
}
```

PUT `/v1/receipts/{receipt_id}/` -> Update an existing receipt
payload example:
```javascript
{
    "name": "Pasta Receipt", // Name has changed
    "instructions": [
        {
            "id": 3, // Note: Id is present, this item if found and updated
            "step_number": 1,
            "description": "Boil the pasta for 8 minutes" // value is changed
        },
        {
            "id": 4, // Note: Id is present but no changed, item is not updated
            "step_number": 2,
            "description": "Drain the pasta"
        },
        {
           // Note: Id is not present: Item is created
            "step_number": 3,
            "description": "mix the pasta with other ingredient"
        }
        // Note: the old step 3 ID is not present, that item will be removed
    ],
    "ingredients": [ // Same update logic for Ingredients
        {
            "id": 1,
            "ingredient_name":"pollo",
            "amount": 300,
            "unit": "gr"
        }
    ]
}
```

## Considerations

- The authentication system is simple and naive, this is just semplification in order present an idea of token authentication. In a real project, a JWT token authentication with OAuth2 would be my first choice, depending on the context.

Most of the files have been created or modified by me.
The only files created by Django are the migrations files, based on the models, and some configurations files.
To avoid confusion, I'm writing a list of the files I wrote.

* /fixtures/*
* /fresco_project/settings.py (modified from a template)
* /fresco_project/urls.py
* /nginx/*
* /v1/api_views/*
* /v1/admin.py, /v1/models.py, /v1/serializers.py
* /docker_startup.sh
* /docker-compose.yml, /docker-compose.override.yml
* /Dockerfile
* /fresco.uwsgi.ini
* /requirements.in
* /run.sh

## Tests
In a real project I would have chosen a unit test approach with pytest framework or similar, depending on the context.
In this case I would test the api behaviour by mocking the responses or using a test database for real testing scenarios.
Tests are not present due to lack of time, sorry for that.
