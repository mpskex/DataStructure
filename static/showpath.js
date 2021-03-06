/*
#	mpsk
#	Beijing University of Technology
#	Copyright 2017
*/

//  全局变量 描述关键点集
var point_on_map = new Array(
    //  宿舍
    Array(491, 99), 
    //  美食园
    Array(418, 412),
    //  图书馆
    Array(377, 139),
    //  逸夫图书馆
    Array(329, 305),
    //  科学楼
    Array(331, 493),
    //  信息楼
    Array(243, 355),
    //  人文楼
    Array(420, 540),
    //  软件楼
    Array(712, 428),
    //  奥运场馆
    Array(495, 515),
    //  三教
    Array(416, 250)
);
var point_name = new Array(
    "宿舍",
    "美食园",
    "图书馆",
    "逸夫图书馆",
    "科学楼",
    "信息楼",
    "人文楼",
    "软件楼",
    "奥运场馆",
    "三教"
);
var static_path = "static/"
//  当前点
var cur_point = -1;
//  动画指针
var frame = 0;
var dy_color_r = 23;
var dy_color_g = 37;
var dy_color_b = 57;
var path_index = new Array();

window.onload=function(){
    //  绘制路径点
    var svg = document.getElementById("node");
    if(svg){
        for(var i=0;i<point_on_map.length;i++)
        {
            var p = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            if(p){
                p.setAttribute("cx", ""+point_on_map[i][0]);
                p.setAttribute("cy", ""+point_on_map[i][1]);
                p.setAttribute("r", "4");
                p.setAttribute("stroke", "red");
                p.setAttribute("stroke-width", "3");
                p.setAttribute("fill-opacity", "0")
                p.setAttribute("filter", "Gaussian_Blur");
                svg.appendChild(p);
            }
        }
        
    }

    var menu = document.getElementById("option");
    var map = document.getElementById("map_holder_node");
    
    map.oncontextmenu = function(e) {
        //  初始化值
        document.getElementById("plimit").value=0;
        var e = e || window.event;
        //  鼠标点的坐标
        var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
        var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
        var x = e.pageX || e.clientX + scrollX;
        var y = e.pageY || e.clientY + scrollY;
        //  菜单出现后的位置
        menu.style.display = "block";
        menu.style.left = x + "px";
        menu.style.top = y + "px";
        //  地图坐标修正
        var map_x = x - 178;
        var map_y = y;
        for(var i=0; i<point_on_map.length;i++)
        {
            if(Math.abs(map_x-point_on_map[i][0])<10
            && Math.abs(map_y-point_on_map[i][1])<10)
            {
                document.getElementById("pname").innerHTML = point_name[i];
                cur_point = i;
                break;
            }
            else
            {
                document.getElementById("pname").innerHTML = "None";
                cur_point = -1;
            }
        }
        //  阻止浏览器默认事件
        return false;
    }

    //  记录Path对象的长度
    CountPath();
    //  隐藏所有Path
    HideAllPath();
    //  设置定时器
    var t1 = window.setInterval(AnimatedPath, 200); 

    //  按钮事件
    document.getElementById("opt_btn_tip").onmouseover = function(e){
        document.getElementById("opt_btn_tip").style.background = "#7869c3";
    }
    document.getElementById("opt_btn_tip").onmouseout = function(e){
        document.getElementById("opt_btn_tip").style.background = "#8f8f8f";
    }
    document.getElementById("opt_btn_add").onmouseover = function(e){
        document.getElementById("opt_btn_add").style.background = "#7869c3";
    }
    document.getElementById("opt_btn_add").onmouseout = function(e){
        document.getElementById("opt_btn_add").style.background = "#8f8f8f";
    }
    document.getElementById("opt_btn_rm").onmouseover = function(e){
        document.getElementById("opt_btn_rm").style.background = "#7869c3";
    }
    document.getElementById("opt_btn_rm").onmouseout = function(e){
        document.getElementById("opt_btn_rm").style.background = "#8f8f8f";
    }
    document.onclick = function(e){
        var e = e || window.event;
        menu.style.display = "none"
    }
    menu.onclick = function(e){
        var e = e || window.event;
        e.cancelBubble = true;
    }
}

function CheckInput()
{
    document.getElementById("node_num").value = cur_point;
    document.getElementById("node_type").value = document.getElementById("ptype").value;
    document.getElementById("cost_limit").value = document.getElementById("plimit").value;

    var node_type = document.getElementById("ptype").value;
    var node_num = cur_point;

    document.getElementById("option").style.display = "none";

    if(cur_point==-1)
    {
        alert("没有选中任何点");
        return false;
    }

    if(node_type!="keynode" && node_type!="waynode")
    {
        alert("Node Type 非法！");
        return false;
    }
    else
    {
        if(isNaN(parseInt(node_num,10)))
        {
            alert("Node Name 非法\n" + node_num);
            return false;
        }
        else
        {
            var cost_limit = document.getElementById("cost_limit").value;
            if(node_type=="keynode")
            {
                if(isNaN(parseInt(cost_limit,10)))
                {
                    alert("Key Node Cost limit 非法！");
                    return false;
                }
                else
                {
                    if(cost_limit=="0")
                    {
                        alert("Key Node doesn't allow zero value!!");
                        return false;
                    }
                }
            }
            else if(node_type=="waynode")
            {

            }
        }
    }
    document.getElementById("option").style.display = "none";
    document.getElementById("nform").submit();
    //AddPointToSidebar(node_num, node_type, cost_limit);
}

function RemovePoint()
{
    document.getElementById("node_num_r").value = cur_point;
    document.getElementById("rform").submit();
}

function GetMousePos()
{
    var e = window.event;
    var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
    var x = e.pageX || e.clientX + scrollX;
    var y = e.pageY || e.clientY + scrollY;
    //  sub the side bar width
    x -= 178;
    alert("X: " + x + "\nY: " + y);
}

function GetLimitValue()
{
    var l = document.getElementById("plimit");
    var d = document.getElementById("plimit_value");
    d.innerHTML = l.value;
}

function AnimatedPath()
{
    console.log(frame);
    if(frame==0)
    {
        HideAllPath();
        frame = frame + 1;
    }
    else if(frame <= path_index.length + 1)
    {
        HideAllPath();
        path_root = document.getElementById("path_holder");
        path_root.childNodes[path_index[frame-1]].style.display = "";
        path_root.childNodes[path_index[frame-1]].style.stroke = "#70fe38";
        frame = (frame + 1)%(path_index.length+1)
    }
    else
    {
        frame = 0;
        console.log("alert: frame exceed!!");
    }
}

function colorRGB2Hex(r, g, b) 
{
    var hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    return hex;
 }

function HideAllPath()
{
    path_root = document.getElementById("path_holder");
    for(var k=0 in path_root.childNodes)
    {
        if(path_root.childNodes[k].nodeName == "path")
        {
            path_root.childNodes[k].style.display = "none";
        }
    }
}

function CountPath()
{
    path_root = document.getElementById("path_holder");
    for(var k=0 in path_root.childNodes)
    {
        if(path_root.childNodes[k].nodeName == "path")
        {
            path_index.push(k);
            console.log(path_root.childNodes[k]);
        }
    }
    console.log(path_index);
}

function draw()
{
    var node = document.getElementById("node");
    var w = node.width = window.innerWidth;
    var h = node.height = window.innerHeight;
}