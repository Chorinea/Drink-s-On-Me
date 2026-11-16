# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.


#display notebook


screen notebook():
    key "n" action DisplayNotebook()
    frame:
        xalign 0.5 ypos 50
        vbox:
            text "screen"

    #if notebook

image notebook_neutral = "images/Notebook/notebook_sample.png"
#image profile_unknown = "images/Notebook/XXXx.png"
#image profile_vampire = "images/Notebook/XXXx.png"
#image profile_werewolf = "images/Notebook/XXXx.png"
#image profile_alien = "images/Notebook/XXXx.png"
#image profile_selkie = "images/Notebook/XXXx.png"
#image profile_ghost = "images/Notebook/XXXx.png"
#image profile_fairy = "images/Notebook/XXXx.png"
#image profile_medusa = "images/Notebook/XXXx.png"
#image profile_doppel = "images/Notebook/XXXx.png"


#init python:
    #def DisplayNotebook():
        #


define notebook_tabs = [0,1,2,3,4,5,6,7] #turn the character profile
#define profile_met = [-1,-1,-1,-1,-1,-1,-1,-1] #-1 = not met; 1 = met them; it matches the character array
#instead use has_visited.. (in script)

define ingredients_known = [ #displays the ingredients on the page per character
    # B, M, T
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1]
]
define character_facts = [ #displays the facts found for each question asked
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1]
]
#if killed reveals the monster in the notebook & facts about it

#making a layer displayable
#detached layer holds the contents of the profile
#define config.detached_layers += ["profile"]
#image profile = Window(Layer("profile"), etc)
init python:
    def set_ingredients_known(correct_drink_array,char_num):
        
        character_reciepe = []
        while ingredient_num > 3:
            #gets the ingredient number from the array from the right character
            ingredient_num = correct_drink_array[[char_num]]
            
        
        
        ingredient_pos = [0,1,2]



        # add dislikes to array
        liked_ingredient = correct_drink_array[likes_pos[char_num]]
        #disliked_ingredients = 

        for ingredient in correct_drink_array:
            if ingredient != liked_ingredient:
                disliked_ingredients.append(ingredient)

        # if liked ingredient is in drink array
        if liked_ingredient in drink_array:
            result_count[0] = 1
            drink_array.remove(liked_ingredient)


    def check_if_met():
        display_profile = 0
        if has_visited[0] == True:
            display_profile = 1

            if question_asked:
                display_questions

            



label DisplayNotebook:
    show notebook_neutral

#write function