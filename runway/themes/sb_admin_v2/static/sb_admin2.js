$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        
        height = (this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height;
        height = height - topOffset;
        
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#content-wrapper").css("min-height", (height-1) + "px");
        }
    })
}); 