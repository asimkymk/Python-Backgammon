#!/usr/bin/env python3
# ASIM KAYMAK
# 1306180004
# Python v3.8
from texttable import Texttable
import codecs
import os
import random
import time
import sys
import io

#creating class for each player controls
class Side:
    def __init__(self, rotate_direction,name):
        self.broken_count = 0
        self.completed_flake_count = 0
        self.rotate_direction = rotate_direction
        self.name = name

# setting up players, dice and empty board
player_x = Side(rotate_direction=1,name= "X")
player_y = Side(rotate_direction=-1,name="Y")
dice_1 = 0
dice_2 = 0
board = {
    "A1": "  ",
    "B1": "  ",
    "C1": "  ",
    "D1": "  ",
    "E1": "  ",
    "F1": "  ",
    "G1": "  ",
    "H1": "  ",
    "I1": "  ",
    "J1": "  ",
    "K1": "  ",
    "L1": "  ",
    "A5": "  ",
    "B5": "  ",
    "C5": "  ",
    "D5": "  ",
    "E5": "  ",
    "F5": "  ",
    "G5": "  ",
    "H5": "  ",
    "I5": "  ",
    "J5": "  ",
    "K5": "  ",
    "L5": "  ",
}
queue = ""
dice_list =list()


# setting up for ui table
table = Texttable()
table.set_cols_align(["c", "c", "c","c", "c", "c","c","c", "c", "c","c", "c", "c","c"])
table.set_cols_valign(["c", "c", "c","c", "c", "c","c","c", "c", "c","c", "c", "c","c"])
col_len = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
table.set_cols_width(col_len)
table_list = [["n", "A", "B", "C", "D", "E", "F", "■■■■■■■■", "G", "H", "I", "J", "K", "L"],
              ["1", board["A1"], board["B1"], board["C1"], board["D1"], board["E1"], board["F1"], "■■■■■■■■",
               board["G1"], board["H1"], board["I1"], board["J1"], board["K1"], board["L1"]],
              ["2", "", "", "", "", "", "", "■■■■■■■■", "", "", "", "", "", ""],
              ["3", "", "", "", "", "Broken Flake of 0x", "Dice No1", "■■■■■■■■■■■■■■■■■■■■■■■■", "Dice No2",
               "Broken Flake of 0y",
               "", "", "", ""],
              ["4", "", "", "", "", "", "", "■■■■■■■■", "", "", "", "", "", ""],
              ["5", board["A5"], board["B5"], board["C5"], board["D5"], board["E5"], board["F5"], "■■■■■■■■",
               board["G5"], board["H5"], board["I5"], board["J5"], board["K5"], board["L5"]]
              ]
table.add_rows(table_list)


#random 2 number creator between 1-6
def rollDie():
    return random.randint(1, 6),random.randint(1, 6)


#main menu starting point
def mainMenu():
    print("MAIN MENU\n"
          "1 - New Game\n"
          "2 - Continue Game\n"
          "3 - Exit (or q)\n"
          "Your Selection : ")
    selection = input()
    if selection == "1":
        newGame()
    elif selection == "2":
        continueGame()
    elif selection == "3" or selection == "q":
        exit()
    else:
        mainMenu()


def newGame():
    # clear board and settings up for starting
    global board
    global dice_1
    global dice_2
    global dice_list
    board["A1"] = "5Y"
    board["E1"] = "3X"
    board["G1"] = "5X"
    board["L1"] = "2Y"
    board["A5"] = "5X"
    board["E5"] = "3Y"
    board["G5"] = "5Y"
    board["L5"] = "2X"
    #delete old log and table file if they were created before
    try:
        open('log.dat', 'w').close()
        open('table.dat', 'w').close()
    except:
        print("Error occured!")


    table_update(dice_1,dice_2,"")
    print(table.draw())


    print("Dice are rolling for starting. Dice No1 = X, Dice No2 = Y for starting point.")
    time.sleep(5)
    # dices rolling until they came with different number
    while dice_1 == dice_2:
        dice_1, dice_2 = rollDie()
    dice_list = ["1", "2"]
    global queue
    file_logger_start(dice_1, dice_2)

    if dice_1<dice_2:
        queue = "Y"
        os.system("cls")
        table_update(dice_1, dice_2, queue)
        print(table.draw())
        print("\nY will start the game")



        time.sleep(3)

        init(queue,2)
    else:
        queue = "X"
        os.system("cls")
        table_update(dice_1, dice_2, queue)
        print(table.draw())
        print("\nX will start the game")


        time.sleep(3)
        init(queue,2)

    time.sleep(2)


