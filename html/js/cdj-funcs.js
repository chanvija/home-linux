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
function clear_tag_text() {
    document.getElementById('new_tag').value = '';
}
function change_image(source) {
    if (source == "datepicker") {
        date_select = document.getElementById('specific_date').value
        if (document.getElementById('ignore_year').checked) {
            checked = 'true'
        } else {
            checked = 'false'
        }
        changeImg('date', date_select, '3', '0', checked)
    } else if (source == "specific_tag") {
        tag_select = document.getElementById('specific_tag').value
        changeImg('default', tag_select, '3', '0', 'false')
    }
}
function test_show_picture(img,tags)
{
    $("<img/>").attr("src", img).on("load",function(){
        s = {w:this.width, h:this.height};   
        f = 800/s.h
        width = s.w * f
        height = s.h * f    
        $("#right1").html($("<img>").attr("src", img).width(width).height(height));
    }); 
    // $("#right").load("2.html")  
    $("#bottom").text(decodeURIComponent(tags));
}

function get_scaler(x,y) {
    cell_width = '1200'
    cell_height = '820'

    f1 = parseInt(cell_width)/x
    f2 = parseInt(cell_height)/y

    if (f1 <= f2) {
        start = f1.toFixed(2)
    }

    _width = x * start
    _height = y * start

    m = start
    for (let f = start;(_width <= cell_width) && (_height <= cell_height); ) {
        _width = x * f
        _height = y * f
        m = f
        f = parseFloat(parseFloat(f).toFixed(2)) + parseFloat('0.01')
    }
  
    return(m)
}

function rotate_image()
{
    x = String(parent.right_frame.document.getElementById('rotate_value').value)

    parent.left_frame.document.getElementById("show_image").style.transform = `rotate(${x}deg)`;

    x = parseInt(x) + parseInt(90)
    parent.right_frame.document.getElementById("rotate_value").value = x;
}

function update_tag_delete(query_type, tag, count, offset)
{
       update_tag('true')
       changeImg(query_type, tag, count, offset, 'false')
}

function update_tag_next(query_type, tag, count, offset)
{
	update_tag('false')
	changeImg(query_type, tag, count, offset, 'false')
}

function update_tag(delete_tag)
{
    var url = "http://192.168.1.13:8081/update_file";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    filter = parent.right_frame.document.getElementById('filter').value
    if (delete_tag == 'false') {
        new_tag = parent.right_frame.document.getElementById('new_tag').value
    } else {
        new_tag = 'delete'
    }
    filter_type = parent.right_frame.document.getElementById('filter_type').value;

    if (parent.right_frame.document.getElementById('replace_tag').checked) {
        replace_tag = 'true'
    } else {
        replace_tag = 'false'
    }

    xhr.setRequestHeader('Access-Control-Allow-Headers', '*');
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        filter: filter,
        new_tag: new_tag,
        replace_tag: replace_tag,
        filter_type: filter_type
    }));
    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        // console.log(data);
        // parent.right_frame.document.getElementById('new_tag').value = ""
        if (data['error'] == null) {
            parent.right_frame.document.getElementById('message').value = "Tag updated successfully"
            parent.right_frame.document.getElementById('user_tags').value = data['updated_tag']
        } else {
            parent.right_frame.document.getElementById('message').value = "Tag update FAILED " + data['error']
        }
    };

}

