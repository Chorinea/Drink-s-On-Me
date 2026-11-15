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

image sue = Placeholder("bg")


#init python:
    #def DisplayNotebook():
        #
       
label start2:
    show sue

#write function