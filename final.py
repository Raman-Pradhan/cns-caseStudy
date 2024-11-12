import streamlit as st
from PIL import Image
import numpy as np
import cv2 as cv
import os
import base64

# Helper functions for RSA encryption and decryption remain the same
# ...
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def modular_multiplicative_inverse(a, b):
    def extended_gcd(aa, bb):
        last_remainder, remainder = abs(aa), abs(bb)
        x, last_x, y, last_y = 0, 1, 1, 0
        while remainder:
            last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
            x, last_x = last_x - quotient * x, x
            y, last_y = last_y - quotient * y, y
        return last_remainder, last_x * (-1 if aa < 0 else 1), last_y * (-1 if bb < 0 else 1)

    g, x, y = extended_gcd(a, b)
    if g != 1:
        raise ValueError(f"No modular inverse exists for a = {a} and b = {b}")
    return x % b

def encrypt_number(number, e, n):
    return pow(number, e, n)

def decrypt_number(encrypted_number, d, n):
    return pow(encrypted_number, d, n)

def encrypt_string(text, e, n):
    return [pow(ord(char), e, n) for char in text]

def decrypt_string(encrypted_chars, d, n):
    return ''.join(chr(pow(char, d, n)) for char in encrypted_chars)

def image_to_int_array(image_path):
    img = cv.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")
    b, g, r = cv.split(img)
    data = np.concatenate([b.flatten(), g.flatten(), r.flatten()])
    return data.astype(int), img.shape  # Ensure the data is in int format

def int_array_to_image(int_array, size, output_path):
    int_array = np.clip(int_array, 0, 255).astype(np.uint8)  # Clip values to prevent overflow/underflow
    channel_size = size[0] * size[1]
    b = int_array[:channel_size].reshape(size[:2])
    g = int_array[channel_size:2*channel_size].reshape(size[:2])
    r = int_array[2*channel_size:].reshape(size[:2])
    img = cv.merge((b, g, r))
    img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    img_pil.save(output_path)

def normalize_data(data):
    min_val = min(data)
    max_val = max(data)
    normalized_data = [int(255 * (x - min_val) / (max_val - min_val)) for x in data]
    return normalized_data

