import pyautogui
import time
import keyboard
import tkinter as tk
import threading
import csv
import os

class User:
    def __init__(self, name, icon_selection_time=2):
        self.name = name
        self.icon_selection_time = icon_selection_time
        self.log = []

    def add_log_entry(self, action):
        self.log.append((time.strftime("%Y-%m-%d %H:%M:%S"), action))

    def save_log_to_csv(self, log_folder="log"):
        log_filename = f"{self.name.replace(' ', '')}_log.csv"
        log_path = os.path.join(log_folder, log_filename)

        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        with open(log_path, mode='w', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['Timestamp', 'Action'])
            log_writer.writerows(self.log)

        print(f"User log saved to {log_path}")

# List of registered users
registered_users = []

# Load existing user data from CSV (if any)
for user in registered_users:
    try:
        with open(f"{user.name}_log.csv", mode='r') as log_file:
            log_reader = csv.reader(log_file)
            next(log_reader)  # Skip header row
            user.log.extend(log_reader)
    except FileNotFoundError:
        pass

def choose_or_register_user():
    root = tk.Tk()
    root.title("User Selection")

    selected_user = None

    def select_user():
        nonlocal selected_user
        selected_user_index = user_listbox.curselection()[0]
        selected_user = registered_users[selected_user_index]
        root.destroy()

    def register_user():
        nonlocal selected_user
        new_user_name = entry_name.get()
        icon_selection_time = entry_time.get()

        # Remove spaces from the full user name to create a log filename
        log_filename = f"{new_user_name.replace(' ', '')}_log.csv"

        new_user = User(new_user_name, float(icon_selection_time))
        registered_users.append(new_user)
        selected_user = new_user

        # Save user log to CSV with the created log filename
        selected_user.save_log_to_csv(log_filename)

        # Update the 'db.csv' file with the new user entry
        users_data_file = "db.csv"
        with open(users_data_file, mode='a', newline='') as users_file:
            users_writer = csv.writer(users_file)
            users_writer.writerow([new_user_name, log_filename, icon_selection_time])
            # Add a newline character after writing each row
            users_file.write('\n')

        root.destroy()


    label_instruction = tk.Label(root, text="Choose a user or register a new user:")
    label_instruction.pack(pady=10)

    user_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    for user in registered_users:
        user_listbox.insert(tk.END, user.name)
    user_listbox.pack(pady=10)

    button_select = tk.Button(root, text="Select User", command=select_user)
    button_register = tk.Button(root, text="Register User", command=register_user)

    button_select.pack(side=tk.LEFT, padx=10)
    button_register.pack(side=tk.RIGHT, padx=10)

    entry_name = tk.Entry(root, width=30)
    entry_name.insert(0, "Enter new user name")
    entry_name.pack(pady=5)

    entry_time = tk.Entry(root, width=30)
    entry_time.insert(0, "Enter icon selection time (seconds)")
    entry_time.pack(pady=5)

    root.mainloop()

    return selected_user

# Function to click on a desktop icon
def click_icon(item_current, user):
    x, y = desktop_icons[item_current]
    pyautogui.click(x, y)
    print(f"Icon {item_current + 1}/{len(desktop_icons)} selected by {user.name}.")
    time.sleep(user.icon_selection_time)
    user.add_log_entry(f"Icon {item_current + 1} selected")



# Desktop icons and settings
desktop_icons = []
num_shortcuts_hor = 3
num_shortcuts_ver = 8
item = 0

# Generate desktop icon coordinates
for i in range(num_shortcuts_hor):
    x_coordinate = 50 + i * 100
    for j in range(num_shortcuts_ver):
        y_coordinate = 50 + j * 120
        desktop_icons.append((x_coordinate, y_coordinate))

# Function to click on a desktop icon
def click_icon(item_current, user):
    x, y = desktop_icons[item_current]
    pyautogui.click(x, y)
    print(f"Icon {item_current + 1}/{len(desktop_icons)} selected by {user.name}.")
    time.sleep(user.icon_selection_time)

# Function to measure the duration of a key press
def key_press_duration():
    start_time = None
    end_time = None

    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and (event.name == "right" or event.name == "left") and start_time is None:
                start_time = time.time()
            if event.event_type == keyboard.KEY_UP and (event.name == "right" or event.name == "left"):
                end_time = time.time()
                if start_time is not None:
                    return float(end_time - start_time)
                else:
                    return 0.0
        except KeyboardInterrupt:
            return 0.0

# Function to open an application
def open_application():
    x, y = desktop_icons[item]
    pyautogui.click(x, y)
    pyautogui.click(x, y)
    close_window()
    exit(0)

# Function to restart the scan
def restart_scan(user):
    global item
    item = 0
    close_window()
    user.add_log_entry("Scan restarted")

# Function to close the window
def close_window():
    window.destroy()

# Window coordinates and interaction
window_coordinates = [(250, 200), (250, 250), (250, 300)]

# Function to scan the window for interaction
def scan_window():
    current_button = 0
    pyautogui.click(250, 150)
    
    while True:
        if current_button > 2:
            current_button = 0
        
        x, y = window_coordinates[current_button]
        pyautogui.moveTo(x, y)

        press_duration = key_press_duration()

        if press_duration > 2:
            pyautogui.click(x, y)
            break
        else:
            current_button += 1

# Function for window interaction
def window_interaction():
    # Start the window scan in the background
    scan_window_thread = threading.Thread(target=scan_window)
    scan_window_thread.daemon = True
    scan_window_thread.start()

    # Configure initial window settings
    window.title("Application Confirmation")
    window.geometry("300x200+100+100")

    # GUI components
    label_instruction = tk.Label(window, text="Do you want to open this application?")
    label_instruction.grid(column=0, row=0, padx=10, pady=10)

    button_accept = tk.Button(window, text="Yes", command=open_application)
    button_restart = tk.Button(window, text="No, restart scan", command=restart_scan)
    button_continue = tk.Button(window, text="No, continue scan", command=close_window)

    button_accept.grid(column=0, row=1, padx=10, pady=5)
    button_restart.grid(column=0, row=2, padx=10, pady=5)
    button_continue.grid(column=0, row=3, padx=10, pady=5)

    window.mainloop()

# Function for complete scan process
def complete_scan(user):
    global item
    click_icon(item, user)

    event = keyboard.read_event(suppress=True)
    press_duration = key_press_duration()

    if press_duration > 2:
        print("Pressed more than 2 seconds")
        global window
        window = tk.Tk()
        window_interaction()
    else:
        if keyboard.KEY_DOWN and event.name == 'right':
            item += 1
        elif keyboard.KEY_DOWN and event.name == 'left':
            item -= 1
        else:
            exit()

if __name__ == "__main__":
    # Load user data from CSV file
    users_data_file = "db.csv"
    try:
        with open(users_data_file, mode='r') as users_file:
            users_reader = csv.DictReader(users_file)
            for row in users_reader:
                name = row['name']
                log_file = row['log_file']
                time_seconds = float(row['time_seconds'])
                registered_users.append(User(name, time_seconds))
    except FileNotFoundError:
        pass

    # Choose or register a user
    selected_user = choose_or_register_user()

    # Display all user logs
    for user in registered_users:
        user.save_log_to_csv()

    # Continue with the rest of your code (scanning and interaction)
    while 0 <= item < len(desktop_icons):
        try:
            complete_scan(selected_user)
        except KeyboardInterrupt:
            exit()