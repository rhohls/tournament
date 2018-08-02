
from __future__ import print_function
import subprocess
class color:
    end = "\033[0m"
    black = "\033[0;30m"
    blackb = "\033[1;30m"
    white = "\033[0;37m"
    whiteb = "\033[1;37m"
    red = "\033[0;31m"
    redb = "\033[1;31m"
    green = "\033[0;32m"
    greenb = "\033[1;32m"
    yellow = "\033[0;33m"
    yellowb = "\033[1;33m"
    blue = "\033[0;34m"
    blueb = "\033[1;34m"
    purple = "\033[0;35m"
    purpleb = "\033[1;35m"
    lightblue = "\033[0;36m"
    lightblueb = "\033[1;36m"

def shell_exe(player1, player2, map):
    print("Playing", player1, "vs", player2)#, "on", map, "...")
    script = "sh filler_py.sh"

    args = script + " " + player1 + " " + player2 + " " + map
    args = args.split()

    popen = subprocess.Popen(args)
    popen.wait()

    result = open("filler.trace", "r")
    lines = result.readlines()

    if len(lines) > 4:
        print("~~~~")
        print ("!!! There was an error with", player1, "playing", player2, "!!!")
        print(lines[2], end='')
        print("~~~~")
     #   A = input("WE HAVE AN ERROR HERE")
     #   print(A)

    scoreline = lines[-1]
    scoreline = scoreline.rstrip()

   # print(scoreline)
    nums = [int(number) for number in scoreline.split("AGAINST") if number.isdigit()]

    return nums

players = ["abanlin", "carli" , "champely", "grati", "hcao", "superjeannot", ]
#players = ["carli"]
player2 = "rhohls"
maps = ["map00", "map01", "map02"]
#maps = ["map02"]
#maps = ["map00"]
replay = 5

def print_result(player1, player2, result):
    if player2 == "rhohls":
        if nums[0] > nums[1]:
            print(color.red + player1, "got: ", result[0], color.end)
            print(player2, "got: ", result[1])
        else:
            print(player1, "got: ", result[0])
            print(color.green + player2, "got: ", result[1], color.end)
    else:
        if nums[0] > nums[1]:
            print(color.green + player1, "got: ", result[0], color.end)
            print(player2, "got: ", result[1])
        else:
            print(player1, "got: ", result[0])
            print(color.red + player2, "got: ", result[1], color.end)
    print("")

"""playing the game:"""
for map in maps:
    for i in range(replay):
        print("~~~ Now playing on:", map, "~~~")
        for player1 in players:
            if i % 2 == 0:
                player2 = player1
                player1 = "rhohls"
            else:
                player2 = "rhohls"
            nums = shell_exe(player1, player2, map)
            print_result(player1, player2, nums)


#print(type(nums[0]))

