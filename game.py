from classes import Board, Player
from logger_conf import logger, reveal_name
import streamlit as st
import pandas as pd


def simulate_game(player_amount, figure_amount, field_amount, roll_duration, move_duration):
    # game init
    no_winner = True

    game_board = Board(player_amount, field_amount)
    players = []
    for i in range(player_amount):
        player = Player("Player-{}".format(i), "Color-{}".format(i), figure_amount)
        game_board.register_player(player)
        players.append(player)

    # game loop
    logger.info("Starting new game simulation..")
    while no_winner:
        for player in players:

            # increment player turns
            player.turns += 1
            logger.info("Player {}, Turn {}:".format(player.name, player.turns))
            logger.debug("Player data before turn: start figures: {}, finished figures: {}".format(reveal_name(player.start_figures), reveal_name(player.finished_figures)))
            # grab players figures from cemetery
            player.grab_figures_from_cemetery(game_board)
            # check for player's figures on board
            if player.has_figures_on_board(game_board):
                if player.roll(roll_duration) == 6 and len(player.start_figures) != 0:
                    player.place_figure(game_board)
                player.move_figure(game_board, player.roll(roll_duration), move_duration)
            # player has no figure on board
            else:
                # three chances to roll a 6
                for i in range(3):
                    if player.roll(roll_duration) == 6:
                        # place new figure
                        player.place_figure(game_board)
                        # move figure
                        player.move_figure(game_board, player.roll(roll_duration), move_duration)
                        break
            # count finished figures to evaluate win condition
            finished_figures = [figure for figure in player.finished_figures if hasattr(figure, "name")]
            if len(finished_figures) == player.figure_amount:
                no_winner = False
                total_real_playtime = sum([player.real_playtime for player in players]) / 60
                total_real_playtime = round(total_real_playtime, 2)
                amount_of_six_stats = [player.amount_of_six for player in players]
                total_dice_eye_stats = [player.total_roll for player in players]
                player_names = [player.name for player in players]
                aos = pd.DataFrame(amount_of_six_stats, index=player_names, columns=["amount"])
                tde = pd.DataFrame(total_dice_eye_stats, index=player_names, columns=["sum"])
                logger.info("Player {} won the game after {} turns!".format(player.name, player.turns))
                st.success("Player {} won the game after {} turns and {} rolls!".format(player.name, player.turns, player.roll_turns))
                st.info("By using this simulator you saved {} minutes of your life avoiding playing senseless games! :)".format(total_real_playtime))
                st.subheader("Sum of dice eyes per player")
                st.bar_chart(tde)
                st.subheader("Total amount of dice eye 6 rolls per player")
                st.bar_chart(aos)
                break

            logger.debug("Player data after turn: start figures: {}, finished figures: {}".format(reveal_name(player.start_figures), reveal_name(player.finished_figures)))
            # debug output of board fields
            logger.debug("Board fields after turn: {}".format(reveal_name(game_board.fields)))


st.title("Mensch ärgere dich nicht")
st.header("Simulation of a german board game")
player_input = st.number_input("Amount of Players:", min_value=2, max_value=6, value=4)
figure_input = st.number_input("Amount of Figures per Player:", min_value=1, max_value=4, value=4)
field_input = st.number_input("Amount of Fields on the Game Board:", min_value=40, max_value=60, step=2, value=40)
roll_duration_input = st.number_input("Duration of one roll in realtime (seconds):", min_value=2, max_value=6, value=3)
move_duration_input = st.number_input("Duration of one figure movement in realtime (seconds):", min_value=5, max_value=15, value=8)

if st.button("Start Game Simulation"):
    simulate_game(player_input, figure_input, field_input, roll_duration_input, move_duration_input)
