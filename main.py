from fastapi import FastAPI

from db import engine
import models
import students
import scores

api = FastAPI()

models.Base.metadata.create_all(bind=engine)

api.include_router(students.router)
api.include_router(scores.router)
