from subprocess import Popen

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

def shell_exe(player1, player2, map="map01"):
    print("Playing", player1, "vs", player2)
    script = "sh filler_py_script.sh"

    args = script + " " + player1 + " " + player2 + " " + map
    args = args.split()

    popen = Popen(args)
    popen.wait()

    result = open("filler.trace", "r")
    lines = result.readlines()
    scoreline = lines[-1]
    scoreline = scoreline.rstrip()
    nums = [int(number) for number in scoreline.split("AGAINST") if number.isdigit()]
    return nums
