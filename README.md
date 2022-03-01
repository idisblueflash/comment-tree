# Comment Tree Project by Flash Hu

## Install
1. create virtual env

    `python3 -m venv venv`
2. install packages

    `source venv/bin/activate`

    `pip install -r requirements.txt`
## Run server
run server with:
`./server_up.sh`

## Generate Testing Data [Optional]
1. setup flask

    `source venv/bin/activate`

    `export FLASK_APP=comment-tree.py`
2. reset database

    `flask reset-db`
3. generate a random user

    `flask generate-user`

4. generate 5 random users

    `flask generate-user -n 5`

5. generate 3 random comments

    `flask generate-comment -n 3`

6. generate 6 random reply

    `flask generate-random-reply -n 6`

7. generate 9 levels reply from the first comment

    `flask generate-random-deep-reply -l 9`
