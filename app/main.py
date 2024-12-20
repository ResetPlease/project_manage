from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from models import *
import asyncpg
import asyncio
import config
from functools import wraps
from typing import Callable
import common
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

async def get_db():
    conn = await asyncpg.connect(config.DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
    
def require_role(role: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(request: Request, db=Depends(get_db)):
            token = request.cookies.get("token")
            if not token:
                raise HTTPException(status_code=401, detail=["Unauthorized", "/login"])
            query = """
                SELECT u.role FROM Users as u LEFT JOIN LoginUserInfo as l ON l.user_id = u.id
                WHERE l.token = $1;
            """
            user_role = await db.fetchval(query, token)
            request.state.user_role = user_role
            if not common.role_validate(role, user_role):
                raise HTTPException(status_code=403, detail=["Insufficient permissions", "/login"])
            return await func(request, db)
        return wrapper
    return decorator


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if isinstance(exc.detail, list) and len(exc.detail) == 2:
        return templates.TemplateResponse("error.html", {"request": request, "error_code": exc.status_code, "error_message": exc.detail})
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error_code": exc.status_code, "error_message": exc.detail}
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error_code": 422, "error_message": exc.errors()}
    )

@app.get("/", response_class=HTMLResponse)
@require_role('user')
async def read_root(request: Request, db=Depends(get_db)):
    user_role = request.state.user_role
    print(user_role)
    if user_role == "admin":
        return templates.TemplateResponse("main.html", {"request": request})
    elif user_role == "user":
        return templates.TemplateResponse("employee.html", {"request": request})
    else:
        raise HTTPException(status_code=403, detail=["Insufficient permissions", "/login"])

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, login_data : LoginRequest, db=Depends(get_db)):
    query = """
        SELECT id FROM Users
        WHERE username = $1 and password_hash = $2;
    """
    id = None
    id = await db.fetchval(query, login_data.username, common.hash_password(login_data.password))
    token = common.generate_token(id)
    query = """
        INSERT INTO LoginUserInfo(token, user_id) VALUES($1, $2) RETURNING user_id;
    """
    result = await db.fetchval(query, token, id)
    if id != None and result != None:
        return {"status" : "ok", "data" : token}
    else:
        return {"status" : 'error', "data" : 'Invalid username or password'}

@app.post("/employees/", response_model=Employee)
async def create_employee(employee: Employee, db=Depends(get_db)):
    query = """
    INSERT INTO Employees (first_name, last_name, email, phone, position, role)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id;
    """
    try:
        employee_id = await db.fetchval(query, employee.first_name, employee.last_name, employee.email, 
                                        employee.phone, employee.position, employee.role)
        employee.id = employee_id
        return employee
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees/", response_model=List[Employee])
async def list_employees(db=Depends(get_db)):
    query = "SELECT * FROM Employees;"
    rows = await db.fetch(query)
    return [Employee(**row) for row in rows]

@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, db=Depends(get_db)):
    query = "SELECT * FROM Employees WHERE id = $1;"
    row = await db.fetchrow(query, employee_id)
    if row:
        return Employee(**row)
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: Employee, db=Depends(get_db)):
    query = """
    UPDATE Employees
    SET first_name = $1, last_name = $2, email = $3, phone = $4, position = $5, role = $6
    WHERE id = $7
    RETURNING *;
    """
    row = await db.fetchrow(query, employee.first_name, employee.last_name, employee.email,
                            employee.phone, employee.position, employee.role, employee_id)
    if row:
        return Employee(**row)
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int, db=Depends(get_db)):
    query = "DELETE FROM Employees WHERE id = $1;"
    result = await db.execute(query, employee_id)
    if result == "DELETE 1":
        return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/projects/", response_model=Project)
async def create_project(project: Project, db=Depends(get_db)):
    query = """
    INSERT INTO Projects (name, description, start_date, end_date)
    VALUES ($1, $2, $3, $4)
    RETURNING id;
    """
    try:
        project_id = await db.fetchval(query, project.name, project.description, 
                                       project.start_date, project.end_date)
        project.id = project_id
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/projects/", response_model=List[Project])
async def list_projects(db=Depends(get_db)):
    query = "SELECT * FROM Projects;"
    rows = await db.fetch(query)
    try:
        return [Project(**row) for row in rows]
    except:
        raise HTTPException(status_code=400, detail='Wrong projects attr')

@app.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: int, db=Depends(get_db)):
    query = "SELECT * FROM Projects WHERE id = $1;"
    row = await db.fetchrow(query, project_id)
    if row:
        return Project(**row)
    raise HTTPException(status_code=404, detail="Project not found")

@app.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: int, project: Project, db=Depends(get_db)):
    query = """
    UPDATE Projects
    SET name = $1, description = $2, start_date = $3, end_date = $4
    WHERE id = $5
    RETURNING *;
    """
    row = await db.fetchrow(query, project.name, project.description, 
                            project.start_date, project.end_date, project_id)
    if row:
        return Project(**row)
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/projects/{project_id}")
async def delete_project(project_id: int, db=Depends(get_db)):
    query = "DELETE FROM Projects WHERE id = $1;"
    result = await db.execute(query, project_id)
    if result == "DELETE 1":
        return {"message": "Project deleted successfully"}
    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/assignments/", response_model=Assignment)
