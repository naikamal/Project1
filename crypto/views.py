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
    sorted_key = sorted(list(key))
    col_order = [key.index(k) for k in sorted_key]
    num_cols = len(key)
    num_rows = -(-len(text) // num_cols)
    padded_text = text.ljust(num_rows * num_cols)
    matrix = [padded_text[i:i+num_cols] for i in range(0, len(padded_text), num_cols)]
    encrypted = ''.join(''.join(row[c] for row in matrix) for c in col_order)
    return encrypted

def columnar_transposition_decrypt(ciphertext, key):
    sorted_key = sorted(list(key))
    col_order = [key.index(k) for k in sorted_key]
    num_cols = len(key)
    num_rows = -(-len(ciphertext) // num_cols)
    col_lengths = [num_rows] * num_cols
    extra = len(ciphertext) % num_cols
    for i in range(extra):
        col_lengths[col_order[i]] -= 1
    columns = []
    index = 0
    for c in sorted_key:
        length = col_lengths[key.index(c)]
        columns.append(ciphertext[index:index+length])
        index += length
    decrypted = ''.join(''.join(row) for row in zip(*columns))
    return decrypted.strip()

# Views
def home(request):
    return render(request, 'home.html')

def encrypt(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        algorithm = request.POST.get('algorithm')
        if algorithm == 'rot13':
            encrypted_text = rot13_encrypt_decrypt(text)
        elif algorithm == 'caesar':
            encrypted_text = caesar_cipher(text, shift=3)
        elif algorithm == 'columnar':
            encrypted_text = columnar_transposition_encrypt(text, key="KEY")
        else:
            encrypted_text = "Invalid Algorithm Selected"
        return render(request, 'encrypt.html', {'result': encrypted_text})
    return render(request, 'encrypt.html')

def decrypt(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        algorithm = request.POST.get('algorithm')
        if algorithm == 'rot13':
            decrypted_text = rot13_encrypt_decrypt(text)
        elif algorithm == 'caesar':
            decrypted_text = caesar_cipher(text, shift=3, decrypt=True)
        elif algorithm == 'columnar':
            decrypted_text = columnar_transposition_decrypt(text, key="KEY")
        else:
            decrypted_text = "Invalid Algorithm Selected"
        return render(request, 'decrypt.html', {'result': decrypted_text})
    return render(request, 'decrypt.html')
