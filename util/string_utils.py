
from random import choices
import string

def generate_random_string(length=10):
        return ''.join(choices(string.ascii_letters + string.digits, k=length))
