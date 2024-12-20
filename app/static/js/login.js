const API_BASE_URL = 'http://localhost:8000';

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

async function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    console.log(username, password,  {username: username, password: password})
    const response = await axios.post(`${API_BASE_URL}/login`,  {username: username, password: password});
    console.log(response.data);
    if(response.data.status == "ok") {
        setCookie("token", response.data.data, 7)
        window.location.replace("/");
    } else {
        alert(response.data.data)
    }
}