def init(queue,due):

    global dice_1
    global dice_2
    global board
    global player_x
    global player_y
    global dice_list

    selection = "0"


    table_update(dice_1,dice_2,queue)
    os.system("cls")
    print(table.draw())
    while due>0:

        print(
            "\nPlease enter the location of the flake that you want to play example 'A1'.\nFor broken flakes please enter dice number for example '1' or '2'\nPlease enter 'PASS' to give up your right.\nPlease enter 'q' to quit game.\n")

        selection = input("Player {} please enter your selection with respect to instructions. (Remaining rights: {}) : ".format(queue, due))

        if selection.upper() == "Q":
            f = io.open("table.dat", mode="a", encoding="utf-8")

            test = "\n"
            f.writelines(test + ",".join(dice_list))
            f.close()
            sys.exit("Your game saved. See you later!")
            #çıkış algoritması yazılacak
        elif selection.upper()  == "PASS":
            due -= 1
        elif queue == "Y" and player_y.broken_count >0:
            if selection in dice_list:
                if selection == "1":
                    if controller(player_y, 'Z', dice_1, player_x):
                        table_update(dice_1, dice_2,queue)
                        dice_list.remove("1")
                        due -= 1
                        os.system("cls")
                        table_update(dice_1, dice_2, queue)
                        print(table.draw())
                    else: print("Seems like you can't move your flake into target location with respect to dice number.")
                elif selection == "2":
                    if controller(player_y, 'Z', dice_2, player_x):
                        table_update(dice_1, dice_2,queue)
                        dice_list.remove("2")
                        due -= 1
                        os.system("cls")
                        table_update(dice_1, dice_2,queue)
                        print(table.draw())
                    else:
                        print("Seems like you can't move your flake into target location with respect to dice number.")
                else:
                    print("You should just pick dice number while you have a broken flake. If there is no optional location you can pass your currently right by input 'pass'")
            else:
                print("You should just pick dice number while you have a broken flake. If there is no optional location you can pass your currently right by input 'pass'")
        elif queue == "X" and player_x.broken_count > 0:
            if selection in dice_list:
                if selection == "1":
                    if controller(player_x, 'Z', dice_1, player_y):
                        table_update(dice_1, dice_2,queue)
                        dice_list.remove("1")
                        due -= 1
                        os.system("cls")
                        table_update(dice_1, dice_2,queue)
                        print(table.draw())
                    else:
                        print("Seems like you can't move your flake into target location with respect to dice number.")
                elif selection == "2":
                    if controller(player_x, 'Z', dice_2, player_y):
                        table_update(dice_1, dice_2,queue)
                        dice_list.remove("2")
                        due -= 1
                        os.system("cls")
                        table_update(dice_1, dice_2,queue)
                        print(table.draw())
                    else:
                        print("Seems like you can't move your flake into target location with respect to dice number.")
                else:
                    print("You should just pick dice number while you have a broken flake. If there is no optional location you can pass your currently right by input 'pass'")
            else:
                print("You should just pick dice number while you have a broken flake. If there is no optional location you can pass your currently right by input 'pass'")
        else:

            if len(selection) !=2:
                print("Please input the flake location correctly")
            elif selection[-1] not in ["1","5"]:
                print("Please input the flake location correctly")
            elif selection[0].upper() not in ["A","B","C","D","E","F","G","H","I","J","K","L"]:
                print("Wrong input recognizitiation!")
            else:
                if queue == "Y":
                    if "1" in dice_list[0]:

                        if controller(player_y,selection.upper(),dice_1,player_x):
                            table_update(dice_1, dice_2,queue)
                            dice_list.remove(dice_list[0])
                            due-=1
                            if game_finished(player_y):
                                os.system("cls")
                                table_update(dice_1, dice_2,queue)
                                print(table.draw())
                                file_object = open('table.dat', 'a')
                                file_object.write("\nGame has already finished.")
                                file_object.close()
                                file_logger(player_y, dice_1, dice_2)
                                sys.exit("Congratulations Player Y won the came!")
                            else:
                                os.system("cls")
                                table_update(dice_1, dice_2,queue)
                                print(table.draw())
                        else:
                            print("Seems like you can't move that location that input. If there is no optional location you can pass your currently right by input 'pass'")
                    else:
                        if controller(player_y, selection.upper(), dice_2, player_x):
                            table_update(dice_1, dice_2,queue)
                            dice_list.remove(dice_list[0])
                            due -= 1
                            if game_finished(player_x):
                                os.system("cls")
                                table_update(dice_1, dice_2,queue)
                                print(table.draw())
                                file_object = open('table.dat', 'a')
                                file_object.write("\nGame has already finished.")
                                file_object.close()
                                file_logger(player_x, dice_1, dice_2)
                                sys.exit("Congratulations Player X won the came!")
                            else:

                                os.system("cls")
                                table_update(dice_1, dice_2,queue)
                                print(table.draw())
                        else:
                            print(
                                "Seems like you can't move that location that input. If there is no optional location you can pass your currently right by input 'pass'")


                else:
                    if "1" in dice_list[0]:

                        if controller(player_x, selection.upper(), dice_1, player_y):
                            table_update(dice_1, dice_2,queue)
                            dice_list.remove(dice_list[0])
                            due -= 1
                            os.system("cls")
                            table_update(dice_1, dice_2,queue)
                            print(table.draw())
                        else:
                            print(
                                "Seems like you can't move that location that input. If there is no optional location you can pass your currently right by input 'pass'")
                    else:
                        if controller(player_x, selection.upper(), dice_2, player_y):
                            table_update(dice_1, dice_2,queue)
                            dice_list.remove(dice_list[0])
                            due -= 1
                            os.system("cls")
                            table_update(dice_1, dice_2,queue)
                            print(table.draw())
                        else:
                            print(
                                "Seems like you can't move that location that input. If there is no optional location you can pass your currently right by input 'pass'")

        if game_finished(player_y):
            os.system("cls")
            table_update(dice_1, dice_2,queue)
            print(table.draw())
            file_object = open('table.dat', 'a')
            file_object.write("\nGame has already finished.")
            file_object.close()
            file_logger(player_y, dice_1, dice_2)
            sys.exit("Congratulations Player Y won the came!")

        if game_finished(player_x):
            os.system("cls")
            table_update(dice_1, dice_2,queue)
            print(table.draw())
            file_object = open('table.dat', 'a')
            file_object.write("\nGame has already finished.")
            file_object.close()

            file_logger(player_x, dice_1, dice_2)
            sys.exit("Congratulations Player X won the came!")






    print("")
    if game_finished(player_y):
        os.system("cls")
        table_update(dice_1, dice_2,queue)
        print(table.draw())
        file_object = open('table.dat', 'a')
        file_object.write("\nGame has already finished.")
        file_object.close()
        file_logger(player_y, dice_1, dice_2)
        sys.exit("Congratulations Player Y won the came!")

    if game_finished(player_x):
        os.system("cls")
        table_update(dice_1, dice_2,queue)
        print(table.draw())
        file_object = open('table.dat', 'a')
        file_object.write("\nGame has already finished.")
        file_object.close()

        file_logger(player_x, dice_1, dice_2)
        sys.exit("Congratulations Player X won the came!")

    if queue == "Y":
        file_logger(player_y,dice_1,dice_2)
    else:
        file_logger(player_x, dice_1, dice_2)
    dice_list = ["1", "2"]
    due = 2
    if queue == "Y":
        print("Dice are rolling for player X")
        time.sleep(3)

        dice_1, dice_2 = rollDie()
        if dice_1 == dice_2:
            due *= 2
            dice_list = ["1","1","2","2"]
        table_update(dice_1, dice_2,"X")
        init("X",due)
    else:
        print("Dice are rolling for player Y")
        time.sleep(3)
        dice_1, dice_2 = rollDie()
        if dice_1 == dice_2:
            due *= 2
            dice_list = ["1","1","2","2"]
        table_update(dice_1, dice_2,"Y")
        init("Y",due)


