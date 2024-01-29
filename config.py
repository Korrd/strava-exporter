import json

class config:
  def read_secrets_file(secrets_file: str) -> list:
    with open(f"{secrets_file}", mode="r") as f:
      config = json.loads(f.read())
      if 'access_token' in config.keys():
        return config['access_token'], \
              config['refresh_token'], \
              config['client_id'], \
              config['client_secret'], \
              ""
      else:
        return config['strava_access_token'], \
              config['strava_refresh_token'], \
              config['strava_client_id'], \
              config['strava_client_secret'], \
              config['dropbox_access_token']

  def write_secrets_file(secrets_file: str,
                        strava_client_id: str = "",
                        strava_client_secret: str = "",
                        strava_access_token: str = "",
                        strava_refresh_token: str = "",
                        dropbox_access_token: str = ""):
    with open(f"{secrets_file}", mode="w") as f:
      config = {}
      config['strava_access_token'] = strava_access_token
      config['strava_refresh_token'] = strava_refresh_token
      config['strava_client_id'] = strava_client_id
      config['strava_client_secret'] = strava_client_secret
      config['dropbox_access_token'] = dropbox_access_token
      f.write(json.dumps(config))

  def read_config_file(config_file: str) -> str:
    with open(f"{config_file}", mode="r") as f:
      config = json.loads(f.read())
      return config['dropbox_path']

  def write_config_file(config_file: str, dropbox_path: str):
    config = {}
    config['dropbox_path'] = dropbox_path
    with open(f"{config_file}", mode="w") as f:
      f.write(json.dumps(config))
