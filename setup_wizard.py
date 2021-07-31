"""The setup wizard for both the Discord bot."""
import json
import os
import sys
import socket
from threading import Thread
from time import sleep


class Wizard:
    """The main class."""
    def __init__(self):
        os.system("clear")
        print("Welcome to the Discord bot setup.\n"
              "This tool will guide you to get your Discord bot running.")
        while True:
            token = input("Discord client token? ")
            if os.system(sys.executable + " test_token.py " + token) == 0:
                open(".TOKEN", "w").write(token)
                break
            else:
                print("Improper token. You need to use a token generated by the Discord developer portal.")
        os.system("clear")
        print("If you have not already set up the Minecraft server, please do it now. On start, it should show an IP.")
        while True:
            server_address = input("What's that IP? ")
            print("Trying to connect to the server...")
            t = Thread(target=self.ping_server, args=(server_address,))
            self.pingOk = False
            t.start()
            sleep(1)
            if self.pingOk:
                break
            else:
                print("The ping to the server failed! Please verify it is running and the IP is correct.")
        os.system("clear")
        print("The setup is now done. Starting the bot...")
        config = {
            "server_address": server_address,
            "bot_channel": None
        }
        json.dump(config, open("config.json", "w"))

    # Asks something to the user with allowed answers
    def _get_choice(self, allowed_values: str):
        allowed_values = [char for char in allowed_values]
        while True:
            choice = input(str(allowed_values) + ":")
            if choice in allowed_values:
                return choice
            else:
                print("Invalid input.")

    # Tests if the given IP has a Minecraft server running with the discadminecraft program.
    def ping_server(self, ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, 25556))
                s.sendall(b"ping")
                response = s.recv(1024)
            if response == b"pong":
                self.pingOk = True
        except ConnectionRefusedError:
            pass
