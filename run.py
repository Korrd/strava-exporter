import os, json
from strava_oauth import strava_oauth as strava_oauth
from strava_workouts import strava_workouts as strava
from dropbox import dropbox
from helpers import misc_functions as misc
from config import config
misc.welcome()

#region #? Read config, secret handling, & do oauth
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
workouts_dir = f"{workdir}/workouts"
tracks_dir = f"{workdir}/tracks"
all_workouts_file = f"{workdir}/temp/all_workouts.json"
secrets_file = f"{workdir}/temp/secrets.json"
config_file = f"{workdir}/temp/config.json"
strava_access_token, strava_refresh_token = "", ""

if not os.path.exists(config_file):
  dropbox_path = dropbox.ask_for_dropbox_path()
  config.write_config_file(config_file=config_file, dropbox_path=dropbox_path)

else:
  dropbox_path = config.read_config_file(config_file)

if not os.path.exists(secrets_file):
  # There's no secrets file. Ask user for client ID & Secret
  strava_client_id, strava_client_secret = strava_oauth.ask_for_secrets()
  dropbox_access_token = dropbox.ask_for_secrets()
  if strava_client_secret == "" or strava_client_id == "" or dropbox_access_token == "":
    print("\033[91m❌ Either strava's \"Client Secret\" or \"Client ID\", or dropbox's \"Access Token\" provided are empty. Check them, then try again.\033[0m")
    exit(1)
  else:
    # Write client info to secrets file
    config.write_secrets_file(secrets_file=secrets_file, \
                            strava_client_id=strava_client_id, \
                            strava_client_secret=strava_client_secret, \
                            dropbox_access_token=dropbox_access_token)
else: 
  # Get all credentials from file
  strava_access_token, \
  strava_refresh_token, \
  strava_client_id, \
  strava_client_secret, \
  dropbox_access_token = config.read_secrets_file(secrets_file)

if dropbox_access_token == "":
  dropbox_access_token = dropbox.ask_for_secrets()

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
                          strava_refresh_token=strava_refresh_token, \
                          dropbox_access_token=dropbox_access_token)

print("\033[92m🔐 Authentication successful!\n\033[0m")
#endregion

# Get full workouts' list to download
workout_list = {x[0]: x[1] \
                for x in strava.get_workout_list(access_token=strava_access_token)}

# Download all workouts
strava.download_all_workouts(workdir=workouts_dir, \
                              workout_list=workout_list, \
                              access_token=strava_access_token)

# Extract tracks and convert them to gpx
print("\033[94mℹ️  Extracting tracks to gpx files...\033[0m")
filelist = strava.get_files(workdir=workouts_dir)

skipped = 0
extracted = 0
for key in filelist.keys():

  if str(filelist[key]).endswith(".json"):
    gpx_file = filelist[key].replace('.json', '.gpx')
    gpx_filename = f"{tracks_dir}/{gpx_file}"

    if not os.path.isfile(gpx_filename):
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
  print(f"\033[92m✅ No new tracks found. Existing ones stored at \"{tracks_dir}\"\033[0m")

#TODO
#! Implement dropbox uploader
#! Implement a way to know which files were already uploaded, so we prevent reuploading them all every single time