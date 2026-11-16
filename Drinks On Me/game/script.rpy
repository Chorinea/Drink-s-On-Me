# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# TO-DO: SWAP PLACEHOLDER CRYPTID NAMES WITH CHARACTER NAMES!!!
# to-do: add character name colors based on char design

define b = Character("Bartender")
define v = Character("Victor")
image vampire neutral = "images/Vampire/vampire_neutralclosed1.png"
image vampire happy = "images/Vampire/vampire_happyclosed.png"
image vampire angry = "images/Vampire/vampire_angryopen.png"
define w = Character("Werewolf")
image werewolf neutral = "images/Werewolf/werewolf_neutral.png"
image werewolf happy = "images/Werewolf/werewolf_happy.png"
image werewolf angry = "images/Werewolf/werewolf_angry.png"
image werewolf shocked = "images/Werewolf/werewolf_shocked.png"
image werewolf true form = "images/Werewolf/werewolf_trueform.png"
define a = Character("Alien")
define s = Character("Shelly")
image selkie neutral = "images/Selkie/selkie_neutral.png"
image selkie happy = "images/Selkie/selkie_happy.png"
image selkie angry = "images/Selkie/selkie_angry.png"
image selkie shocked = "images/Selkie/selkie_shocked.png"
image selkie true form = "images/Selkie/selkie_trueform.png"
define g = Character("Ghost")
define f = Character("Ebony Dark'ness Dementia Raven Way")
image fairy neutral = "images/Fairy/fairy_neutral.png"
image fairy happy = "images/Fairy/fairy_happy.png"
image fairy angry = "images/Fairy/fairy_angry.png"
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

image red_flash = Solid("#ff0000")

label fade_scene:
    show red_flash
    with Dissolve(0.05)
    
    scene black
    with Dissolve(2.0)

    "Ah, what a shame. I will cherish that guest in my memories."

    scene bg room
    return

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
default char_choice_array = [0, 1, 3, 5, 7]

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
    # elif cur_char == 2:
    #     call alien_path
    elif cur_char == 3:
        call selkie_path
    # elif cur_char == 4:
    #     call ghost_path
    elif cur_char == 5:
        call fairy_path
    # elif cur_char == 6:
    #     call medusa_path
    else:
        call doppelganger_path

    return

# dialogue path of vampire
label vampire_path:
    $ drink_result = 0      # initialize drink result
    show vampire neutral
    "A suave and distinguished gentleman walks through the front door. He seems a bit pale."

    if has_visited[0] == True:
        if sus_array[0] == 0:
            show vampire happy
            v "...I came back, but rest assured, it is not because of you! ...I quite enjoy the atmosphere here, is all."
        else:
            show vampire neutral
            v "...Hmm, I suppose I felt that I should give this place another shot. Nothing more."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[0] != 0:
            v "...I might be open to talk a little again."
            show vampire neutral
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
            show vampire angry
            v "Cease making conversation with me."
            return

        v "Hm, ask away then."

        label .questions:
            if sus_array[0] < 3:
                menu:
                    "What do you prefer in a drink?":
                        show vampire happy
                        v "Something strong, but keep it more refined."
                        jump .questions
                    
                    "Any dislikes?":
                        show vampire neutral
                        v "I hate the smell of italian restaurants the most."

                        menu:
                            "Anything else?":
                                v "I wouldn't really call myself a vegan. Best believe I only desire the most ...\"authentic\" sources."
                                jump .questions

                            "Nevermind, I'm done asking questions.":
                                return 

                    "Why are you so beautiful?":
                        show vampire happy
                        v "thank you"
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show vampire angry
                        v "bro wtf"
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
        show vampire neutral
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
            show vampire happy
            v "Hmm, I can smell the strength. It seems passable enough."
            "Victor takes a sip."
            show vampire angry 
            v "What in the world did you put in this? It's absolutely horrid!"
            v "...Ugh, what... Who do you think you are...?"
            call fade_scene
            $ char_choice_array.remove(0)
        else:
            if drink_result == 0:
                show vampire neutral
                "Victor takes a sip."
                v "...incredible. This is a mind-numbingly boring taste. Truly remarkable skills you have, bartender."
            elif drink_result == 1:
                "Victor takes a sip."
                show vampire happy
                v "Hmm, I like it, but it's just not memorable enough..."

            elif drink_result == 2:
                "Victor takes a sip."                
                show vampire neutral
                v "[ingredients[neutral_ingredient]]... is quite boring."
            elif drink_result == 4:
                "Victor takes a sip."                
                show vampire angry
                v "This is both forgettable and mildy disgusting... Please refrain from serving me this again."
            else:
                show vampire angry
                v "this doesnt look good at all..."
                "Looks like he didn't want to drink it at all. Try to add something he would like to mask the drink."

            $ has_visited[0] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Hmph, this establishment is quite disappointing. Best believe I will not step into this establishment postforth."

        hide vampire

    return  

