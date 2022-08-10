import random

top_of_range = input("Let's guess number between 1 and: ")

if top_of_range.isdigit():
    top_of_range = int(top_of_range)

    if top_of_range <= 0:
        print("Please type a larger number than 0.")
        quit()

else:
    print("Please type a number next time.")
    quit()

random_number = random.randint(0, top_of_range + 1)
guess_count = 0

while True:
    guess_count += 1
    user_guess = input("Make a guess: ")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("Please type a number next time.")
        continue

    if user_guess == random_number:
        print("Congratulations!")
        break
    else:
        if user_guess > random_number:
            print("You were ABOVE the number. Try again!")
        else:
            print("You were BELOW the number. Try again!")

print("You got it in", guess_count, "tries.")
