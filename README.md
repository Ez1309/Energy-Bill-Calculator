# ⚡ENERGY BILL CALCULATOR ⚡
#### **Get to know on how much you will get charged based on the state you live and for how long you use a device everyday**
#### Project demo: <https://www.youtube.com/watch?v=a8CwpGARAsQ>

#### Definition :
In a few words, this program can be used to register devices -as well as their power- calculate your month's energy consumption and tell how much you will be charged (based on the price of kWh of a USA state)
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
&emsp; The ```main``` function is only responsible for calling the ```menu``` funcion, which in turn will call the ```print_menu``` and the ```handle_option``` 
funcion. &emsp; The ```print_menu``` function just shows a small menu with 5 options that can be chosen when the function ```handle_option``` is called.    

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







