# Crypto 3

**Question**
> Server running at: 54.165.191.231:2002

> >netcat 54.154.191.231                                                                                       
> M E N U
> =======
> 1. Show public keys
> 2. Encrypt
> 3. Solve challenge
> What do you want to do: 1
> Public Key(N): 22707716705395385903017779098328224417
> 
> M E N U                                                                                
> =======                                                                                
> 1. Show public keys                                                                    
> 2. Encrypt                                                                             
> 3. Solve challenge                                                                     
> What do you want to do: 2                                                              
> Enter string to encrypt: the eagle has landed                                          
> Cryptogram C = M^2 % N: [16706375071175492792039878978962223285, 856516745787598793104]
                                                                                                                                      
## Write-up

The server tells you the cypher is obtained by finding the square of the plaintext mod N. This is a Rabin cipher, 
which relies on the difficulty of calculating the square root modulo a large semiprime (N) unless the factors of that prime are known.

Luckily, the size of this key, 22707716705395385903017779098328224417, is only O(2^124) -- which is easily factored using a general number field sieve.

I used msieve to factor this: 

> > msieve -q 22707716705395385903017779098328224417
> 22707716705395385903017779098328224417
> prp19: 4085722380312421477
> prp19: 5557821748931214221

M E N U
=======
1. Show public keys
2. Encrypt
3. Solve challenge
What do you want to do: Decrypt:
[11193203926281936610602741358557902742, 866255063186730425674749972562607224, 757076103014098105015915072375696]

After playing around with encrypting my own messages, I verified that the encrypted message was formatted as digits mod N, 
so I just ran that through a decryption.

    def decrypt(cypher):
        return it.product(*list(decrypt(cypher)))

    def _decrypt(cypher):
        for c in cypher:
	    # mod_sqrt equivalent to http://ideone.com/r7BAX
            mp = mod_sqrt(c, p)
            mq = mod_sqrt(c, q)
            yp, yq = gcd(p, q)
            r = (yp*p*mq + yq*q*mp) % self.N
            s = (yp*p*mq - yq*q*mp) % self.N
            yield [r, N-r, s, N-s]

This yields 4 candidate answers per digit block (so 64 total combinations), but when we decode the base-N numbers to base 256,  
there is only one valid answer that decodes to only printable characters:

> Rabin(4085722380312421477, 5557821748931214221).solve([
     11193203926281936610602741358557902742,
     866255063186730425674749972562607224,
     757076103014098105015915072375696])
> opopanax judge kalansuwa modernization
