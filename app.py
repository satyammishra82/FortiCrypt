import os
import hashlib
from Crypto.Cipher import AES
import sympy
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

class AES_New:
    def __init__(self, block_size=128, key_length=256):
        self.block_size = block_size
        self.key_length = key_length
        self.key = self.generate_dynamic_key()

    def generate_dynamic_key(self):
        prime_number = sympy.randprime(2**(self.key_length // 2 - 1), 2**(self.key_length // 2))
        prime_str = str(prime_number).encode('utf-8')
        return hashlib.sha256(prime_str).digest()

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_text = self._pad(plaintext)
        ciphertext = cipher.encrypt(padded_text)
        return ciphertext

    def decrypt(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_text = cipher.decrypt(ciphertext)
        return self._unpad(decrypted_text)

    def _pad(self, s):
        pad_len = self.block_size // 8 - len(s) % (self.block_size // 8)
        padding = bytes([pad_len] * pad_len)
        return s + padding

    def _unpad(self, s):
        pad_len = s[-1]
        return s[:-pad_len]

aes_new = AES_New()  # Initialize AES object

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '').encode('utf-8')
        ciphertext_hex = request.form.get('ciphertext', '')

        if 'encrypt' in request.form:
            if plaintext:
                ciphertext = aes_new.encrypt(plaintext)
                ciphertext_hex = ciphertext.hex()
                return render_template('index.html', ciphertext=ciphertext_hex)

            flash("Please enter some text to encrypt.", "danger")

        elif 'decrypt' in request.form:
            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                decrypted_text = aes_new.decrypt(ciphertext)
                decrypted_text_str = decrypted_text.decode('utf-8')
                return render_template('index.html', decrypted_text=decrypted_text_str)
            except Exception as e:
                flash("Error decrypting text: {}".format(str(e)), "danger")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
