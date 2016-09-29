<?php
$filename = "/home/pi/gpio.txt";
$relay = $_GET['relay'];
$fileHandle = fopen($filename,'w') or die ("cant open file");
fwrite($fileHandle,$relay);
echo "File Created";
fclose($fileHandle);
?>