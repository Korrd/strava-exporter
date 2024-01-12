import os, json
from strava_oauth import strava_oauth as oauth
from strava_workouts import strava_workouts as workouts
from helpers import misc_functions as misc

misc.welcome()

#region #? Read config, secret handling, & do oauth
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
workouts_dir = f"{workdir}/workouts"
tracks_dir = f"{workdir}/tracks"
all_workouts_file = f"{workdir}/temp/all_workouts.json"
secrets_file = f"{workdir}/temp/secrets.json"
access_token, refresh_token = "", ""

if not os.path.exists(secrets_file):
  # There's no secrets file. Ask user for client ID & Secret
  client_id, client_secret = oauth.ask_for_secrets()
  if client_secret == "" or client_id == "":
    print("\033[91m❌ Either the \"Client Secret\" or \"ID\" provided are empty. Check them then try again.\033[0m")
    exit(1)
  else:
    # Write client info to secrets file
    oauth.write_secrets_file(secrets_file=secrets_file, \
                            client_id=client_id, \
                            client_secret=client_secret)
else: 
  # Get all credentials from file
  access_token, refresh_token, client_id, client_secret = oauth.read_secrets_file(secrets_file)

if access_token == "":
  # No access token present. Let's retrieve them
  access_token, refresh_token = oauth.do_oauth_flow(client_id=client_id, \
                                                    client_secret=client_secret)
else:
  if not oauth.check_access_token(access_token):
    # Refresh invalid access_token since it's invalid, so we don't bother user
    access_token = oauth.refresh_access_token(client_id=client_id, \
                                              client_secret=client_secret, \
                                              refresh_token=refresh_token)

if access_token == "":
  # If at this point we still have no access token, we've failed and can't do anything about it,
  # so we exit with error
  print("\033[91m❌ Unable to retrieve tokens. Check provided \"Client ID\" & \"Secret\", then try again\033[0m")
  exit(1)
else:
  oauth.write_secrets_file(secrets_file=secrets_file, \
                          client_id=client_id, \
                          client_secret=client_secret, \
                          access_token=access_token, \
                          refresh_token=refresh_token)

print("\033[92m🔐 Authentication successful!\n\033[0m")
#endregion

# Get full workouts' list to download
workout_list = {x[0]: x[1] \
                for x in workouts.get_workout_list(access_token=access_token)}

# Download all workouts
result = workouts.download_all_workouts(workdir=workouts_dir, \
                                        workout_list=workout_list, \
                                        access_token=access_token)
if result:
  print(f"\033[92m✅ Workouts downloaded to {workouts_dir}\n\033[0m")
else: 
  print(f"\033[93m🟡 Some workouts downloaded to {workouts_dir}\n\033[0m")

# Extract tracks and convert them to gpx
print("\033[94mℹ️  Extracting tracks to gpx files...\033[0m")
filelist = workouts.get_files(workdir=workouts_dir)

skipped = 0
extracted = 0
for key in filelist.keys():

  if str(filelist[key]).endswith(".json"):
    gpx_file = filelist[key].replace('.json', '.gpx')
    gpx_filename = f"{tracks_dir}/{gpx_file}"

    if not os.path.isfile(gpx_filename):
      with open(f"{workouts_dir}/{filelist[key]}", mode="r") as f:
        workout = json.load(f)
      track = workouts.decode_polyline(workout['map']['polyline'])
      workouts.write_gpx_from_polyline(coordinates=track, output_file=gpx_filename)
      print(f"🗺️  Extracting to {gpx_file}...")
      extracted =+ 1
    else:
      skipped += 1
if skipped > 0:
  print(f"\033[93m🟡 Skipped {skipped} already existing track{'s' if skipped != 1 else ''}\033[0m")

print(f"\033[92m✅ Success! {extracted} track{'s' if extracted != 1 else ''} extracted to \"{tracks_dir}\"\033[0m")
