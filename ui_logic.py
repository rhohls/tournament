# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 13:23:48 2018

@author: Richard
"""
import json

from collections import OrderedDict 
from PyQt5 import QtWidgets
import os
#from PyQt5 import QtCore, QtGui

class Logic(object):
    
    def __init__(self, ui):
        self.ui = ui
        super(Logic, self).__init__()   
        
        #init objects
        self.defaults_loaded = False
        
        #load defualts
        try:
            with open('config.ini', 'r') as file:
                config = json.load(file)
        except:
            #print("no config")
            config = {}
            
        self.filename_lst = config.get('filename_lst')
        
        
# =============================================================================
#         #Wizzard changes
# =============================================================================
    # FileSelectionPg, TraitSelectionPg, GenSettingsPg, SiteSelectionPg, DataSigaPg, DataSigwPg, DataEcoPg, DispSettingPg
      #  self.ui.PlayerSelectionPg.isComplete = self.playerselect_iscomplete
        self.ui.GeneralSettingPg.validatePage = self.validate_settings
        
    def init_btn_fnc(self):
        #explore buttons
        self.badfile = "('', '')"
        self.ui.btn_explore_1_1.clicked.connect(lambda: self.file_explore_open(self.ui.txt_settingsfile_in, self.ui.txt_settingsfile_out))
        self.ui.btn_explore_1_2.clicked.connect(lambda: self.file_explore_save(self.ui.txt_settingsfile_out))
        self.ui.btn_explore_2_1.clicked.connect(lambda: self.folder_explore_open(self.ui.txt_dir_players))
        self.ui.btn_load.clicked.connect(lambda: self.load_variable())

        self.ui.btn_player_update.clicked.connect(lambda: self.player_list_generate(self.ui.txt_dir_players.text()))
        self.ui.btn_players_deselect.clicked.connect(lambda: self.swap_list(self.ui.lst_players_select, self.ui.lst_players_deselect))
        self.ui.btn_players_select.clicked.connect(lambda: self.swap_list(self.ui.lst_players_deselect, self.ui.lst_players_select))
            
        self.ui.lst_players_select.doubleClicked.connect(lambda: self.swap_list(self.ui.lst_players_select, self.ui.lst_players_deselect))
        self.ui.lst_players_deselect.doubleClicked.connect(lambda: self.swap_list(self.ui.lst_players_deselect, self.ui.lst_players_select))
        
        self.ui.chk_robin_groups.stateChanged.connect(lambda: self.toggle_checkable())
  
        
# =============================================================================
#     BUTTON FUNCTIONS        
# =============================================================================
    
    def toggle_checkable(self):
        if self.ui.chk_robin_groups.isChecked():
            self.ui.spn_robin_groups.setEnabled(True)
            self.ui.label_robbin_groups.setEnabled(True)
        else:
            self.ui.spn_robin_groups.setEnabled(False)
            self.ui.label_robbin_groups.setEnabled(False)  
            
    def folder_explore_open(self, txt_field):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        folder_name = str(folder)            
        if folder_name != self.badfile:
            txt_field.setText(folder_name)
        return        
        
    def file_explore_open(self, txt_field_open, txt_field_save = None):
        file = QtWidgets.QFileDialog.getOpenFileName(None)#, 'Open File', "Tournament Files (*.tour)")
        filename_in = file[0]
        if filename_in != self.badfile:
            txt_field_open.setText(filename_in)
            if txt_field_save:
                txt_field_save.setText(filename_in)
        return
    
    def file_explore_save(self, txt_field_save):         
        file = QtWidgets.QFileDialog.getSaveFileName(None)#, 'Open File', "Tournament Files (*.tour)")
        filename_out = file[0]
        if filename_out != self.badfile:
            txt_field_save.setText(filename_out)
        return

# =============================================================================
#     PLAYER LIST        
# =============================================================================
    def validate_player_list(self):
        new_list = []
        for file in self.player_list:
            file = file.split('.')
            if len(file) == 2 and file[1] == 'filler':
                new_list.append(file[0])
        self.player_list = new_list
    
    def player_list_generate(self, player_path):
        if player_path != "":
            self.player_list = [file for file in os.listdir(player_path) if 
                                os.path.isfile(os.path.join(player_path, file))]
            self.validate_player_list()
            self.list_data_add(self.ui.lst_players_select, self.player_list)
    
    def swap_list(self, list1, list2):
        itemlist = list1.selectedItems()  
        for i in range(0,len(itemlist)):
            rowofitem = list1.row(itemlist[i])
            itemtoswap = list1.takeItem(rowofitem)
            list2.addItem(itemtoswap)
        return
    
    def list_data_add(self, list_widget, list_data):
        #adds list of traits to widget
        if (list_widget.count() > 0):
            list_widget.clear()
        list_widget.addItems(list_data) 
# =============================================================================
#     VERIFICATION AND VALIDATION        
# =============================================================================
    def validate_settings(self):
        if self.ui.spn_set_bestof.value() % 2 == 0:
            self.err_message("Have an odd number for best of matches")
            return (False)
        else:
            return (True)
        
# =============================================================================
#     def playerselect_iscomplete(self):
#         if ((self.ui.lst_players_select.count() <= 0)):
#             return(False)
#         else:
#             return(True)
# =============================================================================

# =============================================================================
#     UI WIZARD STUFF
# =============================================================================

    def err_message(self, text, title = "Error"):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        
        
    def next_button_function(self, pageid):
        #print("page ID:", pageid)
        if pageid == -2:
            if self.ui.txt_settingsfile_in.text() != "":
                self.load_variable()
                
                
                
                
# =============================================================================
#     LOAD AND SAVE
# =============================================================================
    def load_variable(self):
        ui_data_file = None
        try:
            with open(self.ui.txt_settingsfile_in.text(), 'r') as file:
                ui_data_file = json.load(file)
        except:
            if self.ui.txt_settingsfile_in.text() != '':
                self.err_message("There was a problem opening the settings file")
        if ui_data_file:
            self.set_all_variables(ui_data_file)
            
            
    def writeoutput_variables(self):
        ui_data = {}
        
        ui_data['ouputfile'] = self.ui.txt_settingsfile_out.text()
        ui_data['player_selected_list'] = self.listwidget_text(self.ui.lst_players_select)
        ui_data['player_deselected_list'] = self.listwidget_text(self.ui.lst_players_deselect)
        ui_data['player_folder'] = self.ui.txt_dir_players.text()
        ui_data['tournament_type'] = self.get_tounament_type()
        ui_data['seed_type'] = self.get_seed_type()
        ui_data['print_type'] = self.get_print_type()
        ui_data['amount_games'] = self.ui.spn_set_bestof.value()
        ui_data['win_score'] = self.ui.spn_set_winpnt.value()
        ui_data['loss_score'] = self.ui.spn_set_losspnt.value()
        ui_data['num_groups'] = self.ui.spn_robin_groups.value()
        ui_data['multi_groups'] = self.ui.chk_robin_groups.isChecked()

        
        if self.ui.txt_settingsfile_out.text():
            print (self.ui.txt_settingsfile_out.text())
            with open(self.ui.txt_settingsfile_out.text(), 'w') as file:
                file.write(json.dumps(ui_data, indent = 2))
                
        with open(os.path.join(os.getcwd(), 'data.tour'), 'w') as file:
            file.write(json.dumps(OrderedDict(ui_data), indent = 2))
        return                
                
    def set_all_variables(self, ui_data):
        self.ui.txt_settingsfile_out.setText(ui_data.get('ouputfile'))
        self.list_data_add(self.ui.lst_players_select, ui_data.get('player_selected_list'))
        self.list_data_add(self.ui.lst_players_deselect, ui_data.get('player_deselected_list'))
        self.ui.txt_dir_players.setText(ui_data.get('player_folder'))
        self.set_tounament_type(ui_data.get('tournament_type'))
        self.set_seed_type(ui_data.get('seed_type'))
        self.set_print_type(ui_data.get('print_type'))
        self.ui.spn_set_bestof.setValue(ui_data.get('amount_games'))
        self.ui.spn_set_winpnt.setValue(ui_data.get('win_score'))
        self.ui.spn_set_losspnt.setValue(ui_data.get('loss_score'))
        self.ui.spn_robin_groups.setValue(ui_data.get('num_groups'))
        if ui_data.get('multi_groups'):
            self.ui.chk_robin_groups.setChecked(True)
                        

# =============================================================================
#     INFORMATION EXTRACTION
# =============================================================================                
 
    def get_tounament_type(self):
        buttons = ["multi_elim", "swiss", "single_elim", "round_robin", None]
        buttonid = self.ui.btngrp_tournament_type.checkedId()
        return(buttons[buttonid])
        
    def set_tounament_type(self, type_tour):
        buttons = ["multi_elim", "swiss", "single_elim", "round_robin", None]
        buttons.reverse()
        buttonid = buttons.index(type_tour) + 1
        buttonid *= -1
        actual_button = self.ui.btngrp_tournament_type.button(buttonid)
        actual_button.setChecked(True)

    def get_seed_type(self):
        buttons = ["seeded", "random", "none", None]
        buttonid = self.ui.btngrp_seed_type.checkedId()
        return (buttons[buttonid])

    def set_seed_type(self, type_seed):
        buttons = ["seeded", "random", "none", None]
        buttons.reverse()
        buttonid = buttons.index(type_seed) + 1
        buttonid *= -1
        actual_button = self.ui.btngrp_seed_type.button(buttonid)
        actual_button.setChecked(True)

    def get_print_type(self):
        buttons = ["tour", "round", "match", None]
        buttonid = self.ui.btngrp_score_show.checkedId()
        return (buttons[buttonid])

    def set_print_type(self, type_seed):
        buttons = ["tour", "round", "match", None]
        buttons.reverse()
        buttonid = buttons.index(type_seed) + 1
        buttonid *= -1
        actual_button = self.ui.btngrp_score_show.button(buttonid)
        actual_button.setChecked(True)

    def listwidget_text(self, list_widget):
        #list of all text options in list widget
        txt_list = []
        items = []
        for i in range(list_widget.count()):
             items.append(list_widget.item(i))
        txt_list = [j.text() for j in items]          
        return(txt_list)        
                
# =============================================================================
#     INFORMATION lOAD IN
# =============================================================================                       
                
       

# =============================================================================
#     CLOSING
# =============================================================================     


    def finish(self):
        self.writeoutput_variables()












         