# dialogue path of werewolf
label werewolf_path:
    $ drink_result = 0      # initialize drink result
    show werewolf neutral
    "A gruff and sturdy man walks through the front door."  

    if has_visited[1] == True:
        if sus_array[1] == 0:
            show werewolf happy
            w "Hey, we've seen each other before!"
        else:
            show werewolf neutral
            w "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[1] != 0:
            w "...I might be open to talk a little again."
            show werewolf neutral
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
            show werewolf angry
            w "I do not want to talk anymore."
            return

        w "Ask away."

        label .questions:
            if sus_array[1] < 3:
                menu:
                    "What do you prefer in a drink?":
                        show werewolf happy
                        w "Got anything strong? Like, REAL strong? I need something easy to go down, I've had a long night."
                        jump .questions
                    
                    "Any dislikes?":
                        show werewolf neutral
                        w "Anything green ain't really in my diet. Try not to add that in if yah can."

                        menu:
                            "Anything else?":
                                w "Pass me somethin' to stir my drink. That would be mighty \'ppreciated."
                                jump .questions

                            "Nevermind, I'm done asking questions.":
                                return 
                    "Why are you so beautiful?":
                        show werewolf happy
                        w "thank you"
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show werewolf angry
                        w "bro wtf"
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                w ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        w "..."
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
        show werewolf neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[1], 1)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            show werewolf neutral            
            w "...Thanks of the drink."
            show werewolf shocked
            w "What in the-?! This is nasty!!"
            w "Ugh... it hurts..."
            show werewolf true form
            w "You... What do you even want from me?"
            call fade_scene
            $ char_choice_array.remove(1)
        else:
            if drink_result == 0:
                "Jakob takes a sip."
                w "Wow, man. This... tastes like nothing."
            elif drink_result == 1:
                "Jakob takes a sip."                
                w "There's somethin in there I really like, but everything else ain't that striking."
            elif drink_result == 2:
                "Jakob takes a sip."
                w "[ingredients[neutral_ingredient]]... is quite boring."
            elif drink_result == 4:
                "Jakob takes a sip."
                w "Wow, man. This... tastes like nothing. But with a hint of yuck. Can't describe it in any other way, champ."
            else:
                w "...This does not look right. Sorry kid, but I can't drink this."
                "Looks like he didn't want to drink it at all. Try to add something he would like to mask the drink."

            $ has_visited[1] = True
            $ lives_count -= 1

            # parting goodbye lines
            w "Not the best drink I've ever had. I got hope in yah next time, kid. See yah 'round."

        hide werewolf

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
    show selkie neutral
    s "...hello..."

    if has_visited[3] == True:
        if sus_array[3] == 0:
            show selkie happy
            s "Hey, we've seen each other before!"
        else:
            show selkie neutral
            s "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[3] != 0:
            s "...I might be open to talk a little again."
            show selkie neutral
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
            show selkie angry
            s "I do not want to talk anymore."
            return

        s "Ask away."

        label .questions:
            if sus_array[3] < 3:
                menu:
                    "Why are you so beautiful?":
                        show selkie happy
                        s "thank you"
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show selkie angry
                        s "bro wtf"
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                s ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        s "..."
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
        show selkie neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[3], 3)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            show selkie shocked
            s "this seems goo- what have you done?"
            show selkie true from
            s "NOOOOOOOOO"
            call fade_scene
            $ char_choice_array.remove(3)
        else:
            if drink_result == 0:
                s "whole drink is forgettable"
            elif drink_result == 1:
                s "i like it, but its not memorable enough"
            elif drink_result == 2:
                s "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                s "both forgettable and mildy disgusting..."
            else:
                s "this doesnt look good at all..."

            $ has_visited[3] = True
            $ lives_count -= 1

            # parting goodbye lines
            s "Goodbye."

        hide selkie

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
    show fairy neutral
    f "Hi, I'm Ebony Dark'ness Dementia Raven Way!!!!!"  

    if has_visited[5] == True:
        if sus_array[5] == 0:
            show fairy happy
            f "Hey, we've seen each other before!"
        else:
            show fairy neutral
            f "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[5] != 0:
            f "...I might be open to talk a little again."
            show fairy neutral
            "It seems their suspicion has slightly cooled. You can ask them more questions, if you're careful enough."
            $ sus_array[5] -= 1

    # talk or make drink choice
    label .decision:
        "What would you like to do?"
        menu:
            "Talk":
                call .ask_questions
                menu:
                    "What do you prefer in a drink?":
                        show fairy happy
                        v "MILKKKKKKKKKK MILK MILK MILK"
                        jump .questions
                    
                    "Any dislikes?":
                        show fairy neutral
                        v "nothing SOUR BLEGH"

                        menu:
                            "Anything else?":
                                v "NOTHING with nuts, im allergic!!!!"
                                jump .questions

                            "Nevermind, I'm done asking questions.":
                                return 
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
            show fairy angry
            f "I do not want to talk anymore."
            return

        v "Ask away."

        label .questions:
            if sus_array[5] < 3:
                menu:
                    "Why are you so beautiful?":
                        show fairy happy
                        f "thank you"
                        jump .questions     # let player ask more questions after branch end

                    "Are you evil?":
                        show fairy angry
                        f "bro wtf"
                        call .add_sus

                        menu:
                            "Yah cuz your face just looks evil":
                                f ">:("
                                call .add_sus

                                menu:
                                    "...are you a vampire":
                                        f "..."
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
        show fairy neutral
        "You hand the drink to the guest."
        $ set_drink_result_variables(served_drink, correct_drink[5], 5)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            show fairy shocked
            f "this seems goo- what have you done?"

            call fade_scene
            $ char_choice_array.remove(5)
        else:
            if drink_result == 0:
                show fairy neutral
                f "whole drink is forgettable"
            elif drink_result == 1:
                show fairy happy
                f "i like it, but its not memorable enough"
            elif drink_result == 2:
                show fairy neutral
                f "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                show fairy angry
                f "both forgettable and mildy disgusting..."
            else:
                show fairy angry
                f "this doesnt look good at all..."

            $ has_visited[5] = True
            $ lives_count -= 1

            # parting goodbye lines
            f "Goodbye."

        hide fairy

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
    show doppel neutral
    "Someone walks in, looking like... you?"

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
            show doppel angry
            d "Okay that's enough, you're just being a meanie! I don't want to answer any more of your questions."
            b "Look I'm not trying to-"
            d "I don't wanna hear it! Do you talk to everyone else like this?"
            b "Well-"
            d "Me wanna drink now!"
            show doppel angry
            return

        d "Ask away."

        label .questions:
            if sus_array[7] < 3:
                menu:
                    "I think you got something on your face?":
                        call .add_sus
                        show doppel happy talk
                        d "Wahh!! Really? Oh my god that's so embarrassing, what is it?"
                        menu:
                            "It kinda looks like a slice of cheese?":
                                d "Ohh that, silly bartender I obvioiusly know about that."
                                b "Well why is it there then?"
                                d "I'm saving it as a snack for later!"
                                b "A snack...?"
                                d "Yeah, I might even have it with my drink!"
                            "It's the sticky note that's covering literally your whole face!":
                                call .add_sus
                                d "W-What are you talking about, this is just how I look!"
                                b "You have a whole sticky note just ccovering your face! How can you even see me right now?"
                                d "Wahhh... you're just making fun of me..."
                                b "Okay okay I'm sorry, I'll just drop it!"
                                d "..."
                                b "L-Look the drinks on me, okay?"
                                d "Really! You'd do that for me?"
                            "Alright let's just move on from this...":
                                return
                        show doppel happy
                        jump .questions     # let player ask more questions after branch end

                    "What kind of flavor profile are you looking for?":
                        show doppel angry talk
                        d "Oh you know, a little of this, a little of that."
                        b "Okay but if you had to pic one main flavor what would it be?"
                        d "Look I don't know, I'm just a little guy who's had a long day! How about a drink you {b}haven't served anyone else.{/b}"
                        show doppel angry
                
                    "So how long have you been working here?":
                        call .add_sus
                        d "Uhh, I'm not sure. I haven't bothered to keep track, we're more than just our jobs you know?"
                        b "Fair enough, I'm ust surprised we haven't met before this. Not that many people are staffed here."
                        d "C-Crazy, we must have just barely missed each other!"
                        b "Yeah that's probably it, what hours do you usually work?"
                        d "I don't know...?"
                        b "You don't know what time you work?"
                        d "No, I mean..."
                        d "l-like my schedule is just pretty random. I'll just pick up shifts here and there so it kinda looks different each week."
                        b "Uh huh..."

                    "Do you take it dry or wet?":
                        d "Ohhh you know I could take it either way, I'm not too picky about how it goes down~"
                        b "I'm tlaing about drinks."
                        d "..."
                        b "..."
                        d "T-That's totally what I meant!"
                        b "I can only take your word for it..."

                    "Let me guess you like your drinks sweet?":
                        d "Aww are you just saying that because you think I'm sweet?"
                        menu:
                            "You could say that.":
                                d "Bartender! You're making me blush~"
                                b "I like to consider myself a smooth talker."
                                d "I'll be honest I don't have strong opinions on sugary drinks."
                                b "Could you give me a hint?"
                                d "Hmm, well how about this?"
                                d "I'll take the {b}favorite{/b} drink of my {b}favorite{/b} bartender."
                            "Nah, sweet cocktails are just pretty popular.":
                                call .add_sus
                                d "Oh... well are you sure both can't be true?"
                                b "I mean I guess, but I don't really know you."
                                d "Bartender you're so cold!"
                                b "Okay, well tell me something about yourself."
                                d "...Pass."
                            "Gotcha loud and clear.":
                                return 

                    "Are you looking to get drunk or just have something nice to sip on?":
                        d "Well I don't see why both aren't possible."
                        b "Huh... I only ever thought about it as one or the other to be honest."
                        d "I just have a hard time making choices for myself! There's so many options to choose from..."
                        b "So why'd you decide to walk into the bar then?"
                        d "I want a drink only {b}only{/b} you would make."
                        b "Geez that's a lot of pressure."
                        d "I know you can do it"
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

    call doppelganger_path

    # calls character until no chars remain or you lost all your lives
    while char_choice_array and lives_count != 0:
        call char_select 
   
    # win/lose state
    if lives_count == 0:
        "Lose state womp womp" # TO-DO: IMPLEMENT LOSE STATE
    else:
        "Everyone died nahhhhh" # TO-DO: IMPLEMENT WIN STATE     


return
