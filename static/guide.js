var static_path = "static/"

function check_input()
{
    var node_type = document.getElementsByName("node_type").value;
    var node_num = document.getElementsByName("node_num").value;

    if(node_type=="")
    {
        alert("Node Type 不能为空！");
        return false;
    }
    else
    {
        if(node_num=="")
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
    var node = document.getElementById("node");
    var w = node.width = window.innerWidth;
    var h = node.height = window.innerHeight;
}