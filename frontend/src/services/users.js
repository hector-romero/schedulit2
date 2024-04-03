import http from "@/services/api";


export async function getUsers() {
    return http.get('users/').then((users) => {
        console.log(users);
        return users;
    })
}


export async function addUser(email, password, name, role, employee_id) {
    return http.post('users/', {email, password, name, role, employee_id}).then((response) => {
        console.log(response);
        return response;
    });
}

export async function getUser(user_id) {
    return http.get(`users/${user_id}/`).then((user) => {
        console.log(user);
        return user;
    })

}