#all controller
def controller(player,location,move,againstPlayer):

    targetLocation = ""

    if player.broken_count > 0 and location != "Z":      #firstly checking player's  broken flake number and player want to move other flakes except broken flakes
        print("You have broken flake. Firstly, you have to put your flake in game again.")
        return False

    elif player.broken_count > 0 and location == "Z":   #secondly checking player's broken flake and correct selection
        if player.rotate_direction == -1:
            targetLocation = chr(ord("M")-move) + "1"
        if player.rotate_direction == 1:
            targetLocation = chr(ord("M")-move) + "5"

        if board[targetLocation] == "  ":
            board[targetLocation] = "1" + player.name
            player.broken_count -= 1
        elif board[targetLocation][-1] == player.name:
            board[targetLocation] = str(int(board[targetLocation][:-1]) + 1) + player.name
            player.broken_count -= 1
        elif int(board[targetLocation][:-1])>1 and board[targetLocation][-1] == againstPlayer.name:
            print("You can't play at {}. There is {} flakes from opponent player.".format(targetLocation,board[targetLocation]))
            return False

        elif int(board[targetLocation][:-1]) == 1 and board[targetLocation][-1] == againstPlayer.name:
            board[targetLocation] = "1"+ player.name
            player.broken_count -= 1
            againstPlayer.broken_count += 1
        return True

    if player.broken_count == 0 and location == "Z":
        print("You don't have any broken flakes so you shouldn't use Z location.")
        return False
    if board[location][-1] != player.name:
        print("You don't have any flakes that you wrote. Please make sure you input location that you have at least one flake.")
        return False

    #if there is no any broken flakes for player then firstly finding correct targetlocation  to play flake
    if player.rotate_direction == -1:
       if location[-1] == "5":
           targetLocation = chr(ord(location[0]) + move) + "5"
       elif location[-1] == "1":
           if (ord(location[0]) - move)-65< 0:
               targetLocation = chr(ord('@') + abs((ord(location[0]) - move)-65)) + "5"
           else:
               targetLocation = chr(ord(location[0]) - move) + "1"
    if player.rotate_direction == 1:
       if location[-1] == "1":
           targetLocation = chr(ord(location[0]) + move) + "1"
       elif location[-1] == "5":
           if (ord(location[0]) - move)-65 < 0:
               targetLocation = chr(ord('@') + abs((ord(location[0]) - move)-65)) + "1"
           else:
               targetLocation = chr(ord(location[0]) - move) + "5"
    #target location alındı
    #target locationun tablodan boyu uzunsa toplansın mı toplanmasını ı toplanmaya uyguh değilse hata döndür toplanabiliyorsa toplat
    #toparlekn completed flake count u 1 artır aktif location dan 1 düşür
    #eğer tablodan büyük değilse oynanması gerekn yere oynamadan önce orada karşı takımdan taş var mı diye bak
    # 1 tane varsa taşı kır ve oyna location 1 düşür
    # 1 taneden fazlaysa oynayama hata döndür
    if targetLocation[0] > "L" and collected_all_flakes_checker(player):
        if board[location][-1] == player.name and chr(ord(location[0]) + move) == 'M':
            player.completed_flake_count += 1

            if board[location][0] == "1":
                board[location] = "  "
            elif int(board[location][0]) > 1:
                board[location] = str(int(board[location][0]) - 1) + player.name

            return True
        else:

            if(player.name=="X"):


                if (board[chr(ord(location[:-1]) - 1) + "1"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 2) + "1"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 3) + "1"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 4) + "1"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 5) + "1"][-1:] != player.name):


                    player.completed_flake_count += 1

                    if board[location][0] == "1":
                        board[location] = "  "
                    elif int(board[location][0]) > 1:
                        board[location] = str(int(board[location][0]) - 1) + player.name


                    return True
                else:
                    print("There are flakes you need to collect before here.")
                    return False
            if (player.name == "Y"):

                if (board[chr(ord(location[:-1]) - 1) + "5"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 2) + "5"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 3) + "5"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 4) + "5"][-1:] != player.name and
                        board[chr(ord(location[:-1]) - 5) + "5"][-1:] != player.name):

                    player.completed_flake_count += 1

                    if board[location][0] == "1":
                        board[location] = "  "
                    elif int(board[location][0]) > 1:
                        board[location] = str(int(board[location][0]) - 1) + player.name

                    return True
                else:
                    print("There are flakes you need to collect before here.")
                    return False


    if targetLocation[0] > "L" and not collected_all_flakes_checker(player):
        print("Firstly you have to collect all flakes to your side.")
        return False



    if board[targetLocation] == "  ":
        board[targetLocation] = "1" + player.name
        if board[location][:-1] == "1":
            board[location] = "  "
        else:
            board[location] = str(int(board[location][:-1]) - 1) + player.name
        return True
    else:
        if board[targetLocation][-1] == player.name:
            board[targetLocation] = str(int(board[targetLocation][:-1]) +1) + player.name
            if board[location][:-1] == "1":
                board[location] = "  "
            else:
                board[location] = str(int(board[location][:-1]) - 1) + player.name
            return True
        else:
            if int(board[targetLocation][:-1]) > 1:
                print("There is {} flakes from player {} so you can't play at this location.".format(board[targetLocation][:-1],againstPlayer.name))
                return False
            else:
                board[targetLocation] = board[targetLocation][:-1] + player.name
                againstPlayer.broken_count += 1
                if board[location][:-1] == "1":
                    board[location] = "  "
                else:
                    board[location] = str(int(board[location][:-1]) - 1) + player.name
                return True

