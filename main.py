# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:31:53 2018

@author: Richard
"""

from gui import Ui_tournament_ui
from ui_logic import Logic
from PyQt5 import QtWidgets
from roundrobin import RoundRobin
from elimination import Elimination
from json import load
import sys

app = QtWidgets.QApplication(sys.argv)
tournament_ui = QtWidgets.QWizard()
ui = Ui_tournament_ui()
ui.setupUi(tournament_ui)
logic = Logic(ui)
logic.init_btn_fnc()

tournament_ui.button(QtWidgets.QWizard.NextButton).clicked.connect(lambda: 
    logic.next_button_function(tournament_ui.nextId()))
tournament_ui.button(QtWidgets.QWizard.FinishButton).clicked.connect(logic.finish)
    
tournament_ui.show()
app.exec_()

#print ("The ui is done now")

#Play the game:
with open("data.tour", 'r') as file:
    ui_data_file = load(file)
type = ui_data_file.get("tournament_type", None)
if len(ui_data_file.get("player_selected_list")) == 0:
    print("There were no people to play the game")
    print(":(")
    sys.exit()

if type == "round_robin":
    tournament = RoundRobin()
elif type == "single_elim":
    tournament = Elimination()

print("\n PLAYING THE TOURNAMENT NOW \n")
tournament.play_tournament()
print("")
tournament.print_result(table = 0)
print("Final result:")
tournament.calculate_winner()




