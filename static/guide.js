window.onload=function(){
    var static_path = "static/"
    var menu = document.getElementById("option");
    document.oncontextmenu = function(e) {
        var e = e || window.event;
        //鼠标点的坐标
        var oX = e.clientX;
        var oY = e.clientY;
        //菜单出现后的位置
        menu.style.display = "block";
        menu.style.left = oX + "px";
        menu.style.top = oY + "px";
        //阻止浏览器默认事件
        return false;//一般点击右键会出现浏览器默认的右键菜单，写了这句代码就可以阻止该默认事件。
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
    var node_type = document.getElementById("node_type").value;
    var node_num = document.getElementById("node_num").value;

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
            }
            else if(node_type=="waynode")
            {
                if(cost_limit!=NULL && cost_limit!="")
                {
                    alert("Key Node Cost limit 不为空！");
                    return false;
                }
            }
        }
    }
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