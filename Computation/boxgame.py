import sys
import random
import box as box

if len(sys.argv)!= 2:
    name = input("Please enter your name")
else:
    name = sys.argv[1]

score = 0
numbers = list(range(1,11))
gameover = 0

while (gameover == 0):
    if sum(numbers) < 7:
        roll = random.randint(1,6)
    else:
        roll = random.randint(1,6) + random.randint(1,6)
    if box.isvalid(roll,numbers):
        print("Numbers left: " + str(numbers))
        print("Roll: " + str(roll))
        elim = input("Numbers to eliminate")
        while box.parse_input(elim,numbers) == []:
            print("Invalid Input")
            elim = input("Numbers to eliminate")
        while sum(box.parse_input(elim,numbers))!=roll:
            print("Invalid Input")
            elim = input("Numbers to eliminate")    
        remove = box.parse_input(elim, numbers)
        numbers = [x for x in numbers if x not in remove]
    else:
        gameover = 1
        print("Game Over!")

score = sum(numbers)
print("Score for Player " +str(name)+ ": " +str(score)+ " points" )
if score == 0:
    print("Congratulations you shut the box!")
