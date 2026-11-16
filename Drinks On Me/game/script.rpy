# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# TO-DO: SWAP PLACEHOLDER CRYPTID NAMES WITH CHARACTER NAMES!!!
# to-do: add character name colors based on char design

define b = Character("Bartender")
define v = Character("Vampire")
define w = Character("Werewolf")
define a = Character("Alien")
define s = Character("Selkie")
define g = Character("Ghost")
define f = Character("Fairy")
define m = Character("Medusa")
define d = Character("Doppelganger")
image doppel neutral = "images/Doppelganger/doppelganger_neutral.png"
image doppel neutral talk = "images/Doppelganger/doppelganger_neutral_open.png"
image doppel happy = "images/Doppelganger/doppelganger_happy.png"
image doppel happy talk = "images/Doppelganger/doppelganger_happy_open.png"
image doppel angry = "images/Doppelganger/doppelganger_angry.png"
image doppel angry talk = "images/Doppelganger/doppelganger_angry_open.png"
image doppel shocked = "images/Doppelganger/doppelganger_shocked.png"
image doppel true form = "images/Doppelganger/doppelganger_true_form.png"

define ingredients = ["Vodka", "Whiskey", "Bourbon", "Blue Curacao", "Sake", "Amaretto", "Wine", "Gin", "Tequila", "Brandy", 
"Tomato", "Monkshood", "Powdered Green Dust", "Plastic", "Blue Raspberry Swirl", "Milk", "Glitter", "Simple Syrup", "Generic Energy Drink", "Grenadine", 
"Garlic", "Silver Spoon", "Unbranded and Totally Non-Descript Peanut Butter and Chocolate Pieces", "Cinnamon", "Salt", "Lemon", "Mirror", "Sage", "Blood", "Mint"]

# preferred ingredients of each character
# doppelganger likes/dislikes initially -1 as a placeholder
define correct_drink = [
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

default cur_char = -1
default lives_count = 3      # if 0, game over state

default served_drink = []     # edited after clicking "serve" in mixing minigame

default drink_result = 0   # 0-5 for dialogue branching, 3 is win state
default neutral_ingredient = -1      # for drink dialogue

# array pos matches char_select path branching
default sus_array = [0, 0, 0, 0, 0, 0, 0, 0]
default has_visited = [False, False, False, False, False, False, False, False]
default char_choice_array = [0, 1, 2, 3, 4, 5, 6, 7]

transform size_close:
    ysize 800
    fit "contain"

# plays sip and glass clink sound TO-DO
# label sip_sfx:


# sets drink result var to be 0-5 based on num of like/dislike/neutrals (3 is win state), sets neutral ingredient name if applicable
# pop out ingredients in drink array if found -> any leftover items are neutral
# drink array [_, _, _], correct drink array [_, _, _]
init python:
    def set_drink_result_variables(drink_array, correct_drink_array, char_num):
        disliked_ingredients = []
        liked_ingredient = correct_drink_array[likes_pos[char_num]]
        result_count = [0, 0, 0]    # count of like, dislike, and neutral in drink_array

        # add dislikes to array
        for ingredient in correct_drink_array:
            if ingredient != liked_ingredient:
                disliked_ingredients.append(ingredient)

        # if liked ingredient is in drink array
        if liked_ingredient in drink_array:
            result_count[0] = 1
            drink_array.remove(liked_ingredient)

        # if disliked ingredient is in drink array
        for ingredient in disliked_ingredients:
            if ingredient in drink_array: 
                result_count[1] += 1
                drink_array.remove(ingredient)

        # count leftover ingredients in drink array, they are neutral
        for ingredient in drink_array:
            result_count[2] += 1

        # if like
        if result_count[0] == 1:
            if result_count[1] == 0:
                global drink_result
                drink_result = 1    # 1 like, 0 dislikes
            elif result_count[1] == 1:
                global drink_result
                drink_result = 2    # 1 like, 1 dislike

                global neutral_ingredient
                neutral_ingredient = drink_array[0]     # like and dislike was removed from array, array only contains the neutral ingredient
            else:
                global drink_result
                drink_result = 3    # 1 like, 2 dislikes --> win state!
        # if no like
        elif result_count[1] > 0:
            if result_count[1] == 1:
                global drink_result
                drink_result = 4    # 1 dislike, 2 neutrals
            else:
                global drink_result
                drink_result = 5    # 2 dislikes, 1 neutral
        else:
            global drink_result
            drink_result = 0    # all neutrals


label char_select:
    $ random_char = renpy.random.choice(char_choice_array)

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
    $ drink_result = 0      # initialize drink result
    show doppel neutral
    v "1"

    if has_visited[0] == True:
        if sus_array[0] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[0] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[0] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[0] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[0] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[0] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[0] += 1
            if sus_array[0] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[0], 0)

    # serve drink occurs dialogue notes PLACEHOLDER TEXT
    # 0: all neutral --> "whole drink is forgettable"
    # 1: 1 like, 0 dislikes --> "i like it, but its not memorable enough"
    # 2: 1 like, 1 dislike --> point out neutral ingredient "... is quite boring"
    # 3: 1 like, 2 dislikes --> "this seems goo- what have you done?" crashes out --> character drink made --> they don't show up again good job!
    # 4: 1 dislike, 2 neutrals --> "both forgettable and mildy disgusting..."
    # 5: 2 dislikes, 1 neutral --> "this doesnt look good at all..." will not even drink it

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(0)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[0] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return  

