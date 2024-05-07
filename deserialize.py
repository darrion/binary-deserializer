import csv
import functools
import argparse
from io import BufferedReader
from typing import List, Callable
from enum import Enum

class Active(Enum):

    TRUE = b'\xff\xff\xff\xff'
    FALSE = b'\x00\x00\x00\x00'

class BinaryEOF(Exception):

    def __init__(self):
        super().__init__("End of bin file detected.")

def bytes_to_arr(byte_str):
    return [bytes([byte]) for byte in byte_str]

def detect_eof(chunk):
    if not chunk:
        raise BinaryEOF()

def decipher(shift: int, text: str) -> str:
    deciphered_text = ''
    deciphered_char = ''
    for char in text:
        if char.isalpha():
            n = 26
            diff = ord(char) - ord('a') if char.islower() else ord(char) - ord('A')
            base = ord('a') if char.islower() else ord('A')
            shifted_diff = diff + shift
            deciphered_char = chr((shifted_diff % n) + base)
        else:
            deciphered_char = char
        deciphered_text += deciphered_char
    return deciphered_text

def decode_ascii(bytes_str):
    return bytes_str.decode('ascii', errors='replace')

def filter_ascii(text):
    return ''.join(char for char in text if ord(char) < 0xF7)

def decode_bool(bytes_str):
    if bytes_str == Active.TRUE.value:
        return "true"
    elif bytes_str == Active.FALSE.value:
        return "false"
    else:
        return "unknown_state"

def process(buffer: BufferedReader,
            n_bytes: int,
            decode_fn: Callable=None,
            decipher_fn: Callable=None) -> str:
    bytes_str = buffer.read(n_bytes)
    detect_eof(bytes_str)
    text = decode_fn(bytes_str) if decode_fn else bytes_str
    text = filter_ascii(text)
    return decipher_fn(text) if decipher_fn else text
    
def deserialize(file_path: str):

    data = []

    with open(file_path, 'rb') as f:

        letter_shift = 13

        # 165 bytes total
        n_first_name_bytes = 32
        n_last_name_bytes = 36
        n_dob_bytes = 10
        n_email_bytes = 66
        n_active_status_bytes = 4
        n_phone_bytes = 12
        n_zip_bytes = 5

        identifier = 1
        
        while True:

            decipher_names = functools.partial(decipher, letter_shift)
            
            try:
                
                first_name = process(buffer=f,
                                     n_bytes=n_first_name_bytes,
                                     decode_fn=decode_ascii,
                                     decipher_fn=decipher_names)

                last_name = process(buffer=f,
                                    n_bytes=n_last_name_bytes,
                                    decode_fn=decode_ascii,
                                    decipher_fn=decipher_names)

                dob = process(buffer=f,
                              n_bytes=n_dob_bytes,
                              decode_fn=decode_ascii)

                email = process(buffer=f, 
                                n_bytes=n_email_bytes,
                                decode_fn=decode_ascii,
                                decipher_fn=decipher_names)
                
                active_status = process(buffer=f,
                                        n_bytes=n_active_status_bytes,
                                        decode_fn=decode_bool)
                
                phone_number = process(buffer=f, 
                                          n_bytes=n_phone_bytes,
                                          decode_fn=decode_ascii)
                
                zip_code = process(buffer=f,
                                   n_bytes=n_zip_bytes,
                                   decode_fn=decode_ascii)

                data.append([identifier,
                             first_name,
                             last_name,
                             dob,
                             email,
                             active_status,
                             phone_number,
                             zip_code])

                identifier += 1
            except BinaryEOF as ex:
                print (ex)
                return data

def write(data: List, headers: List, file_path: str):
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)  

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Deserialize a client binary')
    parser.add_argument('input_file', type=str, help='Input file to deserialize')
    parser.add_argument('-o', '--output-file', type=str, help='Output file to dump deserialized contents')
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file
    data = deserialize(input_file_path)
    
    headers = ['identifier', 'first_name', 'last_name', 'date_of_birth', 'email', 'active_status', 'phone_number', 'zip_code']

    write(data, headers, output_file_path)
