from pydantic import BaseModel
from typing import List, Optional
import datetime


class Salary(BaseModel):
    id: Optional[int] = None
    employee_id: int
    amount: float
    effective_date: datetime.date


class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: Optional[str] = None
    role: str
    employee_id: Optional[int] = None


class AuditLog(BaseModel):
    id: Optional[int]
    action: str
    timestamp: datetime.datetime


class Employee(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = ""
    position: Optional[str] = ""
    hire_date: Optional[datetime.date] = ""
    role: str = 'user'

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]
    start_date: datetime.date
    end_date: datetime.date

class Assignment(BaseModel):
    id: Optional[int] = None
    employee_id: int
    project_id: int
    start_date: datetime.date
    end_date: datetime.date

class Department(BaseModel):
    id: Optional[int]
    name: str
    manager_id: Optional[int]


class LoginRequest(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    status: str
    data: str

class LoginInfo(BaseModel):
    id: Optional[int]
    role: str
