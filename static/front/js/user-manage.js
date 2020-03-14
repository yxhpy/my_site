function $active($this){
    $this.siblings().removeClass('list-group-item-text');
    $this.addClass('list-group-item-text')
}
$("#set-header,#set-info,#set-pass,#set-article").click(function () {
    $this = $(this);
    $active($this);
    $("#panel-title").html($this.html());
    $('#panel-body-set-header').siblings('.panel-body').addClass('hidden');
    switch ($this.attr('id')) {
        case "set-header":
            $('#panel-body-set-header').siblings('.panel-body').addClass('hidden');
            $('#panel-body-set-header').removeClass('hidden');
            break;
        case "set-info":
            $('#panel-body-set-info').siblings('.panel-body').addClass('hidden');
            $('#panel-body-set-info').removeClass('hidden');
            break;
        case "set-pass":
            $('#panel-body-set-pass').siblings('.panel-body').addClass('hidden');
            $('#panel-body-set-pass').removeClass('hidden');
            break;
        case "set-article":
            $('#panel-body-set-article').siblings('.panel-body').addClass('hidden');
            $('#panel-body-set-article').removeClass('hidden');
            break;
    }
});
function choose_file() {
    $('#head_img').click();
}