import random


class Board:
    """
    a class that represents the Game board
    recommended player_amount is 4-6
    field_amount needs to be an even number, original game amount for 4 players is 40
    """
    def __init__(self, player_amount, field_amount):
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


class Figure:
    def __init__(self, name):
        self.name = name
        self.distance_to_target = -1
        self.field = -1
        self.target_field = -1
        self.finish_slot = -1

    def place(self, board):
        """
        method to place a figure
        """
        self.distance_to_target = board.field_amount

    def move(self, move_amount):
        """
        method to move a figure
        """
        self.distance_to_target = self.distance_to_target - move_amount

    def ban(self):
        """
        method to ban a figure
        """
        self.distance_to_target = -1
        self.field = -1
        self.target_field = -1


class Player:
    """a class that represents a Player of the Board Game"""
    def __init__(self, name, color, figure_amount):
        self.name = name
        self.id = "undefined"
        self.color = color
        self.figure_amount = figure_amount
        self.figures = []
        self.finished_figures = ["0"] * figure_amount
        self.turns = 0
        self.roll_turns = 0
        self.no = "undefined"

        # create start figures for player
        for x in range(self.figure_amount):
            figure = Figure("{}-{}-{}".format(self.name, self.color, x))
            self.figures.append(figure)

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
        for figure in self.figures:
            if figure.name in board.fields:
                return True

        return False

    def grab_figures_from_cemetery(self, board):
        """
        grab players figure(s) from the boards figure cemetery and reset them to figure start pit
        """
        # identify player's banned figures
        player_banned_figures = [figure for figure in board.figure_cemetery if self.name in figure.name]
        # in case there are any banned figures
        if len(player_banned_figures) != 0:
            for figure in player_banned_figures:
                # remove figure(s) from cemetery
                board.figure_cemetery.remove(figure)
                figure.ban()
                # reset figure(s) to start pit
                self.figures.append(figure)

    def place_figure(self, board):
        """
        method to place a new figure to the start position of a board
        """
        start_pos = board.players_start_pos[self.no]

        # in case start position blocked
        if hasattr(board.fields[start_pos], "name"):
            # remove foreign player figure
            board.figure_cemetery.append(board.fields[start_pos])
            print("Target field is blocked by foreign player! Banning figure {}!".format(board.fields[start_pos].name))
        removed_figure = self.figures.pop()
        removed_figure.place(board)
        board.fields[start_pos] = removed_figure

    def select_figure(self, board, move_amount):
        """
        method to select the most suitable figure
        """
        selected_figure = "undefined"

        # find next figure
        for field in board.fields:
            if hasattr(field, "name"):
                if self.name in field.name:
                    # set figure
                    figure = field
                    # get field of figure
                    figure.field = board.fields.index(figure)
                    # check if figure can finish
                    if figure.distance_to_target <= move_amount:
                        # determine free slots in finished_figures
                        free_slots =[]
                        for i in range(len(self.finished_figures)):
                            if self.finished_figures[i] == "0":
                                free_slots.append(i)
                        # return figure if free slot can be reached by move_amount
                        for slot in free_slots:
                            if abs(figure.distance_to_target - move_amount) == slot:
                                figure.finish_slot = slot
                                return figure
                    else:
                        # calc target field  of figure
                        figure.target_field = figure.field + move_amount
                        # handle field loop
                        if figure.target_field > board.field_amount - 1:
                            diff = board.field_amount - figure.field
                            figure.target_field = move_amount - diff
                        # check if more than one of player's figures on field
                        if len(self.figures) < 3:
                            # return figure if it has a chance to ban other figures
                            if hasattr(board.fields[figure.target_field], "name") and self.name not in board.fields[figure.target_field].name:
                                return figure
                            # determine figure with closest distance to target
                            if hasattr(selected_figure, "distance_to_target"):
                                if figure.distance_to_target < selected_figure.distance_to_target:
                                    selected_figure = figure
                            else:
                                selected_figure = figure
                        else:
                            return figure

        return selected_figure

    def move_figure(self, board, move_amount):
        """
        method to select and move a player figure
        """
        # select figure
        figure = self.select_figure(board, move_amount)
        # only proceed if there is a selected figure (figure that is movable)
        if figure != "undefined":
            # check if figure has possible finish slot
            if figure.finish_slot != -1:
                self.finish_figure(board, figure)
            else:
                # remove figure from old field
                board.fields[figure.field] = "0"
                # check if new field is blocked by another figure
                if hasattr(board.fields[figure.target_field], "name"):
                    # check if blocking figure owned by player
                    if self.name in board.fields[figure.target_field].name:
                        # keep player figure on old field
                        board.fields[figure.field] = figure
                        print("Target field is blocked by player's own figure {}! Revert move!".format(board.fields[figure.target_field].name))
                    else:
                        # remove foreign player figure
                        board.figure_cemetery.append(board.fields[figure.target_field])
                        print("Target field is blocked by foreign player! Banning figure {}!".format(board.fields[figure.target_field].name))
                        # move player figure to new field
                        figure.move(move_amount)
                        board.fields[figure.target_field] = figure
                else:
                    # move player figure to new field
                    figure.move(move_amount)
                    board.fields[figure.target_field] = figure

    def finish_figure(self, board, figure):
        board.fields[figure.field] = "0"
        self.finished_figures[figure.finish_slot] = figure
        print("Player {} reached the finish with figure {}!".format(self.name, figure.name))


# temp function to reveal player name on game board
def reveal_name(list):
    new_list = []
    for item in list:
        if hasattr(item, "name"):
            new_list.append(item.name)
        else:
            new_list.append(item)
    return new_list


# game init
no_winner = True

game_board = Board(4, 40)
p1 = Player("Dave", "Red", 4)
game_board.register_player(p1)
p2 = Player("Rose", "Yellow", 4)
game_board.register_player(p2)
p3 = Player("PuPu", "Black", 4)
game_board.register_player(p3)
p4 = Player("Pat", "Blue", 4)
game_board.register_player(p4)
players = [p1, p2, p3, p4]

# game loop
while no_winner:
    for player in players:
        # increment player turns
        player.turns += 1
        # grab players figures from cemetery
        player.grab_figures_from_cemetery(game_board)
        # check for player's figures on board
        if player.has_figures_on_board(game_board):
            if player.roll == 6:
                player.place_figure(game_board)
            player.move_figure(game_board, player.roll())
        # player has no figure on board
        else:
            # three chances to roll a 6
            for i in range(3):
                if player.roll() == 6:
                    # place new figure
                    player.place_figure(game_board)
                    # move figure
                    player.move_figure(game_board, player.roll())
                    break
        # count finished figures to evaluate win condition
        finished_figures = [figure for figure in player.finished_figures if hasattr(figure, "name")]
        if len(finished_figures) == player.figure_amount:
            no_winner = False
            print("Player {} won the game after {} turns!".format(player.name, player.turns))
            break
        # temp output of fields
        print(reveal_name(game_board.fields))
