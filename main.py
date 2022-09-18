from doctest import master
from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd
import requests
import nba_api
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats import endpoints
from nba_api.stats.static import players
import sys

#NBA Players Comparison Program
#
#This program takes in user input for NBA Players and years and outputs a comparison of the two players in the desired years
#Displayed in a simple GUI format
#
#authors: Siddharth Prabakar
#version@ Septmeber 12, 2022

#GETTING PLAYER INFO AS DATA FRAMES
def main(player_1, player_2):
    #Getting dataframe for player 1 chosen by user
    player1 = str(player_1)
    player1_id = find_id(player1)
    player1_season_totals = get_season_totals(player1_id)[["PLAYER_ID", "SEASON_ID", "GP", "FG_PCT", "FG3_PCT", "FT_PCT", "REB", "AST", "PTS"]]

    # Getting dataframe for player 2 chosen by user
    player2 = str(player_2)
    player2_id = find_id(player2)
    player2_season_totals = get_season_totals(player2_id)[["PLAYER_ID", "SEASON_ID", "GP", "FG_PCT", "FG3_PCT", "FT_PCT", "REB", "AST", "PTS"]]

    add_year_search(player1_season_totals, player2_season_totals)

#FINDING ID OF THE PLAYER
def find_id(user_input):
    #Getting a filtered data frame of players by comparing user input to the values in the "full_name" column of nba_api.stats.static.players.py dataset
    lower_user_input = user_input.lower()
    player_data_frame = pd.DataFrame(players.get_players())
    player_data_frame["lower_full_name"] = player_data_frame["full_name"].str.lower()
    filtered_frame = player_data_frame[player_data_frame.lower_full_name == lower_user_input]

    #checking to see if filtered frame is empty. If it is, then user entered invalid input, so program is terminated
    if filtered_frame.empty:
        print("Invalid player name. Please enter full first and last name")
        exit()
    user_player_id = filtered_frame.iloc[0, 0]
    return user_player_id

#GETTING CAREER TOTALS OF PLAYER
def get_season_totals(user_player_id):
    data = endpoints.PlayerCareerStats(player_id=user_player_id).get_data_frames()

    career_totals_all_star_season = data[0]
    return career_totals_all_star_season

#ADDING THE DROPDOWNS FOR YEAR AND BUTTON TO GET COMPARISON RESULTS
def add_year_search(player1_stats, player2_stats):
    #Declaring and placing dropdown for player 1's year
    variable1 = StringVar(master)
    variable1.set("Select Year")

    player1_year_entry = OptionMenu(root, variable1, *list(player1_stats["SEASON_ID"]))
    player1_year_entry.grid(row=4, column=0)

    # Declaring and placing dropdown for player 2's year
    variable2 = StringVar(root)
    variable2.set("Select Year")

    player2_year_entry = OptionMenu(root, variable2, *list(player2_stats["SEASON_ID"]))
    player2_year_entry.grid(row=4, column=3)

    #declaring and placing "Let's Compare
    lets_compare_button = Button(root, text="Let's Compare", command=lambda: compare_players(player1_stats, player2_stats, str(variable1.get()), str(variable2.get())))
    lets_compare_button.grid(row=5, column=2)

