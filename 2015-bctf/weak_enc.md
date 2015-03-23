Weak Enc
--------

In this problem, you are given a python encryption program that takes plaintext and returns an encrypted message.

###  Preliminary -- proof of work

A proof of work is required to prevent brute-force / ddosing the service. you have to find a string with a server-provided nonce as a prefix with a sha1 ending in \0\0. We can just bruteforce this:

    def solve_pow(prefix):
        for suffix in range(0,9999999):
           text = prefix + ('%5d' % hex(suffix))
               if hashlib.sha1(text).digest().endswith('\0\0'):
       	          return text

### The LZW function

    def LZW(s, lzwDict): # LZW written by NEWBIE
        for c in s: updateDict(c, lzwDict)
	result = []
	i = 0
        while i < len(s):
           if s[i:] in lzwDict:
              result.append(lzwDict[s[i:]])
              break
            for testEnd in range(i+2, len(s)+1):
               if not s[i:testEnd] in lzwDict:
                  updateDict(s[i:testEnd], lzwDict)
                  result.append(lzwDict[s[i:testEnd-1]])
                  i = testEnd - 2
                  break
            i += 1
        return result

The plaintext is concatenated to a secret salt, then run through a custom LZW algorithm. This then gets xor'ed with a fixed OTP derived from the MD5 of the salt. The LZW table is populated in order with single letters first, then dynamically during encoding as new sequences are found. This suggests that the plaintext "SALT$a", where "a" is any letter, will always encode to the same value as long as "a" is not in the salt, and when 'a' is in salt, the lzw value of a will reflect the first index of a in salt. 

The lzw results are then concatenated to an OTP. The specific value of this OTP I'm not terribly interested in, as we'll shortly see: The final results are the bytes in the lzw compression xor'ed with the bytes in the OTP.

### Eliminating the OTP, and finding the character encodings 

So now , we know enc(salt$s) = otp ^ lzw(salt$s), etc. and we know which letters are included in salt. this means we know that '$' gets encoded as byte N, where N is the number of unique letters in the salt. and thus if we encode 'salt$!', '!' gets encoded as byte N+1. thus, lzw(salt$s) = enc(salt$s) ^ enc(salt$!) ^ lzw(salt$!). we know that lzw(!) = N + 1, so we can get the numeric value of s for all characters s. Arranging them in order, we know the order of the first occurence of each letter in the salt.

### Finding ngrams

Now we know the encoding of each character. In the actual CTF, we got:

    n: 0
    i: 1
    k: 2
    o: 3

Bruteforceing the solution may still be difficult, so we should figure out a better solution. That is to check ngrams: for all plaintextx of the form salt${abcde}, 'abcde' will encode as a single byte when 'ab' actually appears as a bigram in the salt. 

    salt$ni = 4
    salt$ik = 5
    salt$ko = 6
    salt$on = 7
    salt$nik = 8
    salt$kon = 9
    salt$nin = 10
    ...
Following along the lzw process on paper, we find the salt is "nikonikoninikonikoni" based on the order of the bigrams as it is being lzw-compressed:

    n    ni = 4
    i    ik = 5
    k    ko = 6
    o    on = 7
    ni   nik = 8
    ko   kon = 9
    ni   nin = 10
    nik  niko = 11
    on   oni = 12
    ik   iko = 13
    oni  oni$ = 14

### Decrypting the solution

The message we were asked to decrypt was: NxQ1NDMYcDcw53gVHzI7. Since we know the salt, we can calculate the OTP and xor it against the decrypted message to retrieve lzw(solution). This turns out to be 
0,1,2,3,4,6,4,8,7,5,12,11,10,13,4 which we look up in our lzw table generated from the previous solution:

    nikonikoninikonikoni nikoninikoni



Full solution file: https://gist.github.com/talyian/e4c136466628aa41873a
