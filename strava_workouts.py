import requests, json, time
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
        print(f"{'⏳' if page_number % 2 == 0 else '⌛️'} Downloading workout list. Stand by...", end="\r", flush=True)
        page_number += 1

      # Print or save activities
      for activity in activities:
        result.append([activity["id"], activity["name"]])

    # print(result)
    print(f"\n✅ Got {len(result)} activities\n")

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
    throttle_wait = 901 # Ratelimiter will reset after 15 minutes
    headers = {'Authorization': f'Bearer {access_token}'}
    for item in workout_list.keys():
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

        print(f"✅ 15m: [{usage_15},{limit_15}] daily: [{usage_daily},{limit_daily}] ¦ Downloaded workout \"{workout_list[item]}\"")

      elif status_code == 429: # Hit ratelimiter
        misc.wait_for_it()
        workout = strava_workouts.get_workout(item, access_token=access_token)
        with open(f'{workdir}/{item}-{misc.sanitize_filename(workout_list[item])}.json', 'w') as f:
          f.write(json.dumps(workout, indent=2))

      elif status_code == 500: # Server error
        print(f"❌ Workout \"{workout_list[item]}\" failed to download due to error 500")

      if usage_daily >= limit_daily: # Hit daily ratelimit
        print(f"\n💥 Daily ratelimit reached. Wait until tomorrow and try again.")
        return False
