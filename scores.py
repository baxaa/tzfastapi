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


class ScoreCreate(BaseModel):
    subject_name: str
    score: int


@router.get("/{score_id} ")
def get_students(score_id, db: Session = Depends(get_db)):
    return db.query(models.Student).filter(models.Scores.id == score_id).first()


@router.post("/{student_id}")
def create_student(student_id, score: ScoreCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Students.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student not found")

    model = models.Scores(**score.dict())
    model.student_id = student_id

    db.add(model)
    db.commit()

    return HTTPException(status_code=200, detail=f"model")


@router.patch("/{score_id}")
def update_student(score_id, score: ScoreCreate, db: Session = Depends(get_db)):
    model = db.query(models.Scores).filter(models.Student.id == score_id).first()

    if not model:
        raise HTTPException(status_code=404, detail=f"Student not found")

    model = models.Student(**score.dict())

    db.add(model)
    db.commit()

    return HTTPException(status_code=200, detail=f"model")


@router.delete("/{score_id} ")
def delete_student(score_id, db: Session = Depends(get_db)):
    student_model = db.query(models.Scores).filter(models.Scores.id == score_id).first()

    if not student_model:
        raise HTTPException(status_code=404, detail=f"Student not found")

    db.query(models.Scores).filter(models.Scores.id == score_id).delete()

    return HTTPException(status_code=200, detail="Succesfully deleted")