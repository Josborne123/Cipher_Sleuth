# Notes
"""
To delete everything from the userData table - DELETE FROM userData;
To reset the AUTO_INCREMENT - ALTER TABLE userData AUTO_INCREMENT = 1;
Select all data - SELECT * FROM userData;
"""

# Importing Modules
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
import mysql.connector as mysql


# Main Program
window = customtkinter.CTk()  # Creating main app window
window.geometry('800x600')  # Setting window size
window.title("Cipher Sleuth - Start Screen")  # Setting the title
window.resizable(width=False, height=False) # Not allowing the window to be resized
customtkinter.set_appearance_mode("dark")

# Setting the background images
background_image = customtkinter.CTkImage(light_image=Image.open("Images/background-light.jpg"), dark_image=Image.open("Images/background-dark.jpg"), size=(800,600))
backgroundImage_label = customtkinter.CTkLabel(window, image=background_image, text="")
backgroundImage_label.place(relx=0,rely=0)

def startScreen():

    info_frame = customtkinter.CTkFrame(window, width=650, height=475)
    info_frame.place(relx=0.08125,rely=0.0792)


    def change_themes():
        # Function which changes the theme / appearance of the program depending on the state of theme_button 
        theme = theme_button.cget("textvariable")

        if theme == "dark":
            theme_button.configure(image=light_mode)
            theme_button.configure(textvariable=light)
            customtkinter.set_appearance_mode("light")


        elif theme =="light":
            theme_button.configure(image=dark_mode)
            theme_button.configure(textvariable=dark)
            customtkinter.set_appearance_mode("dark")


    light_mode = customtkinter.CTkImage(light_image=Image.open("Images/light-mode.png")) # Creating and storing the light mode image
    dark_mode = customtkinter.CTkImage(dark_image=Image.open("Images/night-mode.png")) # Creating and storing the dark mode image

    dark = "dark"
    light = "light"

    theme_button = customtkinter.CTkButton(info_frame, image=dark_mode, command=change_themes, text="", width=10, textvariable=dark) # Creating the theme button
    theme_button.place(relx=0.920, rely=0.06) # Placing the theme button on the screen 

    #Note: Fonts aren't / don't work in Replit
    title_label = customtkinter.CTkLabel(info_frame, text="Cipher Sleuth", font=("Comic Sans MS bold", 40), fg_color=("#dbdbdb", "#2b2b2b"))
    title_label.place(relx=0.5, rely=0.08, anchor="center")



    instructions_frame = customtkinter.CTkFrame(info_frame, width=600, height=175) # Creating a frame, where the instructions will go
    instructions_frame.place(relx=0.05, rely=0.2)

    instructions_textbox = customtkinter.CTkTextbox(instructions_frame, font=("Comic Sans MS", 16), width=600, wrap="word", padx=10, pady=10, fg_color=("#dbdbdb", "#2b2b2b"), activate_scrollbars=False) # Create the textbox which will contain the instructions
    instructions_textbox.place(relx=0,rely=0)
    instructions_textbox.insert("0.0", "Once you choose a level, you will be presented with 3 encrypted messages and your challenge is to decipher them.\n\nYou only have 3 lives and are allowed to request a maximum of 3 hints, however be warned as using hints will effect your final score.\n\nThere is no time limit, so go ahead and play.")
    instructions_textbox.configure(state="disabled") # Configuring the textbox so that it is read-only

    def minimize_main(): # Function to minimize main window
        window.wm_state('iconic')


    chooseLevel_label = customtkinter.CTkLabel(info_frame, text="Choose level", font=("Comic Sans MS bold", 30), fg_color=("#dbdbdb", "#2b2b2b"))
    chooseLevel_label.place(relx=0.5, rely=0.7, anchor="center")

    level1_button = customtkinter.CTkButton(info_frame, text="Level 1", command= lambda: [usernameScreen(level1), minimize_main()], fg_color="#32CD32", bg_color=("#dbdbdb", "#2b2b2b"), hover_color="#33A8FF", height=40, corner_radius=15) # Creating button for level 1
    level1_button.place(relx=0.07, rely=0.8)

    level2_button = customtkinter.CTkButton(info_frame, text="Level 2", command= lambda: [usernameScreen(level2), minimize_main()], fg_color="#FF8A33", bg_color=("#dbdbdb", "#2b2b2b"), hover_color="#33A8FF", height=40, corner_radius=15) # Creating button for level 2
    level2_button.place(relx=0.4, rely=0.8)

    level3_button = customtkinter.CTkButton(info_frame, text="Level 3", command= lambda: [usernameScreen(level3), minimize_main()], fg_color="#E40202", bg_color=("#dbdbdb", "#2b2b2b"), hover_color="#33A8FF", height=40, corner_radius=15) # Creating button for level 3
    level3_button.place(relx=0.73, rely=0.8)


