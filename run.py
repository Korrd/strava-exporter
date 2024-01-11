import json, os
from helpers import strava_oauth as oauth
from helpers import strava_workouts as workouts

# TODO: 
#* - Authenticate to strava
#! - List workouts
#! - Export them to a folder

#region #? Some config, & load secrets from file
workdir = f"{os.path.dirname(os.path.realpath(__file__))}"
all_workouts_file = f"{workdir}/temp/all_workouts.json"
secrets_file = f"{workdir}/secrets.json"

if not os.path.exists(secrets_file):
  client_id, client_secret = oauth.ask_for_secrets()
  if client_secret == "" or client_id == "":
    print("❌ Either the client secret or client ID provided are empty. Quitting.")
    exit(1)
  else:
    oauth.write_secrets_file(secrets_file=secrets_file, client_id=client_id, client_secret=client_secret)
  
access_token, refresh_token, client_id, client_secret = oauth.read_secrets_file(secrets_file)
#endregion

# Get tokens from client secret and id
if access_token == "":
  access_token, refresh_token = oauth.do_oauth_flow(client_id=client_id, \
                                                    client_secret=client_secret)
  if access_token == "":
    print("❌ Unable to get access token. Check your credentials and try again")
    exit(1)
  else:
    print("✅ Oauth successful")
    with open(f"{secrets_file}", mode="w") as f:
      buffer = f'{{"client_id": "{client_id}", "client_secret": "{client_secret}", "access_token": "{access_token}", "refresh_token": "{refresh_token}"}}'
      f.write(buffer)

# Get a list of workouts to download and save it to a file
print("✅ Getting workout ID's...")
workout_list = workouts.get_workout_list(access_token=access_token)
with open(all_workouts_file, mode="w") as workout_file:
  buffer = {item[0]: item[1] for item in workout_list}
  buffer = json.dumps(buffer, indent=2)
  workout_file.write(buffer)


# TODO
#! - Store workout_list somewhere
#! - Process list, each downloaded item should go to a file so it's remembered as downloaded
#!   and allow for resume capability
