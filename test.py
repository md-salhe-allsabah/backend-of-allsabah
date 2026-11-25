from db.crud import get_hashed_password_of_user
from utilities.password_manager import *

password = 'shubham&shruti'

shruti_password = get_hashed_password_of_user(5)

check = check_password(hashed_password=shruti_password, plain_password=password)

print(check)