import requests, json, polyline, gpxpy, gpxpy.gpx, os
from helpers import misc_functions as misc

class strava_workouts:
  def get_workout_list(access_token: str) -> list:
    result = []
    page_limit = 200
    headers = {'Authorization': f'Bearer {access_token}'}
    page_number = 1
    do_download = True

    while do_download:
      activities_url = f'https://www.strava.com/api/v3/athlete/activities?page={page_number}&per_page={page_limit}'
      activities_response = requests.get(activities_url, headers=headers)
      status_code = activities_response.status_code

      if status_code == 429:
        misc.wait_for_it()

        continue
      elif status_code == 500:
        print(f"💥 Encountered a \"500 - internal server error\" while retrieving workouts list. Aborting :(")
        exit(1)

      activities = activities_response.json()
      if len(activities) == 0:
        do_download = False
      else:
        print(f"{'⏳' if page_number % 2 == 0 else '⌛️'} Getting workout list {'...' if page_number % 2 == 0 else '.  '}", end="\r", flush=True)
        page_number += 1

      # Print or save activities
      for activity in activities:
        result.append([activity["id"], activity["name"]])

    # print(result)
    print(f"\n\033[94mℹ️  Got {len(result)} activities. Retrieving them...\033[0m")
    if len(result) >= 2000:
      print("\n\033[93m🚦 Since the activity count is greater than strava's daily ratelimit of 2000,\033[0m")
      print("\033[93m🚦 you may have to run this script again tomorrow to finish.\n\033[0m")

    return result

  def get_workout(workout_id: str, access_token: str) -> dict:
    api_url = f"https://www.strava.com/api/v3/activities/{workout_id}"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
      workout_data = response.json()
      # with open(f'workout_{workout_id}.json', 'w') as f:
      return workout_data # json.dump(workout_data, f, indent=2)

    else:
      return {}

  def download_all_workouts(workdir: str, workout_list: dict, access_token: str) -> bool:
    headers = {'Authorization': f'Bearer {access_token}'}
    skipped = 0
    result = True

    for item in workout_list.keys():
      filename = f"{item}-{misc.sanitize_filename(workout_list[item])}.json"
      output_file = f'{workdir}/{filename}'

      if not os.path.isfile(output_file):

        api_url = f"https://www.strava.com/api/v3/activities/{item}"

        response = requests.get(api_url, headers=headers)

        status_code = response.status_code
        # [15min-limit, daily-limit]
        limit_15, limit_daily = map(int, response.headers._store['x-ratelimit-limit'][1].split(","))
        # [15min-limit-usage, daily-limit-usage]
        usage_15, usage_daily = map(int, response.headers._store['x-ratelimit-usage'][1].split(","))

        if status_code == 200: # Success!
          workout_data = response.json()
          with open(f'{workdir}/{item}-{misc.sanitize_filename(workout_list[item])}.json', 'w') as f:
            json.dump(workout_data, f, indent=2)
          print(f"💾 [{usage_15}/{limit_15}], [{usage_daily}/{limit_daily}] ¦ Retrieving \"{workout_list[item]}\"")

        elif status_code == 429: # Hit ratelimiter
          misc.wait_for_it()
          workout = strava_workouts.get_workout(item, access_token=access_token)
          with open(f'{workdir}/{item}-{misc.sanitize_filename(workout_list[item])}.json', 'w') as f:
            f.write(json.dumps(workout, indent=2))
          print(f"💾 [{usage_15}/{limit_15}], [{usage_daily}/{limit_daily}] ¦ Retrieving \"{workout_list[item]}\"")

        elif status_code == 500: # Server error
          print(f"🚫 Workout \"{workout_list[item]}\" failed to download due to error 500")
          result = False

        if usage_daily >= limit_daily: # Hit daily ratelimit
          print("\033[91m💥 Daily ratelimit reached!\n  \033[0m Wait until tomorrow and try again. \n   \033[92mIn the meantime, processing what we have...\033[0m")
          return False

      else:
        skipped += 1

    if skipped > 0:
      print(f"\033[93m🟡 Skipped {skipped} already existing workouts\033[0m")

    return result

  def get_files(workdir: str) -> dict:
    result = {}

    for filename in os.listdir(workdir):
      parts = filename.split("-", 1)
      key = parts[0].strip()
      value = filename
      result[key] = value

    return result

  def decode_polyline(pline: str):
    # Decode a polyline string and return a list of coordinates (latitude, longitude)
    return polyline.decode(pline)

  def write_gpx_from_polyline(coordinates, output_file: str):
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
    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())