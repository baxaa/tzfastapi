from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from db import SessionLocal

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class StudentCreate(BaseModel):
    firstname: str
    lastname: str


@router.get("/{student_id} ")
def get_students(student_id, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    model = models.Student(**student.dict())

    db.add(model)
    db.commit()

    return HTTPException(status_code=200, detail=f"model")


@router.patch("/{student_id}")
def update_student(student_id, student: StudentCreate, db: Session = Depends(get_db)):
    student_model = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student_model:
        raise HTTPException(status_code=404, detail=f"Student not found")

    student_model = models.Student(**student.dict())

    db.add(student_model)
    db.commit()

    return HTTPException(status_code=200, detail=f"student_model")


@router.delete("/{student_id} ")
def delete_student(student_id, db: Session = Depends(get_db)):
    student_model = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student_model:
        raise HTTPException(status_code=404, detail=f"Student not found")

    db.query(models.Student).filter(models.Student.id == student_id).delete()

    return HTTPException(status_code=200, detail="Succesfully deleted")