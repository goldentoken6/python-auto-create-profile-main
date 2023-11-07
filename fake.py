import os
import shutil
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import upwork
import shutil

username = os.getlogin()

# Set the number of profiles to create
json_path = 'upwork/setting.json'
json_path = os.path.abspath(json_path)
num_profiles = upwork.loadJson(json_path)
# Specify the paths to the extensions (CRX files or directories)
extension_paths = [
    "adblocker.crx",
    "XBlocker 1.0.4",
    "XBlocker 1.0.4 - langpack"
]

base_directory = 'C:/path/to/profiles'
#Before restart fake, Delete the folder and its contents
if os.path.exists(base_directory):
    # Delete the folder
    shutil.rmtree(base_directory)
else:
    print(f"The directory '{base_directory}' does not exist.")
    
def create_profile(base_directory, profile_name, extension_paths):

    # Create the path for the new profile directory
    new_profile_directory = os.path.join(base_directory, profile_name)
    # Create the new profile directory if it doesn't exist
    if not os.path.exists(new_profile_directory):
        os.makedirs(new_profile_directory)

        # Create an instance of ChromeOptions
    driver = upwork.install_extensions_on_profile( new_profile_directory, extension_paths )
    # openTempMail(driver)
    email = upwork.openMinuteInBox(driver)
    # slide 6_skill and slide 10 person information
    upwork.loadJson(json_path)
    # open Upwork
    upwork.openUpwork(driver, email)

def profiles(base_directory, num_profiles, extension_paths):
    for i in range(num_profiles):
        upwork.getDataFromJson(i)
        profile_name = f'profile{i+1}'
        create_profile(base_directory, profile_name, extension_paths)

profiles(base_directory, num_profiles, extension_paths)
