from django.contrib.auth.hashers import check_password

hashed_password="pbkdf2_sha256$1000000$3AcYaMdadACycCoOPo9g6B$earGFtsr72+zLsOxa0JYPzFHP8j0jf+t1II+fgyMTNk="
plain_password='hello@123'
if check_password(plain_password,hashed_password):
    print(True)
else:
    print(False)
