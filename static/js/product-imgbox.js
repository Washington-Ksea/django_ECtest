const subimage = document.getElementsByClassName('product-sub-img-button');

for (let i = 0; i < subimage.length; i++) {
    subimage[i].addEventListener('click', e => {
        e.preventDefault();
        target_img = subimage[i].getElementsByClassName('product-sub-img')[0].src;
        
        detail_image = document.getElementById('product-detail-img').src;
        
        document.getElementById('product-detail-img').src = target_img;
        subimage[i].getElementsByClassName('product-sub-img')[0].src = detail_image;
    })
}

