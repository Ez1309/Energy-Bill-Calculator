# ⚡ENERGY BILL CALCULATOR ⚡
#### **Get to know on how much you will get charged based on the state you live and for how long you use a device everyday**
#### Project demo: <https://www.youtube.com/watch?v=a8CwpGARAsQ>

#### Definition :
In a few words, this program can be used to register devices - **_as well as their power_** - calculate your month's energy consumption and tell how much you will be charged (based on the price of kWh of a USA state)
## Required libraries
The project.py file uses the following libraries
>```python
>from tabulate import tabulate
>import pandas as pd
>import keyboard
>import time as tm
>import os
>import sys
>import csv
>import re
>```

And the test_project.py file only uses the ```pytest``` library

>```python
>import pytest
>```

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
>        time_input, time = get_time(state, price, device)
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
When the ```handle_option``` function is called, it uses a while lopp to prompt the user for one of the 5 options in the menu. If the user types a invalid option, the terminal will be cleared using a ```clear_screen``` function which executes the following command
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

>```python
>def get_power(device)
>    while True:
>        power = input("\nWhat's its power (in W or kW)? "
>        match = re.match(r"^([\d]*\.?[\d]*)(?:\s)?(k?w)$", power, re.IGNORECASE)
>
>        if not match:
>            clear_screen()
>            print("------ DEVICE REGISTERING ------")
>            print(f"\nDevice: {device}")
>            print(f'\n"{power}" is not a valid power!\nType the power in a "n W" or "n kW" format')
>            pass
>
>        elif float(match.group(1)) == 0:
>            clear_screen()
>            print("------ DEVICE REGISTERING ------")
>            print(f"\nDevice: {device}")
>            print(f'\n"{power}" is not a valid power!\nThe power cannot be null')
>            pass
>
>        else:
>            power = convert_power(power)
>            return power
>
>```

This function has the role of prompting the user for the power of the device they want to register. To make sure the power is valid, I used a regular expression that, in a few words, looks for patterns like "N w" or "N kw" where N is a number and W (watt) or kW (kilowatt) are the units of power. If the user types a power that does not match this pattern, the terminal will be cleared, and a message saying that the power is invalid will be printed, followed by another message that says what is the right format, and then the loop will be restarted to print the input again. Likewise, if the user types "0 W" or "0 kW" the same thing will happen, but the message will say that the power can't be null. Finally, if the user types a valid power, a function called ```convert_power``` will be called, in order to make sure that the power will be in the correct unit.

