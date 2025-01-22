# Traditional-Python-Banking-System
Developed a banking system using core Python skills that can perform traditional operations like: deposits, withdrawals, savings, customer onboarding and other administrative roles, while using TKinter for GUI

## Description

This is a banking system written in Python for the backend and Tkinter for the GUI.

## How to run

This project can be run either on the GUI or console.

### GUI

To run on the GUI, make sure line `527` of the `gui.py` file is uncommented and line `531` is commented. This is because you can not run the GUI and the console at the same time.
After doing that, go to your terminal and run the following command:

```shell
$ python3 gui.py
```

This command will open the GUI and you can follow the instructions to run the application.

### Console

Just like running the GUI, make sure line `531` of the `gui.py` file is uncommented and line `527` is commented.
Then in your terminal, run:

```shell
$ python3 gui.py
```

This command will open the console and you can follow the instructions to run the application.

## Structure

This project is structured as follows:

```
|--- db
|--- entities
|--- utilities
|--- bank_system.py
|--- gui.py
```

The `db` folder contains code and data relating to saving and loading customer and admin data to and from json files.
The `entities` folder contains code that represents classes and their dependencies on one another.
The `utilities` folder contains code that hosts utility types
The `bank_system.py` file contains code for initiating the bank class and its methods
The `gui.py` file contains code for the user interface and dependency on tkinter.
