#!/bin/bash

# python3 -m pip install fastapi uvicorn[standard] python-multipart python-jose[cryptography] passlib[bcrypt]

# `main`: the file main.py (the Python "module").
# `app`: the object created inside of main.py with the line `app = FastAPI()`.
# `--reload`: make the server restart after code changes. Only use for development.

uvicorn 1-hello_world:app --reload
