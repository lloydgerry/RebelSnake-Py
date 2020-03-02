import json
import os
import random

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "RebelSnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#002366", "headType": "bendr", "tailType": "hook"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))
    directions = ["up", "down", "left", "right"]
    move = None
    shout = "I am a python snake, hear me slither!"
    
    if not data:
        return "data is null"
    # Avoid wall
    board_width = data["board"]["width"]
    board_height = data["board"]["height"]
    my_body = data["you"]["body"]
    head = my_body[0]
    head_prev = my_body[1]
    your_x = head["x"]
    your_y = head["y"]
    print(board_width)

    last_move = (head["x"] - head_prev["x"]) + 2*(head["y"] - head_prev["y"])
    # -1 = left
    # 1 = right
   # -2 = up
    # 2 = down
    # 0 = start
    if (last_move == -1):
        last_move = 'left'
    if (last_move == 1):
        last_move = 'right'
    if (last_move == -2):
        last_move = 'up'
    if (last_move == 2):
        last_move = 'down'
    if (last_move == 0):
        last_move = 'start'

    start_of_game = last_move == 'start'

    if (start_of_game):
        # TODO: need to fix when we start next to a wall
        random.choice(directions)

    top_of_board = board_height - 1 == your_y
    bottom_of_board = board_height == 0
    right_of_board = board_width - 1 == your_y
    left_of_board = board_width == 0

    if top_of_board and last_move == 'up':
        move = random.choice("left", "right")
    elif bottom_of_board and last_move == 'down':
        move = random.choice("left", "right")
    elif right_of_board and last_move == 'right':
        move = random.choice("up", "down")
    elif left_of_board and last_move == 'left':
        move = random.choice("up", "down")
    #else:
        # Choose a random direction to move in if not avoiding wall
        #move = random.choice(directions)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
   
    print(f'move is: {move}')

    if not move:
        move = last_move

    response = {
        "move": move,
        #"shout": shout,
    }
    last_move = response["move"]

    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
