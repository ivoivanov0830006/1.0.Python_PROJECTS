print("Welcome to this QUIZ game!")

playing = input("Do you want to play? ")

if playing.lower() != "yes":
    quit("Ok, may be next time! ")

print("LET'S PLAY :)")
score = 0
questions = 0

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    questions += 1
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    questions += 1
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

answer = input("What does RAM stand for? ")
if answer == "random access memory":
    questions += 1
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

answer = input("What does PSU stand for? ")
if answer == "power supply unit":
    questions += 1
    print("Correct!")
    score += 1
else:
    print("Incorrect!")

print("You got " + str(score) + " question correct!")
print("Your answers are " + str((score / questions) * 100) + "% correct!")
