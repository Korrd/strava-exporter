"""
This module provides configuration management functionality
"""
import json
import getpass as g

class Config:
  """
  #### Description
  This class provides configuration management functionality
  #### Available functions.
  - `ask_for_path(message: str, prompt: str) -> str`: asks the user for a path
  - `read_config_file(config_file: str) -> tuple`: reads the config file
  - `read_downloaded_workouts(db_file: str) -> dict`: reads the downloaded workouts database
  - `write_config_file(config_file: str, tracks_output_path: str, workouts_output_path: str)`: writes the config file
  - `write_downloaded_workouts(db_file: str, workout_db: dict)`: writes the downloaded workouts database
  """

  def ask_for_path(self, message: str, prompt: str) -> str:
    """
    #### Description
    Asks the user for a path
    #### Parameters
    - `message`: message to display before the prompt
    - `prompt`: prompt to display
    #### Returns
    The path provided by the user
    """
    print(message)
    return g.getpass(prompt)

  def read_config_file(self, config_file: str) -> tuple:
    """
    #### Description
    Reads the config file
    #### Parameters
    - `config_file`: path to the config file
    #### Returns
    A tuple containing (tracks_output_path, workouts_output_path)
    """
    with open(config_file, 'r', encoding="utf8") as f:
      config = json.load(f)
      return config['tracks_output_path'], config['workouts_output_path']

  def write_config_file(self, config_file: str, tracks_output_path: str, workouts_output_path: str):
    """
    #### Description
    Writes the config file
    #### Parameters
    - `config_file`: path to the config file
    - `tracks_output_path`: path where tracks will be stored
    - `workouts_output_path`: path where workouts will be stored
    """
    config = {
      'tracks_output_path': tracks_output_path,
      'workouts_output_path': workouts_output_path
    }
    with open(config_file, 'w', encoding="utf8") as f:
      json.dump(config, f, indent=2)

  def read_downloaded_workouts(self, db_file: str) -> dict:
    """
    #### Description
    Reads the downloaded workouts database
    #### Parameters
    - `db_file`: path to the database file
    #### Returns
    A dictionary containing the downloaded workouts
    """
    with open(db_file, 'r', encoding="utf8") as f:
      return json.load(f)

  def write_downloaded_workouts(self, db_file: str, workout_db: dict):
    """
    #### Description
    Writes the downloaded workouts database
    #### Parameters
    - `db_file`: path to the database file
    - `workout_db`: dictionary containing the downloaded workouts
    """
    with open(db_file, 'w', encoding="utf8") as f:
      json.dump(workout_db, f)
