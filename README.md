# Strava exporter

This will export all workouts from strava onto a folder.

It was written so we could upload those workouts to the fog of world app, and reveal those bits the app missed out. This could also be used to store a backup of all workouts as well.

## Usage

- Get the `client id` and `client secret` values from strava's at its [API config page](https://www.strava.com/settings/api). If no API app is set, you can create a new one [following these instructions](https://developers.strava.com/docs/getting-started/#account)

- Just run the script from `run.py`, providing client ID and secret when asked, then wait for it. It'll download all workouts to the [workouts](./workouts/) folder. 
