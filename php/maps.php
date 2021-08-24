<?php
$city = strval($_GET["city"]);
?>

<!DOCTYPE html>  
<html>
<head>  
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />  
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
<title>百度地图-城市定位</title>  
<style type="text/css">  
html{height:100%}  
body{height:100%;margin:0px;padding:0px}  
#container{height:100%}  
</style>  
<script type="text/javascript" src="https://api.map.baidu.com/api?v=3.0&ak=tF8XaCqUG9ZjFR66lqqNXmLzeT24gtGF">
</script>
</head>  
 
<body>  
<div id="container"></div> 
<script type="text/javascript"> 
var map = new BMap.Map("container");
// 创建地图实例  
var point = new BMap.Point(116.404, 39.915);
// 创建点坐标  
map.centerAndZoom(point, 15);
// 初始化地图，设置中心点坐标和地图级别  
map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
map.addControl(new BMap.NavigationControl()); // 添加标准地图控件


// 创建地址解析器实例     
var myGeo = new BMap.Geocoder();      
// 将地址解析结果显示在地图上，并调整地图视野    
myGeo.getPoint( "<?php echo $city ?>" , function(point){      
    if (point) {      
        map.centerAndZoom(point, 15);      
        map.addOverlay(new BMap.Marker(point));

		map.addControl(new BMap.NavigationControl());    
		map.addControl(new BMap.ScaleControl());    
		map.addControl(new BMap.OverviewMapControl());    
		map.addControl(new BMap.MapTypeControl());   
    }      
 }, 
 "<?php echo $city ?>");
</script>  

</body>  
</html>

