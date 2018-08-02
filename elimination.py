# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 08:20:50 2018

@author: Richard
"""
"""
([bracket number, round, match (game number for round), player1, player2, score],
 [                                      etc                                  ])
"""

#TODO colour winner - idea by tbenedict
import json
from random import randint, shuffle
from vm_py import shell_exe, color
from subprocess import call
import sys

class Elimination(object):
    #Todo -- add 3rd place and multi elim
    def __init__(self):
        super(Elimination, self).__init__() 
        self.table = []
        self.open_file()
        self.load_variables()
        self.generate_player_list()
        self.generate_table()
        
        
    def open_file(self):
        with open("data.tour", 'r') as file:
            self.ui_data_file = json.load(file)
    
    def load_variables(self):
        self.num_brackets = self.ui_data_file.get('num_brackets', 1)
        self.data_player_list = self.ui_data_file.get("player_selected_list")
        self.seed_type = self.ui_data_file.get('seed_type', 'none')
        self.third_place = self.ui_data_file.get('third_place', 0)
        self.amount_replay = self.ui_data_file.get("amount_games", 1)
        self.win_point = self.ui_data_file.get("win_score", 1)
        self.loss_point = self.ui_data_file.get("loss_score", 0)
        self.print_update_type = self.ui_data_file.get("print_type", "tour")
        if self.data_player_list == "":
            print("Error, player list was empty")
            sys.exit()
        return


    def number_of_bye(self, player_list):
        self.num_rounds = 1
        power = 2
        num_players = len(player_list)
        while (power < num_players):
            self.num_rounds += 1
            power *= 2
        num_bye = power - num_players
        return num_bye
        
    def add_bye(self, player_list):
        new_list = player_list
        num_bye = self.number_of_bye(player_list)
        insert = 2
        side = 1
        while (num_bye > 0):
            insert_pos = insert * side
            if side == 1:
                new_list.insert(insert_pos - 1, "BYE")
            else:
                new_list.insert(insert_pos + 1, "BYE")
            if side == -1:
                insert += 2
            side *= -1
            num_bye -= 1
            
        return(new_list)          
        
    def generate_player_list(self):
        self.player_list = self.data_player_list
        if (self.seed_type == 'random'):
            shuffle(self.player_list)
  
      
    def generate_table(self):
        self.bye_player_list = self.add_bye(self.player_list)

#        print("player list:", self.player_list)
#        print("player list with bye:", self.bye_player_list)
#        print("number of rounds", self.num_rounds)
        match_num = 0
        len_playlist = len(self.bye_player_list)
#        for match_up in range(0, len_playlist // 2):
#            match = {"bracket_num": 0, "round":0, "match":match_up, "score":(0,0),
#                     "player1":self.bye_player_list[match_num],
#                     "player2":self.bye_player_list[match_num + 1]}
#            match_num += 2
#            self.table.append(match)
            
        for braket_num in range(0, self.num_brackets):
#            if braket_num > 0:
#                len_playlist = len_playlist // 2
            bracket_len_playlist = len_playlist
            
            for round_num in range(0,self.num_rounds):
                if round_num > 0:
                    bracket_len_playlist = bracket_len_playlist // 2
                match_num = 0
                
                for match_up in range(0, bracket_len_playlist // 2):                 
                    if (braket_num == 0 and round_num == 0):
                        match = {"bracket_num": 0, "round":0, "match":match_up, "score":(0,0),
                                 "player1":self.bye_player_list[match_num],
                                 "player2":self.bye_player_list[match_num + 1]}
                    else:
                        match = {"bracket_num": braket_num, "round":round_num, "match":match_up,
                                 "score":(0,0), "player1": "", "player2": ""}
                    match_num += 2
                    self.table.append(match)
                
            
        if (self.third_place and self.num_brackets == 1):
            self.num_brackets += 1
            self.table.append({"bracket_num": 1, "round": self.num_rounds - 2, "match": 2,
                     "score":(0,0), "player1": "", "player2": ""})
            self.table.append({"bracket_num": 1, "round": self.num_rounds - 1, "match": 1,
                     "score":(0,0), "player1": "", "player2": ""})
            





# =============================================================================
#   PLAY GAMES
# =============================================================================

    def play_tournament(self):
        self.print_result()
        for round_num in range(0,self.num_rounds):
 #           print("\n~Playing round~:", round_num)
            self.play_round(round_num)
            
    def play_round(self, round_num):
        if self.print_update_type in ["round", "match"]:
            self.print_result()
#        group_matches = [group for group in self.table if (group['group_num'] == group_num)]     
#        max_round = max([x['round'] for x in group_matches])
        for bracket_num in range(self.num_brackets):
#            print("\nPlaying in bracket:", bracket_num)
            self.play_bracket_round(bracket_num, round_num)


    def play_bracket_round(self, bracket_num, round_num):     
        match_list = [match for match in self.table if
                      (match['bracket_num'] == bracket_num and match['round'] == round_num)]
      #  print(match_list)
        #match_list = [x for x in robinround if (x['round_num'] == round_num)]
        for match_num, match in enumerate(match_list):
#            print("Playing match:", match_num)
            self.play_match(match, match_num)
            
    def play_match(self, match, match_num):
#        print("Details:")
#        print(match)
        if self.print_update_type in ["match"]:
            self.print_result()
        result = self.play_game(match['player1'], match['player2'])
        match['score'] = tuple(result)
       # print("postmatch", match)
        self.update_table(match)

    
    def play_game(self, player1, player2):
        scores = [0,0]
        if player2 == 'BYE' or player1 == 'BYE':
            return(scores)

        for i in range(self.amount_replay):
            score_game = shell_exe(player1, player2)
            if (len(score_game) != 2):
                print("Bad result from game")
            else:
                if score_game[0] > score_game[1]:
                    scores[0] += self.win_point
                    scores[1] += self.loss_point
                else:
                    scores[1] += self.win_point
                    scores[0] += self.loss_point
        return (scores)
    
    
    def update_table(self, match_dict):
        winner_matchto_update = [match for match in self.table if
                      (match['bracket_num'] == match_dict.get('bracket_num') and 
                       match['round'] == (match_dict.get('round') + 1) and
                       match['match'] == (match_dict.get('match') // 2))]
        
                     
        if len(winner_matchto_update) > 1:
            print("Error: more than potential match to update")
        elif (len(winner_matchto_update) == 0) and ((match_dict.get('round') + 1) == self.num_rounds):
#            print("not an issue")
            pass
        elif (len(winner_matchto_update) == 0):
           print("Error: no match to update found",match_dict)
            
        else:
            winner_matchto_update = winner_matchto_update[0]
            match_score = match_dict.get('score')
            #get player that won
            if match_dict.get('player1') in [None, "", "BYE"]:
                new_player = match_dict.get('player2')
            elif match_dict.get('player2') in [None, "", "BYE"]:
                new_player = match_dict.get('player1')
            else:
                if match_score[0] > match_score[1]:
                    new_player = match_dict.get('player1')
                else:
                    new_player = match_dict.get('player2')
            #put in correct player spot    
            if match_dict.get('match') % 2 == 0:
                winner_matchto_update['player1'] = new_player
            else:
                winner_matchto_update['player2'] = new_player

        

        #Todo fix for multi elim
        loser_matchto_update = [match for match in self.table if
                      (match['bracket_num'] == (1) and 
                       (match['round'] == match_dict.get('round')))]               
        if len(loser_matchto_update) > 1:
#            print("Error: more than potential match to update")
            pass
        elif (len(loser_matchto_update) == 0) and ((match_dict.get('round') + 1) == self.num_rounds):
#            print("not an issue")
            pass
        elif (len(loser_matchto_update) == 0):
           #print("Error: no match to update found",match_dict)
           pass
            
        else:
            #print("no loser error")
            loser_matchto_update = loser_matchto_update[-1]
            match_score = match_dict.get('score')
            #get player that won
            if match_dict.get('player1') in [None, "", "BYE"]:
                new_player = match_dict.get('player2')
            elif match_dict.get('player2') in [None, "", "BYE"]:
                new_player = match_dict.get('player1')
            else:
                if match_score[0] < match_score[1]:
                    new_player = match_dict.get('player1')
                else:
                    new_player = match_dict.get('player2')
            #put in correct player spot    
            if match_dict.get('match') % 2 == 0:
                loser_matchto_update['player1'] = new_player
            else:
                loser_matchto_update['player2'] = new_player
        #print("loser_matchto_update", loser_matchto_update)
                

# =============================================================================
#   DO ALL THE PRINTING HERE
# =============================================================================

    def print_result(self, table = 0):
        """print tabulate results"""
        call('clear', shell=True)
        if table:
            print("~~~TABLE~~~")
            print(self.table)
            print("")
        for bracket_num in range(self.num_brackets):
            print("  Bracket_num:", bracket_num)
            self.print_bracket(bracket_num)

    def print_bracket(self, bracket_num):
        bracket_strings = []
        delta = 1
        bracket_matches = [mtch for mtch in self.table if mtch['bracket_num'] == 0]

        for round_num in range(self.num_rounds):
            round_match = [mtch for mtch in bracket_matches if mtch['round'] == round_num]
            if round_num == 0:
                for match in round_match:
                    bracket_strings.append('{:^7}'.format(match['player1'][:5]) + "\\")
                    bracket_strings.append('{:^9}'.format(""))
                    bracket_strings.append('{:^7}'.format(match['player2'][:5]) + "/")
                    bracket_strings.append('{:^9}'.format(""))
            else:
                index = delta - 1
                for match in round_match:
                    bracket_strings[index] += ('{:^7}'.format(match['player1'][:5]) + "\\")
                    index += delta
                    bracket_strings[index] += ('{:^9}'.format(""))
                    index += delta
                    bracket_strings[index] += ('{:^7}'.format(match['player2'][:5]) + "/")
                    index += delta
                    bracket_strings[index] += ('{:^9}'.format(""))
                    index += delta
            delta *= 2


        #add winner
        winner_match = [mtch for mtch in bracket_matches if mtch['round'] == self.num_rounds - 1]
        winner_match = winner_match[0]
        index = delta - 1
        if (winner_match['player1'] in [None, "", "BYE"] or winner_match['player2'] in [None, "", "BYE"] or winner_match['score'] == (0,0)):
            bracket_strings[index] += '{:^7}'.format("")
        elif winner_match['score'][0] > winner_match['score'][1]:
            bracket_strings[index] += '{:^7}'.format(winner_match['player1'][:5])
        else:
            bracket_strings[index] += '{:^7}'.format(winner_match['player2'][:5])

        for string in bracket_strings:
            print(string)
        return

    def calculate_winner(self):
        self.print_result()
        print("Winner of bracket number:", "0")
        bracket_matches = [mtch for mtch in self.table if mtch['bracket_num'] == 0]
        winner_match = [mtch for mtch in bracket_matches if mtch['round'] == self.num_rounds - 1]
        winner_match = winner_match[0]

        if winner_match['score'][0] > winner_match['score'][1]:
            winner = winner_match['player1']
        else:
            winner = winner_match['player2']
        print(color.green, "", winner, color.end)