@echo off
set DISCORD_TOKEN=xxxx
set PLUGINS=bans
if not exist venv (
    python -m venv venv
    venv\Scripts\python.exe -m pip install --upgrade pip
    venv\Scripts\pip install -r requirements.txt
)
:loop
venv\Scripts\python run.py
goto loop
