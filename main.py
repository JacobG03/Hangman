import random
from content import words_list, hangmanpics, quotes
import time
from bs4 import BeautifulSoup
import requests
import json
import pickle
import os
import webbrowser


"""
A Hangman game with a few cool options
made as a fun project to test my own skills.
Made by: Jacob Gluszek
20/09/2020
Disclaimer! English is not my main language..
"""


#Important global variables
won_games = 0
played_games = 0


#The ASCII + 'time.sleep()' is used to simulate the game loading, I feel like it adds the sense of you actually playing a video game. 
def start():    #The game starts with this function
    os.system("cls")    #This function clears the console, it is used a lot throughout the code
    print(r"""
                      _____ _             _   _                   
                     / ____| |           | | (_)                  
                    | (___ | |_ __ _ _ __| |_ _ _ __   __ _       
                     \___ \| __/ _` | '__| __| | '_ \ / _` |      
                     ____) | || (_| | |  | |_| | | | | (_| |_ _ _ 
                    |_____/ \__\__,_|_|   \__|_|_| |_|\__, (_|_|_)
                                                       __/ |      
                                                      |___/        
                                    """)
    time.sleep(2)

    enter_username()    


def enter_username():   #Takes the users name
    os.system("cls")
    print(r"""
           __      _                                                                                        
          /__/ __ | |_ ___ _ __   _   _  ___  _   _ _ __     /\ /\ ___  ___ _ __ _ __   __ _ _ __ ___   ___ _ 
         /_\| '_ \| __/ _ | '__| | | | |/ _ \| | | | '__|   / / \ / __|/ _ | '__| '_ \ / _` | '_ ` _ \ / _ (_)
        //__| | | | ||  __| |    | |_| | (_) | |_| | |      \ \_/ \__ |  __| |  | | | | (_| | | | | | |  __/_ 
        \__/|_| |_|\__\___|_|     \__, |\___/ \__,_|_|       \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|\___(_)
                                  |___/                                                                     
            """)
    name = input("\n                                                        >")
    
    os.system("cls")
    print(r"""
                     _                       _                 _             
                    | |                     (_)               (_)            
                    | |     ___   __ _  __ _ _ _ __   __ _     _ _ __        
                    | |    / _ \ / _` |/ _` | | '_ \ / _` |   | | '_ \       
                    | |___| (_) | (_| | (_| | | | | | (_| |   | | | | |_ _ _ 
                    |______\___/ \__, |\__, |_|_| |_|\__, |   |_|_| |_(_|_|_)
                                  __/ | __/ |         __/ |                
                                 |___/ |___/         |___/                 
        """)
    
    time.sleep(1.25)
    main_menu(name)


def main_menu(name):    #Function that displays the "main menu", user can navigate where he wants to from here

    if played_games == 0:   #This makes sure 'coins' will reset to zero everytime the user starts from the beginning
        coins = 0
    
    os.system("cls")
    print(f"                                                      Logged in as: {name}")
    print(r"""
                 _    _                                         
                | |  | |                                        
                | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
                |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
                | |  | | (_| | | | | (_| | | | | | | (_| | | | |
                |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                     __/ |                      
                                    |___/                       
                    """)
    print("                                 Level: Hard\n                      This game might make your head hurt.\n")
    print("")
    high_score(name, won_games, played_games)
    print("")
    print("1. Let me play! (ง'̀-'́)ง")
    print("2. Ok.. how do I play this game? ಠ_ರೃ")
    print("3. Cheats ޏ₍ ὸ.ό₎ރ")
    print('4. Change user. ~(˘▾˘~) ~(˘▾˘)~ (~˘▾˘)~')
    print("5. **** this, I'm out! (╯°□°）╯︵ ┻━┻\n")


    while True:
        user_choice = input(">")

        if user_choice == "1":
            game(won_games, played_games, name, coins)

        elif user_choice == "2":
            description(played_games, won_games, name, coins)

        elif user_choice == "3":
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO", new=2)
        
        elif user_choice == "4":
            relog()

        elif user_choice == "5":
            os.system("cls")
            
            print(r"""  
                                 _____                _ 
                                /  __ \              | |
                                | /  \/ _   _   __ _ | |
                                | |    | | | | / _` || |
                                | \__/\| |_| || (_| ||_|
                                 \____/ \__, | \__,_|(_)
                                         __/ |          
                                        |___/           
                    """)
            
            time.sleep(2.5)
            quit()
        else:   #If a user inputs something that doesn't do anything, this will make sure it doesn't stack on each other - makes the menu 'fresh'
            main_menu(name)


