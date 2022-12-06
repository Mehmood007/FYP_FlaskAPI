import flask_pymongo
import json
from bson import json_util
import uuid
import players_data
import league_constraints
import players_availability
import finance_calculator

#Connection with Database
try:
    #mongo = flask_pymongo.MongoClient("mongodb://localhost:27017/")
    #db = mongo.my_team
    

    mongo = flask_pymongo.MongoClient("mongodb://my_team:X3Njg1cRrj9QT5Ks@ac-ga3haug-shard-00-00.59spobs.mongodb.net:27017,ac-ga3haug-shard-00-01.59spobs.mongodb.net:27017,ac-ga3haug-shard-00-02.59spobs.mongodb.net:27017/?ssl=true&replicaSet=atlas-ugvkvk-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = mongo.my_team
    mongo.server_info()
except:
    print("Error cannot connect to db")


def signup_new_franchise(franchise_details):
    franchise_details = franchise_details
    franchise_details["draft"] = players_data.draft_details()
    franchise_details["team"] = []
    franchise_details["playing_xi"] = []
    db.franchises.insert_one(franchise_details)
    return True


def login_franchise(login_credentionals):
    franchise = db.franchises.find({"franchise_id":login_credentionals['franchise_id'],'password':login_credentionals['password']})
    session_frechise = db.sessions.find({'user_id':login_credentionals['franchise_id']})
    try:
        franchise = parse_json(franchise[0])
        session = dict(franchise['_id'])['$oid']+str(len(parse_json(session_frechise)))+str(uuid.uuid4())
        db.sessions.insert_one({'session_id':session,'user_previliges':'franchise',"user_id": franchise["franchise_id"]})
        franchise['session_id'] = session
        return franchise
    except IndexError:
        return False



def logout(session_id):
    db.sessions.delete_many({'session_id':session_id})
    return True



def verify_franchise_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'franchise':
            return True
        return False

    except IndexError:
        return False


def franchise_credentials(session_id):
    session_details = db.sessions.find({'session_id':session_id})
    try:
        franchise_id = parse_json(session_details[0])["user_id"]
        franchise_details  = parse_json(db.franchises.find({'franchise_id':franchise_id})[0])
        return franchise_details
    except:
        return {"message":"Something is wrong with session id"}


def verify_admin_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'admin':
            return True
        return False

    except IndexError:
        return False


def get_venues():
    return parse_json(db.venues.find({}))


def select_draft(draft_id,session):
    franchise = franchise_credentials(session)

    if franchise['draft'] == "-":
        franchise['draft'] = players_data.draft_details(draft_id)
        db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{"draft":franchise["draft"]})
        return franchise['draft']
    
    return {"message": "User already have selected draft"}



def select_player(data,session):
    player = data['selected_player']
    franchise = franchise_credentials(session)

    
    if not league_constraints.validate_new_player_squad(franchise["team"],player):
        return {'message':"Player from this category can not be picked"}

    if not league_constraints.validate_local_foriegner_squad(franchise["team"],player):
        return {'message':"Player of this type can not be picked"}
    
    if not finance_calculator.check_validity(franchise['budget'],player['price']):
        return {'message':"Player is out of budget"}

    
    franchise['budget'] -= player['price']
    franchise["draft"].remove(next(fplayer for fplayer in franchise['draft'] if fplayer["playerid"] == player['playerid']))
    franchise["team"].append(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"draft":franchise["draft"],"team":franchise["team"],"budget":franchise['budget']}})

    return {"message": "Player added to team"}



def drop_player(data,session):
    player = data['selected_player']
    franchise = franchise_credentials(session)

    franchise['budget'] += player['price']

    franchise["draft"].append(player)
    franchise["team"].remove(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"draft":franchise["draft"],"team":franchise["team"],'budget':franchise['budget']}})

    return {"message": "Player dropped from Squad"}


def select_playing_xi_player(data,session):
    player = data['selected_player']
    franchise = franchise_credentials(session)
    

    if not league_constraints.validate_local_foriegner_xi(franchise['playing_xi'],player):
        return {'message':"Player of this type can not be picked"}

    franchise["playing_xi"].append(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"playing_xi":franchise["playing_xi"]}})

    return {"message": "Player added to team"}



def drop_playing_xi_player(data,session):
    player = data['selected_player']
    franchise = franchise_credentials(session)
    

    franchise["playing_xi"].remove(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"playing_xi":franchise["playing_xi"]}})

    return {"message": "Player dropped from playing XI"}


def change_availability(data,session):
    player = data['selected_player']
    availability = int(data['availability'])
    previous_availability = player['availability']
    if previous_availability=='full':
        previous_availability=13
    
    previous_availability = int(previous_availability)
    player = players_availability.performance_after_partial_availbility(player,availability,previous_availability)
    player['availability'] = data['availability']
    franchise = franchise_credentials(session)
    
    franchise["draft"].remove(next(fplayer for fplayer in franchise['draft'] if fplayer["playerid"] == player['playerid']))
    franchise["draft"].append(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"draft":franchise["draft"]}})

    return {"message": "Player dropped from playing XI"}




def reject_player(data,session):
    player = data['selected_player']
    franchise = franchise_credentials(session)

    franchise["draft"].remove(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"draft":franchise["draft"]}})

    return {"message": "Player deleted from draft"}


def select_retention(data,session):
    players = data['selected_players']
    franchise = franchise_credentials(session)
    not_in_list_players = []
    for player in franchise['team']:
        if player not in players:
            not_in_list_players.append(player)

    for player in not_in_list_players:
        franchise['budget'] += player['price']

        franchise["draft"].append(player)
        franchise["team"].remove(player)
    db.franchises.find_one_and_update({"franchise_id":franchise["franchise_id"]},{'$set':{"draft":franchise["draft"],"team":franchise["team"],'budget':franchise['budget']}})

    return {"message": "Player retained"}



def parse_json(data):
    return json.loads(json_util.dumps(data))


def add_new_venue(data):
    venues = db.venues.find({"name":data['name']})
    try:
        return parse_json(venues[0])
    except IndexError:
        db.venues.insert_one(data)
        return {"message":"Player added successfully"}