async def create_assignment(assignment: Assignment, db=Depends(get_db)):
    query = """
    INSERT INTO Assignments (employee_id, project_id, start_date, end_date)
    VALUES ($1, $2, $3, $4)
    RETURNING id;
    """
    try:
        assignment_id = await db.fetchval(query, assignment.employee_id, assignment.project_id, 
                                          assignment.start_date, assignment.end_date)
        assignment.id = assignment_id
        return assignment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/assignments/", response_model=List[Assignment])
async def list_assignments(db=Depends(get_db)):
    query = "SELECT * FROM Assignments;"
    rows = await db.fetch(query)
    return [Assignment(**row) for row in rows]

@app.delete("/assignments/{assignment_id}")
async def delete_assignment(assignment_id: int, db=Depends(get_db)):
    query = "DELETE FROM Assignments WHERE id = $1;"
    result = await db.execute(query, assignment_id)
    if result == "DELETE 1":
        return {"message": "Assignment deleted successfully"}
    raise HTTPException(status_code=404, detail="Assignment not found")


@app.post("/salaries/", response_model=Salary)
async def create_salary(salary: Salary, db=Depends(get_db)):
    query = """
    INSERT INTO Salaries (employee_id, amount, effective_date)
    VALUES ($1, $2, $3)
    RETURNING id;
    """
    try:
        salary_id = await db.fetchval(query, salary.employee_id, salary.amount, salary.effective_date)
        salary.id = salary_id
        return salary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/salaries/", response_model=List[Salary])
async def list_salaries(db=Depends(get_db)):
    query = "SELECT * FROM Salaries;"
    rows = await db.fetch(query)
    return [Salary(**row) for row in rows]

@app.delete("/salaries/{salary_id}")
async def delete_salary(salary_id: int, db=Depends(get_db)):
    query = "DELETE FROM Salaries WHERE id = $1;"
    result = await db.execute(query, salary_id)
    if result == "DELETE 1":
        return {"message": "Salary deleted successfully"}
    raise HTTPException(status_code=404, detail="Salary not found")


@app.post("/users/", response_model=User)
async def create_user(user: User, db=Depends(get_db)):
    query = """
    INSERT INTO Users (username, password_hash, role, employee_id)
    VALUES ($1, $2, $3, $4)
    RETURNING id;
    """
    try:
        hash_password = common.hash_password(user.password)
        role_map = {
            "employee" : "user",
            "admin" : "admin"
        }
        user_id = await db.fetchval(query, user.username, hash_password, role_map[user.role], user.employee_id)
        user.id = user_id
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/", response_model=List[User])
async def list_users(db=Depends(get_db)):
    query = "SELECT * FROM Users;"
    rows = await db.fetch(query)
    return [User(**row) for row in rows]


@app.get("/logs/", response_model=List[AuditLog])
@require_role("admin")
async def list_logs(request : Request, db=Depends(get_db)):
    query = "SELECT * FROM AuditLogs ORDER BY timestamp DESC;"
    rows = await db.fetch(query)
    return [AuditLog(**row) for row in rows]


@app.get("/employees-with-salaries/")
async def employees_with_salaries(db=Depends(get_db)):
    query = """
    SELECT e.id, e.first_name, e.last_name, s.amount, s.effective_date
    FROM Employees e
    LEFT JOIN Salaries s ON e.id = s.employee_id
    ORDER BY e.id;
    """
    rows = await db.fetch(query)
    return rows

@app.get("/department-employees/{department_id}")
async def department_employees(department_id: int, db=Depends(get_db)):
    query = """
    SELECT e.id, e.first_name, e.last_name, d.name AS department_name
    FROM Employees e
    JOIN Departments d ON e.id = d.manager_id
    WHERE d.id = $1;
    """
    rows = await db.fetch(query, department_id)
    return rows

@app.get("/employee-info/", response_model=dict)
@require_role("user")
async def employee_info(request: Request, db=Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    
    query = """
    SELECT e.id, e.first_name, e.last_name, e.position, e.role, 
           p.name AS project_name, s.amount AS salary, e.email, e.phone
    FROM Employees e
    LEFT JOIN Assignments a ON e.id = a.employee_id
    LEFT JOIN Projects p ON a.project_id = p.id
    LEFT JOIN Salaries s ON e.id = s.employee_id
    WHERE e.id = (
        SELECT u.employee_id FROM Users u
        JOIN LoginUserInfo l ON u.id = l.user_id
        WHERE l.token = $1
    );
    """
    
    employee_data = await db.fetch(query, token)
    if not employee_data:
        raise HTTPException(status_code=404, detail="Employee not found")

    
    response_data = {
        "name": f"{employee_data[0]['first_name']} {employee_data[0]['last_name']}",
        "role": employee_data[0]["role"],
        "salary": employee_data[0]["salary"],
        "email": employee_data[0]["email"],
        "phone": employee_data[0]["phone"],
        "projects": [project["project_name"] for project in employee_data]
    }

    return response_data