#controller about if player finished game or not
def game_finished(player):
    return player.completed_flake_count == 15

#controller about if player can take his/her flakes or not
def collected_all_flakes_checker(player):
    sum_collected_flakes = player.completed_flake_count
    if player.name == "X":
        for i in range(6):
            if board[chr(ord("G")+i)+"1"][-1] == "X":
                sum_collected_flakes += int(board[chr(ord("G")+i)+"1"][:-1])
    if player.name == "Y":
        for i in range(6):
            if board[chr(ord("G") + i)+"5"][-1] == "Y":
                sum_collected_flakes += int(board[chr(ord("G") + i)+"5"][:-1])
    return sum_collected_flakes == 15

#continue game function.
#reading table.dat part of part
def continueGame():
    f = io.open("table.dat", mode="r", encoding="utf-8")
    global dice_1
    global dice_2
    global board
    global player_x
    global player_y
    global dice_list
    Lines = f.readlines()

    count = 0
    veriler = list()
    dice_1 = int(Lines[8].split("|")[7].strip())
    dice_2 = int(Lines[8].split("|")[9].strip())
    for i in range(len(Lines[3].split("|"))):
        if i not in [0, 1, 8, 15]:
            veriler.append(Lines[3].split("|")[i].strip())
    for i in range(len(Lines[13].split("|"))):
        if i not in [0, 1, 8, 15]:
            veriler.append(Lines[13].split("|")[i].strip())
    if veriler[0] == "": board["A1"] = "  "
    else: board["A1"] = veriler[0]
    if veriler[1] == "": board["B1"] = "  "
    else: board["B1"] =  veriler[1]
    if veriler[2] == "": board["C1"] = "  "
    else: board["C1"] =  veriler[2]
    if veriler[3] == "": board["D1"] = "  "
    else: board["D1"] =  veriler[3]
    if veriler[4] == "": board["E1"] = "  "
    else: board["E1"] =  veriler[4]
    if veriler[5] == "": board["F1"] = "  "
    else: board["F1"] =  veriler[5]
    if veriler[6] == "": board["G1"] = "  "
    else: board["G1"] =  veriler[6]
    if veriler[7] == "": board["H1"] = "  "
    else: board["H1"] =  veriler[7]
    if veriler[8] == "": board["I1"] = "  "
    else: board["I1"] =  veriler[8]
    if veriler[9] == "": board["J1"] = "  "
    else: board["J1"] =  veriler[9]
    if veriler[10] == "": board["K1"] = "  "
    else: board["K1"] =  veriler[10]
    if veriler[11] == "": board["L1"] = "  "
    else: board["L1"] =  veriler[11]
    if veriler[12] == "": board["A5"] = "  "
    else: board["A5"] =  veriler[12]
    if veriler[13] == "": board["B5"] = "  "
    else: board["B5"] =  veriler[13]
    if veriler[14] == "": board["C5"] = "  "
    else: board["C5"] =  veriler[14]
    if veriler[15] == "": board["D5"] = "  "
    else: board["D5"] =  veriler[15]
    if veriler[16] == "": board["E5"] = "  "
    else: board["E5"] =  veriler[16]
    if veriler[17] == "": board["F5"] = "  "
    else: board["F5"] =  veriler[17]
    if veriler[18] == "": board["G5"] = "  "
    else: board["G5"] =  veriler[18]
    if veriler[19] == "": board["H5"] = "  "
    else: board["H5"] =  veriler[19]
    if veriler[20] == "": board["I5"] = "  "
    else: board["I5"] =  veriler[20]
    if veriler[21] == "": board["J5"] = "  "
    else: board["J5"] =  veriler[21]
    if veriler[22] == "": board["K5"] = "  "
    else: board["K5"] =  veriler[22]
    if veriler[23] == "": board["L5"] = "  "
    else: board["L5"] =  veriler[23]

    player_x.broken_count = int(Lines[9].split("|")[6].strip()[:-1])
    player_y.broken_count = int(Lines[9].split("|")[10].strip()[:-1])
    ycount = player_y.broken_count
    xcount = player_x.broken_count
    for x, y in board.items():
        if y == "  ":
            continue
        else:
            if y[-1] == "Y":
                ycount += int(y[:-1])
            else:
                xcount += int(y[:-1])

    player_y.completed_flake_count = 15 - ycount - player_y.broken_count
    player_x.completed_flake_count = 15 - xcount - player_x.broken_count
    if Lines[-1] == "Game has already finished.":
        os.system("cls")
        print("Saved game had already finished. Please start a new game!")
        mainMenu()
    else:
        dice_list = Lines[-1].split(",")
        queue = Lines[-8].split("|")[11].strip()
        os.system("cls")
        table_update(dice_1, dice_2,queue)
        init(queue,len(dice_list))

