const seller_favorite_post = document.getElementsByClassName('seller-favorite-post');

for (let i = 0; i < seller_favorite_post.length; i++) {
    seller_favorite_post[i].addEventListener('click', e => {
        e.preventDefault();
        const csrftoken = getCookie('csrftoken');
        const target_cls = seller_favorite_post[i];
        
        target_user = target_cls.getElementsByClassName('favorite-user')[0].value;
        login_user = target_cls.getElementsByClassName('login-user')[0].value;

        if (target_cls.getElementsByClassName('seller-is-favorite').length > 0) {
            api_url = target_cls.getElementsByClassName('api-url-delete')[0].value;;
        } else if (target_cls.getElementsByClassName('seller-is-not-favorite').length > 0) {
            api_url = target_cls.getElementsByClassName('api-url-create')[0].value;
        }

        api_url = location.origin + api_url;

        axios.defaults.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken, 
        }
        const post_favorite_user = async () => {
            const res = await axios.post(api_url, {
                login_user: login_user,
                target: target_user,
            });
            return res;
        }
        post_favorite_user()
            .then(data => {
                console.log(data.data.message);
                if (!data.data.success) {
                    throw new Error('server process error')
                } 
            })
            .then(data => {
                if (target_cls.getElementsByClassName('seller-is-favorite').length > 0) {
                    target_cls.getElementsByClassName('seller-is-favorite')[0].remove('seller-is-favorite');
                    
                    const div = document.createElement('div');
                    div.className = 'seller-is-not-favorite';
                    div.textContent = 'お気に入り追加'
                    target_cls.insertBefore(div, target_cls.firstChild);
                } else if (target_cls.getElementsByClassName('seller-is-not-favorite').length > 0) {
                    target_cls.getElementsByClassName('seller-is-not-favorite')[0].remove('seller-is-not-favorite');
                    
                    const div = document.createElement('div');
                    div.className = 'seller-is-favorite';
                    div.textContent = 'お気に入り'
                    target_cls.insertBefore(div, target_cls.firstChild);                }
            })
            .catch(err => {
                console.log(err);
            })
    })
}
