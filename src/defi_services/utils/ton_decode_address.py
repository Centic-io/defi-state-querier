import base64
import binascii
# Base64 URL-safe string
def decode_base64_url_safe_to_hex(base64_url_safe):
    # Step 1: Convert Base64 URL-safe to Base64
    base64_standard = base64_url_safe.replace('-', '+').replace('_', '/')
    # Step 2: Decode Base64 to Bytes
    bytes_data = base64.b64decode(base64_standard)
    # Step 3: Convert Bytes to Hexadecimal
    hex_string = binascii.hexlify(bytes_data).decode('utf-8')
    return hex_string