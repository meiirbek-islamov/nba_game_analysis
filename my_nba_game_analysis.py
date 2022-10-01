import re

with open("nba_game_warriors_thunder_20181016.txt", 'r') as reader:
    lines = []
    for line in reader:
        lines.append(line.strip()) 

def all_players(play_by_play):
    players = {}
    for play in play_by_play:
        player_search = re.findall("[^\x00-\x7F].\.\s[a-zA-Z]+|\w\.\s[a-zA-Z]+", play["description"])  #\w\.\s[a-zA-Z]+
        for player in player_search:
            if player not in players.keys():
                players[player] = {"player_name": player, "FG": 0, "FGA": 0, 
                "FG%": None, "3P": 0, "3PA": 0, "3P%": None, 
                "FT": 0, "FTA": 0, "FT%": None, "ORB": 0, 
                "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, 
                "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
                
    return players

def analyse_nba_game(play_by_play_moves):
    
    keys = ["period", "remaining_sec","relevant_team", "away_team", 
            "home_team", "away_score", "home_score","description"]
    
    home_players = ['K. Durant', 'D. Green', 'S. Curry', 
                    'D. Jones', 'K. Thompson', 'K. Looney', 
                    'A. Iguodala','Q. Cook', 'S. Livingston', 
                    'A. McKinnie', 'J. Jerebko', 'J. Bell']
    
    away_players = ['P. George', 'S. Adams', 'D. Schr', 'P. Patterson', 
                    'T. Ferguson', 'N. Noel', 'R. Felton', 
                    'J. Grant', 'Á. Abrines', 'H. Diallo']
    
    dic = {}
    dic["home_team"] = {}
    dic["away_team"] = {}
    dic["home_team"]["name"] = play_by_play_moves[0].split("|")[4]
    dic["away_team"]["name"] = play_by_play_moves[0].split("|")[3]
    dic["home_team"]["players_data"] = []
    dic["away_team"]["players_data"] = []
    
    mvs = [{k:v for (k, v) in zip(keys, row.split('|'))} for row in play_by_play_moves]
    players = all_players(mvs)
    
    for mv in mvs:
        player_search = re.findall("[^\x00-\x7F].\.\s[a-zA-Z]+|\w\.\s[a-zA-Z]+", mv["description"])  #\w\.\s[a-zA-Z]+
        
        if len(player_search) == 0:
            continue
            
        fg_search = re.search("(misses|makes)\s\d-pt", mv["description"])
        
        ft_search = re.search("(misses|makes)\D+free\sthrow", mv["description"])
        
        if fg_search:
            players[player_search[0]]['FGA'] += 1
            if fg_search.group().find("3") != -1:
                players[player_search[0]]['3PA'] += 1
                if fg_search.group().find("makes") != -1:
                    players[player_search[0]]['FG'] += 1
                    players[player_search[0]]['3P'] += 1
                    players[player_search[0]]['PTS'] += 3
                    
            elif fg_search.group().find("makes") != -1:
                players[player_search[0]]['FG'] += 1
                players[player_search[0]]['PTS'] += 2
        
        if ft_search:
            players[player_search[0]]['FTA'] += 1
            if ft_search.group().find("makes") != -1:
                players[player_search[0]]['FT'] += 1
                players[player_search[0]]['PTS'] += 1
                
        # FG%, 3P%, FT%
        if players[player_search[0]]['FGA'] != 0:
            players[player_search[0]]['FG%'] = round(players[player_search[0]]['FG']/players[player_search[0]]['FGA'], 3)
            
        if players[player_search[0]]['3PA'] != 0:
            players[player_search[0]]['3P%'] = round(players[player_search[0]]['3P']/players[player_search[0]]['3PA'], 3)
            
        if players[player_search[0]]['FTA'] != 0:
            players[player_search[0]]['FT%'] = round(players[player_search[0]]['FT']/players[player_search[0]]['FTA'], 3)
        
        # Search for ORB, DRB, TRB
        rb_search = re.search("(Offensive|Defensive)\srebound\s+by", mv["description"])
        if rb_search:
            players[player_search[0]]['TRB'] += 1
            if rb_search.group().find("Offensive") != -1:
                players[player_search[0]]['ORB'] += 1
            elif rb_search.group().find("Defensive") != -1:
                players[player_search[0]]['DRB'] += 1

        # Search for ORB, DRB, TRB, AST, STL, BLK, TOV, PF
        as_search = re.search("assist|block|(Turnover(.*))|foul", mv["description"])
        if as_search:
            if as_search.group().find("assist") != -1:
                players[player_search[1]]['AST'] += 1
            elif as_search.group().find("block") != -1:
                players[player_search[1]]['BLK'] += 1
            elif as_search.group().find("Turnover") != -1:
                players[player_search[0]]['TOV'] += 1
                if as_search.group().find("steal") != -1:
                    players[player_search[1]]['STL'] += 1
            elif as_search.group().find("foul") != -1:
                players[player_search[0]]['PF'] += 1
    
    for key, value in players.items():
        if key in home_players:
            dic["home_team"]["players_data"].append(value)
        else:
            dic["away_team"]["players_data"].append(value)
            
    # Total 
    
    total_home = {"FG": 0, "FGA": 0, 
                "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, 
                "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, 
                "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, 
                "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
    
    total_away = {"FG": 0, "FGA": 0, 
                "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, 
                "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, 
                "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, 
                "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
    
    for key, value in players.items():
        if key in home_players:
            for param, score in value.items():
                if isinstance(score, int):
                    total_home[param] += score
                    
        if key in away_players:
            for param, score in value.items():
                if isinstance(score, int):
                    total_away[param] += score
                    
    total_home["FG%"] = round(total_home["FG"]/total_home["FGA"], 3)
    total_home["3P%"] = round(total_home["3P"]/total_home["3PA"], 3)
    total_home["FT%"] = round(total_home["FT"]/total_home["FTA"], 3)
    
    total_away["FG%"] = round(total_away["FG"]/total_away["FGA"], 3)
    total_away["3P%"] = round(total_away["3P"]/total_away["3PA"], 3)
    total_away["FT%"] = round(total_away["FT"]/total_away["FTA"], 3)
    
    dic["home_team"]["total_score"] = total_home
    dic["away_team"]["total_score"] = total_away
    
    return dic

dic = analyse_nba_game(lines)
print(dic)

def print_nba_game_stats(team_dic): 
    print("players", end=" ")
    for i in range(1, len(team_dic["home_team"]["players_data"][0].keys())):
        print(list(team_dic["home_team"]["players_data"][0].keys())[i], end=" ")
    print()
    
    for j in team_dic["home_team"]["players_data"]:
        values_list = list(j.values())
        for k in values_list:
            print(k, end=" ")
        print()
        
    print("Team Totals", end=" ")
    for j in list(team_dic["home_team"]["total_score"].values()):
        print(j, end=" ")
    print()

    for j in team_dic["away_team"]["players_data"]:
        values_list = list(j.values())
        for k in values_list:
            print(k, end=" ")
        print()
    
    print("Team Totals", end=" ")
    for j in list(team_dic["away_team"]["total_score"].values()):
        print(j, end=" ")
    print()
    
print(print_nba_game_stats(dic))