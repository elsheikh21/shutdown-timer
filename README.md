# shutdown-timer
Just an app to shutdown your PC after a given amount of time, I developed solely because it was a boring Saturday

## How to use

- The app basically has an input widget (from PyQT5) that user enters the number of minutes, after which his/her PC will shutdown automatically
- Expect a notification to pop up informing you of when it will shutdown


## How to setup

- Clone the project - `git clone https://github.com/elsheikh21/shutdown-timer/`
- Make sure poetry is installed. `poetry install`
- run the app `poetry run python -m main.py`
- to package it `poetry run pyinstaller --clean --onedir --name "Shutdown timer" --icon ./image.ico --add-data ./logo.ico;. --add-data ./config.yml;. --version-file version.txt main.py`
