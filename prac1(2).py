import hashlib
import uuid
import os

if not os.path.exists("users.txt"):
    with open("users.txt", "w") as f:
        pass


def register():
    while True:
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        role = input("Введите вашу роль (Администратор/Продавец/Покупатель): ")
        salt = uuid.uuid4().hex
        hash_password = hashlib.sha256(password.encode() + salt.encode())
        hashed_password = hash_password.hexdigest()
        with open("users.txt", "a") as f:
            f.write(f"{username} {hashed_password} {salt} {role}\n")
        print("Регистрация прошла успешно.")
        break


def login():
    while True:
        print("Выберите действие:")
        print("1 - Вход")
        print("2 - Регистрация")
        choice = input("Введите номер действия: ")
        if choice == "1":
            username = input("Введите логин: ")
            password = input("Введите пароль: ")
            with open("users.txt", "r") as f:
                for line in f:
                    fields = line.split()
                    if fields[0] == username:
                        salt = fields[2]
                        hash_password = hashlib.sha256(password.encode() + salt.encode())
                        if hash_password.hexdigest() == fields[1]:
                            role = fields[3]
                            if role == "Администратор":
                                admin_panel()
                            elif role == "Продавец":
                                seller_panel()
                            else:
                                buyer_panel()
                            return
                print("Неправильный логин или пароль. Попробуйте еще раз.")
        elif choice == "2":
            register()
        else:
            print("Неверный ввод. Попробуйте еще раз.")


def admin_panel():
    print("Добро пожаловать в личный кабинет администратора.")
    print("Список всех пользователей:")
    with open("users.txt", "r") as f:
        for line in f:
            fields = line.split()
            print(f"Логин: {fields[0]}, Роль: {fields[3]}")
    change_password()


def seller_panel():
    print("Добро пожаловать в личный кабинет продавца.")
    print("Скоро здесь появится функционал для данной роли пользователя.")


def buyer_panel():
    print("Добро пожаловать в личный кабинет покупателя.")
    print("Скоро здесь появится функционал для данной роли пользователя.")


def change_password():
    while True:
        username = input("Введите логин пользователя, у которого нужно изменить пароль: ")
        with open("users.txt", "r") as f:
            lines = f.readlines()
        found = False
        with open("users.txt", "w") as f:
            for line in lines:
                fields = line.split()
                if fields[0] == username:
                    found = True
                    new_password = input("Введите новый пароль: ")
                    salt = uuid.uuid4().hex
                    hash_password = hashlib.sha256(new_password.encode() + salt.encode())
                    hashed_password = hash_password.hexdigest()
                    f.write(f"{fields[0]} {hashed_password} {salt} {fields[3]}\n")
                    print("Пароль изменен.")
                else:
                    f.write(line)
        if not found:
            print("Пользователь с таким логином не найден")


login()

