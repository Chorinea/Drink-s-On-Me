# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define v = Character("customer")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show vamphappy

    # These display lines of dialogue.

    v "Hi I like drinking things."

    v "Things that are. not blood."

    "I'm feeling especially human today y'know?"

    "something about being a bartender I guess..."

    show vampunhappy
    
    v "Ew I dislike humans."

$chv_sus = 5

menu:
    "Aren't you a human?":
        v "Of course, what kind of question is that!"
        $ chv_sus += 2
    "Me too man, me too":
        show vamphappy
        v "I like you... you have good sense."
        $ chv_sus -= 2


label stats:
    "The customer's suspicion of you is at [chv_sus]. The less suspicious they are, the longer you can talk to them."

    show vamphappy

    v "I'm here for a human drink. Got any reccomendations? It's been a while since I've been outside."

menu:
     "Actually, I'd like to ask some questions to get your tastes.":
        v "This would lead into a menu of questions with different effects on suspicion. If I had the time."
     "Yes, I'll make you a bloody mary!":
        show vampunhappy
        v "Bleh I'm gonna die because you put garlic in it"
     "Yes, I'll make you a strawberry daiquiri!":
        v "Wow way too sweet. I'm never coming back here."
return
