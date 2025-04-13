# 🔐 RSA Encryption & Decryption App (with Mersenne Prime Enhancement)

This Streamlit-based web application allows users to **encrypt and decrypt** various types of data — **numbers, strings, text files, and images** — using an **enhanced RSA algorithm** that incorporates a **fixed Mersenne prime** (`r = 2^5 - 1 = 31`) in the key generation process for added complexity and uniqueness.

---

## ✨ Features

- ✅ Encrypt/Decrypt:
  - Numbers
  - Strings
  - Text Files
  - Images
- 🔐 RSA implementation using **three primes (p, q, r)**, where `r` is a fixed **Mersenne prime**
- 💾 Download encrypted and decrypted files/images
- 📷 Image encryption shows processed output visually
- 🔍 Normalization to maintain image fidelity after encryption

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rsa-mersenne-streamlit.git
cd rsa-mersenne-streamlit
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**

- `streamlit`
- `opencv-python`
- `numpy`
- `Pillow`

Or manually install:

```bash
pip install streamlit opencv-python numpy Pillow
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
rsa-mersenne-streamlit/
│
├── app.py                      # Main Streamlit app
├── encrypted_images/          # Auto-created folder for encrypted image outputs
├── decrypted_images/          # Auto-created folder for decrypted image outputs
├── uploaded_images/           # Stores uploaded original images
├── encrypted_text.txt         # Saved encrypted text file (temporary)
├── decrypted_text.txt         # Saved decrypted text file (temporary)
├── README.md                  # You're here!
└── requirements.txt           # Python dependencies
```

---

## 🛡️ How It Works

### Key Generation

- Input primes: `p`, `q`
- Fixed prime: `r = 31` (Mersenne prime)
- `n = p * q * r`  
- `φ(n) = (p-1)*(q-1)*(r-1)`
- Public exponent `e` is chosen such that `gcd(e, φ(n)) = 1`
- Private key `d = modular_inverse(e, φ(n))`

### Encryption & Decryption

- **Number**: `cipher = (number ^ e) mod n`
- **String**: Each character is encrypted individually using the above formula
- **File**: Content is treated as string
- **Image**:
  - Image is converted to BGR channels and flattened
  - Each pixel is encrypted
  - Encrypted values normalized and reconstructed into an image

---

## 🧪 Sample Use Cases

- 📁 Encrypt secret text files before sharing
- 👁️‍🗨️ Demonstrate secure image transmission
- 🛠️ Educational purpose for learning RSA encryption with twist

---

## ⚠️ Notes

- This tool is **not intended for production**-level security; it is an educational implementation.
- For best performance, use small to medium-size images (JPEG/PNG).
- Ensure the primes `p` and `q` are **distinct and large enough** to enhance security.

---

## 🧑‍💻 Author

Developed by **[Raman Pradhan]**

Feel free to connect and contribute!

---


