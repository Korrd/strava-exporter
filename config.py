"""
Configuration module, containing the config class.
"""
import json
class Config:
  """
  #### Description
  This class provides functions and methods related to app config.
  #### Available functions
  - `ask_for_path(message: str, prompt: str) -> str`: asks the user for a directory path
  - `read_config_file(config_file: str) -> str`: reads the app's config file from disk
  - `read_downloaded_workouts(db_file: str) -> dict`: loads the downloaded workouts database from its JSON file and returns it as a dict
  - `read_secrets_file(secrets_file: str) -> list`: reads the app's secrets file from disk
  - `write_config_file(config_file: str, tracks_output_path: str)`: writes the app's config file to disk
  - `write_downloaded_workouts(db_file: str, workout_db: dict)`: writes the downloaded workouts to its JSON file from a dict
  - `write_secrets_file(secrets_file: str, strava_client_id: str = "", strava_client_secret: str = "", strava_access_token: str = "", strava_refresh_token: str = "")`: writes the app's secrets file to disk
  """
  def read_secrets_file(self, secrets_file: str) -> list:
    """
    #### Description
    Reads the app's secrets file from disk
    #### Parameters
    - `secrets_file`: full path to the file where secrets are stored
    #### Returns
    - A list containing all of the app's secrets
    #### Notes
    """
    with open(secrets_file, mode="r", encoding="utf8") as f:
      conf = json.loads(f.read())
      return conf['strava_access_token'], \
            conf['strava_refresh_token'], \
            conf['strava_client_id'], \
            conf['strava_client_secret']

  def write_secrets_file(self, secrets_file: str,
                        strava_client_id: str = "",
                        strava_client_secret: str = "",
                        strava_access_token: str = "",
                        strava_refresh_token: str = ""):
    """
    #### Description
    Writes the app's secrets file to disk
    #### Parameters
    - `secrets_file`: full path to the file where secrets are stored
    - `strava_client_id`: strava's client ID (from strava's API settings)
    - `strava_client_secret`: strava's client secret (from strava's API settings)
    - `strava_access_token`: strava's access token
    - `strava_refresh_token`: strava's refresh token
    """
    with open(secrets_file, mode="w", encoding="utf8") as f:
      conf = {}
      conf['strava_access_token'] = strava_access_token
      conf['strava_refresh_token'] = strava_refresh_token
      conf['strava_client_id'] = strava_client_id
      conf['strava_client_secret'] = strava_client_secret
      f.write(json.dumps(conf))

  def read_config_file(self, config_file: str) -> str:
    """
    #### Description
    Reads the app's config file from disk
    #### Parameters
    - `config_file`: full path to the file where config is stored
    #### Returns
    - `tracks_output_path`: a path where extracted tracks will be stored, user-provided
    #### Notes
    """
    with open(config_file, mode="r", encoding="utf8") as f:
      conf = json.loads(f.read())
      return conf['tracks_output_path'], conf['workouts_output_path']

  def write_config_file(self, config_file: str, tracks_output_path: str, workouts_output_path: str):
    """
    #### Description
    Writes the app's config file to disk
    #### Parameters
    - `config_file`: where to store config
    - `tracks_output_path`: a path where extracted tracks will be stored, user-provided
    - `workouts_output_path`: a path where extracted workouts will be stored, user-provided
    """
    conf = {}
    conf['tracks_output_path'] = tracks_output_path
    conf['workouts_output_path'] = workouts_output_path
    with open(config_file, mode="w", encoding="utf8") as f:
      f.write(json.dumps(conf))

  def ask_for_path(self, message: str, prompt: str) -> str:
    """
    #### Description
    Asks the user for a directory path
    #### Parameters
    - `message`: message to show to the user
    - `prompt`: prompt for the input box
    #### Returns
    The user-provided path
    """
    print(message)
    return input(prompt)

  def read_downloaded_workouts(self, db_file: str) -> dict:
    """
    #### Description
    Loads the downloaded workouts database from its JSON file and returns it as a dict
    #### Parameters
    - `db_file`: full path to the db file
    #### Returns
    A dict containing all of the already-downloaded workouts
    """
    with open(db_file, mode="r", encoding="utf8") as f:
      return json.loads(f.read())

  def write_downloaded_workouts(self, db_file: str, workout_db: dict):
    """
    #### Description
    Writes the downloaded workouts to its JSON file from a dict
    #### Parameters
    - `db_file`: full path to the db file
    - `workout_db`: the object containing the downloaded workouts
    """
    with open(db_file, mode="w", encoding="utf8") as f:
      f.write(json.dumps(workout_db))