#COMPARING PLAYERS BASED ON USER'S CHOICE OF PLAYERS AND YEARS
def compare_players(player1_statframe, player2_statframe, player1_year, player2_year):
    #creates a frame to display the comparison results
    comparison_frame = LabelFrame(root, width=500, height=250, labelanchor="n")
    comparison_frame.grid(row=6, column=0, columnspan=4)

    #filters the player datasets into just the data for the years chosen by user
    filtered_frame_player1 = player1_statframe[player1_statframe.SEASON_ID == player1_year]
    filtered_frame_player2 = player2_statframe[player2_statframe.SEASON_ID == player2_year]

    #STATS LABELS
    gp_label = Label(comparison_frame, text="GAMES PLAYED", fg="green")
    gp_label.grid(row=0, column=1)

    points_label = Label(comparison_frame, text="POINTS", fg="green")
    points_label.grid(row=1, column=1)

    rebounds_label = Label(comparison_frame, text="REBOUNDS", fg="green")
    rebounds_label.grid(row=2, column=1)

    assists_label = Label(comparison_frame, text="ASSISTS", fg="green")
    assists_label.grid(row=3, column=1)

    fgp_label = Label(comparison_frame, text="FG%", fg="green")
    fgp_label.grid(row=4, column=1)

    fgp3_label = Label(comparison_frame, text="3FG%", fg="green")
    fgp3_label.grid(row=5, column=1)

    ftp_label = Label(comparison_frame, text="FT%", fg="green")
    ftp_label.grid(row=6, column=1)

    #PLAYER 1 STAT LABELS
    player_1_gp = Label(comparison_frame, text=str(filtered_frame_player1.iloc[0, 2]))
    player_1_gp.grid(row=0, column=0)

    player_1_points = Label(comparison_frame, text=str(filtered_frame_player1.iloc[0, 8]))
    player_1_points.grid(row=1, column=0)

    player_1_rebounds = Label(comparison_frame, text=str(filtered_frame_player1.iloc[0,6]))
    player_1_rebounds.grid(row=2, column=0)

    player_1_assists = Label(comparison_frame, text=str(filtered_frame_player1.iloc[0, 7]))
    player_1_assists.grid(row=3, column=0)

    player_1_fgp = Label(comparison_frame, text=str(round(filtered_frame_player1.iloc[0, 3] * 100, 2)))
    player_1_fgp.grid(row=4, column=0)

    player_1_fgp3 = Label(comparison_frame, text=str(round(filtered_frame_player1.iloc[0, 4] * 100, 4)))
    player_1_fgp3.grid(row=5, column=0)

    player_1_ftp = Label(comparison_frame, text=str(round(filtered_frame_player1.iloc[0, 5] * 100, 2)))
    player_1_ftp.grid(row=6, column=0)


    #PLAYER 2 STAT LABELS
    player_2_gp = Label(comparison_frame, text=str(filtered_frame_player2.iloc[0, 2]))
    player_2_gp.grid(row=0, column=2)

    player_2_points = Label(comparison_frame, text=str(filtered_frame_player2.iloc[0, 8]))
    player_2_points.grid(row=1, column=2)

    player_2_rebounds = Label(comparison_frame, text=str(filtered_frame_player2.iloc[0, 6]))
    player_2_rebounds.grid(row=2, column=2)

    player_2_assists = Label(comparison_frame, text=str(filtered_frame_player2.iloc[0, 7]))
    player_2_assists.grid(row=3, column=2)

    player_2_fgp = Label(comparison_frame, text=str(round(filtered_frame_player2.iloc[0, 3] * 100, 2)))
    player_2_fgp.grid(row=4, column=2)

    player_2_fgp3 = Label(comparison_frame, text=str(round(filtered_frame_player2.iloc[0,4] * 100, 2)))
    player_2_fgp3.grid(row=5, column=2)

    player_2_ftp = Label(comparison_frame, text=str(round(filtered_frame_player2.iloc[0, 5] * 100, 2)))
    player_2_ftp.grid(row=6, column=2)




# start of tkinter GUI
#creates Tk and basic composition
root = Tk()
root.title("NBA Players Comparison")
frame = ttk.Frame(root, padding=10)
frame.grid()
root.geometry("350x325")


#creates and places user input fields for players 1 and 2
player1_entry = ttk.Entry(root, width=20)
player1_entry.grid(row=1, column=0)

player2_entry = ttk.Entry(root, width=20)
player2_entry.grid(row=1, column=3)


# compare players button
select_years_button = ttk.Button(root, text="Select Years", command=lambda: main(str(player1_entry.get()), str(player2_entry.get())))
select_years_button.grid(row=3, column=2)

#mainloop that keeps the GUI running
root.mainloop()
