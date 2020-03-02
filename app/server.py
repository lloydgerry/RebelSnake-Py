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
    print(f'board width is: {board_width}')

    last_move_coordinate = (head["x"] - head_prev["x"]) + 2*(head["y"] - head_prev["y"])
    # -1 = left
    # 1 = right
   # -2 = up
    # 2 = down
    # 0 = start
    if (last_move_coordinate == -1):
        last_move = 'left'
    elif (last_move_coordinate == 1):
        last_move = 'right'
    elif (last_move_coordinate == -2):
        last_move = 'up'
    elif (last_move_coordinate == 2):
        last_move = 'down'
    elif (last_move_coordinate == 0):
        last_move = 'start'

    print(f'last move is: {last_move}')
    start_of_game = last_move == 'start'

    if (start_of_game):
        # TODO: need to fix when we start next to a wall
        random.choice(directions)

    top_of_board = your_y == 0
    bottom_of_board = board_height - 1 == your_y
    left_of_board = your_x == 0
    right_of_board = board_width - 1 == your_x

    print(f'top_of_board is: {top_of_board}')
    print(f'last_move == "up" is: {last_move == "up"}')
    print(f'board_height is: {board_height}')
    print(f'your_y is: {your_y}')
    

    # Remove invalid direction based on our last move
    if last_move == "up":
        directions.remove("down")
    if last_move == "left":
        directions.remove("right")
    if last_move == "right":
        directions.remove("left")
    if last_move == "down":
        directions.remove("up")

    # Remove invalid direction based on if at edge of map
    if top_of_board:
        directions.remove("up")
    if bottom_of_board:
        directions.remove("down")
    if right_of_board:
        directions.remove("right")
    if left_of_board:
        directions.remove("left")
    #else:
        # Choose a random direction to move in if not avoiding wall
        #move = random.choice(directions)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
   
    move = random.choice(directions)
    
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
