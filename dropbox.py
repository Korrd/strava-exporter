import dropbox as d
import getpass as g

class dropbox:

  def upload_file(file_path: str, dropbox_path: str, access_token: str) -> bool:
    dbx = d.Dropbox(access_token)
    try:
      with open(file_path, 'rb') as file:
        dbx.files_upload(file.read(), dropbox_path, mode=d.files.WriteMode('overwrite'))
      print(f"\033[91m❌ Failed to upload: {dropbox_path}\033[0m")
      return True
    except Exception as e:
      print(f"\033[94m📘 Dropbox upload successful: {dropbox_path}\033[0m")
      return False

  def ask_for_secrets() -> str:
    print("\033[93m⚠️  Please, provide your Dropbox access token.\n    You can get it from your dropbox app here: https://www.dropbox.com/developers/apps\033[0m")

    dropbox_token = g.getpass("\033[95m🔑 Dropbox Token: \033[0m")

    return dropbox_token

  def ask_for_dropbox_path() -> str:
    print("\033[93m⚠️  Please, provide a full path to a folder where you'd like to upload your tracks to Dropbox")

    dropbox_path = input("\033[95m📂 Dropbox Folder: \033[0m")

    return dropbox_path
