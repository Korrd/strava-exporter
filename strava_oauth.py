"""
This module contains all functions related to strava's oauth flow
"""
import os
import getpass as g
from urllib.parse import urlencode
from http.server import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open_new_tab
import requests
class StravaOauth:
  """
  #### Description
  This class implements strava's oauth flow, which is used to obtain permission from the user to read from its strava's profile
  #### Available functions.
  - `ask_for_secrets() -> list`: asks the user for both strava's client ID and secret
  - `check_access_token(access_token: str) -> bool`: checks if the provided strava access token is still valid
  - `do_oauth_flow(client_id: str, client_secret: str)`: performs strava's oauth flow in order to get the required access tokens
  - `refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str`: gets a new access token using strava's oauth refresh token
  """

  def do_oauth_flow(self, client_id: str, client_secret: str):
    """
    #### Description
    Performs strava's oauth flow in order to get the required access tokens
    #### Parameters
    - `client_id`: client ID from strava's API config
    - `client_secret`: client secret from strava's API config
    #### Notes
    Interactive function. It'll open a browser tab asking the used to authorize this app for read access
    """
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/oauth_success.htm", encoding="utf8") as file:
      html_code = bytes("".join(file.readlines()), "utf-8")

    # Step 1: Get Authorization Code
    redirect_uri = 'http://localhost:8000/'
    auth_url = f'https://www.strava.com/oauth/authorize?{urlencode({"client_id": client_id, "redirect_uri": redirect_uri, "response_type": "code", "scope": "activity:read_all"})}'
    print("\033[93m🟡 Please authorize this script to read from your Strava profile\033[0m")
    print("\033[93m   Ensure the app being authorized is actually yours on Strava's website\033[0m")
    open_new_tab(auth_url)

    class RequestHandler(BaseHTTPRequestHandler):
      """
      Request handler for user reply on oauth flow
      """
      def log_message(self, format, *args):
        # Suppress logging by overriding the log_message method
        pass

      def do_GET(self) -> str:
        """
        Parses authorization code from the redirect URI
        """
        code = self.path.split('code=')[1].split("&")[0]
        # Exchange Authorization Code for Access Token
        token_url = 'https://www.strava.com/oauth/token'
        payload = {
          'client_id': client_id,
          'client_secret': client_secret,
          'code': code,
          'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=payload, timeout=60)
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

  def refresh_access_token(self, client_id: str, client_secret: str, refresh_token: str) -> str:
    """
    #### Description
    This function gets a new access token using strava's oauth refresh token
    #### Parameters
    - `client_id`: client ID from strava's API config page
    - `client_secret`: client secret from strava's API config page
    - `refresh_token`: strava's refresh token
    #### Returns
    A `valid strava's access token` if successful. Otherwise an `empty string`
    """
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
      'client_id': client_id,
      'client_secret': client_secret,
      'refresh_token': refresh_token,
      'grant_type': 'refresh_token'
    }

    response = requests.post(token_url, data=payload, timeout=60)

    if response.status_code == 200:
      access_token = response.json().get('access_token')
      return access_token
    print(f"Error refreshing access token: {response.status_code}, {response.text}")
    return ""

  def check_access_token(self, access_token: str) -> bool:
    """
    #### Description
    Checks if the provided strava access token is still valid
    #### Parameters
    - `access_token`: strava's access token
    #### Returns
    `True` if valid, `False` otherwise
    """
    check_url = 'https://www.strava.com/api/v3/athlete'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(check_url, headers=headers, timeout=60)

    if response.status_code == 200:
      return True
    return False

  def ask_for_secrets(self) -> list:
    """
    #### Description
    Asks the user for both strava's client ID and secret
    #### Returns
    - A `user-provided` list containing two strings: `[client_id, client_secret]`
    """
    print("\033[93m⚠️  Please, provide your Client ID and Secret from Strava's API config.\n    You can get these from here: https://www.strava.com/settings/api\033[0m")

    client_id = g.getpass("\033[95m🪪  Client ID: \033[0m")
    client_secret = g.getpass("\033[95m🔑 Client Secret: \033[0m")

    return client_id, client_secret
