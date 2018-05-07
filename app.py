from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'webuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'correcthorsebatterystaple'
app.config['MYSQL_DATABASE_DB'] = 'FifaTracker'
app.config['MYSQL_DATABASE_HOST'] = '35.227.51.243'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showAddPlayer')
def showAddPlayer():
    return render_template('addPlayer.html')


@app.route('/addPlayer', methods=['POST'])
def addPlayer():
    try:
        _player_name = request.form['playerName']
        # Validate
        if _player_name:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_add_player', (_player_name,))
            data = cursor.fetchall()
            if len(data) == 0:
                conn.commit()
                return json.dumps({'message': '<span>Player added successfully!</span>'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required field</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route("/showAddResult")
def showAddResult():
    # Get all players in the Players table to display in the dropdown.
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Players;")
    data = cursor.fetchall()
    names = []
    for item in data:
        names.append(list(item))
    cursor.close()
    conn.close()

    return render_template("addResult.html", data=names)


@app.route("/addResult", methods=['POST'])
def addResult():
    try:
        _game = request.form['game']
        _home_player = request.form['homePlayer']
        _away_player = request.form['awayPlayer']
        _result = request.form['winner']
        _home_pk = request.form['homePK']
        _away_pk = request.form['awayPK']

        _home_team = request.form['homeTeam']
        _home_stars = request.form['homeStars']
        _away_team = request.form['awayTeam']
        _away_stars = request.form['awayStars']

        _home_goals = request.form['homeGoals']
        _home_shots = request.form['homeShots']
        _home_shotsOT = request.form['homeShotsOnTarget']
        _home_poss = request.form['homePossession']
        _home_tackles = request.form['homeTackles']
        _home_fouls = request.form['homeFouls']
        _home_yellows = request.form['homeYellowCards']
        _home_reds = request.form['homeRedCards']
        _home_injuries = request.form['homeInjuries']
        _home_offsides = request.form['homeOffsides']
        _home_corners = request.form['homeCorners']
        _home_shot_acc = request.form['homeShotAccuracy']
        _home_pass_acc = request.form['homePassAccuracy']

        _away_goals = request.form['awayGoals']
        _away_shots = request.form['awayShots']
        _away_shotsOT = request.form['awayShotsOnTarget']
        _away_poss = request.form['awayPossession']
        _away_tackles = request.form['awayTackles']
        _away_fouls = request.form['awayFouls']
        _away_yellows = request.form['awayYellowCards']
        _away_reds = request.form['awayRedCards']
        _away_injuries = request.form['awayInjuries']
        _away_offsides = request.form['awayOffsides']
        _away_corners = request.form['awayCorners']
        _away_shot_acc = request.form['awayShotAccuracy']
        _away_pass_acc = request.form['awayPassAccuracy']

        # Validation gonna be a long one
        if _game and _home_player and _away_player and _result and _home_team and _home_stars and _away_team and _away_stars and _home_goals and _home_shots and _home_shotsOT and _home_poss and _home_tackles and _home_fouls and _home_yellows and _home_reds and _home_injuries and _home_offsides and _home_corners and _home_shot_acc and _home_pass_acc and _away_goals and _away_shots and _away_shotsOT and _away_poss and _away_tackles and _away_fouls and _away_yellows and _away_reds and _away_injuries and _away_offsides and _away_corners and _away_shot_acc and _away_pass_acc:
            #Validation success, now check captcha
            if request.form['captcha'].upper() != '360D':
                return json.dumps({'html': 'Captcha incorrect'})
            else:
                conn = mysql.connect()
                cursor = conn.cursor()
                # Set the win bits appropriately
                if _result == "home":
                    _home_won = 1
                    _away_won = 0
                    _winner = _home_player
                    _loser = _away_player
                elif _result == "away":
                    _home_won = 0
                    _away_won = 1
                    _winner = _away_player
                    _loser = _home_player
                else:
                    _home_won = 0
                    _away_won = 0
                    _winner = None
                    _loser = None

                param_tuple = (_game, _home_player, _home_team, _home_stars, _home_won, _home_goals, _home_shots, _home_shotsOT, _home_poss, _home_tackles, _home_fouls, _home_yellows, _home_reds, _home_injuries, _home_offsides, _home_corners, _home_shot_acc, _home_pass_acc, _away_player, _away_team, _away_stars, _away_won, _away_goals, _away_shots, _away_shotsOT, _away_poss, _away_tackles, _away_fouls, _away_yellows, _away_reds, _away_injuries, _away_offsides, _away_corners, _away_shot_acc, _away_pass_acc, _winner, _loser, _home_pk, _away_pk)

                cursor.callproc('sp_add_result', param_tuple)

                data = cursor.fetchall()
                if len(data) == 0:
                    conn.commit()
                    return json.dumps('Result added successfully!')
                else:
                    return json.dumps({'error': str(data[0])})

        else:
            return json.dumps({'html':'Please complete all fields.'})
    except Exception as e:
        return json.dumps(str(e))
    finally:
        cursor.close()
        conn.close()

@app.route("/viewStandings")
def viewStandings():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM view_wins")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("viewStandings.html", data=data)


@app.route("/customResults", methods=['POST'])
def customData():
    conn = mysql.connect()
    cursor = conn.cursor()

    _query = request.form['statement']
    _captcha = request.form['captcha']

    print(_query, "\n", _captcha)

    if _captcha == '220':
        try:
            cursor.execute(_query)
            data = cursor.fetchall()
            headers = [i[0] for i in cursor.description]

            return render_template("customResults.html", data=data, headers=headers)
        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()
    else:
        return json.dumps({'html': 'Captcha failed'})


if __name__ == "__main__":
    app.run(port=5001)