def game(won_games, played_games, name, coins):     #This function generates the word, lets you guess it, replaces the blanks, checks if you win or loose
    os.system("cls")
    print(r"""                    
                         _                     _ _             
                        | |                   | (_)            
                        | |     ___   __ _  __| |_ _ __   __ _ 
                        | |    / _ \ / _` |/ _` | | '_ \ / _` |
                        | |___| (_) | (_| | (_| | | | | | (_| |
                        |______\___/ \__,_|\__,_|_|_| |_|\__, |
                                                          __/ |
                                                         |___/ 
                                  """)
    
    word = random.choice(words_list)    #Picks the word to guess randomly from the list
    ready_definition = definition(word, 1)      #This variable is used for the definition() function to scrape the web only once instead of everytime it's called (usefull later on)

    word = word.lower() #Changes it to lowercase (just in case of it being capitalized)
    z = 0 # This variable is used to determine whether to keep showing the definition of the word during the game or no (does so if you bought the option)

    blanks = len(word) * "_"

    #All the necessary lists
    word_list = list(word)      #Used for easier comparison with different lists
    guess_list = []     #Contains missed letters
    blanks_list = list(blanks)      #Used for updating the blanks with correctly guessed letters

    guess = None    #Here to prevent an error

    os.system("cls")

    bought_letter = None    #Here to prevent an error
    stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition)  #Shows the hangman, the blanks, amount of coins, available options
    
    while len(guess_list) < 6:  #While loop which ends when the user runs out of attempts to guess or wins
        guess = input("\nGuess a letter:\n>")
        guess = guess.lower()

        if len(guess) > 1:  #If too many characters at a time it lets the user try again
            if guess == "passwordplease":   #Little cheat :)
                print(f"I like that you said 'please' :) Catch! '{word}'")
            else:
                print("My dude, 1 at a time okay? :)")

        elif guess == "":   #If no characters it lets the user try again
            print("At least give it a try :)")

        elif guess in guess_list:   #If letter was already used it will let the user try again
            print("This letter was already used")

        elif guess == "1":  #If input is 1 and user has enough coins this generates a random not yet guessed letter and passes it to stats() function
            if coins >= 2:
                x = True
                while x:
                    bought_letter = random.choice(word_list)
                    if bought_letter not in blanks_list:
                        x = False
                coins = coins - 2
                stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition)  #Prints hangman, blanks list etc. + the 'bought_letter'
            else:
                print("Not enough coins.")
               
        elif guess == "2":  #Same situation as above but prints the definition of the word
            if coins >= 5:
                coins = coins - 5
                z = 1
                stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition)
            else:
                print("Not enough coins.")

        else:
            #If correctly guessed letter it replaces it at the correct index in blanks_list, takes care of multiple letters
            i = 0
            while i < len(word):
                if guess == word[i]:
                    blanks_list[i] = word_list[i]
                i = i + 1
            
            if guess in word_list: #If the guess was correct it updates the stats() function

                if blanks_list == word_list:    #Every time the guess is correct it checks if the user managed to guess all of the letters, if so it calls the result_screen() function
                    result = "win"      #Passed to the function result_screen() allows it to determinate whether it was a loss or a win

                    result_screen(guess_list, word, name, result, played_games, won_games, coins)

                stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition) #Prints updated stats()

            else:   #If missed guess it:
                if guess.isalpha(): #Checks if it was indeed a letter, if so it adds it to the list containing all missed letters
                    guess_list.append(guess)

                    stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition)
                else:
                    print("Guess the word using letters :)")

    #If the while loop ends that means the user lost
    result = "loss" #Passed to the function result_screen() allows it to determinate whether it was a loss or a win
    result_screen(guess_list, word, name, result, played_games, won_games, coins)


def definition(word, y):    #Returns a definition of the word, takes argument 'y' to determine whether to print 'word - definition...' or return the definition (usefull in a few cases)
    try:
        link_1 = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        link_2 = word

        full_link = link_1 + link_2

        r = requests.get(full_link)
        j = r.json()

        word_definition = j[0]["meanings"][0]["definitions"][0]["definition"]
        
        if y == 0:
            print(f'\n"{word}" - {word_definition}')
        elif y == 1:
            return word_definition
    except: #Sometimes there's no definition found using this function, in that case it raises an exception
        print("Error: No definition found.")


def high_score(name, won_games, played_games):   #Displays 'name, won_games/played_games' of the user with the highest amount of wins during gameplay
    score = [name, won_games, played_games]                                         #Uses pickle to save/load the data everytime the user runs the program
    read_score = pickle.load(open("personalbest.txt", "rb"))
    print(f"                          Highest score ==> {read_score[0]} | {read_score[1]}/{read_score[2]}\n")

    if score[1] > read_score[1]:    #If the user playing has a better score it overwrites the 'personbest.txt' with the new highest score
        pickle.dump(score, open("personalbest.txt", "wb"))


