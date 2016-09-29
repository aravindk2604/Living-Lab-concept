<html>
<body>
<head>
	<meta http-equiv="refresh" content="1; URL=http://192.168.1.106/file.php">
</head>

<?php

$relay_1  = '';
$relay_2  = '';
$relay_3  = '';
$relay_4  = '';
$relay_5  = '';
$relay_6  = '';
$relay_7  = '';
$relay_8  = '';
$error = '';

$file_name = "/home/pi/Relay.txt";

$file=fopen($file_name,"r") or exit("Unable to open file!");

while(!feof($file))
  {
  $line = fgets($file);
  $broken =explode(':', $line);

  if(strcmp($broken[0],'Error') != 0 )
  {
  switch($broken[1])
  {
  	case 1 : $relay_1 = $broken[2] ;
  		break;
  	case 2 : $relay_2 = $broken[2];
  		break;
  	case 3 : $relay_3 = $broken[2];
  		break;
  	case 4 : $relay_4 = $broken[2];
  		break;
  	case 5 : $relay_5 = $broken[2];
  		break;
  	case 6 : $relay_6 = $broken[2];
  		break;
  	case 7 : $relay_7 = $broken[2];
  		break;
  	case 8 : $relay_8 = $broken[2];
  		break;
  }
  }
  else 
  {
    $error = $broken[1];
  }
}
fclose($file);
?>

<table border="1" cellpadding="10">
<tr>
<th>Relay Number</th>
<th>Relay state</th>
</tr>
<tr>
<td> Relay 1 </td>
<td><?php echo $relay_1 ; ?></td>
</tr>
<tr>
<td> Relay 2 </td>
<td><?php echo $relay_2 ; ?></td>
</tr>
<tr>
<td> Relay 3 </td>
<td><?php echo $relay_3 ; ?></td>
</tr>
<tr>
<td> Relay 4 </td>
<td><?php echo $relay_4 ; ?></td>
</tr>
<tr>
<td> Relay 5 </td>
<td><?php echo $relay_5 ; ?></td>
</tr>
<tr>
<td> Relay 6 </td>
<td><?php echo $relay_6 ; ?></td>
</tr>
<tr>
<td> Relay 7 </td>
<td><?php echo $relay_7 ; ?></td>
</tr>
<tr>
<td> Relay 8 </td>
<td><?php echo $relay_8 ; ?></td>
</tr>
</table>
</br>
<h4>Status: <?php echo $error ?> </h4>
</body>
</html>