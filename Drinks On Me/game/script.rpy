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
define w = Character("Jakob")
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
define d = Character("Yoru Nanami")
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
    v "I'll be trying this bar. Don't disappoint me."

    if has_visited[0] == True:
        if sus_array[0] == 0:
            show vampire happy
            v "Surprise! Your favorite customer is back. I expect something impressive..."
        else:
            show vampire neutral
            v "Yes I'm back, try to make something less disgusting this time."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[0] != 0:
            show vampire angry
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
                    show vampire angry
                    v "Enough of this. Your questions bore me. Make me my drink, drink maker."
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
            v "Enough of this. Your questions bore me. Make me my drink, drink maker."
            return

        v "Hm, ask away then."

        label .questions:
            if sus_array[0] < 3:
                menu:
                    "Anything specific you want?":
                        show vampire happy
                        v "It needs to be red."
                        show vampire angry
                        v "I won't drink it if it's not red."
                        jump .questions
                    
                    "You seem fidgety...":
                        show vampire neutral
                        v "Well, I could use a cigarette."
                        show vampire happy
                        v "It helps control the cravings."
                        b "You can't smoke in here."
                        show vampire angry
                        v "Since when??"
                        v "Ugh, whatever. Just get me my drink."
                        call .add_sus
                        jump .questions


                    "What's with the cloak?":
                        show vampire happy
                        v "Cloaks are an excellent way to stay dry. Much better than awful modern textiles."
                        show vampire neutral
                        v "You would do well to switch to one yourself."
                        show vampire happy
                        v "If you could afford it."
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end

                    "What kinds of drinks do you like?":
                        show vampire happy
                        v "Classic, don't do anything crazy or modern."
                        show vampire happy
                        v "I'm also fond of alchohol made with a potato base."
                        v "They're stored underground, how comforting..."
                        show vampire neutral
                        v "Oh, and you can leave off the garnish, nothing with a wooden skewer."
                        jump .questions

                    "Do you play a lot of rpgs? You kinda remind me of a character...":
                        show vampire neutral
                        v "Video games... All technology is obnoxious."
                        show vampire happy
                        v "Why anyone would want to play a game on them is beyond me."
                        call .add_sus
                        jump .questions

                    "What is your least favorite flavor?":
                        show vampire neutral
                        v "Italian food."
                        show vampire angry
                        v "Just walking by a restaurant is stomach turning... ugh."
                        jump .questions
                    
                    "Nevermind, I'm done asking questions.":
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
        show vampire happy
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
                v "hm. I didn’t know it was possible to make something so… inoffensive. Like drinking nothing at all. "
                show vampire happy
                v "Maybe try harder next time, I like to be dazzled, not bored."
            elif drink_result == 1:
                show vampire neutral
                "Victor takes a sip."
                v "Not bad, not bad at all. It has some positive qualities… but it’s not memorable enough."
                show vampire happy
                v "I think it needs a little more of a kick."
            elif drink_result == 2:
                show vampire neutral
                "Victor takes a sip."
                v "[ingredients[neutral_ingredient]]... is quite boring."
                v "Maybe actually try to make the whole drink appealing next time."
            elif drink_result == 4:
                "Victor takes a sip."
                show vampire angry
                v "both forgettable and mildy disgusting... I don’t know how you managed that, given how nosy you seem."
                v "Try harder next time. I won’t even bother drinking this."
            else:
                show vampire angry
                v "Wow. Wow. How incredibly unappealing. Did you happen to spit in my drink as well? If you wanted me to leave, just say so."
                "Looks like he didn't want to drink it at all. Try to add something he would like to mask the drink."                

            $ has_visited[0] = True
            $ lives_count -= 1

            # parting goodbye lines
            v "Hmph, this establishment is quite subpar. I hope to see improvement soon."

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
            w "...Not up to chatting right now."
            return

        w "Well then, ask away."

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
        w "...Thanks of the drink."
        $ set_drink_result_variables(served_drink, correct_drink[1], 1)           

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            "Jakob takes a sip."
            show werewolf shocked
            w "What in the-?! This is nasty!"
            w "Ugh... it... hurts..."
            show werewolf true form
            w "You... What... are you even planning?"
            call fade_scene
            $ char_choice_array.remove(1)
        else:
            if drink_result == 0:
                "Jakob takes a sip."
                show werewolf neutral
                w "Wow, man. This... tastes like nothing."
            elif drink_result == 1:
                "Jakob takes a sip."        
                show werewolf happy        
                w "There's somethin in there I really like, but everything else ain't that striking."
            elif drink_result == 2:
                "Jakob takes a sip."
                show werewolf neutral
                w "[ingredients[neutral_ingredient]]... is quite boring."
            elif drink_result == 4:
                "Jakob takes a sip."
                show werewolf angry
                w "Wow. This... tastes like nothing. But with a hint of yuck. Can't describe it in any other way, champ."
            else:
                show werewolf angry
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
                        w "bro wtf"
                        show doppel angry
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
            s "Um. I don’t mean to be rude but. Since this is a bar and all… Can you just like, make me a drink now?"
            return

        s "Ask away."

        label .questions:
            if sus_array[3] < 3:
                menu:
                    "Nice sweater!":
                        show selkie happy
                        s "Thank you! People always say I-I mean it, is wife material haha."
                        show selkie neutral
                        s "..."
                        b "..."
                        show selkie angry
                        s "Like...as a joke..."
                        s "Because it's so... warm?"
                        show selkie neutral
                        s "Um."
                        show selkie angry
                        s "This is a bar. Can I get my drink soon?"
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end   
                    "Do you have a flavor profile in mind?":
                        show selkie happy
                        s "Hmmm... I like warm flavors, and beachy vibes."
                        s "Like a cosy book you can't put down."
                        show selkie neutral
                        s "Spices are hard to come by, so I also really enjoy those."
                        jump .questions     # let player ask more questions after branch end   
                    "Do you have a favorite color?":
                        show selkie happy
                        s "Easy. Blue."
                        show selkie angry
                        s "It just feels like home..."
                        jump .questions     # let player ask more questions after branch end   
                    "Any flavors I should avoid?":
                        show selkie angry
                        s "Um... I don't like man-made artifical stuff I guess?"
                        b "...?"
                        s "Oh, that sounds strange! I just mean uh,"
                        show selkie neutral
                        s "Anything is fine! I don't have a preference!"
                        b "I see..."
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end   
                    "Read any good books lately?":
                        show selkie happy
                        s "Yes! I just came from the library actually."
                        s "I love romantasy! I just can't get enough of it."
                        show selkie angry
                        s "Though I will say... having the female lead be the monster is shocklingly difficult to find."
                        s "I'm really into Kiera Cass' stuff, even if it's a bit older."
                        s "and not... 100 percent the same, just close..."
                        show selkie neutral
                        s "Ah, sorry, I'm talking too much huh."
                        jump .questions     # let player ask more questions after branch end   
                    "How was the traffic today":
                        show selkie angry
                        s "Oh um, I couldn't tell you. I walked."
                        show selkie neutral
                        s "I don't come into the city super often, mostly just to visit the library."
                        show selkie happy
                        s "Books are so cool... it sucks that they have to be kept somewhere dry- I mean um. That they take up so much space!"
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end      

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
        s "Thank you..."
        $ set_drink_result_variables(served_drink, correct_drink[3], 3)

        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        if drink_result == 3:
            "Shelly takes a sip."
            show selkie shocked
            s "this seems goo- what have you done?"
            show selkie true form
            s "NOOOOOOOOO"
            $ char_choice_array.remove(3)
            call fade_scene
        else:
            if drink_result == 0:
                "Shelly takes a sip."
                show selkie angry
                s "I could’ve just had water and I’d feel less bored."
                show selkie shocked
                s "Wait did I say that outloud?? Sorry, I just uh, maybe try making something different next time?"
                s "bye!!"
            elif drink_result == 1:
                "Shelly takes a sip."
                show selkie happy
                s "Oh, that’s pretty nice. Good job!"
                show selkie angry
                s "Though maybe for next time... It could be a bit cosier?"
            elif drink_result == 2:
                "Shelly takes a sip."
                show selkie angry
                s "Huh. I like the start, but the finish is uh… bleh"
                s "Sorry, I'm sure you tried your best!"
            elif drink_result == 4:
                "Shelly takes a sip."
                show selkie angry
                s "Mm- mildy nasty... and boring at the same time?"
                show selkie neutral
                s "I don't know how you managed it!"
            else:
                show selkie angry
                s "...This looks… really nasty…"
                s "I’m not going to drink that…"
                "Looks like she didn't want to drink it at all. Try to add something she would like to mask the drink."

            $ has_visited[3] = True
            $ lives_count -= 1

            # parting goodbye lines
            s "It's just not as good as I thought it would be. I will take my leave now..."

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
    show fairy happy
    f "Just kidding!... Or am I?"

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
            f "Enough chatter. Make my drink already."
            return
            
        show fairy happy
        f "Talk about myself? Sure <3 <3"

        label .questions:
            if sus_array[5] < 3:
                menu:
                    "Interesting hair color!":
                        show fairy neutral
                        f "I change it every week."
                        show fairy happy
                        f "Last week's was green and yellow. Luckily, yellow is easy to dye over."
                        jump .questions     # let player ask more questions after branch end

                    "What flavors do you like?":
                        show fairy happy
                        f "Rich drinks! I want milk or half and half or something."
                        show fairy neutral
                        f "You really can't go wring with liquors either..."
                        jump .questions     # let player ask more questions after branch end

                    "Have any dietary restrictions?":
                        show fairy angry
                        f "I have an... unusual metal allergy"
                        show fairy neutral
                        f "I’ve never really had any issues with it at bars though!"
                        show fairy angry
                        f "Some fruit actually has enough of it to make me sick, so be a sweetheart and avoid tropical drinks."
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end

                    "What do you do for a living?":
                        show fairy neutral
                        f "I'm a youtuber actually!"
                        show fairy happy
                        f "I run a prank channel."
                        show fairy neutral
                        f "Don't worry, I'm not truman show-ing you right now."
                        show fairy happy
                        f "Totally."
                        jump .questions     # let player ask more questions after branch end

                    "You seem bored?":
                        show fairy angry
                        f "Not gonna lie, this club is kinda dead."
                        show fairy happy
                        f "I came here for nightlife! Action!! Parties!!!"
                        show fairy neutral
                        f "Whatever, if the drinks are good enough..."
                        show fairy happy
                        f "I can use my channel to really boost this place."
                        jump .questions     # let player ask more questions after branch end

                    "Can I have your real name?":
                        show fairy angry
                        f "...hm."
                        show fairy happy
                        f "Can I have yours?"
                        b "Afraid not."
                        show fairy angry
                        f "Boo, don't be so boring."
                        call .add_sus
                        jump .questions     # let player ask more questions after branch end

                    "Nevermind, I'm done asking questions.":
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
            show fairy angry
            f "WHAT- this is RANCID!!"
            f "YOU TRYING TO KILL ME OR SOMETH-"
            call fade_scene
            $ char_choice_array.remove(5)
        else:
            if drink_result == 0:
                show fairy angry
                f "Painfully average. I should’ve known better than to come to some no-name random bar like this"
            elif drink_result == 1:
                show fairy happy
                f "Painfully average. I should’ve known better than to come to some no-name random bar like this."
            elif drink_result == 2:
                show fairy neutral
                f "[ingredients[neutral_ingredient]]... is quite boring"
            elif drink_result == 4:
                show fairy angry
                f "Do you know me at all?? Boring and gross, what a miracle."
                f "I’m not coming back here, ugh"
            else:
                show fairy angry
                f "…Okay so you’re messing with me, great."
                f "Have a horrible night."
                "Looks like she didn't want to drink it at all. Try to add something she would like to mask the drink."

            $ has_visited[5] = True
            $ lives_count -= 1

            # parting goodbye lines
            f "See you around. Or not!"

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
    show doppel happy
    d "hiii I like whatever you like babygirl <3"

    if has_visited[7] == True:
        if sus_array[7] == 0:
            show doppel happy talk
            d "Hey, we've seen each other before!"
        else:
            show doppel neutral talk
            d "We've seen each other before..."

        # logic for decreasing sus by 1 upon revisiting
        if sus_array[7] != 0:
            d "...I might be open to talk a little again."
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

        show doppel happy
        d "Hmm~~~~ Anything you make it delicious~"
        "Yoru takes a sip from the drink."
        d "...Quite a funny taste."
        show doppel true form
        d "...I know what you're trying to do..."
        d "...Please, do with me what you have planned. I would love to see how this unfolds."
        call fade_scene
        $ char_choice_array.remove(7)
        # TO-DO: IMPLEMENT SPECIFIC DIALOGUE FOR PERSONALITY
        # drink result dialogue
        # if drink_result == 3:
        #     v "this seems goo- what have you done?"
        #     $ char_choice_array.remove(7)
        # else:
        #     if drink_result == 0:
        #         v "whole drink is forgettable"
        #     elif drink_result == 1:
        #         v "i like it, but its not memorable enough"
        #     elif drink_result == 2:
        #         v "[ingredients[neutral_ingredient]]... is quite boring"
        #     elif drink_result == 4:
        #         v "both forgettable and mildy disgusting..."
        #     else:
        #         v "this doesnt look good at all..."

        #     $ has_visited[7] = True
        #     $ lives_count -= 1

            # parting goodbye lines
            # v "Goodbye."

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
        "You lost!! Next time, try to make something both tasty AND deadly." # TO-DO: IMPLEMENT LOSE STATE
    else:
        "Hell yes. Now you can absorb their powers and become god. YOU WIN!!!" # TO-DO: IMPLEMENT WIN STATE     


return