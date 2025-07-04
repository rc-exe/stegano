from PIL import Image
import io
import hashlib
from cryptography.fernet import Fernet
import base64
import numpy as np

def generate_key(password):
    """Generate a key from password for encryption"""
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_message(message, password):
    """Encrypt message with password"""
    if not password:
        return message
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(message, password):
    """Decrypt message with password"""
    if not password:
        return message
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(message.encode()).decode()

def encode_message(image_path, message, password, output_path):
    """Hide message in image"""
    # Encrypt the message if password is provided
    if password:
        message = encrypt_message(message, password)
    
    # Convert message to binary
    binary_message = ''.join([format(ord(i), '08b') for i in message])
    binary_message += '1111111111111110'  # Message delimiter
    
    img = Image.open(image_path)
    pixels = np.array(img)
    
    if len(binary_message) > pixels.size * 3:
        raise ValueError("Message too large for the image")
    
    data_index = 0
    for row in pixels:
        for pixel in row:
            for i in range(3):  # For R, G, B channels
                if data_index < len(binary_message):
                    # Modify least significant bit
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
    
    # Save the modified image
    encoded_img = Image.fromarray(pixels)
    encoded_img.save(output_path)

def decode_message(image_path, password):
    """Extract message from image"""
    img = Image.open(image_path)
    pixels = np.array(img)
    
    binary_message = ''
    for row in pixels:
        for pixel in row:
            for value in pixel[:3]:  # R, G, B channels
                binary_message += str(value & 1)
    
    # Split binary message by delimiter
    delimiter = '1111111111111110'
    if delimiter in binary_message:
        binary_message = binary_message[:binary_message.index(delimiter)]
    
    # Convert binary to string
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
    
    # Decrypt if password was used
    if password:
        try:
            message = decrypt_message(message, password)
        except:
            raise ValueError("Incorrect password or no encrypted message found")
    
    return message