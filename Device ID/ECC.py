
from Crypto.PublicKey import ECC

# Generate ECC key pair for server
private_key_server = ECC.generate(curve='P-256')
public_key_server = private_key_server.public_key()

# Generate ECC key pair for client (for demonstration)
private_key_client = ECC.generate(curve='P-256')
public_key_client = private_key_client.public_key()

# Convert keys to bytes for transmission or storage
private_key_server_bytes = private_key_server.export_key(format='PEM')
public_key_server_bytes = public_key_server.export_key(format='PEM')

private_key_client_bytes = private_key_client.export_key(format='PEM')
public_key_client_bytes = public_key_client.export_key(format='PEM')

with open('private_key_server.pem', 'w') as pr_s:
    pr_s.write(private_key_server_bytes)
with open('public_key_server.pem', 'w') as pu_s:
    pu_s.write(public_key_server_bytes)
with open('private_key_client.pem', 'w') as pr_c:
    pr_c.write(private_key_client_bytes)
with open('public_key_client.pem', 'w') as pu_c:
    pu_c.write(public_key_client_bytes)

private_key_s = ECC.import_key(open('private_key_server.pem', 'r').read())
public_key_s = ECC.import_key(open('public_key_server.pem', 'r').read())
private_key_c = ECC.import_key(open('private_key_client.pem', 'r').read())
public_key_c = ECC.import_key(open('public_key_client.pem', 'r').read())

# Print or store keys as needed
print("Server Private Key:\n", private_key_s)
print("Server Public Key:\n", public_key_s)

print("Client Private Key:\n", private_key_c)
print("Client Public Key:\n", public_key_c)