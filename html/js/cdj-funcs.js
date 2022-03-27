function append_tag(cb) {
    v = parent.right_frame.document.getElementById("new_tag").value;
    if (cb.checked) {
        if (!v.includes(cb.value)) {
            n = v + ',' + cb.value
        }
    } else {
        var re = new RegExp(cb.value, "g")
        n = v.replace(re, ",")
        n = n.replace(/,,/g,'')
    }
    n = n.replace(/(^,)|(,$)/g,"")
    parent.right_frame.document.getElementById("new_tag").value = n
}
function show_picture(img)
{
    console.log("show start : " + Date.now())
    $("<img/>").attr("src", img).on("load",function(){
        s = {w:this.width, h:this.height};   
        f = 300/s.w
        _width = s.w * f
        _height = s.h * f    
        $("#right").html($("<img>").attr("src", img).width(_width).height(_height));
        
    }); 
    // $("#right").load("2.html")   
    console.log("show end : " + Date.now())
}
function pic_num_focus() {
    parent.right_frame.document.getElementById('pic_num').value = ""
}
function pic_num_change(query_type, tag, count, max_pic_count) {
    new_pic_num = Number(parent.right_frame.document.getElementById('pic_num').value)
    if (Number(new_pic_num) > Number(max_pic_count)) {
        new_pic_num = Number(max_pic_count) - Number(1)
    } else { 
        new_pic_num = Number(new_pic_num) - Number("1")
    }
    if (new_pic_num == Number("-1")) {
        new_pic_num = Number("0")
    }
	changeImg(query_type, tag, count, new_pic_num, 'false')
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

function clear_new_tag()
{
    parent.right_frame.document.getElementById("new_tag").value = "";
}

function update_tag_clear(query_type, tag, count, offset)
{
       update_tag('clear')
}

function update_tag_delete(query_type, tag, count, offset)
{
       update_tag('delete')
       changeImg(query_type, tag, count, offset, 'false')
}

function update_tag_next(query_type, tag, count, offset)
{
	update_tag('add_tag')
	changeImg(query_type, tag, count, offset, 'false')
}

function update_tag(action)
{
    var url = "http://192.168.1.13:8081/update_file";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);

    filter = parent.right_frame.document.getElementById('filter').value
    switch(action) {
        case "delete":
            new_tag = 'delete';
            break;
        case "clear":
            new_tag = "";
            break;
        case "add_tag":
            new_tag = parent.right_frame.document.getElementById('new_tag').value
            break;
        default:
            return
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
        action: action,
        action_value: new_tag,
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
                console.log("show start : " + Date.now())
                $("#show_image").html($("<img>").attr("src", img).width(_width).height(_height));
                console.log("show end : " + Date.now())

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
                parent.right_frame.document.getElementById('pic_num').value =  current_pic_num 
                parent.right_frame.document.getElementById('pic_count').value =  " of " + data['row_count'] 
                parent.right_frame.document.getElementById('message').value = ""
                parent.right_frame.document.getElementById('rotate_value').value = "90"
                parent.right_frame.document.getElementById('pic_num').oninput = function (){pic_num_change(query_type, tag, count, data['row_count']);};
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
                parent.right_frame.document.getElementById('button_update_tag_delete').onclick = function (){update_tag_delete(query_type, tag, count, delete_offset);};
            });
        } else {
            parent.left_frame.document.getElementById('show_image').innerHTML = '<object type="text/html" data="no-images.html" ></object>';
            $("#next").attr("onclick", 'null')
            parent.right_frame.document.getElementById('pic_num').value =  0
            parent.right_frame.document.getElementById('pic_count').value =  " of " + data['row_count'] 
            parent.right_frame.document.getElementById('system_tags').value = ''
            parent.right_frame.document.getElementById('user_tags').value = ''
            parent.right_frame.document.getElementById('message').value = ""
            parent.right_frame.document.getElementById('pic_num').oninput = ''
            parent.right_frame.document.getElementById('button_update_tag_next').onclick = ''
            parent.right_frame.document.getElementById('button_update_tag_delete').onclick = ''
            parent.right_frame.document.getElementById('filter').value = ''
        }
    };
    setTimeout(function() {
        url = "http://192.168.1.13:8081/get_latest_tags";
        xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.setRequestHeader('Access-Control-Allow-Headers', '*');
        xhr.setRequestHeader("Accept", "application/json");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send()
        xhr.onload = function() {
            var data = JSON.parse(this.responseText);
            console.log(data['tag_list']);
            var text_len = 0
            for (const tag of data['tag_list']) {
                var element = parent.right_frame.document.getElementById("user_tag_" + tag);
                new_tag = "user_tag_" + tag;
                if (element == null || typeof(element) == 'undefined') {
                    if ((text_len + tag.length) > 19) {
                        text_len = 0;
                        var br = document.createElement('br');
                        container.appendChild(br);
                    }
                    text_len = text_len + tag.length
                    checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = tag;
                    checkbox.id = new_tag;
                    checkbox.name = new_tag;
                    label = document.createElement('label');
                    label.htmlFor = new_tag;
                    label.appendChild(document.createTextNode(tag));
                    container = parent.right_frame.document.getElementById("info");
                    container.appendChild(checkbox);
                    container.appendChild(label);
                    parent.right_frame.document.getElementById(new_tag).onclick = function (){append_tag(this);};
                } else {
                    parent.right_frame.document.getElementById(new_tag).checked = false
                }
            };
            user_tags = parent.right_frame.document.getElementById("user_tags").value
            console.log("user_tags : " + user_tags + ":" + Date.now())
            if (user_tags != "") {
                user_tags = user_tags.split(':')
                for (const tag of user_tags) {
                    console.log("tag1 : " + tag);
                    parent.right_frame.document.getElementById("user_tag_" + tag).checked = true
                };
            };
            user_tags = parent.right_frame.document.getElementById('new_tag').value
            console.log("new_tag : " + user_tags + ":")
            if (user_tags != "") {
                user_tags = user_tags.split(',')
                for (const tag of user_tags) {
                    console.log("tag2 : " + tag);
                    parent.right_frame.document.getElementById("user_tag_" + tag).checked = true
                };
            };
        };
    }, 3000);
}