### 5. Convert power
>```python
>def convert_power(power):
>    
>    match = re.match(r"^([\d]*\.?[\d]*)(?:\s)?(k?w)$", power, re.IGNORECASE)
>
>    if len(match.group(2)) == 1:
>        power = match.group(1)
>        power = str(round(float(power))) + " W"
>        return power
>    
>    if len(match.group(2)) == 2:
>        power = match.group(1)
>        power = round(float(power) * 1000)
>        power = str(power) + " W"
>        return power
>
>```
This function simply checks if the power is in W (watts) or in kW (kilowatts). So if the lenght of match.group(2) - **_which stands for the unit_** - is equal to 1, that means that the unit is W, so it will only return the concatenation of the number and the unit " W" (there's a space just for design purposes). On the other hand, if the lenght is equal to 2, that means that the unit is kW so it will divide the number by 1000, add the " W" unit and return this string. The power is sent to the ```get_power``` function, which in turn, returns that value to the ```ask_info``` function.

### 6. Save device function
>```python
>def save_device(device_info):
>    headers = ["Device", "Power"]
>    
>    with open("devices.csv", "a", newline="") as file:
>        file_is_empty = os.stat("devices.csv").st_size == 0
>        writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
>        if file_is_empty:
>            writer.writeheader()
>        writer.writerow(device_info)
>    clear_screen()
>
>```

This function is called in order to save the device information (that is, the device name and its power) in a CSV file, so that the program can acess those information in a future session. I'm using the CSV library to append the device to a file called "devices.csv". I used ```os.stat("devices.csv").st_size == 0``` to check if the file is empty and if it is, the headers "Device,Power" will be created. So lets say that the user created a device with the following information: ```{"Device": "Toaster", "Power:"850 W"}```. If the CSV file does not exist, it will be created and should look like that:


<div align="center">

| Device  | Power |
|:-------:|:-----:|
| Toaster | 850 W |

</div>


### 7. Show info funcion
Before explaining the second option of the menu ```(2) Calculate your energy bill```, I will explain the third option ```(3) Show devices info```. As you can imagine, this function is used to show what are the devices registered in the CSV file. When the user chooses the third option:
>```python
>if option == "3":
>    clear_screen()
>    devices = Devices()
>    devices.show_info()
>    print("\nPress any key to return")
>    tm.sleep(0.1)
>    keyboard.read_key(suppress=True)
>    clear_screen()
>    menu()
>
>```

The terminal is cleared, and a class called ```Devices``` (I´ll talk more about it in a moment) will be initialized, so that the ```show_info``` function can be acessed. This function looks like this

>```python
>def show_info(self):
>    table = []
>    try:
>        with open("devices.csv") as file:
>            reader = csv.reader(file)
>            for Device, Power in reader:
>                table.append({"Device": Device, "Power": Power})
>
>        info = tabulate(table, headers="firstrow", tablefmt="rounded_grid", stralign="center", )
>        print("---- REGISTERED DEVICES ----")
>        print(info)
>    except FileNotFoundError:
>        print("---- DEVICES TABLE DOES NOT EXIST ----")
>        print("\nYou haven't registered any devices yet")
>        return "Error"
>
>```

Basically, it creates a empty list called table and try to read the information of the CSV file "devices.csv". If the file doesn't exist, a error message will be printed and the string "Error" will be returned. If the file exists, the dictionaries with the devices information are appended to the table list. Then, I used tabulate to create and print a formated table with the content of the csv file, that - **_in the context of the previous example_** - looks like this

<div align="center">
    
![image](https://github.com/Ez1309/test/assets/166740385/e83c9c90-f792-4818-bd19-c9f26ecb1c0a)

</div>
    
Then, outside of the class, a message saying ```Press any key to return``` is printed and - **_before clearing the terminal and calling the menu again_** - the ```keyboard.read_key(suppress=True)``` command waits for any key to be pressed. I used the time library - **_imported as tm_** - ```tm.sleep(0.1)``` to avoid catching any previous key pressing.

### 8. Remove device function
>```python
>def remove_device():
>    devices = Devices()
>    clear_screen()
>    info = devices.show_info()
>    if info == "Error":
>        print("\nPress any key to return")
>        tm.sleep(0.1)
>        keyboard.read_key(suppress=True)
>        clear_screen()
>        menu()
>    else:
>        
>        while True:
>            device = input("\nType the device to be removed or press enter to return: ").strip().title()
>            if device == "":
>                clear_screen()
>                menu()
>            if device.lower() not in devices.names:
>                clear_screen()
>                devices.show_info()
>                print(f'\n"{device}" was not found.\nChoose one device listed above')
>                continue
>            else:
>                break
>
>        table = pd.read_csv("devices.csv", index_col="Device")
>        table = table.drop(device)
>        table.to_csv("devices.csv", index=True)
>        remove_options(device)
>
>```

Similar to the ```(3) Show devices info``` option, the ```(4) Remove a device``` option also shows the formated table that contains the registered devices of the CSV file, but after printing the table, it prompts the user to select a device for removal or to press enter and return to the main menu. If the ```show_info``` function returns "Error" - **_which means that that no devices have been registered yet_** - the ```Press any key to return``` message will be printed and the user will be able to return to the main menu, just like it happend with the device showing option. If the user types a device that is not in the listed table, a message saying that the device was not found will be printed and the loop will restart to print the input again. Finally, if the user types a device from the list, the loop will be broken and then, the ```pandas``` library will do the job of reading the CSV file, looking for the row that contains the specified device, and remove it (I am assuming that every device was registered only once. If there's more than one row with the same name, all of them will be removed). After removing a device, the ```remove_options(device)``` function will be called to inform that the selected device has been removed and to make the user choose between removing another device or going back to the main menu.

### 9. Devices class

>```python
>class Devices:
>    def __init__(self):
>        self.devices = []
>        self.names = []
>        self.open_devices()
>        
>    def open_devices(self):
>        # Trying to open the CSV file that contains the devices information
>        try:
>            with open("devices.csv") as file:
>                reader = csv.DictReader(file)
>                for row in reader:
>                    device_name = row["Device"].lower().strip()
>                    power= row["Power"].lower()
>                    device = {device_name:power}
>                    self.devices.append(device)
>                    self.names.append(device_name)
>        except FileNotFoundError:
>            return "Error"
>    
>    def show_info(self):
>        table = []
>        try:
>            with open("devices.csv") as file:
>                reader = csv.reader(file)
>                for Device, Power in reader:
>                    table.append({"Device": Device, "Power": Power})
>
>            info = tabulate(table, headers="firstrow", tablefmt="rounded_grid", stralign="center", )
>            print("---- REGISTERED DEVICES ----")
>            print(info)
>        except FileNotFoundError:
>            print("---- DEVICES TABLE DOES NOT EXIST ----")
>            print("\nYou haven't registered any devices yet")
>            return "Error"
>
>```

This class has the purpose of leading with the registered devices, creating two lists called ```self.devices``` and  ```self.names```. The function ```open_device``` tries to open the "devices.csv" file, returning "Error" if this file doesn't exist. It uses ```csv.DictReader``` to read information about devices as dictionaries and create new ones, where the keys are the devices's names and the values are their respective powers. Those new dictionaries are appended to the ```self.devices``` list and the device's names are appended to the ```self.names```list. The ```show_info``` function prints the registered devices as I said before.

### 10. States class

>```python
>class States:
>    def __init__(self):
>        self.names = []
>        self.info = []
>        self.get_states()
>        self.prices = {d["state"]:d["price"] for d in self.info}
>
>    def get_states(self):
>        with open("energy_price.csv") as file:
>            reader = csv.DictReader(file)
>            for row in reader:
>                state_name = row["State"].lower()
>                price = row["Price"].removesuffix(" cents per kWh")
>                dct = {"state":state_name, "price":price}
>                self.names.append(state_name)
>                self.info.append(dct)
>
>```

This class is responsible for opening the CSV file called "energy_price.csv" - **_using the_** ``get_states`` **_function_** - which contains a list of all USA states, as well as the price of the kWh (unit of power consumption) in each of those states. Just like was done in the Devices class, there are two lists called ```self.names```, that stores the name of each state, and ```self.info``` that store some dictionaries that contains the names of the states and the prices of kWh in each one too. Besides those two lists, there's a dict comprehension that creates a dictionary called ```self.prices``` whose purpose is to keep other dictionaries where the key of each one is the name of the state, and the value is the price of kWh. This dictionary will be used later to get the price of kWh based on the name of the state (more on that later)

### 11. Functions used to calculate the energy bill
Finally, after all of that explanation, there are the most important functions of this project:
- ```calculate_info```
- ```get_state```
- ```get_price```
- ```get_device```
- ```get_time```
- ```get_values```
- ```show_bill```
  
Going back to the ```handle_option``` function, when the user chooses the ```(2) Calculate your energy bill``` option a bunch of things happen

>```python
>def handle_option()
>    while True:
>        option = input(\nChoose an option: ).strip()
>        ...
>
>    if option == "2":
>        clear_screen()
>        state, price = get_state()
>        device = get_device(state, price)
>        time_input, time = get_time(state, price, device)
>        get_values(price, device, time)
>        calculate_menu(state, price, device, time_input)
>
>        ...
>```

### 11.1 Calculate bill function

>```python
>def calculate_info(state, price, device = None, time = None):
>
>    print(f"------- ENERGY BILL CALCULATOR -------")
>    print(f"\nState: {state}")
>    print(f"Price of kWh: ¢ {price}")
>    if device != None:
>        print(f"\nDevice: {device}")
>    if time != None:
>        print(f"Time used: {time}")
>
>```

This function was created for design purposes only. Since the terminal is cleared many times during the process of calculating the energy bill, I decided to build a function that will be called whenever the terminal gets cleared and some previous information has to be shown. By default, the two required parameters are state and price. The other parameters will be passed depending on what stage of bill calculating you are.

### 11.2 Get state function
After choosing the second option and clearing the terminal, the ```get_state``` function is called

>```python
>def get_state():
>    states = States()
>    print(f"------- ENERGY BILL CALCULATOR -------")
>    while True:
>        
>        state = input("\nIn what state do you live? ").strip().lower().title()
>        
>        if state.lower() not in states.names:
>            clear_screen()
>            print(f"------- ENERGY BILL CALCULATOR -------")
>            print(f'\n"{state}" was not found. Type a state of USA.')
>            pass
>        else:
>            clear_screen()
>            price = get_price(states, state)
>            calculate_info(state, price)
>            return (state, price)
>
>```

First, it initializes the ```States``` class and prints a little header, then starts a while loop to prompt the user for a state. If the lowercased state is not in the ```states.names``` list - **_which contains all of the lowercases names of USA states_** - The terminal clearing function is called and the header will be printed followed by a message that tells that the state was not found. If the user types a valid state, the ```get_price``` function will be called to return the float value of the price of kWh in the chosen state.

>```python
>def get_price(states, state)
>
>    price = float(states.prices[state.lower()])
>    return price

After that, the ```calculate_info``` function is called, passing the States class and the chosen state as parameters and those values are sent back to the ```handle option``` function, which leads to the next stage of the bill calculating.

### 11.3 Get device function
Now that the program knows the state you live and the price of kWh in there, the next step is to ask for a registered device
>```python
>def get_device(state, price):
>    clear_screen()
>    devices = Devices()
>    
>    calculate_info(state, price)
>
>    if devices.open_devices() == "Error":
>        print("\nYou haven't registered any devices yet")
>        print("\nPress any key to return")
>        tm.sleep(0.1)
>        keyboard.read_key(suppress=True)
>        clear_screen()
>        menu()
>
>    while True:
>        device = input("\nType a registered device: ").lower().strip().title()
>
>        if device.lower() not in devices.names:
>            clear_screen()
>            calculate_info(state, price)
>            print(f'\nThe device "{device}" was not found.')
>            pass
>        else:
>            clear_screen()
>            calculate_info(state, price, device)
>            return device
>
>```
First, this funcion clears the terminal, inicializates the ```Devices``` class and prints the state and the price - **_using the_** ```calculate_info``` **_function_** - Then it uses the same logic of the ```show_info``` function, in case the there are no devices registered yet. If there are devices, the function prompts the user for a registered device inside a loop. If the lowercased device is not in the ```devices.names``` list, the screen is cleared again, a error message is printed and the loop restarts. On the other hand, if the device is registered, it will be passed as another parameter to the ```calculate_info``` function and returned to the ```handle_option``` function.

### 11.4 Get time function
Now that the user has chosen a state and a device, the last step to calculate the energy consumption is to know for how long this device was used everyday.
>```python
>def get_time(state, price, device):
>    while True:
>        time_input = input("\nFor how long do you use this device everyday? ").strip()
>        match = re.match(r"^(\d+)\s*(hours?|minutes?)(?:\s+and\s+(\d+)\s*(hours?|minutes?))?\s*$", time_input, re.IGNORECASE)
>
>        if not match:
>            clear_screen()
>            calculate_info(state, price, device)
>            print(f'\n"{time_input}" is not a valid time.\nUse a "N hour(s)", "N minute(s)" or a "N hour(s) and N minute(s)" format')
>            continue
>        
>        if "hour" in match.group(2):
>            if not 0 < int(match.group(1)) <= 24:
>                clear_screen()
>                calculate_info(state, price, device)
>                print(f'\n"{time_input}" is not a valid time !\nThe hours must be in the range of 01 to 24')
>                continue
>
>        if "minute" or "minutes" in [match.group(2), match.group(4)]:
>            if not 0 < int(match.group(1)) <= 60 or match.group(3) != None and not 0 < int(match.group(3)) <= 60:
>                clear_screen()
>                calculate_info(state, price, device)
>                print(f'\n"{time_input}" is not a valid time !\nThe minutes must be in the range of 01 to 60')
>                continue
>        else:
>            break
>        time = convert_time(time_input)
>        return (time_input, time)
>
>```

This function has the role of prompting the user for how long the chosen device was used everyday. The content of this input is then sent to a regular expression, that basically looks for patterns like "N hours", "N minutes" or "N hours and N minutes". If there are no matches, the terminal is cleared all of those information (the state, the price and the device) are printed again and a message saying that the time is invalid is printed. It is followed by a more specifc message that informes the accepted format. Similar to that, if the user types a number of hours that is equal to zero or is greater than 24, or a number of minutes that is equal to zero or greater than 60, a message informing that the time is invalid will also be printed. Finally, if the time input is in the correct format, a ```convert_time``` function will be called to convert the number of hours and minutes to a single thing.
>```python
>def convert_time(time):
>    match = re.match(r"^(\d+)\s*(hours?|minutes?)(?:\s+and\s+(\d+)\s*(hours?|minutes?))?\s*$", time, re.IGNORECASE)
>
>    if None in match.groups():
>        if "hour" in match.group(2):
>            return (float(match.group(1)))
>        # Return the converted number of minutes
>        elif "minute" in match.group(2):
>            return (float(match.group(1)) / 60)
>    else:
>        hours = float(match.group(1))
>        minutes = float(match.group(3))
>        converted_minutes = (minutes / 60)
>        return float(hours + converted_minutes)
>
>```
Here, due to the format of the regular expression, if the match is something like "1 hour" or "45 minutes", the matched groups will be (1, hour, None, None) or (45, minutes, None, None). That happens because the regex is meant to accept things like "1 hour and 45 minutes" so the groups will be (1, hour, 45, minutes). With that said, if there's ```None``` in ```match.groups``` - **_which means that the hour looks like "N hours" or "N minutes"_** - the function returns the float of the number if the time is like "N hours" and return the float of the number divided by 60 if the time is like "N minutes". Otherwise, it means that the time is like "N hous and N minutes", so the function convert the minutes into hours, sum the converted minutes with the hours and return the float number of that sum.
<br/>
<br/>
After all that checking, the ```get_time``` function returns the time_input (which is a string and will be used by the ```calculate_info``` function) and the time (which is a float number and will be used to calculate the energy consumption)

### 11.5 Get values function
The last step before showing the bill 
