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

    def place_figure(self, board):
        """
        method to place a new figure to the start position
        """
        # TODO handle exception in case start field is blocked by other figure
        removed_figure = self.figures.pop()
        board.fields[self.no] = removed_figure

    def move_figure(self, board, move_amount):
        """
        method to move a player figure
        """
        # find next figure
        for field in board.fields:
            if self.id in field:
                # get figure name
                figure = field
                # get index of figure
                figure_index = board.fields.index(field)
                # calc new index of figure
                new_field = figure_index + move_amount
                # handle field loop
                if new_field > board.field_amount - 1:
                    diff = board.field_amount - figure_index
                    new_field = move_amount - diff

        print("Moving the figure {} {} fields forward!".format(figure, move_amount))
        # remove figure from old field
        board.fields[figure_index] = "0"
        # add figure to new field
        board.fields[new_field] = figure
        # TODO intelligently select figure to move if more on board

# temp Tests
game_board = Board(4, 40)
p1 = Player("Dave", "Red")
p2 = Player("Rose", "Yellow")
game_board.register_player(p1)
game_board.register_player(p2)
print(game_board.fields)
print(game_board.players)
print(game_board.players_start_pos)

p1.place_figure(game_board)
print(game_board.fields)
p1.move_figure(game_board, p1.roll())
print(game_board.fields)

'''
dice_eye = p1.roll()
print(dice_eye)
if dice_eye == 6:
    p1.place_figure(game_board)
    print(game_board.fields)
    p1.move_figure(game_board, p1.roll())
    print(game_board.fields)

'''



