import os
import sys
import csv
import re
import time as tm

from tabulate import tabulate
import keyboard
import pandas as pd


class Devices:
    def __init__(self):
        self.devices = []
        self.names = []
        self.bill_info = []
        self.open_devices()
        

    def open_devices(self): 
        try:
            with open("devices.csv") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    device_name = row["Device"].lower().strip()
                    power= row["Power"].lower()
                    device = {device_name:power}
                    self.devices.append(device)
                    self.names.append(device_name)
        except FileNotFoundError:
            return "Error"
    
    def show_info(self): 
        table = []
        try:
            with open("devices.csv") as file:
                reader = csv.reader(file)
                for Device, Power in reader:
                    table.append({"Device": Device, "Power": Power})

            info = tabulate(table, headers="firstrow", tablefmt="rounded_grid", stralign="center", )
            print("---- REGISTERED DEVICES ----")
            print(info)
        except FileNotFoundError:
            print("---- DEVICES TABLE DOES NOT EXIST ----")
            print("\nYou haven't registered any devices yet")
            return "Error"
    

devices = Devices()
                    
class States:
    def __init__(self):
        self.names = []
        self.info = []
        self.get_states()
        self.prices = {d["state"]:d["price"] for d in self.info}

    def get_states(self):
        with open("energy_price.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                state_name = row["State"].lower()
                price = row["Price"].removesuffix(" cents per kWh")
                dct = {"state":state_name, "price":price}
                self.names.append(state_name)
                self.info.append(dct)
        


def main():
    menu()
    
def menu():
    print_menu()
    handle_option()

def print_menu():
    print(" ________________________________")
    print("|              MENU              |")
    print("|                                |")
    print("| (1) Register a device          |")
    print("| (2) Calculate your energy bill |")
    print("| (3) Show devices info          |")
    print("| (4) Remove a device            |")
    print("| (5) Exit the program           |")
    print("|________________________________|")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def handle_option():
    while True:
        option = input("\nChoose an option: ").strip()
        if option not in ["1", "2", "3", "4", "5"]:
            clear_screen()
            print_menu()
            print(f'\n"{option}" is not a valid option')
            pass
        else:
            break
        
    if option == "1":
        ask_info()

    if option == "2":
        clear_screen()
        state, price = get_state()
        calculating_steps(state, price)


    if option == "3":
        clear_screen()
        devices.show_info()
        print("\nPress any key to return")
        tm.sleep(0.1)
        keyboard.read_key(suppress=True)
        clear_screen()
        menu()
    
    elif option == "4":
        clear_screen()
        remove_device()
        
    elif option == "5":
        sys.exit()

def calculating_steps(state, price):
    device = get_device(state, price)
    time_input, time = get_time(state, price, device)
    get_values(price, device, time)
    calculate_menu(state, price, device, time_input)

def ask_info():
    clear_screen()
    print("------ DEVICE REGISTERING ------")
    device = input("\nType a device: ").strip().lower().title()
    power = get_power(device)
    device_info = {"Device": device, "Power": power}
    save_device(device_info)
    print(f'The device "{device}" was registered sucessfully!\n')
    register_menu()

def register_menu():
    print("(1) Register another device")
    print("(2) Go back to menu")
    while True:
        option = input("\nChoose an option: ").strip()
        if option not in ["1", "2"]:
            clear_screen()
            print("(1) Register another device")
            print("(2) Go back to menu")
            print(f'\n"{option}" is not a valid option')
            pass
        else:
            break
    if option == "1":
        ask_info()
    if option == "2":
        clear_screen()
        menu()

def get_power(device):

    while True:
        power = input("\nWhat's its power (in W or kW)? ")
        match = re.match(r"^([\d]*\.?[\d]*)(?:\s)?(k?w)$", power, re.IGNORECASE)

        if not match:
            clear_screen()
            print("------ DEVICE REGISTERING ------")
            print(f"\nDevice: {device}")
            print(f'\n"{power}" is not a valid power!\nType the power in a "n W" or "n kW" format')
            pass

        elif float(match.group(1)) == 0:
            clear_screen()
            print("------ DEVICE REGISTERING ------")
            print(f"\nDevice: {device}")
            print(f'\n"{power}" is not a valid power!\nThe power cannot be null')
            pass

        else:
            power = convert_power(power)
            return power
        
def convert_power(power):
    
    match = re.match(r"^([\d]*\.?[\d]*)(?:\s)?(k?w)$", power, re.IGNORECASE)

    if len(match.group(2)) == 1:
        power = match.group(1)
        power = str(round(float(power))) + " W"
        return power
    
    if len(match.group(2)) == 2:
        power = match.group(1)
        power = round(float(power) * 1000)
        power = str(power) + " W"
        return power
    
def save_device(device_info):
    headers = ["Device", "Power"]
    
    with open("devices.csv", "a", newline="") as file:
        file_is_empty = os.stat("devices.csv").st_size == 0
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
        if file_is_empty:
            writer.writeheader()
        writer.writerow(device_info)
    devices.open_devices()  
    clear_screen()
    
def remove_device():
    
    clear_screen()
    info = devices.show_info()
    if info == "Error":
        print("\nPress any key to return")
        tm.sleep(0.1)
        keyboard.read_key(suppress=True)
        clear_screen()
        menu()
    else:
        
        while True:
            device = input("\nType the device to be removed\nor press enter to return: ").strip().title()
            if device == "":
                clear_screen()
                menu()
            if device.lower() not in devices.names:
                clear_screen()
                devices.show_info()
                print(f'\n"{device}" was not found.\nChoose one device listed above')
                pass
            else:
                break

        table = pd.read_csv("devices.csv", index_col="Device")
        table = table.drop(device)
        table.to_csv("devices.csv", index=True)
        remove_options(device)

def remove_options(device):
    clear_screen()
    print(f'The device "{device}" has been removed!')
    print("\n(1) Remove another device")
    print("(2) Go back to menu")
    while True:
        option = input("\nChoose an option: ")
        if option not in ["1", "2"]:
            clear_screen()
            print("(1) Remove another device")
            print("(2) Go back to menu")
            print(f'"{option}" is not a valid option')
            pass
        if option == "1":
            clear_screen()
            remove_device()
        if option == "2":
            clear_screen()
            menu()
            
def calculate_info(state, price, device = None, time = None):
    print(f"------- ENERGY BILL CALCULATOR -------")
    print(f"\nState: {state}")
    print(f"Price of kWh: ¢ {price}")
    if device != None:
        print(f"\nDevice: {device}")
    if time != None:
        print(f"Time used: {time}")

def get_state():
    states = States()
    print(f"------- ENERGY BILL CALCULATOR -------")
    while True:
        
        state = input("\nIn what state do you live? ").strip().lower().title()
        
        if state.lower() not in states.names:
            clear_screen()
            print(f"------- ENERGY BILL CALCULATOR -------")
            print(f'\n"{state}" was not found. Type a state of USA.')
            pass
        else:
            clear_screen()
            price = get_price(states, state)
            calculate_info(state, price)
            return (state, price)
        
def get_price(states, state):
    price = float(states.prices[state.lower()])
    return price

def get_device(state, price):
    clear_screen()
    
    
    calculate_info(state, price)

    if devices.open_devices() == "Error":
        print("\nYou haven't registered any devices yet")
        print("\nPress any key to return")
        tm.sleep(0.1)
        keyboard.read_key(suppress=True)
        clear_screen()
        menu()

    while True:
        device = input("\nType a registered device: ").lower().strip().title()

        if device.lower() not in devices.names:
            clear_screen()
            calculate_info(state, price)
            print(f'\nThe device "{device}" was not found.')
            pass
        else:
            clear_screen()
            calculate_info(state, price, device)
            return device

def get_time(state, price, device):
    while True:
        time_input = input("\nFor how long do you use this device everyday? ").strip()
        match = re.match(r"^(\d+)\s*(hours?|minutes?)(?:\s+and\s+(\d+)\s*(hours?|minutes?))?\s*$", time_input, re.IGNORECASE)

        if not match:
            clear_screen()
            calculate_info(state, price, device)
            print(f'\n"{time_input}" is not a valid time.\nUse a "N hour(s)", "N minute(s)" or a "N hour(s) and N minute(s)" format')
            continue
        
        if "hour" in match.group(2):
            if not 0 < int(match.group(1)) <= 24:
                clear_screen()
                calculate_info(state, price, device)
                print(f'\n"{time_input}" is not a valid time !\nThe hours must be in the range of 01 to 24')
                continue

        if "minute" or "minutes" in [match.group(2), match.group(4)]:
            if not 0 < int(match.group(1)) <= 60 or match.group(3) != None and not 0 < int(match.group(3)) <= 60:
                clear_screen()
                calculate_info(state, price, device)
                print(f'\n"{time_input}" is not a valid time !\nThe minutes must be in the range of 01 to 60')
                continue
        else:
            break
        time = convert_time(time_input)
        return (time_input, time)
        

def convert_time(time):
    match = re.match(r"^(\d+)\s*(hours?|minutes?)(?:\s+and\s+(\d+)\s*(hours?|minutes?))?\s*$", time, re.IGNORECASE)

    if None in match.groups():
        if "hour" in match.group(2):
            return (float(match.group(1)))
        # Return the converted number of minutes
        elif "minute" in match.group(2):
            return (float(match.group(1)) / 60)
    else:
        hours = float(match.group(1))
        minutes = float(match.group(3))
        converted_minutes = (minutes / 60)
        return float(hours + converted_minutes)
        
def get_values(price, device, time):
    
    power = float([i[device.lower()] for i in devices.devices if device.lower() in i][0].removesuffix(" w"))

    daily_usage = round(((power/1000)) * time, 2)
    daily_charge = round(daily_usage * (price/100), 2)
    month_usage = round(daily_usage * 30, 2)
    month_charge = round(daily_charge * 30, 2)
    
    bill_numbers = (daily_usage, daily_charge, month_usage, month_charge)
    devices.bill_info.append(bill_numbers)
    
    

def calculate_menu(state, price, device, time):
    clear_screen()
    calculate_info(state, price, device, time)
    print("\n(1) Choose another device")
    print("(2) Show the bill")

    while True:
        option = input("\nChoose an option: ").strip()
        if option not in ["1", "2"]:
            clear_screen()
            print("\n(1) Choose another device")
            print("(2) Show the bill")
            print(f'\n"{option}" is not a valid option')
        if option == "1": 
            calculating_steps(state, price)
        if option == "2":
            show_bill(state)    

def show_bill(state):
    clear_screen()
  
    du = sum([i[0] for i in devices.bill_info])
    dc = sum([i[1] for i in devices.bill_info])
    mu = sum([i[2] for i in devices.bill_info])
    tc = sum([i[3] for i in devices.bill_info])

    print(f"--------- State of {state}  ---------")
    print(f"\nYour daily electricity usage was {du:.2f} kWh\n")
    print(f"Your daily charge was $ {dc:.2f}\n")
    print(f"Your month electricity usage was {mu:.2f} kWh\n")
    print(f"Your total charge was $ {tc:.2f}")
    print("")

    sys.exit()

if __name__ == "__main__":
    main()