from django.shortcuts import render
from django.http import JsonResponse

# Algorithm definitions
def rot13_encrypt_decrypt(text):
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            result += chr(((ord(char) - ord('a') + 13) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            result += chr(((ord(char) - ord('A') + 13) % 26) + ord('A'))
        else:
            result += char
    return result

def caesar_cipher(text, shift, decrypt=False):
    result = ""
    if decrypt:
        shift = -shift
    for char in text:
        if 'a' <= char <= 'z':
            result += chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            result += char
    return result

def columnar_transposition_encrypt(text, key):
    # Sort key alphabetically to determine column order
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols  # Pad rows as necessary
    padded_text = text.ljust(num_rows * num_cols)  # Add spaces to fit the grid

    # Create the grid (row-wise filling)
    grid = [padded_text[i:i + num_cols] for i in range(0, len(padded_text), num_cols)]

    # Read columns based on sorted key order
    encrypted = ''.join(''.join(row[col] for row in grid) for col in key_order)
    return encrypted


def columnar_transposition_decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    key_order = sorted(range(len(key)), key=lambda k: key[k])

    # Calculate the number of characters per column
    full_cols = len(ciphertext) % num_cols
    col_lengths = [num_rows - 1 if i >= full_cols and full_cols != 0 else num_rows for i in range(num_cols)]

    # Split ciphertext into columns
    columns = []
    start = 0
    for col_length in col_lengths:
        columns.append(ciphertext[start:start + col_length])
        start += col_length

    # Rearrange columns to their original order
    ordered_columns = [''] * num_cols
    for i, col_index in enumerate(key_order):
        ordered_columns[col_index] = columns[i]

    # Read the grid row-wise to reconstruct the text
    decrypted = ''.join(''.join(row) for row in zip(*ordered_columns))
    return decrypted.rstrip()


# Views
def home(request):
    return render(request, 'home.html')


# Views
def encrypt(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        algorithm = request.POST.get('algorithm')
        key = request.POST.get('key')  # Capture the key input
        
        if algorithm == 'rot13':
            encrypted_text = rot13_encrypt_decrypt(text)
        elif algorithm == 'caesar':
            encrypted_text = caesar_cipher(text, shift=3)
        elif algorithm == 'columnar':
            if key:
                encrypted_text = columnar_transposition_encrypt(text, key)
            else:
                encrypted_text = "Key is required for Columnar Transposition."
        else:
            encrypted_text = "Invalid Algorithm Selected"
        return render(request, 'encrypt.html', {'result': encrypted_text})
    return render(request, 'encrypt.html')

def decrypt(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        algorithm = request.POST.get('algorithm')
        key = request.POST.get('key')  # Capture the key input
        
        if algorithm == 'rot13':
            decrypted_text = rot13_encrypt_decrypt(text)
        elif algorithm == 'caesar':
            decrypted_text = caesar_cipher(text, shift=3, decrypt=True)
        elif algorithm == 'columnar':
            if key:
                decrypted_text = columnar_transposition_decrypt(text, key)
            else:
                decrypted_text = "Key is required for Columnar Transposition."
        else:
            decrypted_text = "Invalid Algorithm Selected"
        return render(request, 'decrypt.html', {'result': decrypted_text})
    return render(request, 'decrypt.html')
