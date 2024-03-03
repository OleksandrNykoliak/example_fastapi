from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int
    email: str


class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentDelete(StudentBase):
    pass


class StudentDisplay(StudentBase):
    id: str

    class Config:
        orm_mode = True
