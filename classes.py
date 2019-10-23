import random


class Board:
    """
    a class that represents the Game board
    recommended player_amount is 4-6
    field_amount needs to be an even number, original game amount for 4 players is 40
    """
    def __init__(self, player_amount, field_amount):
        # TODO implement exception for invalid field and player amounts
        self.field_amount = field_amount
        self.fields = ["0"] * field_amount
        self.player_amount = player_amount
        self.players = []
        self.players_start_pos = []
        self.next_start_index = 0
        self.figure_cemetery = []

    def register_player(self, player):
        """
        method to register a new player
        """
        # only register unknown players
        if player.id not in self.players:
            # register player id
            player.id = "{}-{}".format(player.name, player.color)
            self.players.append(player.id)
            # set player number
            player.no = len(self.players) - 1
            # register player start pos
            self.players_start_pos.append(self.next_start_index)
            # increase start index for next player to register
            self.next_start_index += int(self.field_amount / self.player_amount)


class Player:
    """a class that represents a Player of the Board Game"""
    def __init__(self, name, color):
        self.name = name
        self.id = "undefined"
        self.color = color
        self.figures = []
        # TODO implement turns in game loop
        self.turns = 0
        self.roll_turns = 0
        self.no = "undefined"

        # TODO consider dynamic figure amount
        # create start figures for player
        for i in range(4):
            self.figures.append("{}-{}-{}".format(self.name, self.color, i))

    def roll(self):
        """
        method to roll the dice, returns the dice eye
        """
        self.roll_turns += 1

        return random.randint(1, 6)

    def has_figures_on_board(self, board):
        """
        method to check if player has figures on the board, returns boolean
        """
        return self.figures in board.fields

    def grab_figures_from_cemetery(self, board):
        """
        grab players figure(s) from the boards figure cemetery and reset them to figure start pit
        """
        # identify player's banned figures
        player_banned_figures = [figure for figure in board.figure_cemetery if self.name in figure]
        # in case there are any banned figures
        if len(player_banned_figures) != 0:
            for figure in player_banned_figures:
                # remove figure(s) from cemetery
                board.figure_cemetery.remove(figure)
                # reset figure(s) to start pit
                self.figures.append(figure)

    def place_figure(self, board):
        """
        method to place a new figure to the start position
        """
        start_pos = board.players_start_pos[self.no]

        # in case start position blocked
        if board.fields[start_pos] != "0":
            # remove foreign player figure
            board.figure_cemetery.append(board.fields[start_pos])
            print("Target field is blocked by foreign player! Banning figure {}!".format(board.fields[start_pos]))
        removed_figure = self.figures.pop()
        board.fields[start_pos] = removed_figure

    def move_figure(self, board, move_amount):
        """
        method to select and move a player figure
        """
        # TODO intelligently select figure if more on board
        # TODO prio 1: cause there is the chance to ban another players figure
        # TODO prio 2: figure with the closest distance to finish

        # TODO implement logic to put a figure to finish pit
        figure = ""

        # find next figure
        for field in board.fields:
            if self.id in field:
                # get figure name
                figure = field

        # get index of figure
        figure_index = board.fields.index(figure)
        # calc new index of figure
        new_field = figure_index + move_amount
        # handle field loop
        if new_field > board.field_amount - 1:
            diff = board.field_amount - figure_index
            new_field = move_amount - diff

        # remove figure from old field
        board.fields[figure_index] = "0"
        # check if new field is blocked by another figure
        if board.fields[new_field] != "0":
            # check if blocking figure owned by player
            if self.name in board.fields[new_field]:
                # keep player figure on old field
                board.fields[figure_index] = figure
                print("Target field is blocked by player's own figure {}! Revert move!".format(board.fields[new_field]))
            else:
                # remove foreign player figure
                board.figure_cemetery.append(board.fields[new_field])
                print("Target field is blocked by foreign player! Banning figure {}!".format(board.fields[new_field]))
                # add player figure to new field
                board.fields[new_field] = figure
        else:
            # add player figure to new field
            board.fields[new_field] = figure


# temp Tests
game_board = Board(4, 40)
p1 = Player("Dave", "Red")
p2 = Player("Rose", "Yellow")
game_board.register_player(p1)
game_board.register_player(p2)

p1.place_figure(game_board)
p2.place_figure(game_board)
print(game_board.fields)
p1.move_figure(game_board, 10)
print(game_board.fields)
print(game_board.figure_cemetery)
p2.grab_figures_from_cemetery(game_board)
print(game_board.figure_cemetery)
print(p2.figures)

'''
dice_eye = p1.roll()
print(dice_eye)
if dice_eye == 6:
    p1.place_figure(game_board)
    print(game_board.fields)
    p1.move_figure(game_board, p1.roll())
    print(game_board.fields)
'''



