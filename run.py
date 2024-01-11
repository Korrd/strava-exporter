import os
from strava_oauth import strava_oauth as oauth
from strava_workouts import strava_workouts as workouts
from helpers import misc_functions as misc

misc.welcome()

#region #? Read config, secret handling, & do oauth
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
workouts_dir = f"{workdir}/workouts"
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

print("🔐 Authentication successful!\n")
#endregion

# Get full workouts' list to download
print("ℹ️  Getting workout list...")
workout_list = {x[0]: x[1] \
                for x in workouts.get_workout_list(access_token=access_token)}

# Download all workouts
result = workouts.download_all_workouts(workdir=workouts_dir, \
                                        workout_list=workout_list, \
                                        access_token=access_token)

if result:
  print(f"😎 All workouts downloaded to \"{workouts_dir}\".")
else:
  print(f"💥 Done, although some failed to download. Check logs for details. Downloaded to \"{workouts_dir}\"")
