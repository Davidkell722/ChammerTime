from flask import Blueprint, render_template
import json

main = Blueprint('main', __name__)

# Load your league data from JSON files
with open('data/league_data.json') as f:
    league_data = json.load(f)

with open('data/team_history.json') as f:
    team_history = json.load(f)

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
