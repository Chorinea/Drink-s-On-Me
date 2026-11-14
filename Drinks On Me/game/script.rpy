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

$chv_sus = 0

menu:
    "Aren't you a human?":
        v "Of course, what kind of question is that!"
        $ chv_sus -= 1
    "Me too man, me too":
        v "I like you... you have good sense."
        $ chv_sus += 1

return
