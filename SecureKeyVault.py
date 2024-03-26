import pandas as pd
import os
import os.path
from pwinput import pwinput
import string
import tabulate
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

ALPHABET = string.ascii_letters + string.digits

os.system('color')


class textcolor:
    TITLE = '\033[31m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def clear():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')


def get_master_password():
    master_pass = pwinput(prompt="\n Enter master password: ", mask="*")

    processed_password = ""
    for char in master_pass:
        if char.isalpha():
            processed_password += str(ord(char.lower()) - 96)
        else:
            processed_password += char

    master_pass = int(processed_password.replace("-", ""))

    return master_pass


def encrypt(password, master_pass):
    encrypted_password = ""

    for char in password:
        if char in ALPHABET:
            new_pos = (ALPHABET.find(char) + master_pass) % len(ALPHABET)
            encrypted_password += ALPHABET[new_pos]
        else:
            encrypted_password += char

    return encrypted_password


def decrypt(encrypted_password, master_pass):
    decrypted_password = ""

    for char in encrypted_password:
        if char in ALPHABET:
            new_pos = (ALPHABET.find(char) - master_pass) % len(ALPHABET)
            decrypted_password += ALPHABET[new_pos]
        else:
            decrypted_password += char

    return decrypted_password


def create_csv():
    data = {'Url/App name': [], 'Username': [], 'Password': []}
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)


def add(name, encrypted_pass, url):
    user_data = {'Url/App name': [url], 'Username': [name],
                 'Password': [encrypted_pass]}

    df = pd.DataFrame(user_data)
    df.to_csv('data.csv', mode='a', header=False, index=False)

    print(textcolor.OKGREEN + '\n' * 2 + ' ADDED SUCCESSFULLY' + textcolor.ENDC)


def search(url=''):
    df = pd.read_csv('data.csv')

    dfS = df[df['Url/App name'].str.contains(url, na=False,
                                             case=False)]
    index_d = dfS.index.values

    password = []
    dfS = dfS.reset_index()

    for index, row in dfS.iterrows():
        find_password = dfS.loc[index, 'Password']
        dec_password = decrypt(find_password, master_password)
        password.append(dec_password)

    dfS = dfS.set_index(index_d)
    dfS['Password'] = password

    return dfS


def edit(index, new_name, new_password):
    df = pd.read_csv("data.csv")

    # Edit row at given 'index'

    df.loc[index, ['Username', 'Password']] = [new_name, new_password]
    df.to_csv('data.csv', index=False)

    print(textcolor.OKGREEN + '\n' * 2 + ' EDITED SUCCESSFULLY' + textcolor.ENDC)


def delete(index):
    df = pd.read_csv("data.csv")

    df.drop([index], axis=0, inplace=True)
    df.to_csv('data.csv', index=False)

    print(textcolor.OKGREEN + '\n' * 2 + ' DELETED SUCCESSFULLY' + textcolor.ENDC)


def backup():
    df = pd.read_csv("data.csv")
    dp = os.getcwd()
    os.chdir("..")
    cp = os.getcwd()
    print(cp)
    cp = cp + "\\SecureKeyVault\\data.csv"

    if not os.path.isdir('SecureKeyVault_Backup'):
        os.makedirs('SecureKeyVault_Backup')

    df.to_csv(cp, index=False)
    os.chdir(dp)


print(textcolor.TITLE + """\n

╔══╗╔═══╗╔══╗╔╗╔╗╔═══╗╔═══╗╔╗╔══╗╔═══╗╔╗╔╗───╔╗╔╗╔══╗╔╗╔╗╔╗──╔════╗
║╔═╝║╔══╝║╔═╝║║║║║╔═╗║║╔══╝║║║╔═╝║╔══╝║║║║───║║║║║╔╗║║║║║║║──╚═╗╔═╝
║╚═╗║╚══╗║║──║║║║║╚═╝║║╚══╗║╚╝║──║╚══╗║╚╝║───║║║║║╚╝║║║║║║║────║║──
╚═╗║║╔══╝║║──║║║║║╔╗╔╝║╔══╝║╔╗║──║╔══╝╚═╗║───║╚╝║║╔╗║║║║║║║────║║──
╔═╝║║╚══╗║╚═╗║╚╝║║║║║─║╚══╗║║║╚═╗║╚══╗─╔╝║───╚╗╔╝║║║║║╚╝║║╚═╗──║║──
╚══╝╚═══╝╚══╝╚══╝╚╝╚╝─╚═══╝╚╝╚══╝╚═══╝─╚═╝────╚╝─╚╝╚╝╚══╝╚══╝──╚╝──
   


""" + textcolor.ENDC)

data_file = os.path.isfile('data.csv')

if not data_file:
    create_csv()

    print(textcolor.BOLD + "\n WELCOME TO MY PASSWORD MANAGER" + textcolor.ENDC)

    print("\n THIS APPLICATION USES A MASTER PASSWORD\
           \n TO ENCRYPT & DECRYPT YOUR DATA.\
           \n USE ANY ALPHANUMERIC PASSWORD (RECOMMENDED)\
           \n AND REMEMBER THAT.\
           \n\n WARNING: IF YOU LOSE YOUR MASTER PASSWORD, THEN YOU\
           \n WILL NOT BE ABLE TO RECOVER YOUR SAVED PASSWORDS.")

