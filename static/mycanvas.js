var static_path = "static/"

function draw_map(ctx)
{
    var img = new Image();
    img.src = static_path + "map.png";
    img.onload = function()
                {
                    ctx.drawImage(img, 0, 0);
                }
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