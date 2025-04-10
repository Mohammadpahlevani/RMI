# import library
import socket
from _thread import *
from colorama import Fore


# network configuration (socket_family, socket_type)
server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostname()
port = 50000
thread_count = 0


# creating a car rental services
class company():   
    def __init__(self, list_of_cars):
        self.available_cars = list_of_cars

    def display_available_cars(self):
        print(Fore.GREEN + "The cars we have in our company are as follows: ")
        print(Fore.GREEN + "*************************************************")
        send_data = "The cars we have in our company are as follows:#*************************************************"
        for car in self.available_cars:
            print(car)
            send_data = send_data + "# " + car[0] + " ---> " + car[1]
        return send_data

    def current_cars(self):
        value = ""
        for x in self.available_cars:
            value = value + "#" + x[0] + x[1]
        return value

    def add_car(self, client):
        print("Current user info: ",client.get_value())
        pm = "\nThe list of cars that you have already rented:#"
        print("Length of array is: ", len(client.get_array()))
        if len(client.get_array()) > 0:
            index = 1
            for car in client.get_array():
                pm = pm + "# " + car[0] + " ---> " + car[1]
                print(index, "- ", car)
                index += 1
            return pm
        else:
            print(Fore.GREEN + "\n \nYou have not rented any cars from the company.\n"
                  "and thereFore it is not possible to provide services to you in this section.\n")

            pm = "You have not rented any cars from the company.\nand thereFore it is not possible to provide services to you in this section.\n"
            return pm

    def client_and_company_array_handler(self, index , client):
        print ("Index is: ", index)
        print("Inside of index: ", client.get_array_value(index))
        new_car, new_manufacturer  = client.get_array_value(index)
        self.available_cars.append((new_car ,new_manufacturer))
        client.del_b_car(index)
        pm = Fore.GREEN + "\nThanks for returning your rented car"
        return pm

    def lend_car(self, requested_car, requested_car_manufacturer, client_array):
        if (requested_car, requested_car_manufacturer) in self.available_cars:
            print(Fore.GREEN + "\nThe car you requested was rented")
            pm = "\nThe car you requested was rented"
            self.available_cars.remove((requested_car, requested_car_manufacturer))
            client_array.append((requested_car, requested_car_manufacturer))
        else:
            print("\nSorry the car you have requested is currently not in the company")
            pm = "Sorry the car you have requested is currently not in the company"
        return pm


class client:
    def __init__(self, name , password):
        self.name = name
        self.password = password
        self.rented_list = []

    def get_value(self):
        return self.name, self.password

    def get_value_to_migrate(self):
        return self.name + "$" + self.password

    def get_array(self):
        return self.rented_list

    def get_array_value(self,index):
        return self.rented_list[index]

    def del_b_car(self, index):
        del self.rented_list[index]

    def request_car(self):
        print(Fore.GREEN + "Enter the name of the car you'd like to rent: ")
        self.car = input()
        print(Fore.BLUE + "Enter the name of the manufacturer: ")
        self.manufacturer = input()
        return self.car, self.manufacturer

    def return_car(self):
        print(Fore.GREEN + "Enter the name of the car you'd like to return: ")
        self.car = input()
        return self.car


def array_navigation(array , value1 , value2):
    index = 0
    for valid_client in array:
        temp1,temp2 = valid_client.get_value()
        if ( temp1 == value1 and temp2 == value2):
            return index
        index += 1
    return -1


Company = company([("Mitsubishi Outlander 2022", "Mitsubishi"),
                       ("Mustang EcoBoost Convertible 2022", "Ford"),
                       ("Audi E-tron GT 2022", "Audi"),
                       ("BMW 3-Series 2022", "BMW"),
                       ("Mercedes-Benz C-Class 2022", "Mercedes-Benz"),
                       ("Jaguar F-Type P450 Coupe 2022", "Jaguar"),
			           ("Mazda CX-5 2022", "Mazda"),
			           ("Volvo XC90 2022", "Volvo")])


try:
    server_connection.bind((ip, port))
except:
    print("A problem occurred during binding!")


# security implementation
client1 = client("Emma","1111")
client2 = client("William" , "2222")
client3 = client("Sophia" , "3333")
client4 = client("David" ,"4444")
client5 = client("Isabella" ,"5555")
client6 = client("Matthew" ,"6666")
security_array = [client1 , client2, client3, client4, client5, client6]


print(Fore.GREEN + "\nHello!!!\nServer is ready!\nWaiting for clients ...\n")


def client_thread(connection):
    connection.send(str.encode(Fore.GREEN + "\nWelcome to the Company\nplease Enter your information"))
    check = connection.recv(2048)
    check = check.decode("UTF-8")
    check_array = check.split()
    login_check = array_navigation(security_array, check_array[0],check_array[1])
    
    if login_check != -1:
        print(Fore.GREEN + "\nAuthentication Successful!\n")
        print(Fore.BLUE + "Current user info is: " , security_array[login_check].get_value())
        connection.sendall(str.encode("yes"))
        
        while True:
            data = connection.recv(2048)
            data = data.decode("UTF-8")
            choice = int(data)
            print("Choose is: " , choice)
            
            if  choice == 1:
                data = Company.display_available_cars()
                connection.sendall(str.encode(data))
            
            elif choice == 2:
                connection.sendall(str.encode("send info"))
                data = connection.recv(2048)
                data = data.decode("UTF-8")
                data_aray = data.split("#")
                arg1 = data_aray[0]
                arg2 = data_aray[1]
                print("Current user is: ", security_array[login_check].get_value())
                print("Before ---> Current user array is: ", security_array[login_check].get_array())
                data = Company.lend_car(arg1, arg2, security_array[login_check].get_array())
                print("After -----> Current user array is: ", security_array[login_check].get_array())
                connection.sendall(str.encode(data))
           
            elif choice == 3:
                print("Login_Check: ", login_check)
                print("Info: ", security_array[login_check].get_value())
                message = Company.add_car(security_array[login_check])
                print("\nmessage is: " , message)
                connection.sendall(str.encode(message))
                return_car = connection.recv(2048)
                return_car = return_car.decode("UTF-8")
                
                if (return_car != "END"):
                    index = int(return_car)
                    message = Company.client_and_company_array_handler(index , security_array[login_check])
                    print(message)
                    connection.sendall(str.encode(message))
            
            elif choice == 5:
                connection.close()           
            
            if not data:
                break
    
    else:
        print(Fore.RED + "Authentication unsuccessful")
        global thread_count
        
        if thread_count > 0:
            thread_count -= 1
        connection.close()


server_connection.listen(5)     


while True:
    clt, addr = server_connection.accept()
    print(Fore.BLUE + "***Server status report*** ")
    print(Fore.BLUE + "A new client connected with the following information: ")
    print(Fore.BLUE + "Received connection from: " + addr[0] + "  port: " + str(addr[1]))
    start_new_thread(client_thread , (clt,) )
    thread_count += 1
    print(Fore.BLUE + "Number of accepted clients: " + str(thread_count))
server_connection.close()
