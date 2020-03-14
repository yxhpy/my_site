//每0.5s检查是否存在过宽的图片，如果存在就让他宽度自适应宽度
setInterval(function () {
    $img = $('img');
    $width = $('#article-details').width();
    console.log($width);
    for (var i = 0; i < $img.length; i++) {
        console.log($img[i].width, $width);
        if ($img[i].width > $width) {
            $($img[i]).addClass('img-responsive');
        }
    }
}, 500);