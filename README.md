# ⚡ENERGY BILL CALCULATOR ⚡
#### **Get to know on how much you will get charged based on the state you live and for how long you use a device everyday**
#### Project video: <https://www.youtube.com/watch?v=a8CwpGARAsQ>

### Definition :
This project was made for Harvard's CS50 introduction to programming with python. In a nutshell, this program can be used to register devices, as well as their power, calculate your energy consumption and tell on how much you will be charged (based on the price of kWh of a USA state)

## Installation

> [!NOTE]
> To download and run this project, you will need to install [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) on your computer

#### To clone the project, run this command on your terminal
> ```bash
>git clone https://github.com/Ez1309/test/edit/main/README.md
>``` 
<br/>

> [!WARNING]
> Run those commands on your terminal to install the libraries and to make sure the code will work without problems
>```bash
>pip install -r requirements.txt
>```

<br/>

## Usage
> **Type "python project.py" to run the program**
>```bash
>python project.py
>```


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

>$\texttt{\color{white}a}$

>a

<div style="text-align: center;">
| Device | Power |

|:---: | :---: |

| Toaster | 850 W |
</div>

| Device | Power |
|:---:|:---:|
| Toaster | 850 W |


<div align="center">

| Device  | Power |
|:-------:|:-----:|
| Toaster | 850 W |

</div>












