import http from "@/services/api";


export async function getShifts(user_id) {
    return http.get(`shifts/${user_id}/`, {params: {user: user_id}}).then((shifts) => {
        console.log(shifts);
        return shifts;
    })
}
