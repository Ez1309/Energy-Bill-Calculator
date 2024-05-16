# ⚡ENERGY BILL CALCULATOR ⚡
#### **Get to know on how much you will get charged based on the state you live and for how long you use a device everyday**
#### Project demo: <https://www.youtube.com/watch?v=a8CwpGARAsQ>

#### Definition :
In a few words, this program can be used to register devices - **_as well as their power_** - calculate your month's energy consumption and tell how much you will be charged (based on the price of kWh of a USA state)
## Required libraries
The project.py file uses the following libraries
```python
from tabulate import tabulate
import pandas as pd
import keyboard
import time as tm
import os
import sys
import csv
import re
```
And the test_project.py file only uses the ```pytest``` library
```python
import pytest
```
## Code explanation
### 1. Main and Menu functions
>```python
>def main():
>     menu()
>
>def menu():
>     print_menu()
>     handle_option()
>
>def print_menu():
>     print(" ________________________________")
>     print("|              MENU              |")
>     print("|                                |")
>     print("| (1) Register a device          |")
>     print("| (2) Calculate your energy bill |")
>     print("| (3) Show devices info          |")
>     print("| (4) Remove a device            |")
>     print("| (5) Exit the program           |")
>     print("|________________________________|")
>```
The ```main``` function is only responsible for calling the ```menu``` funcion, which in turn will call the ```print_menu``` and the ```handle_option``` 
funcion. The ```print_menu``` function just shows a small menu with 5 options that can be chosen when the function ```handle_option``` is called.    

### 2. Option Handling function
>```python
>def handle_option():
>    while True:
>        option = input("\nChoose an option: ").strip()
>        if option not in ["1", "2", "3", "4", "5"]:
>            clear_screen()
>            print_menu()
>            print(f'\n"{option}" is not a valid option')
>            pass
>        else:
>            break
>        
>    if option == "1":
>        clear_screen()
>        ask_info()
>
>    if option == "2":
>        clear_screen()
>        state, price = get_state()
>        device = get_device(state, price)
>        time_input, time = check_time(state, price, device)
>        get_values(price, device, time)
>        calculate_menu(state, price, device, time_input)
>
>
>    if option == "3":
>        clear_screen()
>        devices = Devices()
>        devices.show_info()
>        print("\nPress any key to return")
>        tm.sleep(0.1)
>        keyboard.read_key(suppress=True)
>        clear_screen()
>        menu()
>    
>    elif option == "4":
>        clear_screen()
>        remove_device()
>        
>    elif option == "5":
>        sys.exit()
>```
When the ```handle_option``` function is called, it uses a while lopp to prompt the user for one of the 5 options in the menu. If the user types a invalid option, the terminal will be cleaned using a ```clear_screen``` function which executes the following command
>```python
>os.system("cls" if os.name == "nt" else "clear")
>```
Right after that, the menu is printed again, followed by a message saying that the chosen option is not valid, and then the loop is restarted.


### 3. Ask info function
If the user chooses the option 1, the function ```ask_info``` will be called
>```python
>def ask_info()
>    clear_screen()
>    print("------ DEVICE REGISTERING ------")
>    device = input("\nType a device: ").strip().lower().title()
>    power = get_power(device)
>    device_info = {"Device": device, "Power": power}
>    save_device(device_info)
>    print(f'The device "{device}" was registered sucessfully!\n')
>    register_menu()
>```

