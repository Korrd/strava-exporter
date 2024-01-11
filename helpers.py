import requests, os, json, getpass as g
from urllib.parse import urlencode
from http.server import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open_new_tab

class strava_oauth:
  def do_oauth_flow(client_id: str, client_secret: str):
    
    # Get auth successful screen
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/oauth_success.htm") as file:
      html_code = bytes("".join(file.readlines()), "utf-8")


    # Step 1: Get Authorization Code
    redirect_uri = 'http://localhost:8000/'
    auth_url = f'https://www.strava.com/oauth/authorize?{urlencode({"client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code", "scope": "activity:read_all"})}'
    print('ℹ️  Please authorize this app to read from your strava profile to continue')
    open_new_tab(auth_url)

    class RequestHandler(BaseHTTPRequestHandler):
      def log_message(self, format, *args):
          # Suppress logging by overriding the log_message method
          pass

      def do_GET(self) -> str:
        # Parse authorization code from the redirect URI
        code = self.path.split('code=')[1].split("&")[0]
        # Exchange Authorization Code for Access Token
        token_url = 'https://www.strava.com/oauth/token'
        payload = {
          'client_id': client_id,
          'client_secret': client_secret,
          'code': code,
          'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=payload)
        if response.status_code != 200:
          self.server.access_token = ""
          self.server.refresh_token = ""
        else:
          # Store access_token as an instance variable,
          # so we can return it later from the do_auth_flow function
          self.server.access_token = response.json().get('access_token')
          self.server.refresh_token = response.json().get('refresh_token')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_code)

    # Start the local server to handle the OAuth redirect
    server = HTTPServer(('localhost', 8000), RequestHandler)
    server.handle_request()
    return server.access_token, server.refresh_token
  
  def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
      'client_id': client_id,
      'client_secret': client_secret,
      'refresh_token': refresh_token,
      'grant_type': 'refresh_token'
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
      access_token = response.json().get('access_token')
      return access_token
    else:
      print(f"Error refreshing access token: {response.status_code}, {response.text}")
      return ""

  def check_access_token(access_token: str) -> bool:
    check_url = 'https://www.strava.com/api/v3/athlete'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(check_url, headers=headers)

    if response.status_code == 200:
      return True
    else:
      return False

  def ask_for_secrets() -> list:
    print("⚠️ Please, provide your Client ID and Secret from strava's API config. \n You can get these from here: https://www.strava.com/settings/api")
    client_id = input("➡️ Client ID: ")
    client_secret = g.getpass("➡️ Client Secret: ")
    print("\n")

    return client_id, client_secret

  def read_secrets_file(secrets_file: str) -> list:
    with open(f"{secrets_file}", mode="r") as f:
      config = json.loads(f.read())
      return config['access_token'], \
            config['refresh_token'], \
            config['client_id'], \
            config['client_secret']

  def write_secrets_file(secrets_file: str, client_id: str, client_secret: str, access_token: str = "", refresh_token: str = ""):
    with open(f"{secrets_file}", mode="w") as f:
      buffer = f'{{"client_id": "{client_id}", "client_secret": "{client_secret}", "access_token": "{access_token}", "refresh_token": "{refresh_token}"}}'
      f.write(buffer)

class strava_workouts:
  def get_workout_list(access_token: str) -> list:
    result = []
    # throttle_wait = 910 # Sleep for 15 minutes before resuming, to avoid hitting API ratelimiter
    page_limit = 200
    headers = {'Authorization': f'Bearer {access_token}'}
    page_number = 1
    do_download = True

    while do_download:
      activities_url = f'https://www.strava.com/api/v3/athlete/activities?page={page_number}&per_page={page_limit}'
      activities_response = requests.get(activities_url, headers=headers)

      activities = activities_response.json()
      if len(activities) == 0:
        do_download = False
      else:
        print(f"{'⏳' if page_number % 2 == 0 else '⌛️'} Downloading workout list. Stand by...", end="\r", flush=True)
        page_number += 1

      # Print or save activities
      for activity in activities:
        result.append([activity["id"], activity["name"]])

    # print(result)
    print(f"\n✅ Got {len(result)} activities\n")

    return result

class misc_functions:
  def welcome():
    print("_______________________")
    print("Strava workout exporter")
    print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n")
