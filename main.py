from flask import Flask,jsonify
from flask import request
import players_data
import players_comparison
import user_management
import draft
import dls_calculator
import playing_xi
import player_retention
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


'''
BELOW ROUTES ARE JUST FOR FANS
'''
@app.route("/allplayers")
def allplayers():
    return jsonify(players_data.all_players())



@app.route("/top_players")
def top_players():
    return jsonify(players_data.get_top_players())



@app.route("/getPlayer/<string:playerid>")
def players_details(playerid):
    return jsonify(players_data.player_details(playerid))


@app.route("/get_player_summary/<string:playerid>")
def player_summary(playerid):
    return jsonify(players_data.get_player_summary(playerid))


@app.route("/compare_players/<string:player1>/<string:player2>")
def player_comparison(player1,player2):
    players_details = players_comparison.compare_two_players(player1,player2)
    return jsonify(players_details)


@app.route("/head-to-head/<string:batsman>/<string:bowler>")
def comparison(batsman,bowler):
    return jsonify(players_comparison.head_to_head(batsman,bowler))




'''
BELOW ROUTES ARE FOR FRANCHISE
'''
@app.route("/franchiseSignUp", methods = ['POST'])
def signUp():
    franchise_details = request.get_json()
    if user_management.signup_new_franchise(franchise_details):
        return jsonify({"message":"User Signed UP successfully"})
    return jsonify({"message":"Error in signing up franchise"})


@app.route("/franchiseLogin", methods = ['POST'])
def login():
    login_credentials = request.get_json()
    login = user_management.login_franchise(login_credentials)
    if login:
        return jsonify(login)
    return jsonify({"message":"Error in signing up franchise"})


@app.route("/logout", methods = ['POST'])
def logout():
    session_id = request.get_json()['session_id']
    user_management.logout(session_id)
    return jsonify({'Message':"Logged out succesfully"})


@app.route("/verify_franchise/<string:session_id>")
def verify_franchise(session_id):
    if user_management.verify_franchise_session(session_id):
        return jsonify(user_management.franchise_credentials(session_id))
    
    return jsonify({"message":"User not authorized for this request"})


@app.route("/all_drafts")
def all_drafts():
    drafts_list = players_data.all_drafts()
    try:
        session = request.headers['session_id']
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            if drafts_list:
                return jsonify(drafts_list)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})


@app.route("/draft_players/<string:draft_id>")
def draft_players(draft_id):
    players_list = players_data.draft_details(draft_id)
    try:
        session = request.headers['session_id']
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            if players_list:
                return jsonify(players_list)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})


@app.route("/select_draft/<string:draft_id>")
def select_draft(draft_id):
    try:
        session = request.headers['session_id']
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            draft_players = user_management.select_draft(draft_id,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})


@app.route("/select_player", methods = ['POST'])
def select_player():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            draft_players = user_management.select_player(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})


@app.route("/drop_player", methods = ['POST'])
def drop_player():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = user_management.drop_player(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})



@app.route("/change_availability", methods = ['POST'])
def change_availability():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = user_management.change_availability(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})





@app.route("/reject_player", methods = ['POST'])
def reject_player():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            draft_players = user_management.reject_player(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})




@app.route("/suggest_players", methods = ['POST'])
def suggest_players():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            suggested_players = draft.suggest_players(data)
            return jsonify(suggested_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    


@app.route("/suggest_player_xi", methods = ['POST'])
def suggest_player_xi():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            suggested_player = playing_xi.suggest_player(data)
            return jsonify(suggested_player)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})



@app.route("/playing_xi_alternate", methods = ['POST'])
def playing_xi_alternate():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = playing_xi.suggest_alternate(data)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})



@app.route("/select_playing_xi_player", methods = ['POST'])
def select_playing_xi_player():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = user_management.select_playing_xi_player(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})



@app.route("/drop_playing_xi_player", methods = ['POST'])
def drop_playing_xi_player():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = user_management.drop_playing_xi_player(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})
    
    return jsonify({"message":"No such draft exists"})


@app.route("/suggest_retention", methods = ['POST'])
def suggest_retention():
    
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = player_retention.retention_suggestion(data)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    
        return jsonify({"message":"User not authorized for this request"})
    
  

@app.route("/select_retention", methods = ['POST'])
def select_retention():
    
        session = request.headers['session_id']
        data = request.get_json()
        if user_management.verify_franchise_session(session):
            draft_players = user_management.select_retention(data,session)
            if draft_players:
                return jsonify(draft_players)
        else:
            return jsonify({"message":"User not authorized for this request"})
    
        return jsonify({"message":"User not authorized for this request"})
    
  

@app.route("/dl_calculator", methods = ['POST'])
def dl_calulator():
    try:
        session = request.headers['session_id']
        data = request.get_json()
        
        if user_management.verify_franchise_session(session) or user_management.verify_admin_session(session):
            par_score = dls_calculator.required_score(int(data["team1Score"]),int(data["oversRemaining"]),int(data["wickets_in_hand"]))
            return jsonify({"required_score":par_score})
        else:
            return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})

'''
BELOW ROUTES ARE FOR ADMIN
'''
@app.route("/add_new_player", methods = ['POST'])
def new_player_info():
    try:
        session = request.headers['session_id']
        if user_management.verify_admin_session(session):
            data = request.get_json()
            return players_data.add_new_player_info(data)
        return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})



@app.route("/set_top_players")
def set_top_players():
    try:
        session = request.headers['session_id']
        if user_management.verify_admin_session(session):
            top_players = players_data.set_top_players()
            return jsonify(top_players)
        return jsonify({"message":"User not authorized for this request1"})
    except:
        return jsonify({"message":"User not authorized for this request"})


@app.route("/venues")
def get_venues():
    try:
        session = request.headers['session_id']
        if user_management.verify_admin_session(session):
            return jsonify(user_management.get_venues())
        return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})


@app.route("/add_new_venue", methods = ['POST'])
def add_new_venue():
    try:
        session = request.headers['session_id']
        if user_management.verify_admin_session(session):
            data = request.get_json()
            return user_management.add_new_venue(data)
        return jsonify({"message":"User not authorized for this request"})
    except:
        return jsonify({"message":"User not authorized for this request"})


#Below route is just for testing purpose and should be eliminated at time of deploy
@app.route("/check/<string:draft_id>")
def alternates(draft_id):
    player_stats = players_data.draft_details(draft_id)
    suggested_players = draft.suggest_players_from_scratch(player_stats)
    return jsonify(suggested_players)


@app.route("/check")
def drafting_player():
    player_stats = players_data.draft_details("draft_22")
    data = {
        "category":"Platinium",
        "role":"All-Rounder",
        "p_type":"Local",
        "speciality":"Economical",
        "draft":player_stats
    }
    
    suggested_players = draft.suggest_players(data)
    return jsonify(suggested_players)

if __name__ == "__main__":
    app.run(debug=True)
