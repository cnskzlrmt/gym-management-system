import bcrypt

plain_password = "cansu123"  # Kullanıcının düz metin şifresi
hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
