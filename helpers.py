import re, time, emoji

class misc_functions:
  def welcome():
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
    # Remove emojis
    result = emoji.replace_emoji(filename,"").strip()

    # Replace invalid characters with underscores
    result = re.sub(r'[\/:*?"<\ \>|]', '_', result).strip()

    return result

  def wait_for_it():
    for x in range(901, 0, -1):
      print(f"\033[33m⏰ Rate limit exceeded. Sleeping for {x} seconds  \033[0m", end='\r', flush=True)
      time.sleep(1)
    print("\n")
