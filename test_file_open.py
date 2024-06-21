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
