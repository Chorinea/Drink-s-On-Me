image ing_0_img = "images/Ingredients/Bases/vodka_.png"
image ing_1_img = "images/Ingredients/Bases/whiskey_.png"
image ing_2_img = "images/Ingredients/Bases/bourbon_.png"
image ing_3_img = "images/Ingredients/Bases/bluecuracao_.png" 
image ing_4_img = "images/Ingredients/Bases/sake_.png"
image ing_5_img = "images/Ingredients/Bases/amaretto_.png"
image ing_6_img = "images/Ingredients/Bases/wine_.png"
image ing_7_img = "images/Ingredients/Bases/gin_.png"
image ing_8_img = "images/Ingredients/Bases/tequila_.png"
image ing_9_img = "images/Ingredients/Bases/brandy_.png"
image ing_10_img = "images/Ingredients/Bases/tomato_.png"
image ing_11_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_11_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_12_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_13_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_14_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_15_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_16_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_17_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_18_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_19_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_20_img = Solid("#173c54", xsize=160, ysize=200)
image ing_21_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_22_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_23_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_24_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_25_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_26_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_27_img = Solid("#aaddff", xsize=160, ysize=200) 
image ing_28_img = Solid("#aaddff", xsize=160, ysize=200)
image ing_29_img = Solid("#aaddff", xsize=160, ysize=200) 

default selected_ingredients = []
    
define ingredient_descriptions = [
    "Vodka: A clear spirit, strong and classic.",
    "Whiskey: Smooth and rich. For the rough nights.", 
    "Bourbon: A full-bodied whiskey with a sweet, vanilla flavor.",
    "Blue Curacao: Deep blue liqueur with a hint of orange flavor. Great for a tropical feel.",
    "Sake: A Japanese rice wine with a delicate, subtle flavor.",
    "Amaretto: Nutty and creamy flavor. Sourced from almonds. Lots of almonds.",
    "Wine: Not aged very long. Quite tacky and cheap flavor profile.",
    "Gin: A botanical spirit with a distinctive juniper flavor.",
    "Tequila: Great for shots! Shots! Shots! But also good for mixing.",
    "Brandy: A distilled spirit made from fermented fruit juice.",
    "Tomato: Red and juicy. Definitely a fruit.",
    "Monkshood: An herb that is described in Parry Hotter. ...I wonder what the other name for this is?",
    "Powdered Green Dust: Glowing and mysterious. Extremely radioative... or at least Superman says so.",
    "Plastic: Great for the planet, and great in drinks!",
    "Blue Raspberry Swirl: Sweet and colorful. The red-blue swirls are beautifully entangled together.",
    "Milk: Simple. Good for mixing. Good for drinking. Good for cereal.",
    "Glitter: OOOHHHH SPARKLY! And its edible!",
    "Simple Syrup: Ol' reliable for adding sweetness to any drink.",
    "Generic Energy Drink: We were gonna call it Blue Heifer but it didn't roll off the tongue that well.",
    "Grenadine: A sweet, red syrup used in cocktails.",
    "Garlic: The fancier cousin of the onion.",
    "Silver Spoon: Well obviously don't drink the spoon. ...Seems the coating is slightly flaking off.",
    "Unbranded and Totally Non-Descript Peanut Butter and Chocolate Pieces: Copyright free and majorly sweet!!",
    "Cinnamon: A warm and cozy addition to any drink.",
    "Salt: A nice salt rim enhances the drinking experience.",
    "Lemon: Sour. And Yellow.",
    "Mirror Shards: Sharp and reflective. Not recommended for human consumption.",
    "Sage: Not like the wise old man. More like the herb. But also wise.",
    "Blood: Who's is it? ...Best not to ask questions.",
    "Mint: Fresh and a bit spicy.",
    ]

# helper function for removing item from selection box
init python:
    def remove_ingredient(lst, index):
        if index < len(lst):
            lst.pop(index)

init python:
    import random
    
    # Creates a randomized order of 0-29 once when the game starts
    def randomized_shelf():
        items = list(range(30))
        random.shuffle(items)
        return items

default shelf_indices = randomized_shelf()      # for shuffling items on shelf


label make_drink:

    call screen minigame_screen

    return

screen minigame_screen():
    add "images/drink_minigame_bg.png"
    default hovered_box_index = None
    default hovered_shelf_item = None
                
    # top row
    hbox:
        xalign 0.5
        ypos 100
        spacing 10

        for item in shelf_indices[0:10]:
            if item in selected_ingredients:
                null width 160 height 200
            else:
                imagebutton:
                    idle Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200))
                    xpos 0
                    ypos 10
                    hover Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200), zoom=1.1)

                    sensitive len(selected_ingredients) < 3     # can only click if ingredients not fully selected yet

                    action Function(lambda itm=item: selected_ingredients.append(itm))  

                    tooltip ingredient_descriptions[item]

    # middle row
    hbox:
        xalign 0.5
        ypos 300
        spacing 10

        # middle row
        for item in shelf_indices[10:20]:
            if item in selected_ingredients:
                null width 160 height 200
            else:
                imagebutton:
                    idle Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200))
                    xpos 0
                    ypos 50
                    hover Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200), zoom=1.1)

                    sensitive len(selected_ingredients) < 3     # can only click if ingredients not fully selected yet

                    action Function(lambda itm=item: selected_ingredients.append(itm))  

                    tooltip ingredient_descriptions[item]

    # bottom row
    hbox:
        xalign 0.5
        ypos 500
        spacing 10

        for item in shelf_indices[20:30]:
            if item in selected_ingredients:
                null width 160 height 200
            else:
                imagebutton:
                    idle Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200)) 
                    xpos 0
                    ypos 100
                    hover Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200), zoom=1.1)

                    sensitive len(selected_ingredients) < 3     # can only click if ingredients not fully selected yet

                    action Function(lambda itm=item: selected_ingredients.append(itm))  
                    
                    tooltip ingredient_descriptions[item]

    # on hover tooltip
    $ current_tooltip = GetTooltip()
    
    if current_tooltip:
        frame:
            xalign 0.5
            ypos 400
            padding (20, 10)
            background Solid("#000000cc")

            text "[current_tooltip]" size 24 color "#ffffff"

    # selected ingredients box
    frame:
        xalign 0.95 ypos 800
        xsize 700 ysize 225
        background Solid("#dfdfefc9")
        padding (30, 30)

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            for i, item in enumerate(selected_ingredients):
                button:
                    action Function(remove_ingredient, selected_ingredients, i)

                    hovered SetScreenVariable("hovered_box_index", i)
                    unhovered SetScreenVariable("hovered_box_index", None)

                    fixed:
                        xsize 160 ysize 200

                        add Transform("ing_%d_img" % item, fit="scale-down", xysize=(160, 200))
                        
                        if hovered_box_index == i:
                            text "X" size 40 color "#ff0000" xalign 0.5 yalign 0.5

    # serve
    if len(selected_ingredients) == 3:
        textbutton "Mix & Serve!":
            xalign 0.5
            yalign 0.85
            padding (20, 15)
            background Solid("#ff5555")
            hover_background Solid("#ff7777")
            text_color "#ffffff"
            text_size 24
            
            # Action to take when they click serve (e.g., jump to your mixing label)
            action [
                SetVariable("served_drink", selected_ingredients),
                SetVariable("selected_ingredients", []),  # Clear the selection after serving
                Return("True")
            ]

