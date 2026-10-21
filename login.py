
import re

STORAGE_FILE = "storage.txt"


def read_logins():
    logins = {}

    try:
        with open(STORAGE_FILE, "r") as f:
            for line in f:
                username, password = line.rstrip("\n").split(",", 1)
                logins[username] = password
    except FileNotFoundError:
        pass

    return logins


def valid_username(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{4,20}", username))


def valid_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )


def register(username, password):
    if not valid_username(username):
        return False, "Invalid username"

    if not valid_password(password):
        return False, "Invalid password"

    logins = read_logins()

    if username in logins:
        return False, "Username already exists"

    with open(STORAGE_FILE, "a") as f:
        f.write(f"{username},{password}\n")

    return True, "Account created"


def login(username, password):
    logins = read_logins()

    if username in logins and logins[username] == password:
        return True, "Login successful"

    return False, "Invalid username or password"


if __name__ == "__main__":
    choice = input("1. Register\n2. Login\nChoose: ")
    username = input("Username: ")
    password = input("Password: ")

    if choice == "1":
        success, message = register(username, password)
    elif choice == "2":
        success, message = login(username, password)
    else:
        success, message = False, "Invalid choice"

    print(message)
