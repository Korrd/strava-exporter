import json, os
from strava_oauth import strava_oauth as oauth
from helpers import strava_workouts as workouts
from helpers import misc_functions as misc

# TODO: 
#* - Authenticate to strava
#* - List workouts
#! - Export each workout to a folder
misc.welcome()

#region #? Some config, secret handling, & oauth
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
all_workouts_file = f"{workdir}/temp/all_workouts.json"
secrets_file = f"{workdir}/temp/secrets.json"
access_token, refresh_token = "", ""

if not os.path.exists(secrets_file):
  # There's no secrets file. Ask user for client ID & Secret
  client_id, client_secret = oauth.ask_for_secrets()
  if client_secret == "" or client_id == "":
    print("❌ Either the \"Client Secret\" or \"ID\" provided are empty. Check them then try again.")
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
  print("❌ Unable to retrieve tokens. Check provided \"Client ID\" & \"Secret\", then try again")
  exit(1)
else:
  oauth.write_secrets_file(secrets_file=secrets_file, \
                          client_id=client_id, \
                          client_secret=client_secret, \
                          access_token=access_token, \
                          refresh_token=refresh_token)

#endregion
print("🔐 Authentication successful!\n")

# Get full workouts' list to download, and store it
print("✅ Getting workout list...")
workout_list = workouts.get_workout_list(access_token=access_token)
with open(all_workouts_file, mode="w") as workout_file:
  buffer = {workout[0]: workout[1] for workout in workout_list}
  buffer = json.dumps(buffer, indent=2)
  workout_file.write(buffer)

# TODO
#* - Store workout_list somewhere
#! - Process list, each downloaded item should go to a file so it's remembered as downloaded
#!   and allow for resume capability
