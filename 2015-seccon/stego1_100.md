Stego 1
-------

A really easy problem, we are given the file: MrFusion.gpjb

As with all stego files, I start by using hachoir-subfiles, which indicates that there are
many subfiles in this file.

To extract them:
```
hachoir-subfile MrFusion.gpjb subfiles/

```

Looking through the subfiles directory, we see a bunch of different
types of image files. Each image contains part of the flag. Inspecting
them individually, we are able to make the flag: SECCON{0CT 21 2015 078},
which is a reference to Back to the Future.
