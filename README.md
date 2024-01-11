# Strava exporter

This will export all workouts from strava onto a folder.

It was written so we could upload those workouts to the fog of world app, and reveal those bits the app missed out. This could also be used to store a backup of all workouts as well.

## Usage

- Open the [stdin](./stdin) file, adding the following one-liner

  ```json
  {"client_id": "<MY_CLIENT_ID>", "client_secret": "<MY_CLIENT_SECRET>", "access_token": "",
  "refresh_token": ""}
  ```

  💡 You can get these from strava's [API config page](https://www.strava.com/settings/api). If no API app is set, you can create a new one [following these instructions](https://developers.strava.com/docs/getting-started/#account)

  > ℹ️ `refresh and access tokens` are optional, since this script will get them via oauth if found empty

- Once set, just run the script from the run.py file and wait for it. It'll download all workouts to the [workouts](./workouts/) folder. 