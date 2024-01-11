import re, time

class misc_functions:
  def welcome():
    print("_______________________")
    print("Strava workout exporter")
    print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n")

  def sanitize_filename(filename: str) -> str:
    # Replace invalid characters with underscores
    result = re.sub(r'[\/:*?"<\ \>|]', '_', filename)

    # Remove leading and trailing whitespaces
    result = result.strip()

    return result

  def wait_for_it():
    for x in range(901, 0, -1):
      print(f"⏰ Rate limit exceeded. Sleeping for {x} seconds  ", end='\r', flush=True)
      time.sleep(1)
    print("\n")