# dialogue path of werewolf
label werewolf_path:
    $ drink_result = 0      # initialize drink result
    show doppel neutral
    v "2"  

    if has_visited[1] == True:
        if sus_array[1] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[1] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[1] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[1] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[1] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[1] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[1] += 1
            if sus_array[1] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[1], 1)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(1)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[1] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return 

# dialogue path of alien
label alien_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "3" 

    if has_visited[2] == True:
        if sus_array[2] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[2] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[2] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[2] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[2] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[2] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[2] += 1
            if sus_array[2] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[2], 2)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(2)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[2] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return

# dialogue path of selkie
label selkie_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "4" 

    if has_visited[3] == True:
        if sus_array[3] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[3] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[3] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[3] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[3] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[3] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[3] += 1
            if sus_array[3] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[3], 3)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(3)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[3] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return  

# dialogue path of ghost
label ghost_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "5"  

    if has_visited[4] == True:
        if sus_array[4] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[4] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[4] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[4] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[4] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[4] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[4] += 1
            if sus_array[4] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[4], 4)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(4)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[4] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return

# dialogue path of fairy
label fairy_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "6"  

    if has_visited[5] == True:
        if sus_array[5] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[5] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[5] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[5] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[5] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[5] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[5] += 1
            if sus_array[5] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[5], 5)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(5)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[5] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return 

# dialogue path of medusa
label medusa_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "7"

    if has_visited[6] == True:
        if sus_array[6] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[6] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[6] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[6] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[6] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[6] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[6] += 1
            if sus_array[6] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[6], 6)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(6)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[6] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return

# dialogue path of doppelganger
label doppelganger_path:
    $ drink_result = 0      # initialize drink result
    show vamp unhappy
    v "8"

    if has_visited[7] == True:
        if sus_array[7] == 0:
            show doppel happy talk
            v "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            v "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[7] != 0:
            v "...I might be open to talk a little again."
            show doppel neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[7] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions

                if sus_array[7] < 3:
                    jump .decision
                else: 
                    "It looks like the guest is no longer up for conversation anymore. Let's make them that drink then."
                    call make_drink
                    jump .after_drink

            "Mix Drink":
                "Are you sure you'd like to mix the drink now? You cannot go back to talk to the guest after this."
                menu:
                    "Yes":
                        call make_drink
                        jump .after_drink
                    "No":
                        jump .decision

    # EDIT CHARACTER QUESTIONS
    # where you ask questions
    label .ask_questions:
        if sus_array[7] >= 3:
            show doppel angry talk
            v "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[7] < 3:
                menu:
                    "Why are you so beautiful?":
                        show doppel happy talk
                        v "thank you"
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show doppel angry talk
                        v "bro wtf"
                        show doppel angry
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                v ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        v "..."
                                        call .add_sus
                                    "Nevermind, I'm done asking questions.":
                                        return
                                    
                            "Nevermind, I'm done asking questions.":
                                return    

                    "Nevermind, I'm done asking questions.":
                        return                                    
            return

        # helper function for halting questions if max sus reached
        label .add_sus():
            $ sus_array[7] += 1
            if sus_array[7] >= 3:
                $ renpy.pop_call()
                return
            return

        return

    # after serve drink

    label .after_drink:
        show doppel neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[7], 7)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            v "this seems goo- what have you done?"
            $ char_choice_array.remove(7)
        else:
            if drink_result == 0:
                v "whole drink is forgettable"
            elif drink_result == 1:
                v "i like it, but its not memorable enough"
            elif drink_result == 2:
                v "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                v "both forgettable and mildy disgusting..."
            else:
                v "this doesnt look good at all..."

            $ has_visited[7] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Goodbye."

        hide doppel

    return


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room
    #start the bg music
    play music "relaxing-jazz-music-loop.mp3"



    # calls character until no chars remain or you lost all your lives
    while char_choice_array and lives_count != 0:
        call char_select 
   
    # win/lose state
    if lives_count == 0:
        "Lose state womp womp" # TO-DO: IMPLEMENT LOSE STATE
    else:
        "Everyone died nahhhhh" # TO-DO: IMPLEMENT WIN STATE     


return