function changeImg(query_type, tag, count, offset, ignore_year)
{
    
    var u = "http://192.168.1.13:8081/get_archive_directory";
    var x = new XMLHttpRequest();
    x.open("POST", u, false)
    x.setRequestHeader('Access-Control-Allow-Headers', '*');
    x.setRequestHeader("Accept", "application/json");
    x.setRequestHeader("Content-Type", "application/json");
    x.send()
    
    d = JSON.parse(x.responseText);
    console.log(d)
    var path_prefix = d['dir_prefix']

    var url = "http://192.168.1.13:8081/get_row";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    xhr.setRequestHeader('Access-Control-Allow-Headers', '*');
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    if (parent.left_frame.document.getElementById('show_deleted').checked) {
        show_deleted = 'true'
    } else {
        show_deleted = 'false'
    }
    if (query_type == "date") {
        mmyy = document.getElementById('specific_date').value
        day = mmyy.split("-")[2]
        month = mmyy.split("-")[1]
        year = mmyy.split("-")[0]
        xhr.send(JSON.stringify({
            offset: offset,
            count: count,
            tag: tag,
            show_deleted: show_deleted,
            query_type: query_type,
            day: day,
            month: month,
            year: year,
            ignore_year: ignore_year
        }));
    } else {
        xhr.send(JSON.stringify({
            offset: offset,
            count: count,
            tag: tag,
            show_deleted: show_deleted,
            query_type: query_type
        }));
    }
    xhr.onload = function() {
        var data = JSON.parse(this.responseText);
        console.log(data);
        
        prev = "#";
        next = "#";

        if (data['row_count'] > 0) {
            img = path_prefix + data['file_list'][0][0];
            $("<img/>").attr("src", img).on("load",function(){     
                s = {w:this.width, h:this.height};   

                cell_width = '1200'
                cell_height = '820'

                f1 = parseInt(cell_width)/s.w
                f2 = parseInt(cell_height)/s.h

                if (f1 <= f2) {
                    start = f1.toFixed(2)
                } else {
                    start = f2.toFixed(2)
                }

                _width = s.w * start
                _height = s.h * start

                m = start
                for (let f = start;(_width <= cell_width) && (_height <= cell_height); ) {
                    _width = s.w * f
                    _height = s.h * f
                    m = f
                    f = parseFloat(parseFloat(f).toFixed(2)) + parseFloat('0.01')
                }

                _width = s.w * m
                _height = s.h * m    
                //alert(s.w + " " + s.h + " " + m)
                $("#show_image").html($("<img>").attr("src", img).width(_width).height(_height));

                new_prev_offset = Number(offset) - Number("1");
                if (new_prev_offset < 0) {
                    new_prev_offset = data['row_count'] - 1;
                }
                new_next_offset = Number(offset) + Number("1");
                current_pic_num = new_next_offset
                if (new_next_offset == data['row_count']) {
                    new_next_offset = Number("0");
                }

                $("#prev_button").attr("onclick", 'changeImg("' + query_type + '", "' + tag + '", ' + count + ', ' + new_prev_offset + ', ' + ignore_year + ")")
                $("#next_button").attr("onclick", 'changeImg("' + query_type + '", "' + tag + '", ' + count + ', ' + new_next_offset + ', ' + ignore_year + ")")

                parent.right_frame.document.getElementById('filter').value = data['file_list'][0][0]
                parent.right_frame.document.getElementById('system_tags').value = data['file_list'][0][1]
                parent.right_frame.document.getElementById('user_tags').value = data['file_list'][0][2]
                // parent.right_frame.document.getElementById('new_tag').value = ""
                parent.right_frame.document.getElementById('pic_count').value =  current_pic_num + " of " + data['row_count'] 
                parent.right_frame.document.getElementById('message').value = ""
                parent.right_frame.document.getElementById('rotate_value').value = "90"
                parent.right_frame.document.getElementById('button_update_tag_next').onclick = function (){update_tag_next(query_type, tag, count, new_next_offset);};
                if ((Number(offset) + Number("1")) == data['row_count']) {
                    delete_offset = Number("0")
                } else {
                    if (show_deleted == 'false') {
                        delete_offset = offset
                    } else {
                        delete_offset = new_next_offset
                    }
                }
                parent.right_frame.document.getElementById('button_update_tag_delete').onclick = function (){update_tag_delete(query_type, 'delete', count, delete_offset);};

            });
        } else {
            parent.left_frame.document.getElementById('show_image').innerHTML = '<object type="text/html" data="no-images.html" ></object>';
            $("#next").attr("onclick", 'null')
        }
    };
}
