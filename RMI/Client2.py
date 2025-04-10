# import library
import socket
from colorama import Fore
from tkinter import *
from functools import partial


# creating a client class
class client():
    def __init__(self, name , password):
        self.name = name
        self.password = password
        self.rented_list = []

    def get_value(self):
        return self.name, self.password


all_cars_in_company = [' Mitsubishi Outlander 2022 | Mitsubishi',
 ' Mustang EcoBoost Convertible 2022 | Ford', ' Audi E-tron GT 2022 | Audi',
 ' BMW 3-Series 2022 | BMW', ' Mercedes-Benz C-Class 2022 | Mercedes-Benz',
 ' Jaguar F-Type P450 Coupe 2022 | Jaguar',
 ' Mazda CX-5 2022 | Mazda',
 ' Volvo XC90 2022 | Volvo']


user = ""
passw = ""
def validate_login(username, password):
    global user, passw
    print(Fore.BLUE + "\nWe are going to verify your account ... ")
    # a list of items
    user = username.get()
    passw = password.get()
    tkWindow.destroy()
    return


#network configuration (socket_family, socket_type)
client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostname()
port = 50000

try:
    client_connection.connect((ip, port))
except:
    print("A problem occurred during binding!")


# opening
response = client_connection.recv(1024)
print(response.decode("utf-8"))


#window GUI interface
tkWindow = Tk()
tkWindow.geometry('275x75+550+300')
tkWindow.title('Login to account')
usernameLabel = Label(tkWindow, text="User name").grid(row=1, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=1, column=1)
passwordLabel = Label(tkWindow,text="Password").grid(row=2, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=2, column=1)
validate_login = partial(validate_login, username, password)
loginButton = Button(tkWindow, text="Login", command=validate_login).grid(row=3, column=1)
tkWindow.mainloop()


# sending user & passw to server for login
check = user + " " + passw
client_connection.send(str.encode(check))


response = client_connection.recv(1024)
response = response.decode("utf-8")


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


# display menu for client
if response == "yes":
    print(Fore.GREEN + "\nAuthentication Successful!")
    print(Fore.BLUE + "\nCurrently User Login: ", user)
    print(Fore.CYAN + """\n                      ********** COMPANY MENU **********
                      1. Display all available cars in company
                      2. Request for car rental
                      3. Returning the rented car
                      4. Exit""")

    while True:
        Input = input(Fore.BLUE + "\nEnter Choice: ")
        print("\n")

        while ( not Input.isnumeric()):
            Input = input("Please enter a number!: ")
       
        if int(Input) == 1:
            client_connection.send(str.encode(Input))
            response = client_connection.recv(1024)
            response = response.decode("UTF-8")
            responses = response.split('#')
            i = 1
            
            for item in responses:
                if i > 2:
                    print("     ", i - 2, "- ",item)
               
                else:
                    print("     ", item)
                i += 1
       
        elif int(Input) == 2:
            client_connection.send(str.encode(Input))
            response = client_connection.recv(1024)
            response = response.decode("UTF-8")
            print(Fore.BLUE + "\nEnter the name of the car you'd like to rent: ")
            car = input()
            print(Fore.BLUE + "\nEnter the name of the manufacturer: ")
            manufacturer = input()
            request_car = car + "#" + manufacturer
            client_connection.send(str.encode(request_car))
            response = client_connection.recv(1024)
            response = response.decode("UTF-8")
            print(Fore.GREEN + response)
       
        elif int(Input) == 3:
            client_connection.send(str.encode(Input))
            response = client_connection.recv(1024)
            response = response.decode("UTF-8")
           
            if "#" in response:
                responses = response.split('#')
                index = 1
                
                for car in responses:
                    if index == 1 or index == 2:
                        print("     ", car)
                        index += 1
                   
                    else:
                        print("     ", index - 2, "- ", car)
                        index += 1
                print("\nEnter the desired car number in range of 1 to ", index - 3, " : ")
                car_num = input()
               
                while (int(car_num) > index - 1 or int(car_num) < 0):
                    print("Enter the desired car number in range of 1 to ", index - 1, " : ")
                    car_num = input()
                add_index = int(car_num) - 1
                add_index_final = str(add_index)
                client_connection.send(str.encode(add_index_final))
                response = client_connection.recv(1024)
                response = response.decode("UTF-8")
                print(Fore.GREEN + response)
           
            else:
                print(Fore.GREEN + response)
                client_connection.send(str.encode("END"))
        
        
        elif int(Input) == 4:
            print(Fore.RED + "Connection terminated. ")
            client_connection.close()
            break

else:
    print(Fore.RED + "Authentication unsuccessful")
