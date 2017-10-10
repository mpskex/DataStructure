//  全局变量 描述关键点集
var point_on_map = new Array(
    //  宿舍
    Array(491, 99), 
    //  礼堂
    Array(406, 163),
    //  图书馆
    Array(377, 139)
);
var point_name = new Array(
    "宿舍",
    "礼堂",
    "图书馆"
);
//  当前点
var cur_point = -1;

window.onload=function(){
    var static_path = "static/"
    var menu = document.getElementById("option");
    var map = document.getElementById("map_holder");
    
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

function draw_map(ctx)
{
    var img = new Image();
    img.src = static_path + "map.png";
    img.onload = function()
                {
                    ctx.drawImage(img, 0, 0);
                }
    var w = ctx.width = img.width;
    var h = ctx.height = img.height;
}

function draw_guide(ctx)
{
    ctx.fillStyle = "rgb(200,0,0)";
    ctx.fillRect (10, 10, 55, 50);
    
    ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
    ctx.fillRect (30, 30, 55, 50);

}

function draw()
{
    var node = document.getElementById("node");
    var w = node.width = window.innerWidth;
    var h = node.height = window.innerHeight;
}