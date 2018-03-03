import bottle
import os
import random
import numpy as np


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


global width
global height


def food_sniffer(my_head, food_locs):
    magnitudes = []

    for fud in food_locs:
        x_diff = abs(my_head[0] - fud[0])
        y_diff = abs(my_head[1] - fud[1])
        magnitudes.append(np.sqrt(x_diff**2 + y_diff**2))

    return magnitudes.index(min(magnitudes))


def move_right(me, others):
    my_move = [me[0][0] + 1, me[0][1]]
    for snek in others:
        if my_move in others[snek]:
            print('Another Snek! Right')
            return False

    for my_sick_bod in me:
        if my_move == my_sick_bod:
            print('My Bod! Right')
            return False

    if my_move[0] >= width:
        print('Muh mooooove! Right', my_move[0], width)
        return False

    return True


def move_left(me, others):
    my_move = [me[0][0] - 1, me[0][1]]
    for snek in others:
        if my_move in others[snek]:
            print('Another Snek! Left')
            return False

    for my_sick_bod in me:
        if my_move == my_sick_bod:
            print('My sick bod! Left')
            return False

    if my_move[0] < 0:
        print('Muh mooooove! Left', my_move[0], width)
        return False

    return True


def move_up(me, others):
    my_move = [me[0][0], me[0][1] - 1]
    for snek in others:
        if my_move in others[snek]:
            print('Another Snek! Up')
            return False

    for my_sick_bod in me:
        if my_move == my_sick_bod:
            print('My sick bod! Up')
            return False

    if my_move[1] < 0:
        print('Muh mooooove! Up', my_move[1], height)
        return False

    return True


def move_down(me, others):
    my_move = [me[0][0], me[0][1] + 1]
    for snek in others:
        if my_move in others[snek]:
            print('Another Snek! Down')
            return False

    for my_sick_bod in me:
        if my_move == my_sick_bod:
            print('My sick bod! Down')
            return False

    if my_move[1] >= height:
        print('Muh mooooove! Down', my_move[1], height)
        return False

    return True


def chasin_ma_tail(my_snake, my_length, other_sneks):
    my_head = my_snake[0]
    my_tail = my_snake[-1]
    x_diff = my_head[0] - my_tail[0]
    y_diff = my_head[1] - my_tail[1]


    if x_diff > 0 and y_diff > 0:


    if my_head[0] - my_tail[0] < 0:
        if move_right(my_snake, other_sneks):
            return 'right'
    if my_head[1] - my_tail[1] < 0:
        if move_down(my_snake, other_sneks):
            return 'down'
    if my_head[1] - my_tail[1] > 0:
        if move_up(my_snake, other_sneks):
            return 'up'
    if my_head[0] - my_tail[0] > 0:
        if move_left(my_snake, other_sneks):
            return 'left'

    return None

def move_snake(data):
    global width
    global height
    directions = ['up', 'down', 'left', 'right']
    my_snek_name = data['you']['name']
    my_snek_hangerings = data['you']['health']
    my_snek_longness = data['you']['length']
    other_sneks = {}
    other_coords = []
    my_snake = []
    food_locs = []

    for snake in data['snakes']['data']:
        if snake['name'] != my_snek_name:
            for key in snake['body']['data']:
                other_coords.append([key['x'], key['y']])
            other_sneks[snake['name']] = [other_coords, snake['health']]

    for key in data['you']['body']['data']:
        my_snake.append([key['x'], key['y']])

    if my_snek_hangerings < 51:

        for munchables in data['food']['data']:
            food_locs.append([munchables['x'], munchables['y']])

        closest_food_index = food_sniffer(my_snake[0], food_locs)

        close_food_x_diff = my_snake[0][0] - food_locs[closest_food_index][0]
        close_food_y_diff = my_snake[0][1] - food_locs[closest_food_index][1]

        if close_food_x_diff < 0:
            if move_right(my_snake, other_sneks):
                return 'right'
        if close_food_y_diff < 0:
            if move_down(my_snake, other_sneks):
                return 'down'
        if close_food_y_diff > 0:
            if move_up(my_snake, other_sneks):
                return 'up'
        if close_food_x_diff > 0:
            if move_left(my_snake, other_sneks):
                return 'left'

        if close_food_x_diff == 0:
            if move_left(my_snake, other_sneks):
                return 'left'
            elif move_right(my_snake, other_sneks):
                return 'right'
            else:
                pass

        if close_food_y_diff == 0:
            if move_up(my_snake, other_sneks):
                return 'up'
            elif move_down(my_snake, other_sneks):
                return 'down'
            else:
                pass
    else:
        where_to_go = chasin_ma_tail(my_snake, my_snek_longness, other_sneks)
        if where_to_go is not None:
            return where_to_go


    if move_right(my_snake, other_sneks):
        return 'right'
    if move_down(my_snake, other_sneks):
        return 'down'
    if move_up(my_snake, other_sneks):
        return 'up'
    if move_left(my_snake, other_sneks):
        return 'left'

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    global width
    width = data['width']
    global height
    height = data['height']

    return {
        'color': '#00FF00',
        'taunt': '{}'.format('STEEEEVE'),
        'head_type': 'bendr',
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    #for key in data:
        #print(key, type(data[key]), data[key])

    move_dir = move_snake(data)

    print(move_dir)

    return {
        'move': move_dir,
        'taunt': 'Grab my Terry-fold!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '192.168.99.1'), port=os.getenv('PORT', '8080'), debug=False)