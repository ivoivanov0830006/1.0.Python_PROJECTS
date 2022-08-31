import random

user_wins = 0
computer_wins = 0

options = ["rock", "paper", "scissors"]

game_over = False

while True:
    if user_wins == 3 or computer_wins == 3:
        game_over = True
        break
    user_pick = input("Type Rock/Paper/Scissors or Q to Quit. ").lower()
    if user_pick == "q":
        quit("Thank you for playing")

    if user_pick not in options:
        print("Choose rock, paper or scissors!")
        continue

    random_number = random.randint(0, 2)
    computer_pick = options[random_number]
    print("You picked", user_pick.upper(), "and computer picked", computer_pick.upper() + ".")

    if user_pick == "rock" and computer_pick == "scissors":
        print("You won!")
        user_wins += 1

    elif user_pick == "paper" and computer_pick == "rock":
        print("You won!")
        user_wins += 1

    elif user_pick == "scissors" and computer_pick == "paper":
        print("You won!")
        user_wins += 1

    else:
        print("You lost!")
        computer_wins += 1
if game_over:
    if computer_wins == 3:
        print(computer_wins, ":", user_wins, " for the computer!")
    else:
        print(user_wins, ":", computer_wins, " for you!")
#print("You won", user_wins, "times.")
#print("Computer won", computer_wins, "times.")
