
// @class mApp Metronic App class 


var mApp = function() {
var initFileInput = function() {
    // init bootstrap popover
    $('.custom-file-input').on('change',function(){
        var fileName = $(this).val();
        $(this).next('.custom-file-label').addClass("selected").html(fileName);
    });
}           

}