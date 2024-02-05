import re, time, emoji, os

class misc_functions:
  """
  #### Description
  This class provides miscelaneous helper functions and methods.
  #### Available functions
  - `()`: 
  """

  def welcome():
    """
    #### Description
    Prints the app's welcome message
    """

    print("\033[37m╔═════════════════════════╗\033[0m".center(89))
    print("\033[37m║ \033[1;31mStrava \033[1;33mWorkout \033[1;31mExporter\033[0;37m ║\033[0m".center(117))
    print("\033[37m╚═╦══════════╦══════════╦═╝\033[0m".center(89))
    print("\033[37mCreated by:  \033[1;31mVictor Martin \033[0;37m  ║" + (" " * 10) + "║" + (" " * 10) + "║ \033[37mGithub:     \033[1;31m@korrd\033[0m")
    print("\033[37m┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╜\033[37m" + (" " * 10) + "║\033[37m" + (" " * 10) + "╙┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\033[0m")
    print("\033[37m" + (" " * 40) + "║\033[0m")
    print((" " * 17) + "\033[1;31m12-01-2024\033[0;37m ┌┈┈┈┈┈┈┈┈┈┈┈╨┈┈┈┈┈┈┈┈┈┈┐ \033[1;31mSpain\033[0m")
    print("\033[37m" + (" " * 17) + ("═" * 11) + "╛" + (" " * 22) + "╘" + ("═" * 6))
    print(("\033[37m" + ("┈" * 71) + "\033[0m"))

  def sanitize_filename(filename: str) -> str:
    """
    #### Description
    Sanitizes a string so it can become a valid filename. 
    #### Parameters
    - `filename`: A string containing the filename to be sanitized
    #### Returns
    The sanitized filename
    #### Notes
    Supports Linux, Macos, and Windows
    """
    # Remove emojis
    result = emoji.replace_emoji(filename,"").strip()

    # Replace invalid characters with underscores
    result = re.sub(r'[\/:*?"<\ \>|]', '_', result).strip()

    return result

  def wait_for_it(extra_message: str = ""):
    """
    #### Description
    Waits for a set amount of time, while printing a message letting the user know how much time is left in seconds.
    #### Parameters
    - `extra_message`: A custom message to be added before the countdown message
    #### Notes
    The countdown will be a one-liner which'll update every second. Useful to avoid log noise
    """
    if extra_message != "":
      print(f"\033[33m⏰ {extra_message}\033[0m")

    for x in range(901, 0, -1):
      print(f"\033[33m⏰ Rate limit exceeded. Sleeping for {x} seconds  \033[0m", end='\r', flush=True)
      time.sleep(1)
    print("\n")

  def is_duplicate(paths: list, filename: str) -> bool:
    """
    #### Description
    Checks if a file already exists on any of the given paths
    #### Parameters
    - `filename`: the name of the file to be checked
    - `paths`: a list where each item represents a full path for a folder
    #### Returns
    `True` if found. Otherwise `False`
    #### Notes
    `filename` must have `no` trailing bars
    """
    for path in paths:
      if os.path.isfile(f"{path}/{filename}"):
        return True
    return False
