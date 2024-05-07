# Decode Binary and Decipher Text

## Requirements
* Python 3.12.2

## Execution
To execute the deserializer: ```python3 deserialize.py [-h] [-o OUTPUT_FILE] input_file```

Ex: ```python3 deserialize.py client_data.bin -o client_data.csv```

## Development
Through the following process, I decoded the binary and deciphered the text:
1. I executed ```hexdump -C client_data.bin``` to view the code as bytes mapped to ASCII characters.
2.  I first noticed that the file begins with a `0x01` value, indicating the start of the file. Hence the initial `f.read(1)` call to skip this byte.
3.  I noticed there were two capitalized values that were unintelligible as names. However, given the pattern of two capitalized values, I assumed these were encoded first and last names.
4.  Following the assumption of (2), I wrote a script to shift each letter in each word 25 times. I noticed that shifting "Evpuneq" for 13 times yielded "Richard". As this is an intelligible name, I assumed that shifting the ASCII value of each letter by 13 would decode all text. This assumption yielded intelligible values even for emails.
5.  I identified emails as the values with @ as a medial character.
6.  I identified dates of birth as the values following the YYYY-MM-DD pattern.
7.  I identified phone numbers as 10-digit values broken into chunks of 3-4 values delineated by dashes.
8.  I assumed zip codes are the 6-digit numbers following the 10-digit phone numbers.
9.  I noticed there are values `0x02` and `0x03` indicating start of text and end of text respectively.

## To Do
1. I did not find the 'Is Active' value in the given time limit. However, on inspection, I noticed a series of four `0xff` values preceding phone numbers. I assume these are truth values, where `0xff\0xff\0xff\0xff` is active and `0x00\0x00\0x00\0x00` is inactive. Given more time, I would parse these values out.
2. I did not separate out postal / zip codes in the given time limit. Given more time, I would parse these values out.
3. I failed to utilize the values of `0x02` and `0x03` for setting bounds on byte reading. Utilizing these values would improve computations.