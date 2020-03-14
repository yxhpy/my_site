setInterval(function (){
    $top = $(document).scrollTop();
    $("nav").css('opacity',(70 - $top) /70);
    $(".return-top").css('opacity', ($top-100)/100);
},10);
$(".return-top").click(function () {
    window.scrollTo(0, 0);
});
$('#login_button').click(function () {
    var form_values = {};
    var input_tags = $("#login_model input");
    for (var i = 0; i < input_tags.length; i++) {
        form_values[input_tags[i].name] = input_tags[i].value;
    }
    form_values['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/login/',
        type: 'POST',
        data: form_values,
        success: function (data) {
            window.location.href = '/'
        },
        error: function (data) {
            var $input_tag;
            var errors = data.responseJSON;
            console.log(data);
            for (var i = 0; i < input_tags.length; i++) {
                $input_tag = $(input_tags[i]);
                var tag_name = $input_tag.attr('name');
                if (errors[tag_name]) {
                    $input_tag.parent().addClass('has-error');
                    $(input_tags[i]).next().text(errors[tag_name]);
                    break;
                }
            }
        }
    })
});
$('#register_button').click(function () {
    $(this).addClass('disable');
    $(this).text('注册中...');
    var form_values = {};
    var input_tags = $("#register_model input");
    for (var i = 0; i < input_tags.length; i++) {
        form_values[input_tags[i].name] = input_tags[i].value;
        $(input_tags[i]).parent().removeClass('has-error');
        $(input_tags[i]).next().text('');
    }
    form_values['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/register/',
        type: 'POST',
        // headers: {
        //            'X-CSRFToken':csrf_token,
        //        },
        data: form_values,
        success: function (data) {
            $this = $('#register_button');
            $this.prev().click();
            $('a[href="#login_model"]').click();
            $('#username_label').val($("#r_username_label").val());
            $('#reset-register-form input').val('')
        },
        error: function (data) {
            var $input_tag;
            var errors = JSON.parse(data.responseText);
            for (var i = 0; i < input_tags.length; i++) {
                $input_tag = $(input_tags[i]);
                var tag_name = $input_tag.attr('name');
                if (errors[tag_name]) {
                    $input_tag.parent().addClass('has-error');
                    $(input_tags[i]).next().text(errors[tag_name]);
                    break;
                }
            }
        }
    });
    $(this).text('注册');
    $(this).removeClass('disable');
});
// setInterval(function () {
//     // $('#id_content').removeAttr('style');
//     // $('#edui1').css('width','auto');
// }, 500);
