"""
This module provides the strava_workouts class, meant to work with strava workouts.
"""
import sys
import json
import os
import gpxpy
import gpxpy.gpx
import polyline
import requests
from helpers import Helpers as helpers
from config import Config

class StravaWorkouts:
  """
  #### Description
  This class provides methods and functions for downloading, converting and storing strava workouts and tracks
  #### Available functions.
  - `decode_polyline(pline: str)`: decodes a polyline and returns a list of coordinates
  - `download_all_workouts(workdir: str, workout_list: dict, access_token: str) -> bool`: implements the get_workout function and downloads all workouts that are still unsaved on the workouts dir
  - `get_files(workdir: str) -> dict`: from a filename where the left part of its "-" represents the strava workout id, and the right part the workout name, returns a dict where its key is the workout id and its content the full filename
  - `get_workout(workout_id: str, access_token: str) -> dict`: retrieves a full workout from strava
  - `get_workout_list(access_token: str) -> list`: gets strava's user workout index
  - `write_gpx_from_polyline(coordinates, output_file: str)`: writes a gpx file to disc from a decoded polyline
  """

  def get_workout_list(self, access_token: str) -> dict:
    """
    #### Description
    Gets strava's user workout index
    #### Parameters
    - `access_token`: strava's access token
    #### Returns
    An index of workouts
    """
    workout_index = []
    page_limit = 200
    headers = {'Authorization': f'Bearer {access_token}'}
    page_number = 1
    do_download = True

    while do_download:
      activities_url = f'https://www.strava.com/api/v3/athlete/activities?page={page_number}&per_page={page_limit}'
      response = requests.get(activities_url, headers=headers, timeout=60)
      status_code = response.status_code

      if status_code == 429:
        _, lim_daily, _, u_daily = helpers.get_rate_limits(self, res=response)

        if u_daily >= lim_daily: # Hit daily ratelimit
          print("\033[91m💥 Daily ratelimit reached!\n  \033[0m Wait until tomorrow and try again.")
          sys.exit(1)
        else:
          helpers.wait_for_it(self=self)
          continue

      elif status_code == 500:
        if workout_index == []:
          print("\033[93m💥 Encountered an internal server error while retrieving the activities' list. Aborting, since no list was retrieved.\033[0m")
          sys.exit(1)
        else:
          print("\033[93m💥 Encountered an internal server error while retrieving the activities' list. Moving on with what we've got.\n  \033[0mYou may want to re-run this script later on to retrieve the rest of it.")
          break

      activities = response.json()
      if len(activities) == 0:
        do_download = False
      else:
        print(f"{'⏳' if page_number % 2 == 0 else '⌛️'} Getting strava's activities list {'...' if page_number % 2 == 0 else '.  '}", end="\r", flush=True)
        page_number += 1

      for activity in activities:
        workout_index.append([activity["id"], activity["name"]])

    print(f"\n\033[94mℹ️  Got {len(workout_index)} activities. Retrieving them...\033[0m")
    if len(workout_index) >= 2000:
      print("\n\033[93m🚦 Since the activity count is greater than strava's daily ratelimit of 2000,\033[0m")
      print("\033[93m🚦 you may have to run this script again tomorrow to finish.\n\033[0m")

    result = {x[0]: x[1] for x in workout_index}
    return result

  def get_workout(self, workout_id: str, access_token: str) -> dict:
    """
    #### Description
    Retrieves a full workout from strava
    #### Parameters
    - `access_token`: strava's access token
    - `workout_id`: workout ID of the workout to be retrieved
    #### Returns
    A dict containing the workout's data
    """
    api_url = f"https://www.strava.com/api/v3/activities/{workout_id}"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(api_url, headers=headers, timeout=60)
    if response.status_code == 200:
      workout_data = response.json()
      return workout_data
    return {}

  # This function is complex by nature.
  # No point on splitting it into smaller ones.
  # pylint: disable=too-many-locals
  def download_all_workouts(self, workdir: str,
                            workout_list: dict,
                            access_token: str,
                            downloaded_workouts_db: dict,
                            workout_db_file: str) -> bool:
    """
    #### Description
    Implements the get_workout function and downloads all workouts that are still unsaved on the workouts dir.
    #### Parameters
    - `access_token`: strava's access token
    - `skipped`: already skipped workouts for the skipped count
    - `workdir`: working directory where our workouts will be stored
    - `workout_list`: a list of workout IDs
    #### Returns
    `True` if successful, `False` otherwise
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    downloaded = 0

    # Remove already-downloaded items from the workout list
    skipped = len(workout_list)
    for key in downloaded_workouts_db.keys():
      try:
        workout_list.pop(int(key))
      except:
        print(f"\033[93m🟡 Skipped workout ID \"{key}\". Might have been deleted from strava after sync.\033[0m")
      skipped = skipped - len(workout_list)

    for key in workout_list.keys():
      value = workout_list[key]
      output_file = f'{workdir}/{key}-{helpers.sanitize_filename(self, filename=value)}.json'

      api_url = f"https://www.strava.com/api/v3/activities/{key}"

      response = requests.get(api_url, headers=headers, timeout=60)

      lim_15, lim_daily, u_15, u_daily = helpers.get_rate_limits(self, res=response)

      if u_daily >= lim_daily: # Hit daily ratelimit
        print("\033[91m💥 Daily ratelimit reached!\n  \033[0m Wait until tomorrow and try again. \n   \033[92mIn the meantime, processing what we have...\033[0m")
        Config.write_downloaded_workouts(self, db_file=workout_db_file, workout_db=downloaded_workouts_db)
        return False

      match response.status_code:
        case 200: # Success!
          with open(output_file, 'w', encoding="utf8") as f:
            json.dump(response.json(), f, indent=2)
          print(f"💾 Retrieving \033[1;90m{value}\033[0m")
          downloaded += 1
          downloaded_workouts_db[key] = "1"
          Config.write_downloaded_workouts(self, db_file=workout_db_file, workout_db=downloaded_workouts_db)

        case 429: # Hit ratelimiter
          helpers.wait_for_it(self, f"15m Limit: [{u_15}/{lim_15}], Daily Limit: [{u_daily}/{lim_daily}]")
          workout = StravaWorkouts.get_workout(self, workout_id=key, access_token=access_token)
          with open(output_file, 'w', encoding="utf8") as f:
            f.write(json.dumps(workout, indent=2))
          print(f"💾 Retrieving \033[1;90m{value}\033[0m")
          downloaded += 1
          downloaded_workouts_db[key] = "1"
          Config.write_downloaded_workouts(self, db_file=workout_db_file, workout_db=downloaded_workouts_db)

        case 500: # Server error
          print(f"🚫 Activity \"{value}\" failed to download due to error 500")
          skipped += 1

        case _:
          print(f"🚫 Unexpected status code ({response.status_code}) while retrieving activity {value}")
          skipped += 1

    if skipped > 0:
      print(f"\033[93m🟡 Skipped {skipped} already existing activit{'ies' if skipped != 1 else 'y'}\033[0m")

    if downloaded != 0:
      print(f"\033[92m✅ {downloaded} activit{'ies' if downloaded != 1 else 'y'} downloaded to \033[37m\"{workdir}\033[0m\"\n")
    else:
      print(f"\033[92m✅ No new activities found. Existing ones stored at \033[37m\"{workdir}\"\n\033[0m")

    return True

  def get_files(self, workdir: str) -> dict:
    """
    #### Description
    From a filename where the left part of its "-" represents the strava `workout ID`, and the right part the `workout name`, returns a dict where its key is the `workout ID` and its value the `full filename`
    #### Parameters
    - `workdir`: working directory where our workout files are currently stored
    #### Returns
    A `dict` where its `key` is the `workout ID` and its `value` the `full filename`
    """
    result = {}
    for filename in os.listdir(workdir):
      workout_id = filename.split("-", 1)[0].strip()
      result[workout_id] = filename

    return result

  def decode_polyline(self, pline: str):
    """
    #### Description
    Decodes a polyline into a set of coordinates
    #### Parameters
    - `pline`: polyline to be decoded
    #### Returns
    A set of coordinates
    """
    return polyline.decode(pline)

  def write_gpx_from_polyline(self, coordinates, output_file: str):
    """
    #### Description
    Writes a gpx file to disc from a decoded polyline
    #### Parameters
    - `coordinates`: a set of coordinates provided by the `decode_polyline` function
    """
    # Create a GPX file with the given coordinates
    gpx = gpxpy.gpx.GPX()

    # Create a GPX track and segment
    track = gpxpy.gpx.GPXTrack()
    segment = gpxpy.gpx.GPXTrackSegment()

    # Add points to the segment
    for lat, lon in coordinates:
      segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon))

    # Add the segment to the track
    track.segments.append(segment)

    # Add the track to the GPX file
    gpx.tracks.append(track)

    # Write the GPX data to the output file
    with open(output_file, 'w', encoding="utf8") as f:
      f.write(gpx.to_xml())

  def extract_all_tracks(self, workouts_dir: str, tracks_dir: str):
    """
    #### Description
    Extracts all tracks from downloaded workouts if not done already.
    #### Parameters
    - `tracks_dir`: folder where to place extracted tracks
    - `workouts_dir`: folder where to look for workouts
    """
    print("\033[94mℹ️  Extracting tracks to gpx files...\033[0m")
    filelist = StravaWorkouts.get_files(self=self, workdir=workouts_dir)
    skipped = 0
    extracted = 0

    #! - Make "Archive" hardcode a config parameter
    archive_dir = f"{tracks_dir}/Archive"
    #! --------------------------------------------

    for key in filelist.keys():

      if str(filelist[key]).endswith(".json"):
        gpx_file = filelist[key].replace('.json', '.gpx')
        gpx_filename = f"{tracks_dir}/{gpx_file}"

        if not helpers.is_duplicate(self, paths=[tracks_dir, archive_dir], filename=gpx_file):
          with open(f"{workouts_dir}/{filelist[key]}", mode="r", encoding="utf8") as f:
            workout = json.load(f)
          track = StravaWorkouts.decode_polyline(self, pline=workout['map']['polyline'])
          StravaWorkouts.write_gpx_from_polyline(self, coordinates=track, output_file=gpx_filename)
          print(f"🗺️  Extracting to \033[1;90m{gpx_file}\033[0m")
          extracted += 1
        else:
          skipped += 1

    if skipped > 0:
      print(f"\033[93m🟡 Skipped {skipped} already existing track{'s' if skipped != 1 else ''}\033[0m")

    if extracted != 0:
      print(f"\033[92m✅ {extracted} track{'s' if extracted != 1 else ''} extracted to \033[37m\"{tracks_dir}\"\033[0m")
    else:
      print(f"\033[92m✅ No new tracks found. Existing ones stored at either \033[37m\"{tracks_dir}\"\033[92m or \033[37m\"{archive_dir}\"\033[0m")
