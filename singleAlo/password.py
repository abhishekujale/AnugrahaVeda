import subprocess

def get_available_wifi_networks():
    # Run the command to get the list of available WiFi networks
    networks_data = subprocess.check_output(['netsh', 'wlan', 'show', 'network']).decode('utf-8').split('\n')
    available_networks = [line.split(':')[1][1:-1] for line in networks_data if "SSID" in line]
    return available_networks

def get_saved_wifi_passwords():
    # Run the command to get the list of WiFi profiles
    profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in profiles_data if "All User Profile" in i]

    wifi_passwords = []
    
    # Loop through each profile and get the password
    for profile in profiles:
        profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
        password = None
        for line in profile_info:
            if "Key Content" in line:
                password = line.split(":")[1][1:-1]
                break
        wifi_passwords.append((profile, password))

    return wifi_passwords

def get_available_saved_wifi_passwords():
    available_networks = get_available_wifi_networks()
    saved_passwords = get_saved_wifi_passwords()
    
    available_saved_passwords = []
    
    for wifi, password in saved_passwords:
        if wifi in available_networks:
            available_saved_passwords.append((wifi, password))
    
    return available_saved_passwords

# Get and print saved WiFi passwords for currently available networks
available_saved_passwords = get_available_saved_wifi_passwords()
for wifi, password in available_saved_passwords:
    print(f"SSID: {wifi}, Password: {password if password else 'None'}")