def download_button(file_path, label):
    with open(file_path, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{os.path.basename(file_path)}">{label}</a>'
        st.markdown(href, unsafe_allow_html=True)

def RSA_image_encryption_with_mersenne(image_path, p, q):
    r = 2**5 - 1  # Mersenne prime (31)
    img_data, img_shape = image_to_int_array(image_path)
    n = p * q * r
    o = (p - 1) * (q - 1) * (r - 1)
    e = 3
    while gcd(e, o) != 1:
        e += 2
    d = modular_multiplicative_inverse(e, o)
    encrypted_img_data = [pow(int(pixel), e, n) for pixel in img_data]
    normalized_encrypted_img_data = normalize_data(encrypted_img_data)
    encrypted_output_path = f"encrypted_images/encrypted_{os.path.basename(image_path)}"
    os.makedirs('encrypted_images', exist_ok=True)
    int_array_to_image(normalized_encrypted_img_data, img_shape, encrypted_output_path)
    return encrypted_output_path, encrypted_img_data, n, e, d

def RSA_image_decryption_with_mersenne(encrypted_image_path, encrypted_img_data, n, d):
    _, img_shape = image_to_int_array(encrypted_image_path)
    decrypted_img_data = np.array([pow(int(pixel), d, n) for pixel in encrypted_img_data], dtype=int)
    decrypted_img_data = np.clip(decrypted_img_data, 0, 255)
    decrypted_output_path = f"decrypted_images/decrypted_{os.path.basename(encrypted_image_path)}"
    os.makedirs('decrypted_images', exist_ok=True)
    int_array_to_image(decrypted_img_data, img_shape, decrypted_output_path)
    return decrypted_output_path

def main():
    st.title("RSA Encryption and Decryption App")

    # Displaying mode selection on the left side
    mode = st.sidebar.selectbox("Choose mode", ["encrypt", "decrypt"])

    if mode == 'encrypt':
        # Display p and q on the same line
        col1, col2 = st.columns(2)
        with col1:
            p = st.number_input("Enter prime number p", min_value=2, step=1, format="%d")
        with col2:
            q = st.number_input("Enter prime number q", min_value=2, step=1, format="%d")
        
        data_type = st.selectbox("Choose data type", ["number", "string", "file", "image"])

        if data_type == 'number':
            number = st.number_input("Enter the number to encrypt", step=1)
            if st.button("Encrypt"):
                r = 2**5 - 1
                n = p * q * r
                o = (p - 1) * (q - 1) * (r - 1)
                e = 3
                while gcd(e, o) != 1:
                    e += 2
                d = modular_multiplicative_inverse(e, o)
                encrypted_number = encrypt_number(number, e, n)
                st.success(f"Encrypted number: {encrypted_number}")
                st.info(f"Public Key (n, e): ({n}, {e}), Private Key (d): {d}")

        elif data_type == 'string':
            text = st.text_input("Enter the string to encrypt")
            if st.button("Encrypt"):
                r = 2**5 - 1
                n = p * q * r
                o = (p - 1) * (q - 1) * (r - 1)
                e = 3
                while gcd(e, o) != 1:
                    e += 2
                d = modular_multiplicative_inverse(e, o)
                encrypted_text = encrypt_string(text, e, n)
                st.success(f"Encrypted string (as integers): {encrypted_text}")
                st.info(f"Public Key (n, e): ({n}, {e}), Private Key (d): {d}")

        elif data_type == 'file':
            uploaded_file = st.file_uploader("Upload a text file", type="txt")
            if uploaded_file is not None:
                text = uploaded_file.getvalue().decode("utf-8")
                if st.button("Encrypt"):
                    r = 2**5 - 1
                    n = p * q * r
                    o = (p - 1) * (q - 1) * (r - 1)
                    e = 3
                    while gcd(e, o) != 1:
                        e += 2
                    d = modular_multiplicative_inverse(e, o)
                    encrypted_text = encrypt_string(text, e, n)
                    encrypted_file_path = "encrypted_text.txt"
                    with open(encrypted_file_path, 'w') as f:
                        f.write(','.join(map(str, encrypted_text)))
                    st.success("Encrypted file content saved.")
                    download_button(encrypted_file_path, "Download Encrypted File")
                    st.info(f"Public Key (n, e): ({n}, {e}), Private Key (d): {d}")

        elif data_type == 'image':
            uploaded_image = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
            if uploaded_image is not None:
                image_path = f"uploaded_images/{uploaded_image.name}"
                os.makedirs('uploaded_images', exist_ok=True)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                if st.button("Encrypt"):
                    encrypted_path, encrypted_img_data, n, e, d = RSA_image_encryption_with_mersenne(image_path, p, q)
                    st.success("Image encrypted and saved.")
                    st.image(encrypted_path, caption="Encrypted Image")
                    download_button(encrypted_path, "Download Encrypted Image")
                    st.info(f"Public Key (n, e): ({n}, {e}), Private Key (d): {d}")
                    st.session_state.encrypted_img_data = encrypted_img_data

    elif mode == 'decrypt':
        col1, col2 = st.columns(2)
        with col1:
            d = st.number_input("Enter the private key (d)", step=1)
        with col2:
            n = st.number_input("Enter the modulus (n)", step=1)

        data_type = st.selectbox("Choose data type", ["number", "string", "file", "image"])

        if data_type == 'number':
            encrypted_number = st.number_input("Enter the number to decrypt", step=1)
            if st.button("Decrypt"):
                decrypted_number = decrypt_number(encrypted_number, d, n)
                st.success(f"Decrypted number: {decrypted_number}")

        elif data_type == 'string':
            encrypted_text = st.text_area("Enter the encrypted text (comma-separated integers)")
            if st.button("Decrypt"):
                try:
                    encrypted_chars = list(map(int, encrypted_text.split(',')))
                    decrypted_text = decrypt_string(encrypted_chars, d, n)
                    st.success(f"Decrypted text: {decrypted_text}")
                except ValueError:
                    st.error("Invalid encrypted text format. Ensure integers are comma-separated.")

        elif data_type == 'file':
            encrypted_file = st.file_uploader("Upload the encrypted text file", type="txt")
            if encrypted_file is not None:
                encrypted_text = encrypted_file.getvalue().decode("utf-8")
                if st.button("Decrypt"):
                    try:
                        encrypted_chars = list(map(int, encrypted_text.split(',')))
                        decrypted_text = decrypt_string(encrypted_chars, d, n)
                        decrypted_file_path = "decrypted_text.txt"
                        with open(decrypted_file_path, 'w') as f:
                            f.write(decrypted_text)
                        st.success("Decrypted file content saved.")
                        download_button(decrypted_file_path, "Download Decrypted File")
                    except ValueError:
                        st.error("Invalid file content format. Ensure integers are comma-separated.")

        elif data_type == 'image':
            uploaded_encrypted_image = st.file_uploader("Upload the encrypted image file", type=["jpg", "jpeg", "png"])
            if uploaded_encrypted_image is not None:
                encrypted_image_path = f"uploaded_encrypted_images/{uploaded_encrypted_image.name}"
                os.makedirs('uploaded_encrypted_images', exist_ok=True)
                with open(encrypted_image_path, "wb") as f:
                    f.write(uploaded_encrypted_image.getbuffer())
                if st.button("Decrypt"):
                    if 'encrypted_img_data' in st.session_state:
                        encrypted_img_data = st.session_state.encrypted_img_data
                        decrypted_path = RSA_image_decryption_with_mersenne(encrypted_image_path, encrypted_img_data, n, d)
                        st.success("Image decrypted and saved.")
                        st.image(decrypted_path, caption="Decrypted Image")
                        download_button(decrypted_path, "Download Decrypted Image")
                    else:
                        st.error("Encrypted image data not found in session state. Please encrypt the image first.")

if __name__ == "__main__":
    main()
