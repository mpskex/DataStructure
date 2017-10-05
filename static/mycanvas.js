var static_path = "static/"

function check_input()
{
    var node_type = document.getElementsByName("node_type").value;
    var node_num = document.getElementsByName("node_num").value;

    if(node_type=="" || node_type==null)
    {
        alert("Node Type 不能为空！");
        return false;
    }
    else
    {
        if(node_num=="" || node_num == null)
        {
            alert("Node Name 不能为空！");
            return false;
        }
        else
        {
            if(node_type=="keynode")
            {
                var cost_limit = document.getElementsByName("cost_limit").value;
                if(cost_limit=="")
                {
                    alert("Key Node Cost limit 不能为空！");
                    return false;
                }
            }
        }
    }
    alert
    document.getElementById("node").submit();
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
    var map_canv = document.getElementById("map");
    var guide_canv = document.getElementById("guide");
    var w = map_canv.width = guide_canv.width = window.innerWidth;
    var h = map_canv.height = guide_canv.height = window.innerHeight;
    if (map_canv.getContext)
    {
        var map_ctx = map_canv.getContext('2d');
        var guide_ctx = guide_canv.getContext('2d');
        //var w = c.width = window.innerWidth;
        //var h = c.height = window.innerHeight;

        // drawing code here
        draw_map(map_ctx);
        draw_guide(guide_ctx);
    }
    else
    {
        // canvas-unsupported code here
        alert("网页不支持HTML5，请更换Chrome、Safari等浏览器")
    }
}