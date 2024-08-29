
from Crypto.PublicKey import RSA

# Generate ECC key pair for server
private_key = RSA.generate(1024)
public_key = private_key.public_key()

# Convert keys to bytes for transmission or storage
private_key_export = private_key.export_key().decode()
public_key_export = public_key.export_key().decode()

with open('private_key.pem', 'w') as pr:
    pr.write(private_key_export)
with open('public_key.pem', 'w') as pu:
    pu.write(public_key_export)

private_key = RSA.import_key(open('private_key.pem', 'r').read())
public_key = RSA.import_key(open('public_key.pem', 'r').read())

# Print or store keys as needed
print("Private Key:\n", private_key)
print("Public Key:\n", public_key)