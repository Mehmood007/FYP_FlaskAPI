import pre_processing
import players_data
def retention_suggestion(data):
    squad = data['squad']
    if len(squad)<14:
        return {'message':'Your squad is incomplete first complete squad'}

    top_batters = []
    top_bowlers = []
    for player in squad:
        top_batters = sort_batters(player,top_batters)
        top_bowlers = sort_bowlers(player,top_bowlers)

    
    suggested = []

    suggested.extend(top_batters[:4])

    for i in range(4):
        for j in range(len(top_bowlers)):
            if suggested[i]['playerid']==top_bowlers[j]['playerid']:
                top_bowlers.remove(top_bowlers[j])
                break
    
    suggested.extend(top_bowlers[:4])

    only_ids = []
    for player in suggested:
        only_ids.append(player['playerid'])

    suggested = []
    for player in squad:
        if player['playerid'] in only_ids:
            suggested.append(player)
    

    

    return suggested

    

def worth_wrt_price(player_score,amount):
    return player_score/amount



def sort_batters(player,sorted_batters):
    player_score = player["batting_avg"]*player["batting_sr"]
    player_score = worth_wrt_price(player_score,player['price'])
    for index, batter in enumerate(sorted_batters):
        if batter["score"]<player_score:
            sorted_batters.insert(index,{"playerid":player["playerid"],"score":player_score})
            return sorted_batters
    sorted_batters.append({"playerid":player["playerid"],"score":player_score})
    return sorted_batters


def sort_bowlers(player,sorted_bowllers):
    player_score = player["bowling_average"]*player["bowling_sr"]
    player_score = player_score*player['price']
    if player_score!=0:
        for index, bowler in enumerate(sorted_bowllers):
            if bowler["score"]>player_score:
                sorted_bowllers.insert(index,{"playerid":player["playerid"],"score":player_score})
                return sorted_bowllers
            if bowler["score"]==0:
                sorted_bowllers.insert(index,{"playerid":player["playerid"],"score":player_score})
                return sorted_bowllers
            
    sorted_bowllers.append({"playerid":player["playerid"],"score":player_score})
    return sorted_bowllers


def get_psl_stats(player):
    stats = player['stats']