Tournament
=============

Installation 
------------
- Step 1. Install Brew:

  Thanks to Tolsadus for the WTC brew - https://raw.githubusercontent.com/tolsadus/42homebrewfix
  
  Run this command from your terminal:
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Tolsadus/42homebrewfix/master/install.sh)"
```

- Step 2. Install Python:

  From the terminal run:
  ```
  brew install python3
  ```
  This step will take a while ... be patient.
  
  
- Step 3. Install PyQt:
  From the terminal run:
  ```
  pip3 install pyqt5
  ```
Running the game
----------------
From then you should be able to run the tournament using:
```
python3 main.py
```
On hitting finish the results will play in the terminal

Changing the map can be don in the "vm_py.py" file. Simply edit the map in the parameters

For the player page you will need to select the folder where the players are, and then update the list from the folder.


Confusion regards the front page:

This is where you can a load file where the state of the settings are stored. On the first run through there will be no settings to load, however you can choose to save what settings you select in the GUI in this file. This will allow easy replay of the tournament without having to edit all the settings again.




Disclaimer
----------
This project is still in beta. Some feature arent working as intended and some dont work at all. Its possible for random error messages to occur and stuff to not work at all. Sorry.

Error handling and checking isnt at full capacity as of yet (we in beta).