print('\n\n NOTE: MASTER PASSWORD IS A USER DEFINED VALUE\
       \n NEEDED TO ENCRYPT & DECRYPT DATA CORRECTLY.')

while True:

    try:

        master_password = get_master_password()
        break

    except:
        print(textcolor.WARNING + '\n WARNING: MASTER PASSWORD CONSISTS OF LETTERS & NUMBERS ONLY.' + textcolor.ENDC)

while True:

    try:

        clear()

        print(textcolor.BOLD + "\n" + " " * 50 + "MENU" + textcolor.ENDC)

        print("\n" * 3 + " [01] ADD NEW CREDENTIAL\
            \n\n [02] SEARCH CREDENTIAL\
            \n\n [03] EDIT CREDENTIAL\
            \n\n [04] DELETE CREDENTIAL")

        menu_option = int(input("\n" * 3 + " SELECT AN OPTION & PRESS ENTER : "))

        if menu_option == 1:

            clear()

            print(textcolor.BOLD + "\n" * 2, "ADD NEW CREDENTIAL\n" + textcolor.ENDC)
            name = input("\n ENTER NAME/USERNAME, YOU WANT TO SAVE: ")
            password = pwinput(prompt="\n ENTER PASSWORD, YOU WANT TO SAVE: ", mask="*")
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO SAVE: ")

            if name == '':
                name = 'UNAVAILABLE'
            if password == '':
                password = 'UNAVAILABLE'
            if url == '':
                while url == '':
                    print(textcolor.WARNING + '\n WARNING: PLEASE ENTER A URL OR APP NAME: ' + textcolor.ENDC)
                    url = input("\n ENTER URL OR APP NAME, YOU WANT TO SAVE: ")

            encrypted_pass = encrypt(password, master_password)
            add(name, encrypted_pass, url)

        elif menu_option == 2:

            clear()

            print(textcolor.BOLD + "\n" * 2, "SEARCH CREDENTIAL \n" + textcolor.ENDC)
            print("\n [01] SEE A SPECIFIC SAVED CREDENTIAL\
                      \n\n [02] SEE ALL SAVED CREDENTIALS")
            sub_option = int(input("\n" * 3 + " SELECT AN OPTION & PRESS ENTER : "))

            if sub_option == 1:
                url = input("\n ENTER URL OR APP NAME, YOU WANT TO SEARCH: ")
                show_result = search(url)
                show_in_md = show_result.to_markdown(tablefmt="orgtbl",
                                                     index=False)
                print('\n')
                print(show_in_md)

            if sub_option == 2:
                show_result = search()
                show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)
                print('\n')
                print(show_in_md)

        elif menu_option == 3:

            clear()

            print(textcolor.BOLD + "\n" * 2, "EDIT CREDENTIAL" + textcolor.ENDC)
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO EDIT: ")

            show_result = search(url)
            show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)
            print('\n')
            print(show_in_md)
            print('\n' * 2)

            if len(show_result) > 1:
                index = int(input("\n SELECT AN INDEX VALUE & PRESS ENTER : "))
            else:
                index = show_result.index.values
                index = int(index)

            new_name = input("\n ENTER NEW NAME/USERNAME: ")
            new_password = pwinput(prompt="\n ENTER NEW PASSWORD : ", mask="*")

            # Exception----------------------

            if new_name == '':
                old_name = show_result.loc[index, 'Username']
                new_name = old_name

            if new_password == '':
                old_password = show_result.loc[index, 'Password']
                new_password = old_password

            new_password = encrypt(new_password, master_password)
            edit(index, new_name, new_password)

        elif menu_option == 4:

            clear()

            print(textcolor.BOLD + "\n" * 2, "DELETE CRDENTIAL \n" + textcolor.ENDC)
            url = input("\n ENTER URL OR APP NAME, YOU WANT TO DELETE: ")

            show_result = search(url)  # call fun, to show respective data related to url
            show_in_md = show_result.to_markdown(tablefmt="orgtbl", index=False)
            print('\n')
            print(show_in_md)
            print('\n' * 2)

            if len(show_result) > 1:
                index = int(input("\n SELECT AN INDEX VALUE & PRESS ENTER : "))
            else:
                index = show_result.index.values
                index = int(index)

            confirm = input("\n DO YOU WANT TO CONTINUE, ENTER [Y/N] : ")

            if confirm == 'y' or confirm == 'Y':
                delete(index)

        print("\n" * 2)
        Continue = input("\n PRESS ENTER TO 'OK' ")
        backup()

    except:
        print(textcolor.FAIL + '\n ERROR: NOT FOUND !' + textcolor.ENDC)
        print("\n" * 2)
        Continue = input("\n PRESS ENTER TO 'OK' ")
        continue
