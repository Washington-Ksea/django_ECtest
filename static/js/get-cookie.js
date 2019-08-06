//https://qiita.com/soup01/items/f356d6ee09534007f76d
getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        document.cookie.split(';').forEach(c => {
            let m = c.trim().match(/(\w+)=(.*)/);
            console.log(m);
            if(m !== undefined && m[1] == name) {
                value = decodeURIComponent(m[2]);
            }
        });
    }
}