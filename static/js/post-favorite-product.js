const product_favorite_post = document.getElementsByClassName('product-favorite-post');

for (let i = 0; i < product_favorite_post.length; i++) {
    product_favorite_post[i].addEventListener('click', e => {
        e.preventDefault();
        const csrftoken = getCookie('csrftoken');
        const target_cls = product_favorite_post[i];
        
        target_product = target_cls.getElementsByClassName('favorite-product')[0].value;
        login_user = target_cls.getElementsByClassName('login-user')[0].value;

        if (target_cls.getElementsByClassName('product-is-favorite').length > 0) {
            api_url = target_cls.getElementsByClassName('api-url-delete')[0].value;;
        } else if (target_cls.getElementsByClassName('product-is-not-favorite').length > 0) {
            api_url = target_cls.getElementsByClassName('api-url-create')[0].value;
        }

        api_url = location.origin + api_url;

        axios.defaults.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken, 
        }
        const post_favorite_product = async () => {
            const res = await axios.post(api_url, {
                login_user: login_user,
                target: target_product,
            });
            return res;
        }
        post_favorite_product()
            .then(data => {
                console.log(data.data.message);
                if (!data.data.success) {
                    throw new Error('server process error')
                } 
            })
            .then(data => {
                if (target_cls.getElementsByClassName('product-is-favorite').length > 0) {
                    target_cls.getElementsByClassName('product-is-favorite')[0].remove('product-is-favorite');
                    
                    const div = document.createElement('div');
                    div.className = 'product-is-not-favorite';
                    div.textContent = 'お気に入り追加'
                    target_cls.insertBefore(div, target_cls.firstChild);
                } else if (target_cls.getElementsByClassName('product-is-not-favorite').length > 0) {
                    target_cls.getElementsByClassName('product-is-not-favorite')[0].remove('product-is-not-favorite');
                    
                    const div = document.createElement('div');
                    div.className = 'product-is-favorite';
                    div.textContent = 'お気に入り'
                    target_cls.insertBefore(div, target_cls.firstChild);                }
            })
            .catch(err => {
                console.log(err);
            })
    })
}