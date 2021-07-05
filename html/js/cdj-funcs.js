function show_picture(img)
{
    $("<img/>").attr("src", img).on("load",function(){
        s = {w:this.width, h:this.height};   
        f = 1000/s.w
        width = s.w * f
        height = s.h * f    
        $("#right").html($("<img>").attr("src", img).width(width).height(height));
    }); 
    // $("#right").load("2.html")   
}