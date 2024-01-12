import re, time, emoji

class misc_functions:
  def welcome():
    print("╔═════════════════════════╗".center(80))
    print("║ Strava Workout Exporter ║".center(80))
    print("╚═╦══════════╦══════════╦═╝".center(80))
    print("Created by:  Victor Martin  ║" + (" " * 10) + "║" + (" " * 10) + "║     Github: @korrd")
    print("┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╜" + (" " * 10) + "║" + (" " * 10) + "╙┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈")
    print((" " * 39) + "║")
    print((" " * 16) + "12-01-2024 ┌┈┈┈┈┈┈┈┈┈┈┈╨┈┈┈┈┈┈┈┈┈┈┐ Spain")
    print((" " * 16) + ("═" * 11) + "╛" + (" " * 22) + "╘" + ("═" * 6))
    print(("┈" * 70))

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
