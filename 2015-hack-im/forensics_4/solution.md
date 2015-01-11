# Forensics 4

**Question**
> This image contains a pagefile. Can you tell the size of it (in bytes)? 
> Password to open archive:Synergy@123
> Flag format: flag{flag} 

## Write-up
Seemed too easy... Pulled the core file out of the .rar file, used strings on it and saw:
PagefileSize: 0x7ff7e000

Converted to decimal: 2146951168.

Flag was `flag{2146951168}`