#table update function after input selection immediately
def table_update(dice_1,dice_2,sira):
    global table_list
    global table
    global dice_list

    table_list[1][1] = board["A1"]
    table_list[1][2] = board["B1"]
    table_list[1][3] = board["C1"]
    table_list[1][4] = board["D1"]
    table_list[1][5] = board["E1"]
    table_list[1][6] = board["F1"]
    table_list[1][8] = board["G1"]
    table_list[1][9] = board["H1"]
    table_list[1][10] = board["I1"]
    table_list[1][11] = board["J1"]
    table_list[1][12] = board["K1"]
    table_list[1][13] = board["L1"]
    table_list[5][1] = board["A5"]
    table_list[5][2] = board["B5"]
    table_list[5][3] = board["C5"]
    table_list[5][4] = board["D5"]
    table_list[5][5] = board["E5"]
    table_list[5][6] = board["F5"]
    table_list[5][8] = board["G5"]
    table_list[5][9] = board["H5"]
    table_list[5][10] = board["I5"]
    table_list[5][11] = board["J5"]
    table_list[5][12] = board["K5"]
    table_list[5][13] = board["L5"]
    if dice_1 != 0 and dice_2 != 0:
        if "1" not in dice_list:

            table_list[3][6] = "Dice No1 " + str(dice_1) + "  played"
        else:
            table_list[3][6] = "Dice No1 " + str(dice_1)
        if "2" not in dice_list:

            table_list[3][8] = "Dice No2 " + str(dice_2) + "  played"
        else:
            table_list[3][8] = "Dice No2 " + str(dice_2)

    table_list[3][5] = "Broken Flake of " + str(player_x.broken_count) + "X"
    table_list[3][9] = "Broken Flake of " + str(player_y.broken_count) + "Y"
    table_list[3][10] = "Turn for       " + sira

    table.reset()
    table.add_rows(table_list)
    file = codecs.open("table.dat", "w", "utf-8")
    file.write(table.draw())
    file.close()

# log.dat append functions
def file_logger(player,dice_1,dice_2):
    file_object = open('log.dat', 'a')
    file_object.write(player.name + " " + str(dice_1) + " " + str(dice_2) + "\n")
    file_object.close()

def file_logger_start(dice_1,dice_2):
    file_object = open('log.dat', 'a')
    file_object.write(str(dice_1) + "\n" + str(dice_2) + "\n")
    file_object.close()
if __name__ == "__main__":
    mainMenu()
