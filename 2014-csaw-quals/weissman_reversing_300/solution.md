The file is a custom LZ-type compressed archive. byte ‘\x13’ divides the file into 9-byte chunks. You can re-use a
prefix of an existing chunk instead of a current chunk. a three-byte chunk encodes reusing a previous prefix. the first
7-bits are the length of the used chunk.

The first file is the HTML at http://burtleburtle.net/bob/hash/

Replacing each three byte chunk to encode a previous prefix with zeros of correct length and using the 9 byte chunks as
is gives a valid jpeg file for key.jpg. The image is corrupted/distorted, but opening in GIMP gives a good enough view
of the key part to recover:

The decompression code is in decompress.py

key{I know how long it’d take, and I can prove it}
