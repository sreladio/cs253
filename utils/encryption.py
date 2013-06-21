from lib import bcrypt

def rot13(string_to_evaluate):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    str_ro = ''

    for i in string_to_evaluate:
      if i.lower() in alphabet:
        for j in range(0, len(alphabet)):
          if i == alphabet[j]:
            str_ro += alphabet[(13 + j) % len(alphabet)]
            
          elif i == alphabet[j].upper():
            str_ro += alphabet[(13 + j) % len(alphabet)].upper()
      else:
        str_ro += i

    return str_ro

def hash(value):
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(str(value), salt)

def valid_hash(value, hashed):
  return bcrypt.hashpw(value, hashed) == hashed