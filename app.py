from flask import Flask, render_template, request, redirect
import random
from index_forms import Menu
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


class Player:
    gold_counter = 0
    health_points = 5


def new_game(width, height):
    game_board = [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
    game_board[-1][0] = 2
    global gold_amount
    gold_amount = 0

    for row in game_board:
        if row[0] != 2:
            row[random.randint(0, len(row) - 1)] = 3 
        for cell in row:
            if cell == 1:
                gold_amount += 1
        print(*row)
    return game_board


@app.route('/', methods=['get', 'post'])
def index():
    global start_loc
    form = Menu()
    if form.validate_on_submit():
        width = form.width.data
        height = form.height.data
        Player.health_points = height
        Player.gold_counter = 0
        start_loc = new_game(width, height)
        return redirect(f'/game/{width}/{height}')
    return render_template('index.html', form=form)


@app.route('/game/<width>/<height>', methods=['get', 'post'])
def game(width, height):
    width = int(width)
    height = int(height)
    current_row = 0
    current_col = 0

    for i in range(height):
        for j in range(width):
            if start_loc[i][j] == 2:
                current_row = i
                current_col = j

    if Player.health_points and gold_amount == Player.gold_counter:
        return render_template('end-game-sheet.html', title='Ты выиграл!')

    if Player.health_points == 0:
        return render_template('end-game-sheet.html', title='Ты повержен!')

    up = request.form.get('up')
    if up == 'up' and 2 not in start_loc[0]:
        if start_loc[current_row - 1][current_col] == 1:
            Player.gold_counter += 1
        if start_loc[current_row - 1][current_col] == 3:
            Player.health_points -= 1
        start_loc[current_row - 1][current_col] = 2
        start_loc[current_row][current_col] = 0

    down = request.form.get('down')
    if down == 'down' and 2 not in start_loc[-1]:
        if start_loc[current_row + 1][current_col] == 1:
            Player.gold_counter += 1
        if start_loc[current_row + 1][current_col] == 3:
            Player.health_points -= 1
        start_loc[current_row + 1][current_col] = 2
        start_loc[current_row][current_col] = 0

    left = request.form.get('left')
    if left == 'left':
        check = True
        for j in range(height):
            if 2 != start_loc[j][0]:
                check = True
            else:
                check = False
                break

        if check:
            if start_loc[current_row][current_col - 1] == 1:
                Player.gold_counter += 1
            if start_loc[current_row][current_col - 1] == 3:
                Player.health_points -= 1
            start_loc[current_row][current_col - 1] = 2
            start_loc[current_row][current_col] = 0

    right = request.form.get('right')
    if right == 'right':
        check = False
        for j in range(height):
            if start_loc[j][-1] != 2:
                check = True
            else:
                check = False
                break
        if check:
            if start_loc[current_row][current_col + 1] == 1:
                Player.gold_counter += 1
            if start_loc[current_row][current_col + 1] == 3:
                Player.health_points -= 1
            start_loc[current_row][current_col + 1] = 2
            start_loc[current_row][current_col] = 0

    return render_template('game_part.html',
                           game_board=start_loc,
                           gold_counter=Player.gold_counter,
                           health_points=Player.health_points)


if __name__ == '__main__':
    app.run()
