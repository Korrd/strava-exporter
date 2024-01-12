# <img src="./img/Strava_Exporter_Logo.png" alt="logo" width="24"> Strava Exporter 

This tool will `export all workouts from strava onto a folder`, then `extract each workout's track and save each to gpx` files. Useful for sharing tracks and doing backups.

## Motivation

Strava will only provide batch downloads of **ALL** of an user account's contents at once, which is inconvenient since we may only wish to downloads workouts and its tracks.

Hence, I decided to write this tool so I could sync those workouts to other apps and do some backups as well.

## Features

- `Oauth flow support`: Implements strava's oauth, saving the pain of having to do all sort of things to get a proper token.
- `Platforms supported`: Meant to be run on either **🍎 MacOS**, **🐧 Linux**.
- `Ratelimiting support`: This tool respects [strava's rate-limits](https://developers.strava.com/docs/rate-limits/)
  - **15m ratelimiter**: It'll pause and then resume as the ratelimiter resets.
  - **Daily ratelimiter**: The tool will move on to the next step and extract tracks from all already downloaded workouts. You may run it again the next day to finish with remaining downloads.
- `Resume capability`: You can stop it (*^C*) and continue at any time.

## Prerequisites

If needed, install all required packages described on the `requirements.txt` file using pip as follows:

```bash
pip install -r requirements.txt
```

## Usage

<style>video {border-radius: 12px;}</style>

<video width="640" controls>
  <source src="./img/strava-exporter.mp4" type="video/mp4" controls autoplay>
  Your browser does not support the video tag.
</video>

- Get the `Client ID` & `Secret` values from strava's at its [API config page](https://www.strava.com/settings/api). If no API app is set, you can create a new one [following these instructions](https://developers.strava.com/docs/getting-started/#account)

- Just run the tool from `run.py`, providing `Client ID` and `Secret` when asked, then wait for it. 

  - Retrieved workouts can be found on the [workouts](./workouts/) folder, **in json format** & with all its metadata intact.
  - All `extracted tracks` will be saved to the [tracks](./tracks/) folder **in gpx format**. These come from each workout [polyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm).

## Collaborating

- If you feel like expanding on it, let me know! `Pull-requests` with bugfixed, improvements and new features `are welcome` 💪🏼🔥.

- **🏴‍☠️ Windows** support not yet validated. If you feel like adding support, let me know! 😎.

- While oauth is supported, it's interactive and hence makes it difficult to use this as part of automation. Any help on implementing userless oauth is welcome.