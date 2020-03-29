import time
def intro():
  print("Welcome to my own password Encrypter/Decrypter!  Which action would you like to take?")
  print("+=====================================+")
  print("1: Encrypt a password")
  print("2: Decrypt a previously encrypted password")
  print("+=====================================+")

  choice = ''
  while(choice != 1 and choice != 2):
    choice = int(input("(Enter a 1 or 2): "))
    if (choice !=1 and choice != 2):
      print("\n Please enter only 1 and 2")

  if choice == 1:
    print("Action Selected: Encryption")
    print("+=====================================+")
    encrypt()
  elif choice == 2:
    print("+=====================================+")
    print("Action Selected: Decryption")
    decrypt()
  else:
    print("Invalid input, please enter 1 or 2")

def encrypt():
  print("Please enter a password to be Encrypted")
  password = input("\nPassword: ")
  print("Okay! I will encrypt the password: " + password + " for you.")
  time.sleep(1)
  print("Encrypting........")
  time.sleep(1)


  ASCII_list = []
  for i in range(len(password)):
    ASCII_list.append(ord(password[i]))
 # print(ASCII_list)

  shifted_list = []
  for i in range(len(ASCII_list)):
    shifted_list.append(ASCII_list[i]+4)
 # print(shifted_list)
  
  encrypted_list = [] 
  for i in range(len(shifted_list)):
    encrypted_list.append(chr(shifted_list[i]))
 # print(encrypted_list)

  encrypted_string = ''.join(encrypted_list)
 # print(encrypted_string)
  encrypt2(encrypted_string,password)


def encrypt2(encrypted_string,password):
  
  reverse_encrypted_string = ""
  for i in range(len(encrypted_string)):
    reverse_encrypted_string = encrypted_string[i] + reverse_encrypted_string
  
  # print(reverse_encrypted_string)

  encrypted_final = reverse_encrypted_string + encrypted_string + reverse_encrypted_string
  print("+======================================+")
  print("Original Password: " + password) 
  print("Encrypted Password: " + encrypted_final)
  print("+======================================+")

  print("Please copy your Encrypted password: " + encrypted_final) 
  print("\nNOTE: Rerun the program and paste this Encryption into 'Decrypt a previously encrypted password'")

  print("\nWould you like to save your encryption to passwords.txt?")
  print("1: Yes")
  print("2: No")

  choice = ''
  while(choice != 1 and choice != 2):
    choice = int(input("(Enter a 1 or 2): "))
    if (choice !=1 and choice != 2):
      print("\n Please enter only 1 and 2")

  if choice == 1:
    print("\n\nAction Selected: Save Encryption")
    print("+=====================================+")
    encryptSave(encrypted_final,password)
  elif choice == 2:
    print("+=====================================+")
    print("Okay! see you next time.")



def encryptSave(encrypted_final,password):
  
  choice = input("What is the password for: ")
  time.sleep(1)
  print("\nOkay, now saving you decrypted passcode " + encrypted_final + " into passwords.txt. ")
  time.sleep(2)
  print("Saving....")

  f = open("passwords.txt", "a+")
  f.write(choice + " |")
  f.write(" Encrypted Password" + ": " + encrypted_final + " |")
  f.write("\n")
  f.close()

  time.sleep(2)
  print("\nSuccessfully logged entry for " + encrypted_final + ". Please check passwords.txt") 

    

def decrypt():
  print("Please enter an Encrypted password for Decryption")
  print("(this only works for already encrypted passwords from this program)")
  password = input("\nPassword: ")
  print("Okay! I will decrypt the password " + password + " for you.")
  time.sleep(1)
  print("Decrypting........")
  time.sleep(1)

  encrypted_reduced = password[0:len(password)//3]
 # print(encrypted_reduced)
  encrypted_reversed = encrypted_reduced[::-1]
  #print(encrypted_reversed)

  decrypt2(encrypted_reversed,password)

def decrypt2(encrypted_reversed,password):
  
  ASCII_list = []
  for i in range(len(encrypted_reversed)):
    ASCII_list.append(ord(encrypted_reversed[i]))
  #print(ASCII_list)

  shifted_list = []
  for i in range(len(ASCII_list)):
      shifted_list.append(ASCII_list[i]-4)
  #print(shifted_list)
  
  decrypted_list = [] 
  for i in range(len(shifted_list)):
    decrypted_list.append(chr(shifted_list[i]))
  
  

  #print(decrypted_list)

  decrypted_string = ''.join(decrypted_list)
  print("+======================================+")
  print("Original Password: " + password) 
  print("Decrypted Password: " + decrypted_string)
  print("+======================================+")

  print("Would you like to save your decryption to passwords.txt?")
  print("1: Yes")
  print("2: No")

  choice = ''
  while(choice != 1 and choice != 2):
    choice = int(input("(Enter a 1 or 2): "))
    if (choice !=1 and choice != 2):
      print("\n Please enter only 1 and 2")

  if choice == 1:
    print("\n\nAction Selected: Save Decryption")
    print("+=====================================+")
    decryptSave(decrypted_string)
  elif choice == 2:
    print("+=====================================+")
    print("Okay! see you next time.")
  
  else:
    print("Invalid input, please enter 1 or 2")

def decryptSave(decrypted_string):
  
  choice = input("What is the password for: ")
  time.sleep(1)
  print("\nOkay, now saving your decrypted passcode " + decrypted_string + " into passwords.txt. ")
  time.sleep(2)
  print("Saving....")

  f = open("passwords.txt", "a+")
  f.write(choice + " |")
  f.write(" Decrypted Password" + ": " + decrypted_string + " |")
  f.write("\n")
  f.close()

  time.sleep(2)
  print("\nSuccessfully logged entry for " + decrypted_string + ". Please check passwords.txt") 

intro()
