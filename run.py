"""
Main file
"""
import json
import os
import asyncio
from strava_oauth import StravaOauth
from strava_workouts import StravaWorkouts
from helpers import Helpers
from config import Config

async def main():
  """
  Main function that handles the Strava workout export process.
  Manages OAuth authentication, downloads workouts, and extracts tracks.
  """
  helpers = Helpers()
  config = Config()
  strava_oauth = StravaOauth()

  helpers.welcome()

  workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
  secrets_file = f"{workdir}/settings/secrets.json"
  config_file = f"{workdir}/settings/config.json"
  workout_db_file = f"{workdir}/settings/downloaded_workouts.json"

  # Create settings directory if it doesn't exist
  os.makedirs(os.path.dirname(secrets_file), exist_ok=True)

  # Config file management
  if not os.path.exists(config_file):
    tracks_dir = config.ask_for_path(message="\033[93m⚠️  [Optional] Please, provide a full path to a folder for storing your tracks on",
                                  prompt="\033[95m📂 Tracks Folder: \033[0m")

    workouts_dir = config.ask_for_path(message="\033[93m⚠️  [Optional] Please, provide a full path to a folder for storing your workouts on",
                                    prompt="\033[95m📂 Workouts Folder: \033[0m")

    if tracks_dir == "":
      tracks_dir = f"{workdir}/tracks"
      print(f"\033[94mℹ️  Custom tracks output dir not set. Defaulting to \"{tracks_dir}\"\033[0m")

    if workouts_dir == "":
      workouts_dir = f"{workdir}/workouts"
      print(f"\033[94mℹ️  Custom workouts output dir not set. Defaulting to \"{workouts_dir}\"\033[0m")

    config.write_config_file(config_file=config_file,
                          tracks_output_path=tracks_dir,
                          workouts_output_path=workouts_dir)
  else:
    tracks_dir, workouts_dir = config.read_config_file(config_file)

  # Activities DB file management
  if not os.path.exists(workout_db_file):
    downloaded_workouts_db = {}
  else:
    downloaded_workouts_db = config.read_downloaded_workouts(workout_db_file)

  # Create output dirs if they don't exist
  os.makedirs(workouts_dir, exist_ok=True)
  os.makedirs(tracks_dir, exist_ok=True)

  # Handle OAuth credentials and tokens
  credentials = {}
  if os.path.exists(secrets_file):
    with open(secrets_file, 'r', encoding='utf-8') as f:
      credentials = json.load(f)

    # Check if we have a valid access token
    if credentials.get('strava_access_token') and strava_oauth.check_access_token(credentials['strava_access_token']):
      access_token = credentials['strava_access_token']
    elif credentials.get('strava_refresh_token'):
      # Try to refresh the token
      access_token = strava_oauth.refresh_access_token(
        credentials['strava_client_id'],
        credentials['strava_client_secret'],
        credentials['strava_refresh_token']
      )
    else:
      access_token = None
  else:
    credentials = {}
    access_token = None

  # If we don't have valid credentials, get new ones
  if not access_token:
    if not (credentials.get('strava_client_id') and credentials.get('strava_client_secret')):
      client_id, client_secret = strava_oauth.ask_for_secrets()
      if not client_id or not client_secret:
        print("\033[91m❌ Either strava's \"Client Secret\" or \"Client ID\" provided are empty. Check them, then try again.\033[0m")
        return
      credentials['strava_client_id'] = client_id
      credentials['strava_client_secret'] = client_secret

    # Get new tokens through OAuth flow
    access_token, refresh_token = strava_oauth.do_oauth_flow(
      credentials['strava_client_id'],
      credentials['strava_client_secret']
    )

    if not access_token:
      print("\033[91m❌ Failed to get access token. Please check your credentials and try again.\033[0m")
      return

    # Save new tokens
    credentials['strava_access_token'] = access_token
    credentials['strava_refresh_token'] = refresh_token
    with open(secrets_file, 'w', encoding='utf-8') as f:
      json.dump(credentials, f)

  print("\033[92m🔐 Authentication successful!\033[0m")

  async with StravaWorkouts() as strava_workouts:
    print("\n⏳ Getting strava's activities list ...")
    workout_list = await strava_workouts.get_workout_list_async(access_token)

    if workout_list:
      success = strava_workouts.download_all_workouts(
        workdir=workouts_dir,
        workout_list=workout_list,
        access_token=access_token,
        downloaded_workouts_db=downloaded_workouts_db,
        workout_db_file=workout_db_file
      )

      if success:
        strava_workouts.extract_all_tracks(workouts_dir=workouts_dir, tracks_dir=tracks_dir)

if __name__ == "__main__":
  asyncio.run(main())
