import dropbox as d
import getpass as g

class dropbox:

  def list_files(access_token: str, folder_path: str):
    dbx = d.Dropbox(access_token)
    try:
      result = dbx.files_list_folder(folder_path)
      file_names = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)]
      return file_names
    except:
      return []

  def upload_file(file_path: str, dropbox_path: str, access_token: str) -> bool:
    dbx = d.Dropbox(access_token)
    try:
      with open(file_path, 'rb') as file:
        dbx.files_upload(file.read(), dropbox_path, mode=d.files.WriteMode('overwrite'))
      print(f"\033[94m📘 Dropbox upload successful at \"{dropbox_path}\"\033[0m")
      return True
    except:
      print(f"\033[91m❌ Failed to upload \"{dropbox_path}\"\033[0m")
      return False

  def ask_for_secrets() -> str:
    print("\033[93m⚠️  Please, provide your Dropbox access token.\n    You can get it from your dropbox app here: https://www.dropbox.com/developers/apps\033[0m")

    dropbox_token = g.getpass("\033[95m🔑 Dropbox Token: \033[0m")

    return dropbox_token

  def ask_for_dropbox_path() -> str:
    print("\033[93m⚠️  Please, provide a full path to Dropbox a folder to store your tracks on")

    dropbox_path = input("\033[95m📂 Dropbox Folder: \033[0m")

    return dropbox_path
