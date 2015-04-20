# Strength (Crypto, 110 pts)

Downloading the problem file, we see:

	{N, e, c}
	{<a 1024-bit number>, <a number>, <a number}
	{<a 1024-bit number>, <a number>, <a number}
	{<a 1024-bitnumber>, <a number>, <a number}
	... 20 sets ...

where `N` value is the same in every row. `N, e, c` and then suggest that this is a RSA cipher, with (N,e) being the public key and c being the ciphertext.

Remember that in RSA, `m**e == c (mod N)`. Since we have multiple values of `e` and `c` at our disposal, we can combine them to find other powers of `m`. Our goal is to find `m (mod N)`, which should be possible if two of the `e`'s we're given are relatively prime. I used factordb to factor all the exponents and found exactly one pair, 1804229351, 17249876309, which were relatively prime.

Now, because `gcd(e1, e2) == 1`, using the Extended Euclidean Formula, we can find the Bezout coefficients a, b that solve the following equation:

    a * e1 + b* b2 == 1

Note that if we take m the power of either side of the equation, we get:

    m ** ( a*e1 + b*e2) == m**1 (mod N)
    ..
    (m**e1)**a + (m**e2)**b == m (mod N)
    ..
    c1**a * c2**b == m (mod N)     # where c1, c2 are the given ciphertexts for e1, e2

As it turns out, a was negative, so we needed to calculate a modular inverse. The Chinese Remainder theorem provides us a solution:

    def invert(e, n):  # calculates e**-1 (mod n)
      t, nt, r, nr = 0, 1, n, e
      while nr:
        r, (q, nr) = nr, divmod(r, nr)
        t, nt = nt, t - q * nt
      return t % n

    invert(c1 ** (-a)) * c2 ** b == m

Full solution: [solve.py]



 
