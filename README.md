# Strava exporter

This will export all workouts from strava onto a folder.

It was written so we could upload those workouts to the fog of world app, and reveal those bits the app missed out. This could also be used to store a backup of all workouts as well.

## Usage

- Get the `Client ID` & `Secret` values from strava's at its [API config page](https://www.strava.com/settings/api). If no API app is set, you can create a new one [following these instructions](https://developers.strava.com/docs/getting-started/#account)

- Just run the script from `run.py`, providing `Client ID` and `Secret` when asked, then wait for it. It'll download all workouts to the [workouts](./workouts/) folder. 

  ℹ️ Once provided, `Client ID` & `Secret` will be locally stored to [this file](./temp/secrets.json) and won't be requested again unless needed. This file is **not versioned**.. *but not encrypted either*.
