# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# TO-DO: SWAP PLACEHOLDER CRYPTID NAMES WITH CHARACTER NAMES!!!
# to-do: add character name colors based on char design

define v = Character("Vampire")
define w = Character("Werewolf")
define a = Character("Alien")
define s = Character("Selkie")
define g = Character("Ghost")
define f = Character("Fairy")
define m = Character("Medusa")
define d = Character("Doppelganger")

define ingredients = ["Vodka", "Whiskey", "Bourbon", "Blue Curacao", "Sake", "Amaretto", "Wine", "Gin", "Tequila", "Brandy", 
"Tomato", "Wormwood", "Powdered Green Dust", "Plastic", "Blue Raspberry Swirl", "Milk", "Glitter", "Simple Syrup", "Generic Energy Drink", "Grenadine", 
"Garlic", "Silver Spoon", "Unbranded and Totally Non-Descript Peanut Butter and Chocolate Pieces", "Cinnamon", "Salt", "Lemon", "Mirror", "Sage", "Blood", "Mint"]

# preferred ingredients of each character
# doppelganger likes/dislikes initially -1 as a placeholder
define char_preferences = [
    [0, 10, 20], 
    [1, 11, 21], 
    [2, 12, 22], 
    [3, 13, 23], 
    [4, 14, 24], 
    [5, 15, 25], 
    [6, 16, 26], 
    [-1, -1, -1]
]

# defines where liked ingredient pos is of each character in char_preferences
# doppelganger is initially -1
define likes_pos = [0, 0, 2, 2, 0, 1, 1, -1]

define cur_char = -1
define lives_count = 3      # if 0, game over state
define drink_result = -1   # 0-5 for dialogue branching, 3 is win state

# array pos matches char_select path branching
define sus_array = [0, 0, 0, 0, 0, 0, 0, 0]
define has_visited = [False, False, False, False, False, False, False, False]
define char_choice_array = [0, 1, 2, 3, 4, 5, 6, 7]

transform size_close:
    ysize 800
    fit "contain"

# plays sip and glass clink sound TO-DO
# label sip_sfx:

# !!! sep python section for drink mixing minigame !!!

# serve drink occurs dialogue notes PLACEHOLDER TEXT
# all neutral --> "whole drink is forgettable"
# 1 like, 0 dislikes --> "i like it, but its not memorable enough"
# 1 like, 1 dislike --> point out neutral ingredient "...is quite boring"
# 1 like, 2 dislikes --> "this seems goo- what have you done?" crashes out --> character drink made --> they don't show up again good job!
# 1 dislike, 2 neutrals --> "both forgettable and mildy disgusting..."
# 2 dislikes, 1 neutral --> "this doesnt look good at all..." will not even drink it

# sets drink result var to be 0-5 based on num of like/dislike/neutrals (3 is win state), sets neutral ingredient name if applicable
# drink score -> +2 for like, +1 per dislike -> score == 3 win state
# pop out ingredients in drink array if found -> any leftover items are neutral
# init python:
#     def drink_match_var_setting(drink_array, character_pref_array):




label char_select:
    define random_char = renpy.random.choice(char_choice_array)

    while random_char == cur_char:
        $ random_char = renpy.random.choice(char_choice_array)     # reroll random char if same as cur

    $ cur_char = random_char

    if cur_char == 0:
        call vampire_path
    elif cur_char == 1:
        call werewolf_path
    elif cur_char == 2:
        call alien_path
    elif cur_char == 3:
        call selkie_path
    elif cur_char == 4:
        call ghost_path
    elif cur_char == 5:
        call fairy_path
    elif cur_char == 6:
        call medusa_path
    else:
        call doppelganger_path

    return

# dialogue path of vampire
label vampire_path:
    show vamp unhappy
    v "1" 

    if has_visited[0] == True:
        v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[0] != 0:
            v "...you can ask me another question."
            $ sus_array[0] -= 1

    # TO-DO: IMPLEMENT BRANCHING DIALOGUE FOR ASKING QUESTIONS SECTION
    # make sure to break out of dialogue if sus == 3

    # after serve drink
    
    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(0)

    # else wrong --> branching dialogue notes on drink TO-DO --> remember to add the else statement!
    $ has_visited[0] = True
    $ lives_count -= 1

    # parting goodbye lines

    return  

# dialogue path of werewolf
label werewolf_path:
    show vamp unhappy
    v "2"  

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(1)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[1] = True
    $ lives_count -= 1
    # parting goodbye lines

    return 

# dialogue path of alien
label alien_path:
    show vamp unhappy
    v "3" 

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(2)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[2] = True
    $ lives_count -= 1
    # parting goodbye lines

    return

# dialogue path of selkie
label selkie_path:
    show vamp unhappy
    v "4" 

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(3)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[3] = True
    $ lives_count -= 1
    # parting goodbye lines

    return  

# dialogue path of ghost
label ghost_path:
    show vamp unhappy
    v "5"  

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(4)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[4] = True
    $ lives_count -= 1
    # parting goodbye lines

    return

# dialogue path of fairy
label fairy_path:
    show vamp unhappy
    v "6"  

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(5)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[5] = True
    $ lives_count -= 1
    # parting goodbye lines

    return 

# dialogue path of medusa
label medusa_path:
    show vamp unhappy
    v "7"

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(6)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[6] = True
    $ lives_count -= 1
    # parting goodbye lines

    return

# dialogue path of doppelganger
label doppelganger_path:
    show vamp unhappy
    v "8"

    # if right --> TO-DO: ADD IF STATEMENT FOR CHECKING CORRECTNESS
    v "this seems goo- what have you done?"
    $ char_choice_array.remove(7)

    # else wrong --> branching dialogue notes on drink
    $ has_visited[7] = True
    $ lives_count -= 1
    # parting goodbye lines

    return


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # calls character until no chars remain or you lost all your lives
    while char_choice_array and lives_count != 0:
        call char_select 
   
    # win/lose state
    if lives_count == 0:
        "Lose state womp womp" # TO-DO: IMPLEMENT LOSE STATE
    else:
        "Everyone died nahhhhh" # TO-DO: IMPLEMENT WIN STATE     

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show vamp happy

    # These display lines of dialogue.

    v "Hi I like drinking things."

    v "Things that are. not blood."

    "I'm feeling especially human today y'know?"

    "something about being a bartender I guess..."

    show vamp unhappy
    
    v "Ew I dislike humans."



$chv_sus = 0

menu:
    "Aren't you a human?":
        v "Of course, what kind of question is that!"
        $ chv_sus += 2
    "Me too man, me too":
        show vamp happy
        v "I like you... you have good sense."


label stats:
    "The customer's suspicion of you is at [chv_sus]. The less suspicious they are, the longer you can talk to them."

show vamp happy at left, size_close

v "I'm here for a human drink. Got any reccomendations? It's been a while since I've been outside."

menu:
    "Actually, I'd like to ask some questions to get your tastes.":
        v "This would lead into a menu of questions with different effects on suspicion. If I had the time."

    "Yes, I'll make you a bloody mary!":
        show vamp unhappy
        v "Bleh I'm gonna die because you put garlic in it"

    "Yes, I'll make you a strawberry daiquiri!":
        v "Wow way too sweet. I'm never coming back here."

return
