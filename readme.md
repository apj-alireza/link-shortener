# ToDo:
-[X] invalid token returns 500, return 401 unauthorized
-[X] invalid username returns 500, return 401 unauthorized


# Task
## Environment variables [DONE]

## CRUD (Create, Read, Update, Delete) APIs for link management
- Endpoint:
    - POST /links
        - Store the destination address and ID to links tables
        - return destination address, ID, redirect URL after successful creation
        - Redirect-URL is: HOST/r/{RANDOM_STRING} 
    - GET /links -> returns list of user links
    - UPDATE /links/{ID}
        - Update the destination link based on it's ID
    - DELETE /links/{ID}
        - Delete the link by it's ID
        
    -connect all of them to the middleware


## Redirect
- Endpoint GET /r/{RANDOM_STRING}
redirect to destination address based on the random string


## to ask:
the coorect way of base models in main file