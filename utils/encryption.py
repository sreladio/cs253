from py_bcrypt import bcrypt

def rot13(string_to_evaluate):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    s = ''

    for i in string_to_evaluate:
      if i.lower() in alphabet:
        for j in range(0, len(alphabet)):
          if i == alphabet[j]:
            s += alphabet[(13 + j) % len(alphabet)]
            
          elif i == alphabet[j].upper():
            s += alphabet[(13 + j) % len(alphabet)].upper()
      else:
        s += i

    return s

def hash(value):
  salt = bcrypt.gensalt()
  return bcrypt.hashpw(str(value), salt)

def valid_hash(value, hashed):
  return bcrypt.hashpw(value, hashed) == hashed