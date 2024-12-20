-- Таблица сотрудников
CREATE TABLE Employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    position VARCHAR(50),
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'editor', 'user'))
);

-- Таблица проектов
CREATE TABLE Projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE
);

-- Таблица назначений
CREATE TABLE Assignments (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES Employees(id) ON DELETE CASCADE,
    project_id INT NOT NULL REFERENCES Projects(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE
);

-- Таблица отделов
CREATE TABLE Departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manager_id INT UNIQUE REFERENCES Employees(id) ON DELETE SET NULL
);

-- Таблица зарплат
CREATE TABLE Salaries (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES Employees(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    effective_date DATE NOT NULL
);

-- Таблица пользователей системы
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'editor', 'user')),
    employee_id INT UNIQUE REFERENCES Employees(id) ON DELETE CASCADE
);

-- Таблица аудита действий
CREATE TABLE AuditLogs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE LoginUserInfo (
    token   TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES Users(id) ON DELETE SET NULL
)