def usernameScreen(level):

    def storeUsername(userUsername):
        level()
        db = mysql.connect( # Connecting to database
            host = "localhost",
            user = "root",
            passwd = "johnsql123",
            database = "CipherUserData"
        )

        cursor = db.cursor() 
        cursor.execute("INSERT INTO userData (username) VALUES (%s)", (userUsername,))
        db.commit() # Saving username to database
        db.close() # Closing the connection
        usernameScreen_window.destroy() # Closing username window


    def validateUsername(): # Validating Username function
        global userUsername 
        userUsername = usernameEntry_entry.get() 

        db = mysql.connect( # Connecting to database
            host = "localhost",
            user = "root",
            passwd = "johnsql123",
            database = "CipherUserData"
        )

        cursor = db.cursor()
        cursor.execute("SELECT username FROM userData")
        results = cursor.fetchall() 
        userNameArray = []
        for i in results:
            userNameArray.append(i[0])

        if userUsername in userNameArray: # If username is taken, tell the user to re-enter
            invalidUsername_label = customtkinter.CTkLabel(usernameScreen_window, text="Username already taken. Please enter another.", font=("Comic Sans MS", 17), fg_color=("#EBEBEA", "#252424"))
            invalidUsername_label.place(relx=0.5, rely=0.75, anchor="center")            
        
        elif userUsername not in userNameArray:
            storeUsername(userUsername) # If the username is valid (not already taken) then call the function to store it in the database

        db.close()


    usernameScreen_window = customtkinter.CTkToplevel(window)
    usernameScreen_window.geometry('400x200')
    usernameScreen_window.title("Enter Username")

    enterUsername_label = customtkinter.CTkLabel(usernameScreen_window, text="Enter Username:", font=("Comic Sans MS bold", 30), fg_color=("#EBEBEA", "#252424"))
    enterUsername_label.place(relx=0.5, rely=0.15, anchor="center")

    usernameEntry_entry = customtkinter.CTkEntry(usernameScreen_window, width=200, height=50, font=("Comic Sans MS", 15))
    usernameEntry_entry.place(relx=0.5, rely=0.5, anchor="center")
 
    usernameEntry_entry.bind("<Return>", (lambda event: validateUsername())) # When enter button is the username will be validated
    

def level1():
    level1_window = customtkinter.CTkToplevel(window) # Creating level 1 window
    level1_window.geometry('800x600')
    level1_window.title("Cipher Sleuth - Level 1")

    caesarCipher_label = customtkinter.CTkLabel(level1_window, text="Level 1 - Caesar Cipher", font=("Comic Sans MS bold", 30), fg_color=("#EBEBEA", "#252424"))
    caesarCipher_label.place(relx=0.5, rely=0.075, anchor="center")


    line2_label = customtkinter.CTkLabel(level1_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.14, anchor="center")

    caesarCipherExplanation_label1 = customtkinter.CTkLabel(level1_window, text="This is an encryption method where each letter in a message is shifted by a fixed", font=("Comic Sans MS", 17), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label2 = customtkinter.CTkLabel(level1_window, text="number of positions in the alphabet For example with a shift of 3, A becomes D", font=("Comic Sans MS", 17), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label1.place(relx=0.1, rely=0.16)
    caesarCipherExplanation_label2.place(relx=0.1, rely=0.20)

    line2_label = customtkinter.CTkLabel(level1_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.265, anchor="center")

    
def level2():
    level2_window = customtkinter.CTkToplevel(window) # Creating level 2 window
    level2_window.geometry('800x600')
    level2_window.title("Cipher Sleuth - Level 2") 


def level3():
    level3_window = customtkinter.CTkToplevel(window) # Creating level 3 window
    level3_window.geometry('800x600')
    level3_window.title("Cipher Sleuth - Level 3") 


startScreen()
window.mainloop()  # Starting the program





# Code for the level1 window which i have temporarly removed
#### The block of code below is causing an error when entering the username ####
#caesarCipherExplanation = customtkinter.CTkTextbox(level1_window, font=("Comic Sans MS", 16), width=600, wrap="word", padx=10, pady=10, fg_color=("#dbdbdb", "#2b2b2b"), activate_scrollbars=False)
#caesarCipherExplanation.place(relx=0.1, rel=0.2)
#caesarCipherExplanation.insert("0.0", "Instructions ...")