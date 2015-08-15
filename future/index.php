<HTML>

<HEAD>
<TITLE>Allegro's future</TITLE>
</HEAD>

<BODY>

<?php

$dir = opendir(".");

while ($name = readdir($dir)) {
   $file_name = basename($name);
   $file_size = filesize($name);
   
   if (is_file($name) && (eregi(".html", $name) || eregi(".txt", $name) || eregi(".zip", $name) || eregi(".gz", $name))) {
      if ($file_size >= (1024*1024)) {
         $file_list[$file_name] = round($file_size / (1024 * 1024) * 100) / 100 . " MB";
      } elseif ($file_size >= 1024) {
         $file_list[$file_name] = round($file_size / 1024 * 100) / 100 . " KB";
      } else {
         $file_list[$file_name] = round($file_size * 100) / 100 . " bytes";
      }
      
   }
}

closedir($dir);

ksort($file_list);
reset($file_list);

?>

<P><FONT SIZE=+2>Allegro's future</FONT></P>
<HR>
<P>

<?php

while (list ($name, $size) = each ($file_list)) {
   echo "<a href=\"$name\">$name</a> ($size)<br>";
}

?>

</P>
<HR>
There's a friendlier cached index at <a href="info.html">info.html</a>.
<FONT SIZE=-1>PHP scripting by: Henrik Stokseth.</FONT>
</BODY>
</HTML>

