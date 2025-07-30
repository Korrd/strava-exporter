"""
This module provides helper functions for the strava_workouts class
"""
import os
import time
import re
import asyncio
from typing import List, Tuple

class Helpers:
  """
  #### Description
  This class provides helper functions for the strava_workouts class
  #### Available functions.
  - `get_rate_limits(res: requests.Response) -> tuple`: gets strava's rate limits from a response
  - `is_duplicate(paths: list, filename: str) -> bool`: checks if a file exists in any of the provided paths
  - `sanitize_filename(filename: str) -> str`: sanitizes a filename
  - `wait_for_it(message: str)`: waits for strava's rate limit to reset
  """

  def get_rate_limits(self, res) -> Tuple[int, int, int, int]:
    """
    #### Description
    Gets strava's rate limits from a response
    #### Parameters
    - `res`: response from strava's API
    #### Returns
    A tuple containing (15m_limit, daily_limit, 15m_usage, daily_usage)
    """
    # Handle comma-separated rate limits (e.g., "200,2000")
    limits = res.headers.get('X-RateLimit-Limit', '0,0').split(',')
    lim_15 = int(limits[0])
    lim_daily = int(limits[1]) if len(limits) > 1 else 0

    # Handle comma-separated usage values
    usage = res.headers.get('X-RateLimit-Usage', '0,0').split(',')
    u_15 = int(usage[0])
    u_daily = int(usage[1]) if len(usage) > 1 else 0

    return lim_15, lim_daily, u_15, u_daily

  async def get_rate_limits_async(self, res) -> Tuple[int, int, int, int]:
    """
    #### Description
    Gets strava's rate limits from an async response
    #### Parameters
    - `res`: response from strava's API
    #### Returns
    A tuple containing (15m_limit, daily_limit, 15m_usage, daily_usage)
    """
    # Handle comma-separated rate limits (e.g., "200,2000")
    limits = res.headers.get('X-RateLimit-Limit', '0,0').split(',')
    lim_15 = int(limits[0])
    lim_daily = int(limits[1]) if len(limits) > 1 else 0

    # Handle comma-separated usage values
    usage = res.headers.get('X-RateLimit-Usage', '0,0').split(',')
    u_15 = int(usage[0])
    u_daily = int(usage[1]) if len(usage) > 1 else 0

    return lim_15, lim_daily, u_15, u_daily

  def wait_for_it(self, message: str = ""):
    """
    #### Description
    Waits for strava's rate limit to reset
    #### Parameters
    - `message`: message to be displayed while waiting
    """
    print(f"\033[93m⏰ Rate limit hit! Waiting 15 minutes... {message}\033[0m")
    time.sleep(900)

  async def wait_for_it_async(self, message: str = ""):
    """
    #### Description
    Waits for strava's rate limit to reset asynchronously
    #### Parameters
    - `message`: message to be displayed while waiting
    """
    print(f"\033[93m⏰ Rate limit hit! Waiting 15 minutes... {message}\033[0m")
    await asyncio.sleep(900)

  def is_duplicate(self, paths: List[str], filename: str) -> bool:
    """
    #### Description
    Checks if a file exists in any of the provided paths
    #### Parameters
    - `paths`: list of paths to check
    - `filename`: filename to check
    #### Returns
    `True` if the file exists in any of the provided paths, `False` otherwise
    """
    for path in paths:
      if os.path.exists(f"{path}/{filename}"):
        return True
    return False

  def sanitize_filename(self, filename: str) -> str:
    """
    #### Description
    Sanitizes a filename
    #### Parameters
    - `filename`: filename to sanitize
    #### Returns
    A sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Remove control characters
    filename = "".join(char for char in filename if ord(char) >= 32)
    return filename

  def welcome(self):
    """
    #### Description
    Prints a welcome message
    """
    print("""                           ╔═════════════════════════╗
                           ║ Strava Workout Exporter ║
                           ╚═╦══════════╦══════════╦═╝
Created by:  Victor Martin   ║          ║          ║ Github:     @korrd
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╜          ║          ╙┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
                                        ║
                 12-01-2024 ┌┈┈┈┈┈┈┈┈┈┈┈╨┈┈┈┈┈┈┈┈┈┈┐ Spain
                 ═══════════╛                      ╘══════
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈""")
