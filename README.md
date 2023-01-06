# Sure cost calculator app

# Setup
The app requires docker to be installed https://docs.docker.com/desktop/install/mac-install/. Default install should also give you access to docker-compose which is used by the Makefile. The Makefile has a few commands to make development a little easier. To bootstrap the app simply run `make init`. That command will build the docker container, spin up the db/Django web service, run migrations, and tail the logs. The container will be about 600MB.

# Authentication
Once the app is running, create an admin user with `make createsuperuser username=sure_user email=sure@gmail.com`. The `username` and `password` you create from the prompt will be required to authenticate to use the service. In this example I am using httpie which can be installed with `brew install httpie` but Postman or curl will work just as well. Dealers choice.

```
http post http://127.0.0.1:8000/api/token/ username=sure_user password=1
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 483
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 06 Jan 2023 01:29:33 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.16
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcyOTY4ODczLCJpYXQiOjE2NzI5Njg1NzMsImp0aSI6IjliNWY1ZTAwMmRmNzRmYWM4NWUzMTI5YzdjOTA4YmYyIiwidXNlcl9pZCI6MX0.aUZmMmKnTKRcEQLhGTXLsq6ex6c0mzbSgCzcpAdnhNo",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MzA1NDk3MywiaWF0IjoxNjcyOTY4NTczLCJqdGkiOiJmY2IwNTA2YWZlNmQ0NzRjOTQ1NGZmZThmMjExOGQ4NSIsInVzZXJfaWQiOjF9.4am8ycA1YDnF2Y8r08iHvc_vLk4RHCw1VyYsH4q_aeY"
}
```

The access token is valid for 5 minutes. When it expires you can either re authenticate or grab the refresh token and hit

```
http post http://127.0.0.1:8000/api/token/refresh/ refresh=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MzA1NDk3MywiaWF0IjoxNjcyOTY4NTczLCJqdGkiOiJmY2IwNTA2YWZlNmQ0NzRjOTQ1NGZmZThmMjExOGQ4NSIsInVzZXJfaWQiOjF9.4am8ycA1YDnF2Y8r08iHvc_vLk4RHCw1VyYsH4q_aeY`
```

The access token returned from that call will be valid for 24 hours.

# Test
To run the entire test suite use the make command `make tests`. Note this requires the web service to be up or it will error out.
```
make tests
docker exec -ti sure-assignment-web-1 sh -c "pytest ."
=============================================================================================================== test session starts ================================================================================================================
platform linux -- Python 3.8.16, pytest-7.2.0, pluggy-1.0.0
django: settings: sureapp.settings (from ini)
rootdir: /code, configfile: pytest.ini
plugins: celery-4.4.1, Faker-15.3.4, django-4.5.2
collected 45 items

lib/tests/test_cost_calculator.py ...........                                                                                                                                                                                                [ 24%]
quotes/tests/test_quote_service.py ..                                                                                                                                                                                                        [ 28%]
quotes/tests/test_quotes.py .........                                                                                                                                                                                                        [ 48%]
states/tests/test_states.py .......                                                                                                                                                                                                          [ 64%]
users/tests/test_user_service.py ....                                                                                                                                                                                                        [ 73%]
users/tests/test_users.py ............
```

# Application usage
The Django project has three domains. There are no FK constraints across apps by design. If an app requires data from another app there will be an `<app>_service.py` that will be responsible for hydrating their models with the appropriate data. This pattern was implemented with the foresight that these apps might be broken into their own services at some point. Allowing FK constraints across apps makes it very easy to query data via the ORM but makes it very hard to decouple when services are seperated.

## Routes
```
# USERS
http://localhost:8000/users/ -> POST user or list users. Admin only
http://localhost:8000/users/<int:user_id>/ -> GET user or PATCH. Admin and IF the user is calling their own data

# STATES
http://localhost:8000/states/<int:state_id>/ -> GET state or PATCH. Admin only

# QUOTES
http://localhost:8000/quotes/<int:quote_id>/ -> GET quote. Admin and IF the user is calling their own data
```

## Quote creation
The quote is created as the user is registered in the app. The following data is required in the payload to successfully create a user:
![Screen Shot 2023-01-05 at 6 59 28 PM](https://user-images.githubusercontent.com/11825992/210914410-15d267d3-7155-413f-b6ce-a12823b050e7.png)
The User object uses the default Django auth `User` model but the extra metadata is stored in `UserInformation` which has a FK to the `User` model. If the user is patched with different quote data such as `has_pet`, a new quote will be created and the previous one deleted. As of now there is a unqiue constraint to only allow one active quote per user. That could be easily changed if desired by Product.

## State data
All active states will be held in the `State` model. This will also hold all costs associated with the state such as flood and monthly tax. If a hurricane cost were to be added it would require a migration to add a new column(also alter the calculator logic). You can patch a state object to update its data. If a user has a quote created based on a state, and the state data gets updated, the next time the user GET's their quote it will be updated using the new state data and be persisted to the database.

