import os, json
from strava_oauth import strava_oauth as strava_oauth
from strava_workouts import strava_workouts as strava
from helpers import misc_functions as helpers
from config import config

helpers.welcome()

#region #? Read config, secret handling, & do oauth
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
secrets_file, config_file = f"{workdir}/temp/secrets.json", f"{workdir}/temp/config.json"
workout_db_file = f"{workdir}/temp/downloaded_workouts.json"
strava_access_token, strava_refresh_token = "", ""

if not os.path.exists(config_file):
  tracks_dir = config.ask_for_path(message="\033[93m⚠️  [Optional] Please, provide a full path to a folder to store your tracks on",
                                    prompt="\033[95m📂 Tracks Folder: \033[0m")

  workouts_dir = config.ask_for_path(message="\033[93m⚠️  [Optional] Please, provide a full path to a folder to store your workouts on",
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

if not os.path.exists(workout_db_file):
  downloaded_workouts_db = {}
  with open(workout_db_file, mode="w") as f:
    f.write(json.dumps(downloaded_workouts_db))
else:
  downloaded_workouts_db = config.read_downloaded_workouts(db_file=workout_db_file)

if not os.path.exists(secrets_file):
  # There's no secrets file. Ask user for client ID & Secret
  strava_client_id, strava_client_secret = strava_oauth.ask_for_secrets()
  if strava_client_secret == "" or strava_client_id == "":
    print("\033[91m❌ Either strava's \"Client Secret\" or \"Client ID\" provided are empty. Check them, then try again.\033[0m")
    exit(1)
  else:
    # Write client info to secrets file
    config.write_secrets_file(secrets_file=secrets_file, \
                            strava_client_id=strava_client_id, \
                            strava_client_secret=strava_client_secret)

else: 
  # Get all credentials from file
  strava_access_token, \
  strava_refresh_token, \
  strava_client_id, \
  strava_client_secret = config.read_secrets_file(secrets_file)

if strava_access_token == "":
  # No access token present. Let's retrieve them
  strava_access_token, strava_refresh_token = strava_oauth.do_oauth_flow(client_id=strava_client_id, \
                                                    client_secret=strava_client_secret)
else:
  if not strava_oauth.check_access_token(strava_access_token):
    # Refresh invalid access_token, so we don't bother user
    strava_access_token = strava_oauth.refresh_access_token(client_id=strava_client_id, \
                                              client_secret=strava_client_secret, \
                                              refresh_token=strava_refresh_token)

if strava_access_token == "":
  # If at this point we still have no access token, we've failed and can't do anything about it,
  # so we exit with error
  print("\033[91m❌ Unable to retrieve tokens. Check provided strava's \"Client ID\" & \"Secret\", then try again\033[0m")
  exit(1)
else:
  config.write_secrets_file(secrets_file=secrets_file, \
                          strava_client_id=strava_client_id, \
                          strava_client_secret=strava_client_secret, \
                          strava_access_token=strava_access_token, \
                          strava_refresh_token=strava_refresh_token)

print("\033[92m🔐 Authentication successful!\n\033[0m")
#endregion

# Get full workouts' list to download
workout_list = {x[0]: x[1] \
                for x in strava.get_workout_list(access_token=strava_access_token)}

# Download all workouts
strava.download_all_workouts(workdir=workouts_dir, \
                              workout_list=workout_list, \
                              access_token=strava_access_token, \
                              downloaded_workouts_db=downloaded_workouts_db, \
                              workout_db_file=workout_db_file)

# Extract tracks and convert them to gpx
print("\033[94mℹ️  Extracting tracks to gpx files...\033[0m")
filelist = strava.get_files(workdir=workouts_dir)

skipped = 0
extracted = 0
archive_dir = f"{tracks_dir}/Archive"
for key in filelist.keys():

  if str(filelist[key]).endswith(".json"):
    gpx_file = filelist[key].replace('.json', '.gpx')
    gpx_filename = f"{tracks_dir}/{gpx_file}"

    if not (helpers.is_duplicate(paths=[tracks_dir, archive_dir], filename=gpx_file)):
      with open(f"{workouts_dir}/{filelist[key]}", mode="r") as f:
        workout = json.load(f)
      track = strava.decode_polyline(workout['map']['polyline'])
      strava.write_gpx_from_polyline(coordinates=track, output_file=gpx_filename)
      print(f"🗺️  Extracting to {gpx_file}...")
      extracted += 1
    else:
      skipped += 1

if skipped > 0:
  print(f"\033[93m🟡 Skipped {skipped} already existing track{'s' if skipped != 1 else ''}\033[0m")

if extracted != 0:
  print(f"\033[92m✅ {extracted} track{'s' if extracted != 1 else ''} extracted to \"{tracks_dir}\"\033[0m")
else:
  print(f"\033[92m✅ No new tracks found. Existing ones stored at either \"{tracks_dir}\" or \"{archive_dir}\"\033[0m")

#TODO: 
#! - Make "Archive" hardcode a config parameter
