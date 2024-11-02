from flask import Blueprint, render_template
import json
import os

main = Blueprint('main', __name__)

# Set default data in case JSON files are missing
default_league_data = {
    "teams": [
        {"id": 1, "name": "Team Alpha", "rank": 1, "wins": 10, "losses": 2},
        {"id": 2, "name": "Team Beta", "rank": 2, "wins": 8, "losses": 4}
    ]
}

default_team_history = {
    "1": {"2022": {"wins": 10, "losses": 2}},
    "2": {"2022": {"wins": 8, "losses": 4}}
}

# Load league data from file if available, otherwise use default data
if os.path.exists('data/league_data.json'):
    with open('data/league_data.json') as f:
        league_data = json.load(f)
else:
    league_data = default_league_data

# Load team history from file if available, otherwise use default data
if os.path.exists('data/team_history.json'):
    with open('data/team_history.json') as f:
        team_history = json.load(f)
else:
    team_history = default_team_history

@main.route('/')
def home():
    # Sort teams by power rankings and standings
    power_rankings = sorted(league_data['teams'], key=lambda x: x['rank'])
    standings = sorted(league_data['teams'], key=lambda x: x['wins'], reverse=True)
    return render_template('home.html', power_rankings=power_rankings, standings=standings)

@main.route('/team/<int:team_id>')
def team(team_id):
    # Retrieve data for a specific team
    team_data = next((team for team in league_data['teams'] if team['id'] == team_id), None)
    if not team_data:
        return "Team not found", 404
    team_history_data = team_history.get(str(team_id), {})
    return render_template('team.html', team=team_data, history=team_history_data)
