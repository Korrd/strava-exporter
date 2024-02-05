import json

class config:
  def read_secrets_file(secrets_file: str) -> list:
    with open(f"{secrets_file}", mode="r") as f:
      config = json.loads(f.read())
      if 'access_token' in config.keys():
        return config['access_token'], \
              config['refresh_token'], \
              config['client_id'], \
              config['client_secret']
      else:
        return config['strava_access_token'], \
              config['strava_refresh_token'], \
              config['strava_client_id'], \
              config['strava_client_secret']

  def write_secrets_file(secrets_file: str,
                        strava_client_id: str = "",
                        strava_client_secret: str = "",
                        strava_access_token: str = "",
                        strava_refresh_token: str = ""):
    with open(f"{secrets_file}", mode="w") as f:
      config = {}
      config['strava_access_token'] = strava_access_token
      config['strava_refresh_token'] = strava_refresh_token
      config['strava_client_id'] = strava_client_id
      config['strava_client_secret'] = strava_client_secret
      f.write(json.dumps(config))

  def read_config_file(config_file: str) -> str:
    with open(f"{config_file}", mode="r") as f:
      config = json.loads(f.read())
      return config['tracks_output_path']

  def write_config_file(config_file: str, tracks_output_path: str):
    config = {}
    config['tracks_output_path'] = tracks_output_path
    with open(f"{config_file}", mode="w") as f:
      f.write(json.dumps(config))

  def ask_for_tracks_output_path() -> str:
    print("\033[93m⚠️  [Optional] Please, provide a full path to a folder to store your tracks on")
    return input("\033[95m📂 Output Folder: \033[0m")
