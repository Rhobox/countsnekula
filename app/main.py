import bottle
import os
import random
import math


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


global width
global height
global jitter
jitter = None


def food_sniffer(my_head, food_locs):
    magnitudes = []

    for fud in food_locs:
        x_diff = abs(my_head[0] - fud[0])
        y_diff = abs(my_head[1] - fud[1])
        magnitudes.append(math.sqrt(x_diff**2 + y_diff**2))

    return magnitudes.index(min(magnitudes))


def move_right(me, others):
    my_move = [me[0][0] + 1, me[0][1]]
    for snek in others:
        print(others[snek][0])
        if my_move in others[snek]:
            print('Another Snek! Right')
            return False
        elif my_move == [others[snek][0][0][0] + 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0] - 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] - 1]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] + 1]:
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
        print(others[snek][0])
        if my_move in others[snek]:
            print('Another Snek! Left')
            return False
        elif my_move == [others[snek][0][0][0] + 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0] - 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] - 1]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] + 1]:
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
        print(others[snek][0])
        if my_move in others[snek]:
            print('Another Snek! Up')
            return False
        elif my_move == [others[snek][0][0][0] + 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0] - 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] - 1]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] + 1]:
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
        print(others[snek][0])
        if my_move in others[snek]:
            print('Another Snek! Down')
            return False
        elif my_move == [others[snek][0][0][0] + 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0] - 1, others[snek][0][0][1]]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] - 1]:
            return False
        elif my_move == [others[snek][0][0][0], others[snek][0][0][1] + 1]:
            return False

    for my_sick_bod in me:
        if my_move == my_sick_bod:
            print('My sick bod! Down')
            return False

    if my_move[1] >= height:
        print('Muh mooooove! Down', my_move[1], height)
        return False

    return True


def square_cw(my_snake, my_length, other_sneks, recursive = False):
    for x in range(1, my_length):
        if my_length/x in range(x-1, x+1):
            sq_width = x
            sq_height = my_length/x

    snek_x = []
    snek_y = []
    unique_x = []
    unique_y = []

    for coords in my_snake:
        snek_x.append(coords[0])
        snek_y.append(coords[1])

    for x in snek_x:
        if x not in unique_x:
            unique_x.append(x)

    for y in snek_y:
        if y not in unique_y:
            unique_y.append(y)

    print(sq_width, len(unique_x))
    if len(unique_x) < sq_width:
        if move_left(my_snake, other_sneks):
            return 'left'
        elif move_right(my_snake, other_sneks):
            return 'right'
        elif not recursive:
            return square_ccw(my_snake, my_length, other_sneks, True)

    print(sq_height, len(unique_y))
    if len(unique_y) < sq_height:
        if move_up(my_snake, other_sneks):
            return 'up'
        elif move_down(my_snake, other_sneks):
            return 'down'
        elif not recursive:
            return square_ccw(my_snake, my_length, other_sneks, True)

    if move_right(my_snake, other_sneks):
        return 'right'
    elif move_down(my_snake, other_sneks):
        return 'down'

    return None


def square_ccw(my_snake, my_length, other_sneks, recursive = False):
    for x in range(1, my_length):
        if my_length / x in range(x - 1, x + 1):
            sq_width = x
            sq_height = my_length / x

    snek_x = []
    snek_y = []
    unique_x = []
    unique_y = []

    for coords in my_snake:
        snek_x.append(coords[0])
        snek_y.append(coords[1])

    for x in snek_x:
        if x not in unique_x:
            unique_x.append(x)

    for y in snek_y:
        if y not in unique_y:
            unique_y.append(y)

    print(sq_width, len(unique_x))
    if len(unique_x) < sq_width:
        if move_left(my_snake, other_sneks):
            return 'left'
        elif move_right(my_snake, other_sneks):
            return 'right'
        elif not recursive:
            return square_cw(my_snake, my_length, other_sneks, True)

    print(sq_height, len(unique_y))
    if len(unique_y) < sq_height:
        if move_up(my_snake, other_sneks):
            return 'up'
        elif move_down(my_snake, other_sneks):
            return 'down'
        elif not recursive:
            return square_ccw(my_snake, my_length, other_sneks, True)

    if move_left(my_snake, other_sneks):
        return 'left'
    elif move_up(my_snake, other_sneks):
        return 'up'

    return None

def chasin_ma_tail(my_snake, my_length, other_sneks):
    my_head = my_snake[0]
    my_tail = my_snake[-1]
    x_diff = my_head[0] - my_tail[0]
    y_diff = my_head[1] - my_tail[1]

    if (x_diff > 0 and y_diff > 0) or (x_diff < 0 and y_diff > 0) and move_right(my_snake, other_sneks)\
            and move_down(my_snake, other_sneks):
        print('Sq_CW')
        return square_cw(my_snake, my_length, other_sneks)
    elif (x_diff > 0 and y_diff <0) or (x_diff < 0 and y_diff < 0) and move_left(my_snake, other_sneks)\
            and move_up(my_snake, other_sneks):
        print('sq_CCW')
        return square_ccw(my_snake, my_length, other_sneks)

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
        'taunt': '{}'.format('It is I, Count Snekula!'),
        'head_type': 'bendr',
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    global jitter
    if jitter is None:
        jitter = 0
    elif jitter == 0:
        jitter = 1
    else:
        jitter = 0
    data = bottle.request.json

    #for key in data:
        #print(key, type(data[key]), data[key])

    move_dir = move_snake(data)

    if jitter == 0:
        taunt = 'I\'ve got the jitters!'
    else:
        taunt = 'Jitter! Jitter! Jitter'

    return {
        'move': move_dir,
        'taunt': taunt
    }

@bottle.post('/end')
def end():
    return {}

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'), debug=False)
