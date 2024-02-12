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
import random
from wonderwords import RandomSentence, RandomWord
from dataclasses import dataclass

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

score = 1000 # Setting the initial Score

def startScreen():

    # Setting up the information frame
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



    instructions_frame = customtkinter.CTkFrame(info_frame, width=600, height=200) # Creating a frame, where the instructions will go
    instructions_frame.place(relx=0.05, rely=0.2)

    instructions_textbox = customtkinter.CTkTextbox(instructions_frame, font=("Comic Sans MS", 16), width=600, wrap="word", fg_color=("#dbdbdb", "#2b2b2b"), activate_scrollbars=False) # Create the textbox which will contain the instructions
    instructions_textbox.place(relx=0,rely=0)
    instructions_textbox.insert("0.0", "Once you choose a level, you will be presented with 3 encrypted messages and your challenge is to decipher them.\n\nYou have unlimited lives and are allowed to request a maximum of 3 hints, however be warned as using hints and getting questions wrong will effect your final score.\n\nThere is no time limit, so go ahead and play.")
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
        cursor.execute("SELECT username FROM userData") # Running the shown query
        results = cursor.fetchall() # Storing the results
        userNameArray = []
        for i in results:
            userNameArray.append(i[0]) # Looping through the results and storing them in an array

        if userUsername in userNameArray: # If username is taken, tell the user to re-enter
            invalidUsername_label = customtkinter.CTkLabel(usernameScreen_window, text="Username already taken. Please enter another.", font=("Comic Sans MS", 17), fg_color=("#EBEBEA", "#252424"))
            invalidUsername_label.place(relx=0.5, rely=0.75, anchor="center")            
        
        elif userUsername not in userNameArray:
            storeUsername(userUsername) # If the username is valid (not already taken) then call the function to store it in the database

        db.close() # Closing database connection


    # Setting up the username screen window
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
    level1_window.geometry('1000x800')
    level1_window.title("Cipher Sleuth - Level 1")

    sentenceObj = RandomSentence()
    wordObj = RandomWord()
    unencryptedMessage1 = wordObj.word() # Generating a random word
    unencryptedMessage2 = sentenceObj.simple_sentence() # Generating a random sentence
    unencryptedMessage3 = sentenceObj.sentence() # Gererating a random more complex sentence 

    def caesarCipher(message): # Function which will encrypt the generate word / sentence using the Caesar Cipher
        shift = random.randint(1,26)
        encryptedMessage = []
        for word in message.split():
            encryptedWord = ""
            for char in word:
                if char.isalpha():
                    offset = ord('a') if char.islower() else ord('A')
                    encryptedWord += chr((ord(char) - offset + shift) % 26 + offset)
                else:
                    encryptedWord += char
            encryptedMessage.append(encryptedWord)


        encryptedMessage = ' '.join(encryptedMessage)
        return encryptedMessage, shift # Returning the encrypted message and shift used
    
    # Calling the caesarCipher procedure using the generated unencrypted messages and then storing the encrypted message and shift used
    encryptedSentence1, shiftM1 = caesarCipher(unencryptedMessage1)
    encryptedSentence2, shiftM2 = caesarCipher(unencryptedMessage2)
    encryptedSentence3, shiftM3 = caesarCipher(unencryptedMessage3)

    # Creating score label
    score_label = customtkinter.CTkLabel(level1_window, text="Score: 0", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    score_label.place(relx=0.95, rely=0.025, anchor="e")

    # Creating heading label
    caesarCipher_label = customtkinter.CTkLabel(level1_window, text="Level 1 - Caesar Cipher", font=("Comic Sans MS bold", 30), fg_color=("#EBEBEA", "#252424"))
    caesarCipher_label.place(relx=0.5, rely=0.05, anchor="center")

    # Creating a label to seperate elements on the screen
    line2_label = customtkinter.CTkLabel(level1_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.1, anchor="center")

    # Creating labels to explain the cipher
    caesarCipherExplanation_label1 = customtkinter.CTkLabel(level1_window, text="This is an encryption method where each letter in a message is shifted backwards by ", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label1.place(relx=0.15, rely=0.125)

    caesarCipherExplanation_label2 = customtkinter.CTkLabel(level1_window, text="a fixed number of positions in the alphabet. For example with a shift of 3, D becomes A", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label2.place(relx=0.15, rely=0.175)

    # Creating a label to seperate elements on the screen
    line2_label = customtkinter.CTkLabel(level1_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.23, anchor="center")

    # creating a label to display the alphabet
    alphabet_label = customtkinter.CTkLabel(level1_window, text="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    alphabet_label.place(relx=0.25, rely=0.25)

    # Creating label to display first encrypted message
    encryptedMessage1_label = customtkinter.CTkLabel(level1_window, text=f"Encrypted Message 1 - {encryptedSentence1}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage1_label.place(relx=0.1, rely=0.3)

    # Creating an entry where the user will enter their answer
    userDecrypt1_entry = customtkinter.CTkEntry(level1_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt1_entry.place(relx=0.325, rely=0.375)

    # Creating label to display second encrypted message
    encryptedMessage2_label = customtkinter.CTkLabel(level1_window, text=f"Encrypted Message 2 - {encryptedSentence2}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage2_label.place(relx=0.1, rely=0.5)

    # Creating an entry where the user will enter their answer
    userDecrypt2_entry = customtkinter.CTkEntry(level1_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt2_entry.place(relx=0.325, rely=0.575)

    # Creating label to display third encrypted message
    encryptedMessage3_label = customtkinter.CTkLabel(level1_window, text=f"Encrypted Message 3 - {encryptedSentence3}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage3_label.place(relx=0.1, rely=0.7)

    # Creating an entry where the user will enter their answer
    userDecrypt3_entry = customtkinter.CTkEntry(level1_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt3_entry.place(relx=0.325, rely=0.775)

    # Creating 3 buttons to check the user's answer and then call the relevant check procedure
    checkMessage1_button = customtkinter.CTkButton(level1_window, text="Check", command= lambda: checkAnswer1(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage1_button.place(relx=0.685, rely=0.375)

    checkMessage2_button = customtkinter.CTkButton(level1_window, text="Check", command= lambda: checkAnswer2(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage2_button.place(relx=0.685, rely=0.575)
    
    checkMessage3_button = customtkinter.CTkButton(level1_window, text="Check", command= lambda: checkAnswer3(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage3_button.place(relx=0.685, rely=0.775)

    # Creating 3 buttons which will allow hte user to request a hint
    hint1_button = customtkinter.CTkButton(level1_window, text="Hint", command = lambda: [requestHint1(), updateScoreHint()], font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#CD32CD", hover_color="#33A8FF")
    hint1_button.place(relx=0.775, rely=0.375)

    hint2_button = customtkinter.CTkButton(level1_window, text="Hint", command = lambda: [requestHint2(), updateScoreHint()], font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#CD32CD", hover_color="#33A8FF")
    hint2_button.place(relx=0.775, rely=0.575)

    hint3_button = customtkinter.CTkButton(level1_window, text="Hint", command = lambda: [requestHint3(), updateScoreHint()], font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#CD32CD", hover_color="#33A8FF")
    hint3_button.place(relx=0.775, rely=0.775)

    def updateScoreHint(): # If the user uses a hint this function will be called and divide their current score by 5
        global score
        score = score / 5

    def updateScoreLabel(score): # Updating the user's score onto the screen
        score_label.configure(text=f"Score: {int(score)}")


    # The following 3 procedures will display a hint to the user by telling them the shift of the encryption
    def requestHint1(): 
        encryptedMessage1_label.configure(text=f"Encrypted Message 1 - {encryptedSentence1} - Hint: Shifted by {shiftM1}")
        hint1_button.place_forget()
    
    def requestHint2():
        encryptedMessage2_label.configure(text=f"Encrypted Message 2 - {encryptedSentence2} - Hint: Shifted by {shiftM2}")
        hint2_button.place_forget()

    def requestHint3():
        encryptedMessage3_label.configure(text=f"Encrypted Message 3 - {encryptedSentence3} - Hint: Shifted by {shiftM3}")
        hint3_button.place_forget()

    # If the user guesses wrong then this label will display
    incorrect_label = customtkinter.CTkLabel(level1_window, text="Incorrect, try again!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))

    # Following 3 procedures will check if the user's guess is correct
    def checkAnswer1():
        userDecrypt1 = userDecrypt1_entry.get() # Storing the user's guess in a variable
        if userDecrypt1 == unencryptedMessage1: # If the user's answer is correct
            checkMessage1_button.place_forget() # Remove the "Check" button
            hint1_button.place_forget() # Remove the "hint" button
            correct_label = customtkinter.CTkLabel(level1_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424")) # Display correct to the screen
            correct_label.place(relx=0.685, rely=0.375)
            global score
            score += 1000 # Update score
            updateScoreLabel(score)
            incorrect_label.place_forget() # Remove incorrect label if it is displayed.
        else: # If user is not correct
            incorrect_label.place(relx=0.425, rely=0.415) # Display incorrect label
            score = score / 5 # Update score
            updateScoreLabel(score)


    def checkAnswer2():
        userDecrypt2 = userDecrypt2_entry.get()
        if userDecrypt2 == unencryptedMessage2:
            checkMessage2_button.place_forget()
            hint2_button.place_forget()
            correct_label = customtkinter.CTkLabel(level1_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
            correct_label.place(relx=0.685, rely=0.575)
            global score
            score += 2000
            updateScoreLabel(score)
            incorrect_label.place_forget()
        else:
            incorrect_label.place(relx=0.425, rely=0.615)
            score = score / 5
            updateScoreLabel(score)


    def checkAnswer3():
        userDecrypt3 = userDecrypt3_entry.get()
        if userDecrypt3 == unencryptedMessage3:
            checkMessage3_button.place_forget()
            hint3_button.place_forget()
            correct_label = customtkinter.CTkLabel(level1_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
            correct_label.place(relx=0.685, rely=0.775)
            global score
            score += 3000
            updateScoreLabel(score)
            incorrect_label.place_forget()
        else:
            incorrect_label.place(relx=0.425, rely=0.815)
            score = score / 5
            updateScoreLabel(score)

    # Button for when the user has finished, once clicked it will call the saveSCore() procedure
    finished_button = customtkinter.CTkButton(level1_window, text="Finished?", command=lambda: saveScore(), font=("Comic Sans MS", 18), width=175, height=50, corner_radius=15, fg_color="#e8a717", hover_color="#33A8FF")
    finished_button.place(relx=0.5, rely=0.9, anchor="center")

    def saveScore():
        global userUsername 
        global score
        db = mysql.connect( # Connecting to database
            host = "localhost",
            user = "root",
            passwd = "johnsql123",
            database = "CipherUserData"
        )

        cursor = db.cursor()
        sql_update = "UPDATE userData SET score = (%s) WHERE username = (%s)" # Query
        cursor.execute(sql_update, (score, userUsername)) # Executing query
        db.commit() # Saving username to database
        db.close() # Closing the connection

        level1_window.wm_state('iconic') # Hiding the level1 window
        leaderboard() # Calling the leaderboard screen 

def level2():
    # Setting up the level2_window
    level2_window = customtkinter.CTkToplevel(window)
    level2_window.geometry('1000x800')
    level2_window.title("Cipher Sleuth - Level 2") 

    # Creating score label
    score_label = customtkinter.CTkLabel(level2_window, text="Score: 0", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    score_label.place(relx=0.95, rely=0.025, anchor="e")

    # Creating heading label
    atbashCipher_label = customtkinter.CTkLabel(level2_window, text="Level 2 - Atbash Cipher", font=("Comic Sans MS bold", 30), fg_color=("#EBEBEA", "#252424"))
    atbashCipher_label.place(relx=0.5, rely=0.05, anchor="center")

    # Creating a label to divide elements on the screen
    line2_label = customtkinter.CTkLabel(level2_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.1, anchor="center")

    # Creating 2 labels to explain the cipher
    caesarCipherExplanation_label1 = customtkinter.CTkLabel(level2_window, text="This is a substitution cipher where each letter in the plaintext is replaced by its ", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label1.place(relx=0.15, rely=0.125)

    caesarCipherExplanation_label2 = customtkinter.CTkLabel(level2_window, text="reverse in the alphabet For example, 'A' becomes 'Z', 'B' becomes 'Y', and so on.", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
    caesarCipherExplanation_label2.place(relx=0.15, rely=0.175)

    line2_label = customtkinter.CTkLabel(level2_window, text="-------------------------", font=("Comic Sans MS bold", 23), fg_color=("#EBEBEA", "#252424"))
    line2_label.place(relx=0.5, rely=0.23, anchor="center")

    # Creating a label to display the alphabet
    alphabet_label = customtkinter.CTkLabel(level2_window, text="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    alphabet_label.place(relx=0.25, rely=0.25)


    def atbash_encrypt(text): # Function which will encrypt the generated word / sentence using the atbash cipher
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    encrypted_text += chr(90 - (ord(char) - 65))
                else:
                    encrypted_text += chr(122 - (ord(char) - 97))
            else:
                encrypted_text += char
        return encrypted_text
        
    sentenceObj = RandomSentence()
    wordObj = RandomWord()
    unencryptedMessage1 = wordObj.word() # Generating a random word
    unencryptedMessage2 = sentenceObj.simple_sentence() # Generating a random sentence
    unencryptedMessage3 = sentenceObj.sentence() # Generating a random more complex sentence

    # Calling the atbash_encrypt function and storing the encrypted messages
    encryptedMessage1 = atbash_encrypt(unencryptedMessage1)
    encryptedMessage2 = atbash_encrypt(unencryptedMessage2)
    encryptedMessage3 = atbash_encrypt(unencryptedMessage3)
 
    # Creating label to display encrypted message 1
    encryptedMessage1_label = customtkinter.CTkLabel(level2_window, text=f"Encrypted Message 1 - {encryptedMessage1}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage1_label.place(relx=0.1, rely=0.3)

    # Creating entry space for user's answer
    userDecrypt1_entry = customtkinter.CTkEntry(level2_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt1_entry.place(relx=0.325, rely=0.375)

    # Creating label to display encrypted messsage 2
    encryptedMessage2_label = customtkinter.CTkLabel(level2_window, text=f"Encrypted Message 2 - {encryptedMessage2}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage2_label.place(relx=0.1, rely=0.5)

    # Creating entry space for the user's answer
    userDecrypt2_entry = customtkinter.CTkEntry(level2_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt2_entry.place(relx=0.325, rely=0.575)

    # Creating label to display encrypted message 3
    encryptedMessage3_label = customtkinter.CTkLabel(level2_window, text=f"Encrypted Message 3 - {encryptedMessage3}", font=("Comic Sans MS", 20), fg_color=("#EBEBEA", "#252424"))
    encryptedMessage3_label.place(relx=0.1, rely=0.7)

    # Creating entry space for the user's answer
    userDecrypt3_entry = customtkinter.CTkEntry(level2_window, width=350, height=30, font=("Comic Sans MS", 16))
    userDecrypt3_entry.place(relx=0.325, rely=0.775)

    # Creating 3 buttons to check the answer and calling the relevation procedure
    checkMessage1_button = customtkinter.CTkButton(level2_window, text="Check", command= lambda: checkAnswer1(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage1_button.place(relx=0.685, rely=0.375)

    checkMessage2_button = customtkinter.CTkButton(level2_window, text="Check", command= lambda: checkAnswer2(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage2_button.place(relx=0.685, rely=0.575)
    
    checkMessage3_button = customtkinter.CTkButton(level2_window, text="Check", command= lambda: checkAnswer3(), font=("Comic Sans MS", 18), width=30, height=28, corner_radius=15, fg_color="#32CD32", hover_color="#33A8FF")
    checkMessage3_button.place(relx=0.685, rely=0.775)

    def updateScoreLabel(score): # Update score to screen
        score_label.configure(text=f"Score: {int(score)}")

    # If the user guesses wrong then this label will display
    incorrect_label = customtkinter.CTkLabel(level2_window, text="Incorrect, try again!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))

    # Following 3 procedures will check if the user's guess is correct
    def checkAnswer1():
        userDecrypt1 = userDecrypt1_entry.get() # Storing the user's guess in a variable
        if userDecrypt1 == unencryptedMessage1: # If the user is correct
            checkMessage1_button.place_forget() # Remove the "Check" button
            correct_label = customtkinter.CTkLabel(level2_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424")) # Display correct to the screen
            correct_label.place(relx=0.685, rely=0.375)
            global score
            score += 1500 # Update score
            updateScoreLabel(score)
            incorrect_label.place_forget()
        else: # If user is not correct
            incorrect_label.place(relx=0.425, rely=0.415) # Display incorrect label
            score = score / 5 # Update score
            updateScoreLabel(score)


    def checkAnswer2():
        userDecrypt2 = userDecrypt2_entry.get()
        if userDecrypt2 == unencryptedMessage2:
            checkMessage2_button.place_forget()
            correct_label = customtkinter.CTkLabel(level2_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
            correct_label.place(relx=0.685, rely=0.575)
            global score
            score += 2500
            updateScoreLabel(score)
            incorrect_label.place_forget()
        else:
            incorrect_label.place(relx=0.425, rely=0.615)
            score = score / 5
            updateScoreLabel(score)


    def checkAnswer3():
        userDecrypt3 = userDecrypt3_entry.get()
        if userDecrypt3 == unencryptedMessage3:
            checkMessage3_button.place_forget()
            correct_label = customtkinter.CTkLabel(level2_window, text="Correct!", font=("Comic Sans MS", 18), fg_color=("#EBEBEA", "#252424"))
            correct_label.place(relx=0.685, rely=0.775)
            global score
            score += 3500
            updateScoreLabel(score)
            incorrect_label.place_forget()
        else:
            incorrect_label.place(relx=0.425, rely=0.815)
            score = score / 5
            updateScoreLabel(score)


    # Creating button for when user is finished, once clicked it will call the saveScore() procedure
    finished_button = customtkinter.CTkButton(level2_window, text="Finished?", command=lambda: saveScore(), font=("Comic Sans MS", 18), width=175, height=50, corner_radius=15, fg_color="#e8a717", hover_color="#33A8FF")
    finished_button.place(relx=0.5, rely=0.9, anchor="center")

    def saveScore():
        global userUsername 
        global score
        db = mysql.connect( # Connecting to database
            host = "localhost",
            user = "root",
            passwd = "johnsql123",
            database = "CipherUserData"
        )

        cursor = db.cursor()
        sql_update = "UPDATE userData SET score = (%s) WHERE username = (%s)" # Query
        cursor.execute(sql_update, (score, userUsername)) # Executing query
        db.commit() # Saving username to database
        db.close() # Closing the connection

        level2_window.wm_state('iconic') # Hiding the level2_window
        leaderboard() # Calling leaderboard() module



def level3():
    level3_window = customtkinter.CTkToplevel(window) # Creating level 3 window
    level3_window.geometry('1000x800')
    level3_window.title("Cipher Sleuth - Level 3") 


def leaderboard():
    # Setting up the leaderboard window
    leaderboard_window = customtkinter.CTkToplevel(window)
    leaderboard_window.geometry('800x600')
    leaderboard_window.title("Leaderboard")

    # Creating title label
    title_label = customtkinter.CTkLabel(leaderboard_window, text="Leaderboard", font=("Comic Sans MS bold", 40), fg_color=("#EBEBEB", "#2b2b2b"))
    title_label.place(relx=0.5, rely=0.08, anchor="center")

    db = mysql.connect( # Connecting to database
        host = "localhost",
        user = "root",
        passwd = "johnsql123",
        database = "CipherUserData"
    )

    cursor = db.cursor()
    cursor.execute("SELECT username, score FROM userData ORDER BY score DESC, username") # Executing the written query
    results = cursor.fetchall() # Getting the results

    @dataclass
    class userLeaderboardData: # Creating an array of records
        username: str
        score: int

    leaderboardArray = [] # Setting up empty array 

    for i in results: # Storing the results in an array of records
        username = i[0]
        score = i[1]
        leaderboardArray.append(userLeaderboardData(username,score))

    db.close() # Closing connection to the database

    
    global userUsername

    # Note on this binary search
    # I don't know the number exactly but when the database contains too many entries the binary search doesn't work for some reason 

    # Binary Search Algorithm to find the position of the current user
    position = 0
    target = userUsername
    found = False
    lower_pointer = 0
    upper_pointer = len(leaderboardArray)

    while(found != True) and (lower_pointer <= upper_pointer):
        mid_pointer = int((lower_pointer + upper_pointer)/2)
        if(leaderboardArray[mid_pointer].username == target):
            found = True
            position = mid_pointer
        elif(leaderboardArray[mid_pointer].username < target):
            lower_pointer = mid_pointer + 1
        else:
            upper_pointer = mid_pointer - 1

    position += 1

    # Creating 10 labels to display the top 10 players

    firstplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"1     {leaderboardArray[0].username}     {leaderboardArray[0].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    firstplace_label.place(relx=0.5, rely=0.2, anchor="center")
    
    secondplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"2     {leaderboardArray[1].username}     {leaderboardArray[1].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    secondplace_label.place(relx=0.1, rely=0.3, anchor="w")

    thirdplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"3     {leaderboardArray[2].username}     {leaderboardArray[2].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    thirdplace_label.place(relx=0.9, rely=0.3, anchor="e")

    fourthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"4     {leaderboardArray[3].username}     {leaderboardArray[3].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    fourthplace_label.place(relx=0.5, rely=0.375, anchor="center")

    fifthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"5     {leaderboardArray[4].username}     {leaderboardArray[4].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    fifthplace_label.place(relx=0.5, rely=0.45, anchor="center")

    sixthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"6     {leaderboardArray[5].username}     {leaderboardArray[5].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    sixthplace_label.place(relx=0.5, rely=0.525, anchor="center")

    seventhplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"7     {leaderboardArray[6].username}     {leaderboardArray[6].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    seventhplace_label.place(relx=0.5, rely=0.6, anchor="center")

    eighthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"8     {leaderboardArray[7].username}     {leaderboardArray[7].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    eighthplace_label.place(relx=0.5, rely=0.675, anchor="center")

    ninthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"9     {leaderboardArray[8].username}     {leaderboardArray[8].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    ninthplace_label.place(relx=0.5, rely=0.75, anchor="center") 

    tenthplace_label = customtkinter.CTkLabel(leaderboard_window, text=f"10     {leaderboardArray[9].username}     {leaderboardArray[9].score}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    tenthplace_label.place(relx=0.5, rely=0.825, anchor="center")

    positionText = ""
    if position == 1:
        positionText = "1st"
    elif position == 2:
        positionText = "2nd"
    elif position == 3:
        positionText = "3rd"
    else:
        positionText = f"{position}th"

    # Creating and displaying what position the current user came.
    userplacing_label = customtkinter.CTkLabel(leaderboard_window, text=f"You placed {positionText}", font=("Comic Sans MS", 25), fg_color=("#EBEBEA", "#252424"))
    userplacing_label.place(relx=0.5, rely=0.9, anchor= "center")




startScreen() # Calling startScreen module
window.mainloop()  # Starting the program