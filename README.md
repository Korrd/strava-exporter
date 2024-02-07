# <img src="./img/Strava_Exporter_Logo.png" alt="logo" width="24"> Strava Exporter 

This tool will `export all workouts from strava onto a folder`, then `extract each workout's track and save each to gpx` files. Useful for sharing tracks and doing backups.

## Motivation

Strava will only provide batch downloads of **ALL** of an user account's contents at once, which is inconvenient since we may only wish to download workouts and its tracks.

Hence, I decided to write this tool so I could sync those workouts to other apps and do some backups as well.

## Features

- `Oauth flow support`: Implements strava's oauth, saving the pain of having to do all sort of things to get a proper token.
- `Multiple platforms supported`: Meant to be run on either **🍎 MacOS**, **🐧 Linux**.
- `Ratelimiting support`: This tool respects [strava's rate-limits](https://developers.strava.com/docs/rate-limits/)
  - **15m ratelimiter**: It'll pause and then resume as the ratelimiter resets.
  - **Daily ratelimiter**: The tool will move on to the next step and extract tracks from all already downloaded workouts. You may run it again the next day to finish downloading your data.
- `Resume capability`: You can stop it (*^C*), then resume from where it left at any time.
- `Idempotence`: It'll skip workouts already downloaded, and ensure your already-downloaded workouts always reflect what's on your strava account. Hence, any changes to already-downloaded workouts on strava will be synced to your local.
- `Custom tracks output folder`: Useful if you wish to store tracks somewhere else, like `Google Drive`, `Dropbox`, a `network or external drive`, etc. This can also be used so those are picked up for importing by other apps, like [🌎 Fog of World's track sync](https://medium.com/p/b29f73172b7e).

## Prerequisites

If needed, install all required packages described on the `requirements.txt` file as follows:

```bash
make setup
```

## Usage

<video width="640" controls autoplay>
  <source src="https://raw.githubusercontent.com/Korrd/strava-exporter/main/img/strava-exporter.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

- Get the `Client ID` & `Secret` values from strava's at its [API config page](https://www.strava.com/settings/api). If no API app is set, you can create a new one [following these instructions](https://developers.strava.com/docs/getting-started/#account)

- Just run the tool by doing `make run`, providing `Client ID` and `Secret` and any other parameters when asked, then wait for it.

  - Retrieved workouts can be found on the [workouts](./workouts/) folder, **in json format** & with all its metadata intact.
  - All `extracted tracks` will be saved to either the [tracks](./tracks/) or custom-set folder **in gpx format**. These come from each workout [polyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm).

## Collaborating

Pull requests are welcome. For more info, see the [Contributing](./CONTRIBUTING.md) file.
