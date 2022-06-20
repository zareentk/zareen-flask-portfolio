#!/bin/bash

tmux kill-session

cd /root/zareen-flask-portfolio || exit

git fetch && git reset origin/main --hard

python -m venv python3-virtualenv

source "/root/zareen-flask-portfolio/python3-virtualenv/bin/activate"

pip install -r requirements.txt

TMUX_SESSION="redeploy"
COMMAND="flask run --host=0.0.0.0"

tmux new-session -d -s "$TMUX_SESSION" "$COMMAND"

echo "name of tmux session is $TMUX_SESSION"