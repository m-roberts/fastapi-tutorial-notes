# My FastAPI Tutorial Notes

This repository represents code snippets that I have taken from https://fastapi.tiangolo.com/tutorial/ and my corresponding notes.
Often, this is just a summary of what was written, but more concise.
I haven't written this for others, but it may offer some use in its current form.

I have only focused on some sections; mainly the content of and further reading presented in [RealPython's 'Using FastAPI to Build Python Web APIs' guide](https://realpython.com/fastapi-python-web-apis/).

I focused on the following sections:
* [`Tutorial - User Guide - Intro`](https://fastapi.tiangolo.com/tutorial/)
* [`First Steps`](https://fastapi.tiangolo.com/tutorial/first-steps/)
* [`Path Parameters`](https://fastapi.tiangolo.com/tutorial/path-params/)
* [`Query Parameters`](https://fastapi.tiangolo.com/tutorial/query-params/)
* [`Request Body`](https://fastapi.tiangolo.com/tutorial/body/)
* [`Query Parameters and String Validations`](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)
* [`Path Parameters and Numeric Validations`](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
* [`Dependency injection` to handle reusable logic for permissions, database sessions, and others](https://fastapi.tiangolo.com/tutorial/dependencies)
* [`Security` utilities to integrate authentication and authorization based on standards](https://fastapi.tiangolo.com/tutorial/security)
* [`Background tasks` for simple operations like sending an email notification](https://fastapi.tiangolo.com/tutorial/background-tasks)

Perhaps this may be of use to you as well.

## TODO
* Section on `Body` object
* Section on `Request` object

## Minimum Requirements
Python 3.10+ (required for [PEP 604](https://www.python.org/dev/peps/pep-0604/))
* `typing.Union[int, str]` -> `int | str`
* `typing.Optional[str]` -> `str | None`

## Links
### Automatic interactive API documentation
[Swagger UI](https://github.com/swagger-api/swagger-ui): http://127.0.0.1:8000/docs
[Redoc](https://github.com/Redocly/redoc): http://127.0.0.1:8000/redoc

### Raw Data
Raw OpenAPI schema: http://127.0.0.1:8000/openapi.json

### Further Reading

* [Bigger applications in multiple files](https://fastapi.tiangolo.com/tutorial/bigger-applications)
* [FastAPI + Web Sockets for real-time communication](https://fastapi.tiangolo.com/advanced/websockets)

## `01-hello_world.py`

### Getting familiar

Step 1 is to import FastAPI:
```
from fastapi import FastAPI
```
FastAPI is a Python class that provides all the functionality for your API.


Step 2 is to create a FastAPI instance:
```
app = FastAPI()
```

This `app` is the same one you refer to, to run the live server with uvicorn: `$ uvicorn main:app --reload`


Step 3 is to define a path operation decorator:

```
@app.get("/")
```

Step 4 is to define the path operation function, or the function that goes below the path operation decorator:
```
async def root():
```
Note: You could also define it as a normal function (`def`) instead of using `async def` if there is no need to `await` for anything in the function:
```
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

```
@app.get('/')
def results():
    results = some_library()
    return results
```
If your application (somehow) doesn't have to communicate with anything else and wait for it to respond, use `async def`.



Step 5 is to return the content:
```
    return {"message": "Hello World"}
```

You can return a dictionary, list, or singular values as strings, integers, and so on.
You can also return pydantic models.

## `02-order_matters.py`

### Order Matters: Put Fixed Paths First

Because path operations are evaluated in order, you need to make sure that the path for `/users/me` is declared before the one for `/users/{user_id}`:
```
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

Otherwise, the path for `/users/{user_id}` would also match for `/users/me`, thinking that it’s receiving the parameter `user_id` with a value of `"me"`.

## `03-pydantic_data_models.py`

You can use different type hints to define types, including Enums, etc. For more advanced usages, `pydantic` is used:

### Using `pydantic` Models to Define Request Body

Import `pydantic`'s `BaseModel` object and create a class that inherits from it:
```
from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str
    email: str | None = None
    age: int | None = None
```

Then use this for type hinting on the input of an API path:
```
@app.post("/users/")
async def create_user(user: User):
    return user
```

All automatic documentation is updated, and this also provides you with better editor support, such as autocompletion and type checks.

## `04-path_parameters_containing_paths.py`

OpenAPI doesn't support a way to declare a path parameter to contain a path inside, as that could lead to scenarios that are difficult to test and define.
Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette:
```
@app.get("/files/{file_path:path}")
```

Docs would still work, although **not adding any documentation telling that the parameter should contain a path**.

e.g. a path of `/home/johndoe/myfile.txt` (with a leading slash - `/`) would mean the URL would be: `/files//home/johndoe/myfile.txt` (with a double slash - `//`).

## `05-additional_validation.py`

### Add additional conditional checks for queries

It is possible to do customize a request with additional validation using `Query`.

```
q: str | None = Query(None)
```
makes the parameter optional, the same as:
```
q: str | None = None
```

In this code example, it is used as the default value of the parameter, setting parameters `min_length`, `max_length` and `regex` (available for `str`s):
```
async def read_item(
    q: str
    | None = Query(
        None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$"
    )
):
```

Also, `title` and `description` are included in the generated OpenAPI and used by the documentation user interfaces and external tools.

To make the parameter required, set the default value (first parameter) to `...`:
```
    q: str | None = Query(..., title="Query string", min_length=3, max_length=50, regex="^fixedquery$")
```

### Query parameter list / multiple values

It is possible to allow multiple values to be submitted under a particular parameter.
```
async def read_items(q: list[str] | None = Query(["foo", "bar"])):
```
would allow a URL like `http://localhost:8000/items/?q=foo&q=bar` to produce the following response:
```
{
  "q": [
    "foo",
    "bar"
  ]
}
```

### Number validation

Number validation is similar:
```
size: float = Query(..., gt=0, lt=10.5)
```

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

### Path Parameters

`Path` parameters can take all the same parameters as for `Query`:
```
    item_id: int = Path(..., title="The ID of the item to get"),
```

It is always required, even if this is not explicitly defined in the default value.

### Ordering Parameters As Needed

FastAPI doesn't care about order of parameters. Python will complain if you put a value with a "default" before a value that doesn't have a "default".
If you have a required parameter (with respect to incoming data), but want to put the path as the first argument, then some trickery is required.
```
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
```
This will fail, as `q` should be first. Unless...
```
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
```

## `06-dependencies.py`

## Overview

A dependency is just a function that can take all the same parameters that a path operation function can take:
```
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```

You can think of it as a path operation function without the "decorator" (without the `@app.get("/some-path")`).

Although you use `Depends` in the parameters of your function the same way you use `Body`, `Query`, etc., `Depends` only takes 1 parameter:
```
async def read_items(commons: dict = Depends(common_parameters)):
```

With regards to `async`, the same rules apply while defining your functions.

You can define dependencies that in turn can define dependencies themselves.

## Classes as Dependencies

This parameter must be a callable (a function or a class) that takes parameters in the same way that path operation functions do.
As mentioned before, `dict` can't handle type hinting, so:
```
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
```
where
```
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
```

Note: for FastAPI, this could be `commons = Depends(CommonQueryParams)` - the type hint is not what is used by FastAPI here. Declaring it helps the editor, and so should be included.

FastAPI helps with reducing duplicated code by providing a shortcut for when the dependency is specifically a class that FastAPI will "call" to create an instance of the class itself:
```
commons: CommonQueryParams = Depends()
```
## `07-subdependencies.py`

This file shows a simple example of how dependencies can scale.

```
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
```
depends on:
```
def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: str | None = Cookie(None)
)
```
which depends on:
```
def query_extractor(q: str | None = None):
    return q
```

### Dependency Caching

FastAPI caches responses from sub-dependency calls - they are called only once PER REQUEST.

To avoid using the cache, pass `use_cache=False` to `Depends`:
```
async def needy_dependency(
    fresh_value: str = Depends(
        get_value,
        use_cache=False
    )
):
    return {"fresh_value": fresh_value}
```

## `08-specifying-dependencies.py`

If return values are not needed, then they can be specified in the decorator:
```
@app.get("/items/", dependencies=[Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

If a dependency is required on all paths, it can be set globally:
```
app = FastAPI(dependencies=[Depends(verify_token)])
```

This is useful for situations such as data validation, where an exception is raised.

## `09-dependencies-with-yield.py`

It is also possible to perform tasks after sending a response.
To achieve this, `yield` is used instead of `return` (i.e. a generator). Code that is run **after** `yield` can be done effectively as a background task after the response has been delivered.
This can be useful for tasks such as closing a connection to a database - the data is already fetched:
```
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
```

Sub-dependencies can have a mix of `return` and `yield`.

Note, however, that errors can not be returned to the user after this point!

## `10-security.py`

FastAPI has many tools for simplifying the use of security. The security system is based on the dependency injection system.

For most cases, `OAuth2PasswordBearer` is appropriate, with `tokenUrl` set to a relative URL that should be used to get the token (path operation needs to exist):
```
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

The `oauth2_scheme` variable is an instance of `OAuth2PasswordBearer`, but it is also a "callable":
```
async def get_current_user(token: str = Depends(oauth2_scheme)):
```

This allows for getting the current user directly in the path operation functions and dealing with the security mechanisms at the Dependency Injection level, using `Depends`.

In OAuth2's "password flow", the user's username and password is needed from a form: `OAuth2PasswordRequestForm`:
```
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
```
This gives us `form_data.username` and `form_data.password` as part of the OpenAPI specification.

`HTTPException`s are used for HTTP 400 and 401 errors.

Token route needs to respond with JSON:
```
return {"access_token": user.username, "token_type": "bearer"}
```

## `11-security-jwt.py`

`passlib` is used for hashing and verifying passwords.

JWTs (JSON Web Tokens) are a way to offer some actual security to the login process, along with password hashing.
It condenses text into an `xxxxxx.yyyyyy.zzzzzz` string format. It is not encrypted, but it is signed.
JWT is a good fit for handling user authentication tokens with expiration (e.g. 1 week).

`python-jose` provides a convenient way to interact with JWTs.

`timedelta` is used to create and check unix timestamps for expiration.

A secure random secret key is needed for signing outgoing and authenticating incoming tokens.

`/token` path needs a Pydantic model:
```
@app.post("/token", response_model=Token)
```

Note: the JWT specification gives an optional key, `sub`, for the subject of the message. In this case, it is used for the token itself:
```
# set
access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
)

# get
username: str = payload.get("sub")
```

### JWT - more broadly

JWTs can be used to provide users (and bots) with permissions relating to an identified entity OTHER THAN identifying a user and allowing them to perform operations directly on an API.

Actions can be performed without even needing an account - just with the JWT token your API generated for that.

Using these ideas, JWT can be used for way more sophisticated scenarios.

To avoid ID collisions, consider implementing a prefix system that ensures that different entities with the same name are not misidentified.

## `12-bg-tasks.py`

Import and use `BackgroundTasks` with parameters in path operation functions and dependencies to add background tasks:
```
def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q
```

FastAPI will create the object of type BackgroundTasks for you and pass it as that parameter wherever it is needed.

This is not recommended for heavy background computation, especially when state does not need to be shared. Use [Celery](https://docs.celeryproject.org/en/stable/) instead.

Useful for small tasks like sending an email.

## `example_proj/`

Copied from [n-guitar/fastapi-sample](https://github.com/n-guitar/fastapi-sample/tree/main/src/tutorial/bigger-applications) for speed.

Users and items are simplified greatly.
`routers` contains the routers for each class of the API with `APIRouter`, which acts as a "mini `FastAPI`" class.
`internal` contains `admin.py`, which is provided as a mock of an externally located `APIRouter` with some admin path operations that the organization shares between several projects. In `main.py`, the router is configured for the needs of this application specifically when imported:
```
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
```
`dependencies.py` contains functions for tokens required by different parts of the application - `get_query_token` (all paths) and `get_token_header` (`/admin` path):
```
app = FastAPI(dependencies=[Depends(get_query_token)])
...
dependencies=[Depends(get_token_header)],
```
Because a query token (`"jessica"`) is always required, viewing http://127.0.0.1:8000/ directly will produce an error explaining that the query token is missing:
```
{
    "detail": [
        {
            "loc": [
                "query",
                "token"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

and an error in the logs:
```
INFO:     127.0.0.1:53646 - "GET / HTTP/1.1" 422 Unprocessable Entity
```

Obviously, the `/` route in http://127.0.0.1:8000/docs shows that a token is required for this path.
