# passwordmanager
Password manager using Fernet encryption for encrypting and decrypting passwords
Standard Libraries Used:
os: For file handling and checking file existence.
json: To store and retrieve password data in a structured format (JSON).
random and string: To generate random passwords.
hashlib: To hash the master password securely using the SHA-256 algorithm.

cryptography Library:
Specifically, Fernet encryption is used for encrypting and decrypting passwords. Fernet ensures:
Symmetric encryption (AES-128 in GCM mode).
Message integrity checks to prevent tampering.
Base64 encoding of encrypted data for safe storage.
