

from fastapi import FastAPI
from config.db import engine, Base
import models
from routes.student import student
from routes.book import book
# from routes.authentication import auth
from routes.autocompleteStudent import autoStudent
from routes.autocompleteBook import autoBook
from routes.connectionReq import connection
from routes.borrow import borrow
from routes.admin1 import admin

app = FastAPI()

# drop all tables associated with metadata
# Base.metadata.drop_all(engine)

# create all tables associated with metadata
Base.metadata.create_all(engine)

# app.include_router(auth)
app.include_router(student)
app.include_router(book)
app.include_router(autoStudent)
app.include_router(autoBook)
app.include_router(connection)
app.include_router(admin)
app.include_router(borrow)


