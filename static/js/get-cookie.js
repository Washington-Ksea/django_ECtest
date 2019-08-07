//https://qiita.com/soup01/items/f356d6ee09534007f76d
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        document.cookie.split(';').forEach(c => {
            let m = c.trim().match(/(\w+)=(.*)/);
            if(m !== undefined && m[1] == name) {
                cookieValue = decodeURIComponent(m[2]);
            }
        });
    }
    return cookieValue;
}
