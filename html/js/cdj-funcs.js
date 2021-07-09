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

function changeImg(target_div_id, tag, count, offset)
{
    // var target_div = document.getElementById(target_div_id);
    // target_div.src = image;
    var url = "http://192.168.1.10:8081/get_row";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader('Access-Control-Allow-Headers', '*');
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        offset: offset,
        count: count,
        tag: tag
    }));
    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        console.log(data);
        path_prefix = "../../pictures-archive/";
        prev = "#";
        next = "#";

        img = path_prefix + data[0];

        // alert(data + " " + data.length)

        $("<img/>").attr("src", img).on("load",function(){     
            s = {w:this.width, h:this.height};   
            f = 820/s.h
            _width = s.w * f
            _height = s.h * f    
            $("#show_image").html($("<img>").attr("src", img).width(_width).height(_height));

            new_prev_offset = Number(offset) - Number("1");
            if (new_prev_offset < 0) {
                new_prev_offset = 0;
            }
            new_next_offset = Number(offset) + Number("1");

            $("#prev").attr("onclick", 'changeImg("' + target_div_id + '", "' + tag + '", ' + count + ', ' + new_prev_offset + ")")
            $("#next").attr("onclick", 'changeImg("' + target_div_id + '", "' + tag + '", ' + count + ', ' + new_next_offset + ")")
        });
    };
}