
import instaloader
import os

def download_specific_highlight(instance, user, highlight_id):
    profile = instaloader.Profile.from_username(instance.context, user)
    os.makedirs(user, exist_ok=True)
    os.chdir(user)
    
    for highlight in instance.get_highlights(user=profile):
        if str(highlight.unique_id) == highlight_id:
            for item in highlight.get_items():
                instance.download_storyitem(item, '{}/{}'.format(highlight.owner_username, highlight.title))
            break
    
    os.chdir("..")

def delete_files_with_specific_extensions(folder_path, extensions):
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split(".")[-1]
            if file_extension in extensions:
                file_path = os.path.join(root_folder, file)
                try:
                    os.remove(file_path)
                    print(f"{file_path} deleted.")
                except Exception as e:
                    print(f"Error occurred while deleting {file_path}: {e}")

# Initialize Instaloader instance
instance = instaloader.Instaloader()
username = ""
password = ""

instance.compress_json = False

# Check if you have a session file to load, if not, login using credentials
try:
    instance.load_session_from_file(username, "cookies.txt")
except FileNotFoundError:
    try:
        instance.login(username, password)
    except:
        # If login fails, load the session using sessionid and csrftoken (not recommended if you use VPN)
        instance.load_session(username, {"sessionid": "YOUR SESSION ID HERE", "csrftoken": "YOUR CSRFTOKEN HERE"})

# Save the session to a file for future use
instance.save_session_to_file("cookies.txt")

if instance.context.is_logged_in:
    print(f"Logged as {username}")
else:
    print("An error occurred while logging into the account.")

# Specify the username and highlight ID
user = ""
highlight_id = ""  # Replace with your specific highlight ID

# Download the specific highlight
download_specific_highlight(instance, user, highlight_id)

# Delete unwanted files
folder_path = user
extensions = ["xz", "txt", "json"]
delete_files_with_specific_extensions(folder_path, extensions)

