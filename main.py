# from fastapi import FastAPI

# app= FastAPI()

# @app.get("/")
# def home():
#     return{"message": "Server is live"}

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import OperationalError
from database import engine, get_session
from models import Student

app = FastAPI()

@app.on_event("startup")
def on_startup():
 try:
     SQLModel.metadata.create_all(engine)
     print("Database Connected Successfully!")
 except OperationalError as e:
     print("Database Connection Failed:", e)
      
      
@app.get("/")
def home():
    return{"message": "Server is live"}


#Create Student in database
@app.post("/student")
def add_student(student: Student, session: Session= Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

#Read all or Get all student data
@app.get("/students")
def get_all_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

#Read one, Get on student details

@app.get("/student/{student_id}")
def get_student(student_id: int, session: Session= Depends(get_session)):
    student= session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code =404, detail= "Student not found")
    return student

#Update Student details
@app.put("/student/{student_id}")
def update_student(
    student_id: int, updated: Student,
    session: Session = Depends(get_session)):
    
    student= session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code= 404, detail= "Student is not found")
    student.name= updated.name
    student.course= updated.course
    # student.name =updated.email
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

#delete Student Details
@app.delete("/student/{student_id}")
def delete_student(
    student_id: int, session: Session= Depends(get_session)
):
    student= session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code= 404, detail= "Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted"}