def stats(guess_list, blanks_list, guess, coins, bought_letter, word, z, ready_definition): #This function basically prints everything necessary while the user is guessing the word
    os.system("cls")                                                                        #It prints the amount of 'coins', options available, hangman ASCII, missed letters,
                                                                                            #updated blanks_list, and depending on the input it also prints the definition of the word
    print(f"You have {coins} coins.")                                                       #and the 'bought_letter'
    print("Store:")
    print("    1. Give 1 random letter. Cost: 2 coins")
    print("    2. Give definition of the word. Cost: 5 coins\n")
    print(hangmanpics[len(guess_list)])
    print("                                 Misses ==> ", *guess_list, sep=" ",)
    print("           ", *blanks_list, sep=" ")

    if z == 1:
        print(ready_definition)

    if guess == "1":
        print(f"\nHere you go: '{bought_letter}'. {coins} coins left.")


def result_screen(guess_list, word, name, result, played_games, won_games, coins):  #Depending whether the user guessed the word or not it will update the amount of coins the user has,
    if result == "win":                                                             #update 'won_games' and 'played_games', print the hangmans state and lets the user decide what to do now
        won_games = won_games + 1
        played_games = played_games + 1

        coins = coins + 2 + 6 - len(guess_list) 
        os.system("cls")

        print(hangmanpics[len(guess_list)])
        print(f"\nWell done {name}!\nYou guessed the word: '{word}'.\n")

        y = 0
        definition(word, y)

    elif result == "loss":
        played_games = played_games + 1
        os.system("cls")

        print(hangmanpics[len(guess_list)])
        print(f"\nNo attempts left! Secret word: '{word}'.\n")

        y = 0
        definition(word, y)

    print(f"You have {coins} coins.")
    print(f"\nYour wins/games ratio: {won_games}/{played_games}\n")

    print("1. Continue playing")
    print("2. Return to Main menu")
    print("3. 'ALT + F4', but not really :)")

    while True:
        user_choice = input("\n>")

        if user_choice == "1":
            game(won_games, played_games, name, coins)

        elif user_choice == "2":
            high_score(name, won_games, played_games)
            main_menu(name)

        elif user_choice == "3":
            os.system("cls")
            
            print(r"""  
                         _____                _ 
                        /  __ \              | |
                        | /  \/ _   _   __ _ | |
                        | |    | | | | / _` || |
                        | \__/\| |_| || (_| ||_|
                         \____/ \__, | \__,_|(_)
                                 __/ |          
                                |___/           
                    """)
            
            time.sleep(1.75)
            os.system("cls")
            print(r"""
                                        ⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⣿⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣄⡀⠀⢻⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⠃⢰⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⢶⣶⣶⣾⣿⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢠⡀⠐⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢸⣷⡄⠀⠣⣄⡀⠀⠉⠛⢿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⣿⣿⣦⠀⠹⣿⣷⣶⣦⣼⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣷⣄⣸⣿⣿⣿⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                        ⣿⣿⡿⢛⡙⢻⠛⣉⢻⣉⢈⣹⣿⣿⠟⣉⢻⡏⢛⠙⣉⢻⣿⣿⣿
                                        ⣿⣿⣇⠻⠃⣾⠸⠟⣸⣿⠈⣿⣿⣿⡀⠴⠞⡇⣾⡄⣿⠘⣿⣿⣿
                                        ⣿⣿⣟⠛⣃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿
                                        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
            """)
            time.sleep(0.75)
            quit()
        else:
            print("Just type a number from 1-3 to choose.")


def description(played_games, won_games, name, coins):  #This is basically a sub_menu in the main_menu explaining how the game works
    os.system("cls")

    print("The way it works:\nBasically you have to guess a word before the the stickman hangs.\nSo you are allowed to miss a letter only 6 times.\n")
    print("You guess one letter at a time.\nWith every guessed word you gain coins. With those you are able to buy some help during the game.\n")
    print("The overall goal of this game is to guess as many words as you can.")
    print("Warning! Returning to the Main menu resets your score (It will be only saved when you beat the highest score in the game).\nGood luck and have fun!")
    print("\n1. Start playing")
    print("2. Back to main Menu")
    print("3. I got quotes.. Want some? (￣▽￣)ノ")

    while True:
        user_choice = input("\n>")

        if user_choice == "1":
            game(won_games, played_games, name, coins)

        elif user_choice == "2":
            main_menu(name)
        
        elif user_choice == "3":
            quote_generator()


def relog():    #Makes it seem as if the user is changing accounts, basically takes input for a new name
    os.system("cls")
    print(r"""
                     _                       _                            _         
                    | |                     (_)                          | |        
                    | |     ___   __ _  __ _ _ _ __   __ _     ___  _   _| |_       
                    | |    / _ \ / _` |/ _` | | '_ \ / _` |   / _ \| | | | __|      
                    | |___| (_) | (_| | (_| | | | | | (_| |  | (_) | |_| | |_ _ _ _ 
                    |______\___/ \__, |\__, |_|_| |_|\__, |   \___/ \__,_|\__(_|_|_)
                                  __/ | __/ |         __/ |                        
                                 |___/ |___/         |___/                         
            """)
    time.sleep(1.25)

    enter_username()


def quote_generator():  #Added because.. why not? Just prints a random quote from a list of quotes in 'content.py'
    quote = random.choice(quotes)
    print(quote)


start()