This function has the purpose of asking the user to register a device, along with its power, creating a dictionary called ```device_info``` which contains the name of the device as one value, and its power as the other value. Right after that, the fuction ```save_device``` is called passing the dictionary as the argument, and a message saying that the device was registered sucessfully is printed. After registering a device, the function ```register_menu``` is called, so that the user can choose between registering another device or going back to the main menu.
### 4. Get power function
```python
def get_power(device)
    while True:
        power = input("\nWhat's its power (in W or kW)? "
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
```
This function has the role of prompting the user for the power of the device they want to register. To make sure the power is valid, I used a regular expression that, in a few words, looks for patterns like "N w" or "N kw" where N is a number and W (watt) or kW (kilowatt) are the units of power. If the user types a power that does not match this pattern, the terminal will be cleaned, and a message saying that the power is invalid will be printed, followed by another message that says what is the right format, and then the loop will be restarted to print the input again. Likewise, if the user types "0 W" or "0 kW" the same thing will happen, but the message will say that the power can't be null. Finally, if the user types a valid power, a function called ```convert_power``` will be called, in order to make sure that the power will be in the correct unit.
### 5. Convert power
```python
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
```
This function simply checks if the power is in W (watts) or in kW (kilowatts). So if the lenght of match.group(2) - **_which stands for the unit_** - is equal to 1, that means that the unit is W, so it will only return the concatenation of the number and the unit " W" (there's a space just for design purposes). On the other hand, if the lenght is equal to 2, that means that the unit is kW so it will divide the number by 1000, add the " W" unit and return this string. The power is sent to the ```get_power``` function, which in turn, returns that value to the ```ask_info``` function.

### 6. Save device function
```python
def save_device(device_info):
    headers = ["Device", "Power"]
    
    with open("devices.csv", "a", newline="") as file:
        file_is_empty = os.stat("devices.csv").st_size == 0
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
        if file_is_empty:
            writer.writeheader()
        writer.writerow(device_info)
    clear_screen()
```
This function is called in order to save the device information (that is, the device name and its power) in a CSV file, so that the program can acess those informations in a future session. I'm using the CSV library to append the device to a file called "devices.csv". I used ```os.stat("devices.csv").st_size == 0``` to check if the file is empty and if it is, the headers "Device,Power" will be created. So lets say that the user created a device with the following information: ```{"Device": "Toaster", "Power:"850 W"}```. If the CSV file does not exist, it will be created and should look like that:

|  Device | Power |
|---------|-------|
| Toaster | 850 W |

### 7. Show info funcion
Before explaining the second option of the menu ```(2) Calculate your energy bill```, I will explain the third option ```(3) Show devices info```. As you can imagine, this function is used to show what are the devices registered in the CSV file. When the user chooses the third option:
```python
if option == "3":
        clear_screen()
        devices = Devices()
        devices.show_info()
        print("\nPress any key to return")
        tm.sleep(0.1)
        keyboard.read_key(suppress=True)
        clear_screen()
        menu()
```
The terminal is cleaned, and a class called ```Devices``` (I´ll talk more about it in a moment) will be initialized, so that the ```show_info``` function can be acessed. This function looks like this
```python
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
```
Basically, it creates a empty list called table and try to read the information of the CSV file "devices.csv". If the file doesn't exist, a error message will be printed and the string "Error" will be returned. If the file exists, the dictionaries with the devices information are appended to the table list. Then, I used tabulate to create and print a formated table with the content of the csv file, that - in the context of the previous example - looks like this

> ![image](https://github.com/Ez1309/test/assets/166740385/e83c9c90-f792-4818-bd19-c9f26ecb1c0a)

Then, outside of the class, a message saying ```Press any key to return``` is printed and - **_before cleaning the terminal and calling the menu again_** - the ```keyboard.read_key(suppress=True)``` command waits for any key to be pressed. I used the time library - **_imported as tm_** - ```tm.sleep(0.1)``` to avoid catching any previous key pressing.

### 8. Remove device function
```python
def remove_device():
    devices = Devices()
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
            device = input("\nType the device to be removed or press enter to return: ").strip().title()
            if device == "":
                clear_screen()
                menu()
            if device.lower() not in devices.names:
                clear_screen()
                devices.show_info()
                print(f'\n"{device}" was not found.\nChoose one device listed above')
                continue
            else:
                break

        table = pd.read_csv("devices.csv", index_col="Device")
        table = table.drop(device)
        table.to_csv("devices.csv", index=True)
        remove_options(device)
```
Similar to the ```(3) Show devices info``` option, the ```(4) Remove a device``` option also shows the formated table that contains the registered devices of the CSV file, but after printing the table, it prompts the user to select a device for removal or to press enter and return to the main menu. If the ```show_info``` function returns "Error" - **_which means that that no devices have been registered yet_** - the ```Press any key to return``` message will be printed and the user will be able to return to the main menu, just like it happend with the device showing option. If the user types a device that is not in the listed table, a message saying that the device was not found will be printed and the loop will restart to print the input again. Finally, if the user types a device from the list, the loop will be broken and then, the ```pandas``` library will do the job of reading the CSV file, looking for the row that contains the specified device, and remove it (I am assuming that every device was registered only once. If there's more than one row with the same name, all of them will be removed). After removing a device, the ```remove_options(device)``` function will be called to inform that the selected device has been removed and to make the user choose between removing another device or going back to the main menu.

### 9. Devices class
```python
class Devices:
    def __init__(self):
        self.devices = []
        self.names = []
        self.open_devices()
        
    def open_devices(self):
        # Trying to open the CSV file that contains the devices information
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
```
This class has the purpose of leading with the registered devices, creating two lists called ```self.devices``` and  ```self.names```. The function ```open_device``` tries to open the "devices.csv" file, returning "Error" if this file doesn't exist. It uses ```csv.DictReader``` to read information about devices as dictionaries and create new ones, where the keys are the devices's names and the values are their respective powers. Those new dictionaries are appended to the ```self.devices``` list and the device's names are appended to the ```self.names```list. The [```show_info```](https://github.com/Ez1309/test/edit/main/README.md#7-show-info-funcion) function prints the registered devices as I said before.

  
