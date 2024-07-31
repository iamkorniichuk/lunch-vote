# Lunch Vote

Internal service for its 'employees which helps them to make a decision at the lunch place.

## Installation

#### 1. Setting up environment

First of all, you need to create [.env](./.env) file inside root folder.
For **testing purposes** there is [example.env](./example.env). You can rename/copy it to [.env](./.env) file.

> :warning: Beware not to use [example.env](./example.env) as main env file in production! This makes your site extremely vulnerable.

#### 2. Starting Docker

To build and run Docker container:

```sh
docker compose up -d --build
```

> :warning: Make sure you have running Docker program instance.

## Testing

#### 1. Running tests

To run Django tests use this command:

```sh
docker exec lunch-vote-web-1 python manage.py test
```

#### 2. Initial data

To load testing fixtures run:

```sh
docker exec lunch-vote-web-1 python manage.py loaddata users restaurants votes
```

> :warning: Beware not to use these fixtures in production! It can compromise your site's security.

## Example Flow

#### 1. Sign up

```sh
curl --request POST \
  --url http://localhost/users/signup/ \
  --header 'Content-Type: application/json' \
  --data '{
  "username": "ilarion",
  "password": "12-my-p4ssword"
}'
```

#### 2. Create Restaurant

```sh
curl --request POST \
  --url http://localhost/restaurants/ \
  --header 'Authorization: Bearer {{ACCESS_TOKEN}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "Tasty Food"
}'
```

#### 3. Add today's Menu

```sh
curl --request POST \
  --url http://localhost/menus/ \
  --header 'Authorization: Bearer {{ACCESS_TOKEN}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "restaurant": {{RESTAURANT_PK}},
  "items": [
    {
      "name": "Barbecue sauce"
    },
    {
      "name": "Pizza"
    },
    {
      "name": "Fanta"
    }
  ]
}'
```

> :warning: You can't add/edit menu for the restaurant added by another user.

#### 4. Get today's Menus & theirs votes

```sh
curl --request GET \
  --url http://localhost/restaurants/ \
  --header 'Authorization: Bearer {{ACCESS_TOKEN}}' \
  --header 'Content-Type: application/json'
```

#### 5. Vote for today's Menu

```sh
curl --request POST \
  --url http://localhost/votes/{{RESTAURANT_PK}}/ \
  --header 'Authorization: Bearer {{ACCESS_TOKEN}}' \
  --header 'Content-Type: application/json'
```

> :warning: You can't vote for your own menu or vote twice.

#### 6. Get results of Voting for certain Date

```sh
curl --request GET \
  --url 'http://localhost/restaurants/?menu_date={{ISO_FORMAT_DATE}}' \
  --header 'Authorization: Bearer {{ACCESS_TOKEN}}' \
  --header 'Content-Type: application/json'
```

> :heavy_check_mark: The current winner of this date will be on top of the list.
