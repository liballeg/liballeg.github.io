#!/usr/bin/env python
# Written by Grzegorz Adam Hankiewicz, gradha@users.sourceforge.net.
# Please scream to me if something goes wrong.

html_header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
   <head>
      <title>Allegro's future proposals</title>
      <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
      <meta name="description" content="A game programming library">
      <meta name="keywords" content="allegro,library,developement,games,programming,portable,dos,linux,windows">
      <meta name="author" content="Grzegorz Adam Hankiewicz">
      <link rel="icon" href="../images/alex.png" type="image/png">
      <meta http-equiv="Content-Style-Type" content="text/css">
      <link rel="stylesheet" title="Default" type="text/css" href="../web_style.css">
   </head>
   <body text="#000000" bgcolor="#FFFFFF" link="#0000EF" vlink="#51188E" alink="#FF0000">
<h1><font color="#3366FF" face="helvetica,verdana">Allegro's future proposals</font></h1>
Here's a detailed index of the submited proposals. If the proposal
you are looking for is not listed here, maybe you should check the
<a href="http://alleg.sourceforge.net/future/index.php">non cached
index</a> or wait a little longer. You can select a file by date
or size, or browse their detailed descriptions below:<p>
"""   #"

html_footer = """
<div class="footer">
<hr size=0>
<table width="100%"><tr><td>
   <a href="http://petition.eurolinux.org/index_html?LANG=en"><img
      src="../images/nopatents.png" border="0" alt="No ePatents" height=33
      width=88 vspace=1 hspace=1
   ></a>
   <a href="http://www.anybrowser.org/campaign/"><img
      src="../images/anyb.png" border="0" alt="Viewable with any browser"
      height=31 width=88 vspace=1 hspace=1
   ></a>
   <a href="http://validator.w3.org/check/referer"><img
      src="../images/valid-html40.png" border="0" alt="Valid HTML 4.0!"
      title="Follow this link to verify that this page contains valid HTML 4.0 code" height=31 width=88 vspace=1 hspace=1
   ></a>
   <a href="http://jigsaw.w3.org/css-validator/validator/referer"><img
      src="../images/valid-css.png" border="0" alt="Valid CSS!"
      title="Follow this link to verify that this page uses a valid CSS" height=31 width=88 vspace=1 hspace=1
   ></a>
</td><td align="right">
   <a href="create_mirror_info.py">View source code of this script</a>
   <a href="mailto:gradha@users.sourceforge.net">Contact the webmaster</A>.
</td></tr></table>
</div>

</body>
</html>
"""

import sys, os, time

class INFO:
   def __init__(self, filename, path):
      self.name = filename
      self.path = os.path.join(path, filename)
      self.data = ""
      try:
         self.time = os.path.getmtime(self.path)
         self.ctime = time.strftime("%Y - %02m - %02d", time.localtime(self.time))
         self.size = os.path.getsize(self.path)
         self.build_description()
      except OSError: # failsafe code for info.html
         self.time = self.size = 0
         self.ctime = " time not available"
         
      self.ksize = "%0.2f" % (self.size / 1024.0)

   def build_description(self):
      file = open(self.path, "rt")
      line = file.readline()
      while line and line[0] == '#':
         if line[:8] == "# date: ": self.ctime = line[8:]
         else: self.data = "%s%s" % (self.data, line[1:])
         line = file.readline()
      file.close()
      self.data = self.data.replace("&", "&amp;")
      self.data = self.data.replace("<", "&lt;")
      self.data = self.data.replace(">", "&gt;")

def sort_by_name(list):
   t = map(lambda x: (x.name, x), list)
   t.sort()
   return t

def sort_by_time(list):
   t = map(lambda x: (x.ctime, x), list)
   t.sort()
   t.reverse()
   return t
   
def sort_by_size(list):
   t = map(lambda x: (x.size, x), list)
   t.sort()
   t.reverse()
   return t
   
def show_help():
   print "\tUsage '%s target_directory'" % sys.argv[0]
   print "\ttarget_directory has to contain the Allegro documents"
   print "\tA new target_directory/info.html will be created"

if __name__ == "__main__":
   try:
      target_directory = sys.argv[1]
      files = {}
      # get files with full path
      for file, info in map(lambda x: (x, INFO(x, target_directory)),
         os.listdir(target_directory)):
         files[file] = info
         
   except (OSError, IndexError), msg:
      print "Incorrect parameter."
      show_help()
      raise # just to get the useful traceback
      
   # remove unwanted files
   for key in ["index.html", "index.php", "create_mirror_info.py", "mirror_alleg_future.py"]:
      try: del files[key]
      except KeyError: pass
   info_html = files.setdefault("info.html",
      INFO("info.html", target_directory))
   del files["info.html"]

   # get newset timestamp
   newest_file = reduce(max, map(lambda x: x.time, files.values()))

   # no need to regenerate file if timestamps are older
   if newest_file > info_html.time:
      file = open(info_html.path, "wt")
      file.write(html_header)

      # write the indexes
      file.write('<h2>Ordered by date</h2><blockquote><table>\n')
      for order, item in sort_by_time(files.values()):
         file.write('<tr><td align=right>%s</td><td><a href="#%s">[see '
            'description]</a> <a href="%s">%s</a></td></tr>\n' % (
            item.ctime, item.name, item.name, item.name))
      file.write('</table></blockquote><h2>Ordered by size</h2><blockquote><table>\n')
      for order, item in sort_by_size(files.values()):
         file.write('<tr><td align=right>%s KB</td><td><a href="#%s">[see '
            'description]</a> <a href="%s">%s</a></td></tr>\n' % (
            item.ksize, item.name, item.name, item.name))
      file.write('</table></blockquote><hr>\n<table>')
      colored = 0

      # Now write detailed information
      for order, item in sort_by_name(files.values()):
         if not colored: s = '<tr><td>'
         else: s = '<tr bgcolor="#eeeeee"><td>'
         colored = not colored
         
         s = '%s<b><a href="%s">%s</a> -\n' % (s, item.name, item.name)
         s = '%s<a name="%s">%s</a>' % (s, item.name, item.ctime)
         s = '%s -\n%s KB</b><blockquote>' % (s, item.ksize)
         if item.data: s = '%s<b>Description:</b> %s\n' % (s, item.data)
         else: s = '%s<b>No description available.</b>' % s
         file.write('%s</blockquote>&nbsp;</td></tr>\n' % s)
         
      file.write('</table>\n%s' % html_footer)
      file.close()
