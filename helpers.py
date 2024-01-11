import requests

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
