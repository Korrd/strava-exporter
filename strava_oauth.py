"""
This module contains all functions related to strava's oauth flow
"""
import os
import getpass as g
from urllib.parse import urlencode, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open_new_tab
import requests

class StravaOauth:
  """
  #### Description
  This class implements strava's oauth flow, which is used to obtain permission from the user to read from its strava's profile
  #### Available functions.
  - `ask_for_secrets() -> tuple`: asks the user for both strava's client ID and secret
  - `check_access_token(access_token: str) -> bool`: checks if the provided strava access token is still valid
  - `do_oauth_flow(client_id: str, client_secret: str) -> tuple`: performs strava's oauth flow in order to get the required access tokens
  - `refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str`: gets a new access token using strava's oauth refresh token
  """

  def do_oauth_flow(self, client_id: str, client_secret: str):
    """
    #### Description
    Performs strava's oauth flow in order to get the required access tokens
    #### Parameters
    - `client_id`: client ID from strava's API config
    - `client_secret`: client secret from strava's API config
    #### Returns
    A tuple of (access_token, refresh_token)
    """
    try:
      client_id = int(client_id)  # Convert to integer
    except ValueError:
      print("\033[91m❌ Client ID must be a number.\033[0m")
      return None, None

    with open(f"{os.path.dirname(os.path.realpath(__file__))}/oauth_success.htm", encoding="utf8") as file:
      html_code = bytes("".join(file.readlines()), "utf-8")

    class RequestHandler(BaseHTTPRequestHandler):
      def __init__(self, *args, **kwargs):
        self.auth_code = None
        super().__init__(*args, **kwargs)

      def log_message(self, format, *args):
        pass  # Suppress logging

      def do_GET(self):
        try:
          # Parse query parameters
          query_components = parse_qs(self.path.split('?')[1])

          if 'error' in query_components:
            print(f"\033[91m❌ Authorization error: {query_components['error'][0]}\033[0m")
            self.server.auth_code = None
          elif 'code' in query_components:
            self.server.auth_code = query_components['code'][0]
          else:
            print("\033[91m❌ No authorization code received\033[0m")
            self.server.auth_code = None

          # Send response to browser
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()
          self.wfile.write(html_code)
        except Exception as e:
          print(f"\033[91m❌ Error handling OAuth callback: {e}\033[0m")
          self.server.auth_code = None

    # Step 1: Get Authorization Code
    redirect_uri = 'http://localhost:8000/'
    auth_url = f'https://www.strava.com/oauth/authorize?{urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "activity:read_all"
    })}'

    print("\033[93m🟡 Please authorize this script to read from your Strava profile\033[0m")
    print("\033[93m   Ensure the app being authorized is actually yours on Strava's website\033[0m")

    # Start local server before opening browser
    server = HTTPServer(('localhost', 8000), RequestHandler)
    server.auth_code = None

    # Open browser for authorization
    open_new_tab(auth_url)

    # Wait for the callback
    server.handle_request()

    if not server.auth_code:
      print("\033[91m❌ Failed to get authorization code\033[0m")
      return None, None

    # Step 2: Exchange code for token
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
      'client_id': client_id,
      'client_secret': client_secret,
      'code': server.auth_code,
      'grant_type': 'authorization_code'
    }

    try:
      response = requests.post(token_url, data=payload, timeout=60)
      response.raise_for_status()  # Raise exception for bad status codes

      tokens = response.json()
      return tokens.get('access_token'), tokens.get('refresh_token')
    except requests.exceptions.RequestException as e:
      print(f"\033[91m❌ Error exchanging code for token: {e}\033[0m")
      return None, None

  def refresh_access_token(self, client_id: str, client_secret: str, refresh_token: str) -> str:
    """
    #### Description
    This function gets a new access token using strava's oauth refresh token
    #### Parameters
    - `client_id`: client ID from strava's API config page
    - `client_secret`: client secret from strava's API config page
    - `refresh_token`: strava's refresh token
    #### Returns
    A `valid strava's access token` if successful. Otherwise None
    """
    try:
      client_id = int(client_id)
    except ValueError:
      print("\033[91m❌ Client ID must be a number.\033[0m")
      return None

    token_url = 'https://www.strava.com/oauth/token'
    payload = {
      'client_id': client_id,
      'client_secret': client_secret,
      'refresh_token': refresh_token,
      'grant_type': 'refresh_token'
    }

    try:
      response = requests.post(token_url, data=payload, timeout=60)
      response.raise_for_status()
      return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
      print(f"\033[91m❌ Error refreshing token: {e}\033[0m")
      return None

  def check_access_token(self, access_token: str) -> bool:
    """
    #### Description
    Checks if the provided strava access token is still valid
    #### Parameters
    - `access_token`: strava's access token
    #### Returns
    `True` if valid, `False` otherwise
    """
    if not access_token:
      return False

    check_url = 'https://www.strava.com/api/v3/athlete'
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
      response = requests.get(check_url, headers=headers, timeout=60)
      return response.status_code == 200
    except requests.exceptions.RequestException:
      return False

  def ask_for_secrets(self) -> tuple:
    """
    #### Description
    Asks the user for both strava's client ID and secret
    #### Returns
    A tuple containing (client_id, client_secret)
    """
    print("\033[93m⚠️  Please, provide your Client ID and Secret from Strava's API config.\n    You can get these from here: https://www.strava.com/settings/api\033[0m")

    while True:
      client_id = g.getpass("\033[95m🪪  Client ID: \033[0m")
      try:
        int(client_id)  # Validate it's a number
        break
      except ValueError:
        print("\033[91m❌ Client ID must be a number. Please try again.\033[0m")

    client_secret = g.getpass("\033[95m🔑 Client Secret: \033[0m")
    return client_id, client_secret
