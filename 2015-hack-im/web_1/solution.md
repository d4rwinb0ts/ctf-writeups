# Web 1

**Question**
>To Err is human! 
>An error may not always be an indication of something wrong, but can be the stepping stone of success. 
>Flag format: flag{flag}

## Write-up

The error text is deterministic based upon your IP of origin: http://54.165.191.231/ToErrisHuman.php starts with “Tn”, then continues to print characters two per request. This is clearly either a file or the key itself.

The full sequence is: TnVsbGNvbkdvYTIwMTVAV0VCMDAxMTAw. It’s Base64. Here’s what it decodes to: NullconGoa2015@WEB001100.

The flag was: `flag{NullconGoa2015@WEB001100}`
