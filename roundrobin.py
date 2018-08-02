# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:51:56 2018

@author: Richard
"""

import json
from random import randint, shuffle
from vm_py import shell_exe, color
from subprocess import call
import sys, os

""" -----
Example of game table

([group number, round, match (game number for round), player1, player2, score],
 [                                      etc                                  ])
"""

class color:
    end = "\033[0m"
    black = "\033[0;30m"
    blackb = "\033[1;30m"
    white = "\033[0;37m"
    whiteb = "\033[1;37m"
    red = "\033[0;31m"
    redb = "\033[1;31m"
    green = "\033[0;32m"
    greenb = "\033[1;32m"
    yellow = "\033[0;33m"
    yellowb = "\033[1;33m"
    blue = "\033[0;34m"
    blueb = "\033[1;34m"
    purple = "\033[0;35m"
    purpleb = "\033[1;35m"
    lightblue = "\033[0;36m"
    lightblueb = "\033[1;36m"
class RoundRobin(object):
    
    def __init__(self):
        super(RoundRobin, self).__init__() 
        self.table = []
        self.score = {}
        self.open_file()
        self.load_variables()
        self.generate_player_list()
        self.generate_table()
        
        for player in self.data_player_list:
            self.score[player] = 0
        
        
    def open_file(self):
        with open("data.tour", 'r') as file:
            self.ui_data_file = json.load(file)
    
    def load_variables(self):
        if self.ui_data_file.get('multi_groups', False):
            self.num_groups = self.ui_data_file.get('num_groups', 1)
        else:
            self.num_groups = 1
        self.data_player_list = self.ui_data_file.get("player_selected_list")
        self.seed_type = self.ui_data_file.get('seed_type', 'none')
        self.amount_replay = self.ui_data_file.get("amount_games", 1)
        self.win_point = self.ui_data_file.get("win_score", 1)
        self.loss_point = self.ui_data_file.get("loss_score", 0)
        self.print_update_type = self.ui_data_file.get("print_type", "tour")
        if self.data_player_list == "":
            print("Error, player list was empty")
            sys.exit()
            
    def generate_player_list(self):
        self.player_list = self.data_player_list
        if (self.seed_type == 'random'):
            shuffle(self.player_list)

    def group_players(self, player_list):
        final_list = []
        player_per_group = len(player_list) // self.num_groups
        extra_players = len(player_list) % self.num_groups
        
        for groupnum in range(self.num_groups):
            group_list = []
            for i in range(player_per_group):
                #this add the first x players to group then the next set
                group_list.append(player_list[i + player_per_group * groupnum])
            final_list.append(group_list)
        
        #adding any extra players
        for j in range(extra_players):
            final_list[j].append(player_list[-(j+1)])
        return final_list       

  
      
    def generate_table(self):
        self.player_list = self.group_players(self.player_list)
#        print("player list:", self.player_list)
        for group_num, group in enumerate(self.player_list):
            if len(group) % 2 == 1:
                group.append("BYE")
 
            num_players_in_group = len(self.player_list[group_num])
#            print("group is", group)
#            print("num players is", num_players_in_group)
            schedule = self.match_up_numbers(num_players_in_group)
            
            for round_num, robinround in enumerate(schedule):
                for match_num, matchup in enumerate(robinround):

                    match = {"group_num":group_num, "round":round_num, "match":match_num, "score":(0,0),
                             "player1":self.player_list[group_num][matchup[0]],
                             "player2":self.player_list[group_num][matchup[1]]}
                    self.table.append(match)


    def match_up_numbers(self,num_teams): 
        teams = list(range(num_teams))
        match_ups = []
        rounds = len(teams) - 1

        for turn in range(rounds):
            pairings = []
            for i in range(int(len(teams) / 2)):
                pairings.append((teams[i], teams[len(teams) - i - 1]))
            teams.insert(1, teams.pop()) #rotate teams by 1
            match_ups.append(pairings)
#        print(match_ups)

        return match_ups


    def calc_score(self, player):
        match_list = [match for match in self.table if (match['player1'] == player or match['player2'] == player)]
        net_score = 0
        for match in match_list:
            if match['player1'] == player:
                net_score += match['score'][0]
            else:
                net_score += match['score'][1]

        self.score[player] = net_score
        return net_score


# =============================================================================
#   PLAY GAMES
# =============================================================================

    def play_tournament(self):
        self.print_result()
        for group_num, group in enumerate(self.player_list):
            print("Playing group:", group_num, group)
            self.play_group(group_num)
            
    def play_group(self, group_num):
        group_matches = [group for group in self.table if (group['group_num'] == group_num)]
        max_round = max([x['round'] for x in group_matches])
        for round_num in range(max_round + 1):
            print("Playing round:", round_num)          
            self.play_round(group_num, round_num)
#            self.print_result()

    def play_round(self, group_num, round_num):
        if self.print_update_type in ["round", "match"]:
            self.print_result()
        match_list = [match for match in self.table if
                      (match['group_num'] == group_num and match['round'] == round_num)]
        for match_num, match in enumerate(match_list):
            #print("Playing match:", match_num)
            self.play_match(match, match_num)
            
    def play_match(self, match, match_num):
        if self.print_update_type in ["match"]:
            self.print_result()
        result = self.play_game(match['player1'], match['player2'])
        match['score'] = tuple(result)
        #print("result was:", result)

        
    def play_game(self, player1, player2):
        scores = [0,0]
        if player2 == 'BYE' or player1 == 'BYE':
            return(scores)

        for i in range(self.amount_replay):
            score_game = shell_exe(player1, player2)
            if (len(score_game) != 2):
                print(color.red, "Bad result from game", color.end)
            else:
                if score_game[0] > score_game[1]:
                    scores[0] += self.win_point
                    scores[1] += self.loss_point
                else:
                    scores[1] += self.win_point
                    scores[0] += self.loss_point
        return (scores)



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
        for group_num, group in enumerate(self.player_list): 
            print(" GROUP:", group_num)
            self.print_group(group)

    def print_group(self, player_group):
        num_players = len(player_group)
        if player_group[-1] == 'BYE':
            num_players -= 1
        self.print_topline(num_players)
        self.print_player_line(player_group)

        for player in player_group:
            if player == 'BYE':
                continue
            self.print_line(num_players)            
            string = [""]
            string.append('{:>7}'.format(player[:6]))
            player_matches = [x for x in self.table if (x["player1"] == player or x["player2"] == player)]

            for player2 in player_group:
                if player2 == player:
                    string.append('{: ^7}'.format("X"))
                    continue
                elif player2 == "BYE":
                    continue  
                match = [x for x in player_matches if (x["player1"] == player2 or x["player2"] == player2)]
                match = match[0]
                score = match['score']
                if match['player1'] == player:
                    score_str = '{: ^7}'.format(str(score[0]))
                else:
                    score_str = '{: ^7}'.format(str(score[1]))
                string.append(score_str)
            
            score = self.calc_score(player)
            string.append('{:^7}'.format(str(score)))   
            string.append("")
            string = "│".join(string)
            print(string)
            
        self.print_bottomline(num_players)


    def print_player_line(self, player_group):
        string = ["","       "]
        for player in player_group:
            if player != "BYE":
                string.append('{:^7}'.format(player[:5]))
        string.append('{:^7}'.format("SCORE"))
        string.append("")
        string = "│".join(string)
        print(string)

    def print_line(self, length):
        print('├───────┼', end='')
        for i in range(length):
            print('───────┼', end='')
        print("───────┤")

    def print_topline(self, length):
        print('┌───────┬', end = '')
        for i in range(length):
            print('───────┬', end='')
        print("───────┐")
        
    def print_bottomline(self, length):
        print('└───────┴', end = '')
        for i in range(length):
            print('───────┴', end='')
        print("───────┘")


# =============================================================================
#   CALCULATE WINNER
# =============================================================================

    def calculate_winner(self):
        self.print_result()
        for group_num, group in enumerate(self.player_list):
            print("Winner of group:", group_num)
            self.group_winner(group)

    def group_winner(self, group):
        score_list = {key: value for key, value in self.score.items() if key in group}

        maxv = max(score_list.values())
        winner_list = [key for key, val in score_list.items() if val == maxv]
        if len(winner_list) == 1:
            print(color.green, winner_list[0], color.end)
        elif len(winner_list) == 2:
            print("  There was a tie between:", winner_list[0], "and", winner_list[1])
            self.tie_break(winner_list)
        else:
            print("  There were multiple winners, they are:")
            for winner in winner_list:
                print("    ",color.green, winner, color.end)

    def tie_break(self, winner_list):
        match = [x for x in self.table if (x["player1"] == winner_list[0] and x["player2"] == winner_list[1]
                                        or x["player1"] == winner_list[1] and x["player2"] == winner_list[0])]
        if len(match) == 1:
            match = match[0]
            score = match['score']
            if score[0] > score[1]:
                winner = match['player1']
            else:
                winner = match['player2']
            print("    The tie was broken and the winner is:", color.green, winner, color.end)
