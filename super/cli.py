import click
import bcrypt
from super.db import add_search_history, add_user, clear_session, get_user_history, get_user_id, load_session, save_session 
import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()

current_user_id = None
# Main group
@click.group()
@click.pass_context
def cli(ctx):
    '''
    Commands to Fetch and Store Weather Data
    '''
    ctx.ensure_object(dict)
    ctx.obj['user_id'] = load_session()


# Lets you define group for user authentication
@click.group(name="user")
def user():
    '''
    Commands regarding User Login and Signup
    '''
    pass




# User Signup
@click.command(name="signup")
@click.option('--username', '-u', help="Username", required=True, prompt="Your Username")
@click.option('--password', '-p', help="Password", required=True, prompt="Your Password", hide_input=True)
def signup_user(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    add_user(username, password_hash)
    click.echo("User signed up successfully!")

# User Login
@click.command(name="login")
@click.option('--username', '-u', help="Username", required=True, prompt="Your Username")
@click.option('--password', '-p', help="Password", required=True, prompt="Your Password", hide_input=True)
def login_user(username, password):
    user_data = get_user_id(username)
    if user_data:
        user_id, stored_password_hash = user_data
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            save_session(user_id)
            click.echo("Login successful!")
        else:
            click.echo("Invalid username or password.")
    else:
        click.echo("Invalid username or password.")

@click.command(name="logout")
def logout_user():
    clear_session()
    click.echo("Logged out successfully.")





# Weather Fetch Command (requires OpenWeatherMap API)
@click.command(name="weather")
@click.option('--location', '-l', help="Location to fetch weather for", required=True)
@click.pass_context
def fetch_weather(ctx, location):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
        weather_data = json.dumps(weather_info)
        click.echo(f"Weather in {location}: {weather_info}")

        if ctx.obj['user_id']:
            add_search_history(ctx.obj['user_id'], location, weather_data)
        else:
            click.echo("You are not logged in. This search will not be saved to history.")
    else:
        click.echo("Failed to retrieve weather data.")

# View Search History
@click.command(name="history")
@click.pass_context
def view_history(ctx):
    """View user search history"""
    if ctx.obj['user_id'] is None:
        click.echo("You need to be logged in to view search history.")
        return
    
    history = get_user_history(ctx.obj['user_id'])
    click.echo("Search History:")
    for entry in history:
        click.echo(f"Time: {entry[0]}, Location: {entry[1]}, Data: {entry[2]}")

user.add_command(signup_user)
user.add_command(login_user)
user.add_command(logout_user)
cli.add_command(user)
cli.add_command(fetch_weather)
cli.add_command(view_history)



