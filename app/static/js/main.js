async function fetchEmployees() {
    const response = await axios.get('/employees/');
    const employees = response.data;
    const tableBody = document.getElementById('employees-table-body');
    tableBody.innerHTML = '';
    console.log(employees)
    employees.forEach(employee => {
        const row = `<tr>
            <td>${employee.id}</td>
            <td>${employee.first_name}</td>
            <td>${employee.last_name}</td>
            <td>${employee.email}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editEmployee(${employee.id}, '${employee.first_name}', '${employee.last_name}', '${employee.email}')">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteEmployee(${employee.id})">Delete</button>
            </td>
        </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

async function saveEmployee() {
    const id = document.getElementById('employee-id').value;
    const firstName = document.getElementById('employee-first-name').value;
    const lastName = document.getElementById('employee-last-name').value;
    const email = document.getElementById('employee-email').value;

    if (id) {
        await axios.put(`/employees/${id}`, { first_name: firstName, last_name: lastName, email });
    } else {
        const response = await axios.post('/employees/', { first_name: firstName, last_name: lastName, email : email });
        console.log(response.data);
    }

    fetchEmployees();
    bootstrap.Modal.getInstance(document.getElementById('employeeModal')).hide();
}

function editEmployee(id, firstName, lastName, email) {
    document.getElementById('employee-id').value = id;
    document.getElementById('employee-first-name').value = firstName;
    document.getElementById('employee-last-name').value = lastName;
    document.getElementById('employee-email').value = email;
    new bootstrap.Modal(document.getElementById('employeeModal')).show();
}

async function deleteEmployee(id) {
    await axios.delete(`/employees/${id}`);
    fetchEmployees();
}

async function fetchProjects() {
    const response = await axios.get('/projects/');
    const projects = response.data;
    const tableBody = document.getElementById('projects-table-body');
    tableBody.innerHTML = '';
    console.log(projects)
    projects.forEach(project => {
        const row = `<tr>
            <td>${project.id}</td>
            <td>${project.name}</td>
            <td>${project.description}</td>
            <td>${project.start_date}</td>
            <td>${project.end_date}</td>
            <td>
                <button class="btn btn-warning btn-sm" onclick="editProject(${project.id}, '${project.name}', '${project.description}')">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteProject(${project.id})">Delete</button>
            </td>
        </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

async function saveProject() {
    const id = document.getElementById('project-id').value;
    const name = document.getElementById('project-name').value;
    const description = document.getElementById('project-description').value;
    const start_date = document.getElementById('start_date').value;
    const end_date = document.getElementById('end_date').value;
    console.log("Project: ", id, name, description);
    if (id) {
        await axios.put(`/projects/${id}`, { name: name, description: description, start_date : start_date, end_date : end_date });
    } else {
        const response = await axios.post('/projects/', { name: name, description: description, start_date : start_date, end_date : end_date });
        console.log(response.data);
    }

    fetchProjects();
    bootstrap.Modal.getInstance(document.getElementById('projectModal')).hide();
}

function editProject(id, name, description) {
    document.getElementById('project-id').value = id;
    document.getElementById('project-name').value = name;
    document.getElementById('project-description').value = description;
    new bootstrap.Modal(document.getElementById('projectModal')).show();
}

async function deleteProject(id) {
    await axios.delete(`/projects/${id}`);
    fetchProjects();
}

function openCreateEmployeeModal() {
    document.getElementById('employee-form').reset();
    document.getElementById('employee-id').value = '';
    new bootstrap.Modal(document.getElementById('employeeModal')).show();
}

function openCreateProjectModal() {
    document.getElementById('project-form').reset();
    document.getElementById('project-id').value = '';
    new bootstrap.Modal(document.getElementById('projectModal')).show();
}

// Assignments
async function fetchAssignments() {
    const response = await axios.get('/assignments/');
    const assignments = response.data;
    const tableBody = document.getElementById('assignments-table-body');
    tableBody.innerHTML = '';
    assignments.forEach(assignment => {
        const row = `<tr>
            <td>${assignment.id}</td>
            <td>${assignment.employee_id}</td>
            <td>${assignment.project_id}</td>
            <td>${assignment.start_date}</td>
            <td>${assignment.end_date || ''}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteAssignment(${assignment.id})">Delete</button>
            </td>
        </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

async function deleteAssignment(id) {
    await axios.delete(`/assignments/${id}`);
    fetchAssignments();
}

function openCreateAssignmentModal() {
    document.getElementById('assignment-form').reset();
    new bootstrap.Modal(document.getElementById('assignmentModal')).show();
}

async function saveAssignment() {
    const employeeId = document.getElementById('assignment-employee-id').value;
    const projectId = document.getElementById('assignment-project-id').value;
    const startDate = document.getElementById('assignment-start-date').value;
    const endDate = document.getElementById('assignment-end-date').value;

    await axios.post('/assignments/', {
        employee_id: employeeId,
        project_id: projectId,
        start_date: startDate,
        end_date: endDate || null,
    });

    fetchAssignments();
    bootstrap.Modal.getInstance(document.getElementById('assignmentModal')).hide();
}

// Salaries
async function fetchSalaries() {
    const response = await axios.get('/salaries/');
    const salaries = response.data;
    const tableBody = document.getElementById('salaries-table-body');
    tableBody.innerHTML = '';
    salaries.forEach(salary => {
        const row = `<tr>
            <td>${salary.id}</td>
            <td>${salary.employee_id}</td>
            <td>${salary.amount}</td>
            <td>${salary.effective_date}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteSalary(${salary.id})">Delete</button>
            </td>
        </tr>`;
        tableBody.insertAdjacentHTML('beforeend', row);
    });
}

async function deleteSalary(id) {
    await axios.delete(`/salaries/${id}`);
    fetchSalaries();
}

function openCreateSalaryModal() {
    document.getElementById('salary-form').reset();
    new bootstrap.Modal(document.getElementById('salaryModal')).show();
}

async function saveSalary() {
    const employeeId = document.getElementById('salary-employee-id').value;
    const amount = document.getElementById('salary-amount').value;
    const effectiveDate = document.getElementById('salary-effective-date').value;

    await axios.post('/salaries/', {
        employee_id: employeeId,
        amount: amount,
        effective_date: effectiveDate,
    });

    fetchSalaries();
    bootstrap.Modal.getInstance(document.getElementById('salaryModal')).hide();
}


// Fetch Users
async function fetchUsers() {
    try {
        const response = await axios.get('/users/');
        const users = response.data;
        const tableBody = document.getElementById('users-table-body');
        tableBody.innerHTML = '';
        users.forEach(user => {
            const row = `<tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.role}</td>
                <td>${user.employee_id || '-'}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="editUser(${user.id}, '${user.username}', '${user.role}', ${user.employee_id || null})">Edit</button>
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// Open Create User Modal
function openCreateUserModal() {
    document.getElementById('user-form').reset();
    document.getElementById('user-id').value = '';
    const userModal = new bootstrap.Modal(document.getElementById('userModal'));
    userModal.show();
}

// Edit User
function editUser(id, username, role, employee_id) {
    document.getElementById('user-id').value = id;
    document.getElementById('user-username').value = username;
    document.getElementById('user-role').value = role;
    document.getElementById('user-employee-id').value = employee_id || '';
    const userModal = new bootstrap.Modal(document.getElementById('userModal'));
    userModal.show();
}

// Save User
async function saveUser() {
    try {
        const id = document.getElementById('user-id').value;
        const username = document.getElementById('user-username').value;
        const password = document.getElementById('user-password').value;
        const role = document.getElementById('user-role').value;
        const employee_id = document.getElementById('user-employee-id').value || null;

        const user = { username, password, role, employee_id };

        if (id) {
            console.log('Editing user is not implemented yet');
        } else {
            await axios.post('/users/', user);
            alert('User created successfully');
        }

        const userModal = bootstrap.Modal.getInstance(document.getElementById('userModal'));
        userModal.hide();
        fetchUsers();
    } catch (error) {
        console.error('Error saving user:', error);
    }
}

function logout() {
    setCookie("token", "", 1);
    window.location.replace("/login");
}

function go_to_logs(){
    window.location.replace("/logs/");
}

window.onload = function() {
    fetchProjects();
    fetchEmployees();
    fetchAssignments();
    fetchSalaries();
    fetchUsers();
};
