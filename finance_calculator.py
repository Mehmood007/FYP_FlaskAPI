def calculate_team_price(players):
    total_players_expense = 0
    for player in players:
        total_players_expense += player['price']

    return total_players_expense


def players_within_budget(players,budget):
    total_team_expense = calculate_team_price(players)
    if budget >= total_team_expense:
        return True
    return False



def performance_to_budget_ratio(player):
    batting_score = player_score(player["batting_avg"],player["batting_sr"])
    bowling_score = player_score(player["bowling_average"],player["bowling_sr"])

    budget = player["price"]
    batting_budget_ratio = 0
    bowling_budget_ratio = 0
    if batting_score != 0:
        batting_budget_ratio = batting_score/budget
    if bowling_score != 0:
        bowling_budget_ratio = (1/bowling_score)/budget

    return batting_budget_ratio,bowling_budget_ratio



def check_validity(current_budget,player_price):
    if player_price<current_budget:
        return True
    return False


def player_score(avg,sr):
    return avg*sr