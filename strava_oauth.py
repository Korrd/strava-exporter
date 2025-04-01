"""
This module provides OAuth functionality for Strava API authentication.
"""
import getpass as g
import http.server
import json
import urllib.parse
import webbrowser
import requests

class RequestHandler(http.server.BaseHTTPRequestHandler):
  """
  Handles the OAuth callback request from Strava.
  Stores the authorization code in the class variable.
  """
  authorization_code = None

  def do_GET(self):
    """Handle GET request to the callback URL"""
    query_components = urllib.parse.parse_qs(self.path.split('?')[1])

    if 'code' in query_components:
      RequestHandler.authorization_code = query_components['code'][0]
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(b"Authorization successful! You can close this window.")
    else:
      self.send_response(400)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(b"Authorization failed! Please try again.")

  def log_message(self, format, *args):
    """Override to disable logging"""
    return

class StravaOauth:
  """
  Handles OAuth authentication flow for Strava API.
  Manages client credentials, access tokens, and refresh tokens.
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

    # Step 1: Get Authorization Code
    redirect_uri = 'http://localhost:8000/'
    auth_url = f'https://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=activity:read_all'

    print("\n\033[93m⚠️  Please authorize this script to read from your strava profile.\033[0m")
    print("\033[93m⚠️  Make sure the app you're authorizing is indeed yours on strava's website.\033[0m")

    # Start local server before opening browser
    server = http.server.HTTPServer(('localhost', 8000), RequestHandler)
    RequestHandler.authorization_code = None

    # Open browser for authorization
    webbrowser.open_new_tab(auth_url)

    # Wait for callback
    server.handle_request()

    if not RequestHandler.authorization_code:
      print("\033[91m❌ Failed to get authorization code\033[0m")
      return None, None

    # Step 2: Exchange code for token
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
      'client_id': client_id,
      'client_secret': client_secret,
      'code': RequestHandler.authorization_code,
      'grant_type': 'authorization_code'
    }

    try:
      response = requests.post(token_url, data=payload, timeout=60)
      response.raise_for_status()  # Raise exception for bad status codes

      tokens = response.json()
      return tokens.get('access_token'), tokens.get('refresh_token')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
      print(f"\033[91m❌ Error exchanging authorization code: {e}\033[0m")
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
    Prompts the user for Strava client ID and secret.
    Returns a tuple of (client_id, client_secret).
    """
    print("\033[93m⚠️  Please, provide your strava's \"Client ID\" and \"Client Secret\"\033[0m")
    print("\033[94mℹ️  You can find them at https://www.strava.com/settings/api\033[0m")
    client_id = g.getpass("\033[95m🔑 Client ID: \033[0m")
    client_secret = g.getpass("\033[95m🔑 Client Secret: \033[0m")
    return client_id, client_secret
