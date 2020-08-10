"""Main Logic to drive the Game-Play

Classic Housie Board game

Also known as Bingo
https://en.wikipedia.org/wiki/Bingo_(British_version)
"""
from typing import Dict, List

from utils import load_json, save_json, clear_screen
from constants import INSTRUCTIONS, Number, FOLLOW_GAME_TICKETS_NOT_FOUND_MSG
from models import Housie, Ticket, load_tickets
from display_util import display_followed_game
from generate_ticket import generate_ticket


def print_options() -> str:
	"""Prints the options to allow the user to drive the program flow"""
	option = 'default'
	while option not in ['N', 'T', 'F', 'Q']:
		clear_screen()
		print(INSTRUCTIONS)
		if option != 'default':
			print("Sorry that is not a valid input. Please try again")
		option = input("\nSelect an option to get started: ").upper()
	return option


def host_new_game():
	"""Host a Housie Game.
	Starts with a blank board. Randomly picks numbers and updates the board when you ask it to
	"""
	options = "Press 'Enter' to pick the next number\nPress 'Q' followed by 'Enter' to quit\n"
	housie = Housie()
	clear_screen()
	print(housie.display_board())
	user_choice = ''
	while user_choice not in ['Q', 'q']:
		user_choice = input(options)
		housie.pick_next()
		clear_screen()
		print(housie.display_board())


def follow_game():
	"""Allows you to play along/follow a game being hosted by someone else.

	Reads your tickets from 'data/followed_tickets.json' and displays them.
	Refer to the 'data/generated_tickets.json' file to understand the format of the file.

	Reads the board from housie.json on startup. Displays the board.
	Allows you to enter the numbers being called out by the host, and updates your tickets and the board.
	The state of the board is persisted even if you exit the program.
	To start a new game, update the followed_housie.json file with the content []

	NOTE: This mode doesn't let you generate numbers randomly on the board. This is because the whole purpose of this
	mode is to allow to follow a game being hosted by someone else.

	If you want to host a game and play with friends, use the generate tickets mode to distribute tickets to your
	friends, and then use the host a game mode to play.
	"""
	already_selected_numbers = load_json('data/followed_housie.json')
	housie = Housie(already_selected_numbers)
	ticket_data: Dict[str, List[Ticket]] = load_tickets('data/followed_tickets.json')
	if not ticket_data:
		print(FOLLOW_GAME_TICKETS_NOT_FOUND_MSG)
		return None
	mark_tickets_full_board(housie, ticket_data)
	while True:
		clear_screen()
		display_followed_game(housie, ticket_data)
		user_choice = input("Press 'Q' to quit. Enter next number: ")
		if user_choice == 'Q' or user_choice == 'q':
			break
		elif user_choice.isnumeric():
			number = int(user_choice)
			housie.pick_manual(number)
			save_json(housie.selected, 'data/followed_housie.json')
			mark_tickets(number, ticket_data)


def mark_tickets_full_board(housie: Housie, ticket_data: Dict[str, List[Ticket]]):
	"""Updates the tickets with all numbers from the housie board"""
	for name, tickets in ticket_data.items():
		for ticket in tickets:
			ticket.mark_numbers(housie.selected)


def mark_tickets(number: Number, ticket_data: Dict[str, List[Ticket]]):
	"""Updates the tickets with all numbers from the housie board"""
	for name, tickets in ticket_data.items():
		for ticket in tickets:
			ticket.mark_number(number)


def generate_tickets():
	"""Allows you to generate housie tickets for use in a game. Enter the names of the players and numbers of tickets
	per player

	Saves the generated tickets to a file 'generated_tickets.json'
	"""
	clear_screen()
	names = input("Enter the names of users playing the game. Separate each name with a space: ")
	number = input("Enter the number of tickets to be generated per user: ")
	ticket_data: Dict[str, List[Ticket]] = {}
	names = map(str.strip, names.split())
	for name in names:
		tickets = [generate_ticket() for i in range(int(number))]
		print(name)
		for ticket in tickets:
			print(ticket.display_ticket())
		ticket_data[name] = [ticket.rows for ticket in tickets]
	save_json(ticket_data, 'data/generated_tickets.json')
	print("The generated tickets can also be found in the 'data/generated_tickets.json' file")


def main_menu():
	"""The starting menu presented to the user

	Supported Options are as follows :

	'N' - Host a New Game
		Displays the board, randomly picks numbers

	'T' - Generate Tickets
		Generate tickets for Players to use to play the game. Also stores the tickets to 'data/generated_tickets.json'

	'F' - Follow a Game
		This mode allows you to follow a game being hosted by someone else, i.e. someone else is calling out the
		numbers as you sit and mark your tickets. This mode automates the marking of your tickets and shows a nice
		visual display of the board and your tickets.

		Before using this mode, enter your ticket(s) into the 'data/followed_tickets.json' file. Then start this mode
		and keep entering the numbers being called out. The status of your ticket(s) are automatically updated on
		screen.

	'Q' - Quit

	"""
	option = print_options()
	if option == 'N':
		host_new_game()
	elif option == 'F':
		follow_game()
	elif option == 'Q':
		print("Thank you for playing! Bye")
	elif option == 'T':
		generate_tickets()
	else:
		print("Sorry this feature is not available yet!")


if __name__ == '__main__':
	main_menu()
	# demo_board()
