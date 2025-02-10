Script that detects if new grades have been added. Requires a .env file to store the credentials for both the university and the Telegram API (https://core.telegram.org/bots/api).

.env file content:
```sh
USERNAME=
PASSWORD=
BOT_TOKEN=
CHAT_ID=
```

To run the script headless on a Linux server, uncomment lines 71-72 and comment out line 74. Additionally, install Xvfb with the following commands:
```sh
sudo apt-get update
sudo apt-get install -y xvfb
```

Run the script with :
xvfb-run -a python3 qis.py