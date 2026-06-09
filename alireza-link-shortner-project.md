بLink shortner:

# Phase 1
components:
- SQL db to store:
    - users
    - links -> users

# DoD:
- RESTful API user manageemnt + authentication
- RESTful API CRUD (Create, Read, Update, Delete) on user's links
- redirect urls to the desired destination


# APIs:
POST /user
request body in json:
- username
- password
response boyd:
- JWT token

GET /user
Header: 'Authenticaion: bearer JWT-TOKEN'
response body:
- username
- ID


POST /link
Header: 'Authenticaion: bearer JWT-TOKEN'
request body:
- destination link
response body:
- id
- shortend url with random id

GET /link
Header: 'Authenticaion: bearer JWT-TOKEN'
response body:
- list of user links

GET /link/{ID}
Header: 'Authenticaion: bearer JWT-TOKEN'
response body:
- information about the link based on provided id

UPDATE /link/{ID}
Header: 'Authenticaion: bearer JWT-TOKEN'
request body:
- destination url 
response body:
- information about the link based on provided id

DELETE /link/{ID}
Header: 'Authenticaion: bearer JWT-TOKEN'
response body:
- deleted succesfuly


Example:

input link: google.com

DOMAIN.COM/poijwapjasdoijzpxocijpoaiwjer

client -> 127.0.0.1:8080/poijwapjasdoijzpxocijpoaiwjer - redirect -> google.com


# path Summary
- RESTful API
- Fast API
- JWT token
- 


# Phase 2
SOON...
