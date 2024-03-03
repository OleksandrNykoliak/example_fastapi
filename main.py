from fastapi import FastAPI, HTTPException, Form
from models import Student
from schemas import StudentCreate, StudentDisplay, StudentUpdate, StudentDelete
from mongoengine.errors import NotUniqueError
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/form", response_class=FileResponse)
async def read_root():
    return FileResponse("templates/index.html")


@app.post("/students/", response_model=StudentDisplay)
async def create_student(name: str = Form(...), age: int = Form(...), email: str = Form(...)):
    try:
        student_obj = Student(
            name=name, age=age, email=email).save()
        # return {"id": str(student_obj.id), "name": student_obj.name, "age": student_obj.age, "email": student_obj.email}
        return RedirectResponse(url='/all_students', status_code=303)

    except NotUniqueError:
        raise HTTPException(
            status_code=400, detail='Студент з таким email вже існує')


@app.get("/all_students/", response_model=list[StudentDisplay], response_class=FileResponse)
async def get_all_students():
    students = Student.objects()
    # return [StudentDisplay(id=str(student.id), age=student.age, name=student.name, email=student.email) for student in students]
    return FileResponse("templates/students.html")


@app.put("/students/{student_id}/", response_model=StudentDisplay)
async def update_student(student_id: str, student: StudentUpdate):
    student_obj = Student.objects(id=student_id).first()
    if not student_obj:
        raise HTTPException(status_code=404, detail='Студент не знайдений')
    student_obj.update(name=student.name, age=student.age, email=student.email)
    return StudentDisplay(id=str(student_obj.id), age=student.age, name=student.name, email=student.email)


@app.patch("/students/{student_id}/", response_model=StudentDisplay)
async def patch_student(student_id: str, student: StudentUpdate):
    student_obj = Student.objects(id=student_id).first()
    if not student_obj:
        raise HTTPException(status_code=404, detail='Студент не знайдений')
    student_obj.update(**student.dict(exclude_unset=True))
    return StudentDisplay(id=str(student_obj.id), age=student.age, name=student.name, email=student.email)


@app.delete("/students/{student_id}/", response_model=StudentDelete)
async def delete_student(student_id: str):
    student_obj = Student.objects(id=student_id).first()
    if not student_obj:
        raise HTTPException(status_code=404, detail='Студент не знайдений')
    student_obj.delete()
    return StudentDelete(name=student_obj.name, age=student_obj.age, email=student_obj.email)
