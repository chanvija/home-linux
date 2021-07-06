function show_picture(img)
{
    $("<img/>").attr("src", img).on("load",function(){
        s = {w:this.width, h:this.height};   
        f = 300/s.w
        _width = s.w * f
        _height = s.h * f    
        $("#right").html($("<img>").attr("src", img).width(_width).height(_height));
        
    }); 
    // $("#right").load("2.html")   
}
function test_show_picture(img,tags)
{
    $("<img/>").attr("src", img).on("load",function(){
        s = {w:this.width, h:this.height};   
        f = 800/s.h
        width = s.w * f
        height = s.h * f    
        $("#right1").html($("<img>").attr("src", img).width(width).height(height));
        // alert(width + " " + height)
    }); 
    // $("#right").load("2.html")  
    $("#bottom").text(decodeURIComponent(tags));
}