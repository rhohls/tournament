from subprocess import Popen

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
