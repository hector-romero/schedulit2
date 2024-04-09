import http from "@/services/api";


export async function getShifts(user_id) {
    return http.get(`users/${user_id}/shifts/`).then((shifts) => {
        console.log(shifts);
        return shifts;
    })
}
