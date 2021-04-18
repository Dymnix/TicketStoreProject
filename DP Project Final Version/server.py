#DEFENSIVE PROGRAMMING PROJECT FINAL VERSION
#Justin Sanner, Kayla Fortune, Michael Hopkins
#SERVER
#VERSION DATE: 11/08/2020

#--------------------------------------------------------------------------------------------

#Initialization
import socket
import random
from datetime import date
from datetime import datetime

#--------------------------------------------------------------------------------------------

#Connect server with client
def startup():
    print("Starting server...")
    s = socket.socket()
    port = 12345
    s.bind(('', port))
    print("Server is running. Waiting for client...")
    s.listen(5)
    c, addr = s.accept()
    print("Client connected from",addr)
    loginMenu(s, port, c, addr)
    
#--------------------------------------------------------------------------------------------

#Menu on program startup
def loginMenu(s, port, c, addr):

    #Prints menu and selects an option from client
    sendData = ("\nWelcome to the famous Ticket Store!\n\nThe available options are:\n\t1. New User Registration\n\t2. Returning User\n\t3. Exit\n\nWhat number will you choose? ")
    c.send(sendData.encode())
    option = c.recv(1024).decode()
    option = option.strip()
    
    #Redirects to option chosen.
    if option == '1':
        userRegistration(s, port, c, addr) #Creates new users in account.txt
    elif option == '2':
        loginReturningUser(s, port, c, addr) #Allows users to login and access the rest of the program
    elif option == '3':
        logout(s, port, c, addr) #Quits program     
    else: #If no valid option, restarts login menu
        sendData = ("\nYou did not enter a valid option!! Please try again!!")
        c.send(sendData.encode())
        loginMenu(s, port, c, addr)
    
#--------------------------------------------------------------------------------------------

#Creates new users in account.txt
def userRegistration(s, port, c, addr):
    sendData = ("\nThis is new user registration!")
    c.send(sendData.encode())

    #Getting user info with option to go back to main menu (first name)
    sendData = ("\nEnter your first name or enter 'quit' to go back to the main menu: ")
    c.send(sendData.encode())
    firstName = c.recv(1024).decode()
    firstName=firstName.strip()
    if firstName=="quit":
        loginMenu(s, port, c, addr)

    #Getting user info with option to go back to main menu (last name)
    sendData=("\nEnter your last name or enter 'quit' to go back to the main menu: ")
    c.send(sendData.encode())
    lastName = c.recv(1024).decode()
    lastName=lastName.strip()
    if lastName=="quit":
        loginMenu(s, port, c, addr)

    #Getting user info with option to go back to main menu (email)
    sendData = ("\nEnter your email or enter 'quit' to go back to the main menu: ")
    c.send(sendData.encode())
    email = c.recv(1024).decode()
    email=email.strip()
    if email=="quit":
        loginMenu(s, port, c, addr)

    #Checks if the entered email belongs to a user already
    fileName = "accounts.txt"
    try:
        f=open(fileName, "r")
    except FileNotFoundError:
        f=open(fileName, "x")
        f=open(fileName, "r")
    accountList = [x.strip() for x in f.readline().split(', ')]
    while accountList != ['']:
        if accountList[3] == email:
            sendData = ("\nThis email is already in use. Please try again.")
            c.send(sendData.encode())
            f.close()
            userRegistration(s, port, c, addr)
        accountList = [x.strip() for x in f.readline().split(', ')]
    f.close()

    #Tries to open accounts.txt. If fails, returns to login menu
    try:
        f=open(fileName, "r")
    except FileNotFoundError:
        sendData = ("\nAn error has occured while creating your account. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 008)")
        c.send(sendData.encode())
        loginMenu(s, port, c, addr)

    #Assigns an account number between 1 and 999999
    accountNum = random.randint(1,999999)

    #If the account number does not exist, sets variable to a string for later use.
    #If it does already exist, chooses another account number and checks again.
    #If the account number matches 100 or more times, returns to login menu with error message.
    accountList = [x.strip() for x in f.readline().split(', ')]
    attemptCount = 0
    while accountList != ['']:
        if accountList[0] == accountNum:
            attemptCount = attemptCount + 1
            f.close()
            if attemptCount >= 100:
                sendData = ("\nAn error has occured while creating your account. Please try again. (ERROR CODE 009)")
                c.send(sendData.encode())
                loginMenu(s, port, c, addr)                
            try:
                f=open(fileName, "r")
            except FileNotFoundError:
                sendData = ("\nAn error has occured while creating your account. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 010)")
                c.send(sendData.encode())
                loginMenu(s, port, c, addr)
            accountList = [x.strip() for x in f.readline().split(', ')]
            accountNum = random.randint(1,999999)
        accountList = [x.strip() for x in f.readline().split(', ')]
    accountNum = str(accountNum)
    f.close()    

    #Loops until password and passwordConfirm match or 'quit' is entered.        
    passMatch=False
    while(passMatch==False):

        #Getting user info with option to go back to main menu (password)
        sendData = ("\nEnter your Password or enter 'quit' to go back to the main menu: ")
        c.send(sendData.encode())
        password = c.recv(1024).decode()
        password=password.strip()
        if password=="quit":
            passMatch=True
            loginMenu(s, port, c, addr)

        #Getting user info with option to go back to main menu (passwordConfirm)       
        sendData=("\nPlease confirm your Password or enter 'quit' to go back to the main menu: ")
        c.send(sendData.encode())
        passwordConfirm = c.recv(1024).decode()
        passwordConfirm=passwordConfirm.strip()
        if passwordConfirm=="quit":
            passMatch=True
            loginMenu(s, port, c, addr)

        #If the passwords match, begins account creation process
        if(password==passwordConfirm):
            sendData = ("\nCONGRATS " + firstName + " " + lastName + ", you have registered a new acccount!! You have been awarded 50 points! Please log in now to use them.")
            c.send(sendData.encode())
            passMatch=True

        #If passwords did not match, goes back to top of loop
        else:
            sendData = ("\nThe passwords did not match. Try Again!")
            c.send(sendData.encode())


    #writes new user info into accounts file
    f=open(fileName, "a")
    info=[accountNum,firstName,lastName,email,password,'50']
    for i in range(len(info)):
        if(i<(len(info))-1):
            f.write(info[i]+", ")
        else:
            f.write(info[i]+"\n")
    f.close()

    #Returns to main menu
    loginMenu(s, port, c, addr) 
    
#--------------------------------------------------------------------------------------------

#Allows users to login and access the rest of the program
def loginReturningUser(s, port, c, addr):

    #Tries to open accounts list file. If file does not exist, redirects to user registration, where the file can be created.
    fileName = "accounts.txt"
    try:
        f=open(fileName, "r")
    except FileNotFoundError:
        sendData=("\nNo accounts exist yet... You're the first ever user! Please create an account to get started!")
        c.send(sendData.encode())
        userRegistration(s, port, c, addr)
    
    accountList = [x.strip() for x in f.readline().split(', ')]
    if accountList == [""]:
        sendData= ("\nNo accounts exist yet... You're the first ever user! Please create an account to get started!")
        c.send(sendData.encode())
        userRegistration(s, port, c, addr)
        
    #log in using email
    sendData=("\nEnter your email or enter 'quit' to go back to the main menu: ")
    c.send(sendData.encode())
    email = c.recv(1024).decode()
    email=email.strip()
    if email=="quit":
        loginMenu(s, port, c, addr)

    #checks for if the email is valid. If it is, it compares the password entered and the stored password. If equal, sends users to main menu. 
    while accountList != ['']:
        if accountList[3] == email:
            sendData=("\nEnter your Password or enter 'quit' to go back to the main menu: ")
            c.send(sendData.encode())
            password = c.recv(1024).decode()
            password=password.strip()
            if password=="quit":
                loginMenu(s, port, c, addr)
            if password==accountList[4]:
                accountNum=accountList[0]
                firstName=accountList[1]
                lastName=accountList[2]
                currentPoints=accountList[5]
                f.close()
                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            else:
                sendData=("\nPassword incorrect. Please try again.")
                c.send(sendData.encode())
                f.close()
                loginReturningUser(s, port, c, addr)
        else:
            accountList = [x.strip() for x in f.readline().split(', ')]

    #If email or password are not valid, begins login again
    sendData=("\nThe email you entered is invalid. Please try again.")
    c.send(sendData.encode())
    f.close()
    loginReturningUser(s, port, c, addr)

#--------------------------------------------------------------------------------------------

#Quits program 
def logout(s, port, c, addr):
    try:
        sendData=("Good bye!")
        c.send(sendData.encode())
        exit(0)
    except: #If program fails to close here, restarts the program
        main()
        
#--------------------------------------------------------------------------------------------

#Main menu of the program.
def mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):

    #Tries to display current first name and points. If invalid first name or points, error message is displayed.
    try:
        sendData=("\n~~~~~~~~~~~~~~MAIN MENU~~~~~~~~~~~~~~\n")
        c.send(sendData.encode())
        sendData=(firstName + ", you currently have " + currentPoints + " points.")
        c.send(sendData.encode())
    except NameError:
        sendData=("\nAn error has occured while logging in. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 001)")
        c.send(sendData.encode())
        loginMenu(s, port, c, addr)

    #prints menu and selects option
    sendData=("\n\t1. View Events\n\t2. Ticket Purchasing\n\t3. User Ticket History\n\t4. Enter Code\n\t5. User Info\n\t6. Log Out\n")
    c.send(sendData.encode())
    sendData=("\nPlease select an option: ")
    c.send(sendData.encode())
    option = c.recv(1024).decode()

    #Redirects to option chosen.
    if option.strip() == '1': #Prints all available events and their ticket prices
        mainMenuViewEvents(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr) 
    elif option.strip() == '2': #Allows users to purchase tickets using points
        mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr) 
    elif option.strip() == '3': #Shows previous ticket purchases
        mainMenuTicketHistory(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    elif option.strip() == '4': #Allows users to enter a code for points
        mainMenuEnterCode(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr) 
    elif option.strip() == '5': #Allows users to change name, email, or password
        userInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr) 
    elif option.strip() == '6': #Quits program  
        logout(s, port, c, addr)     
    else: #If no valid option, lets user pick another option
        sendData=("\nYou did not enter a valid option!! Please try again!!")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    

#--------------------------------------------------------------------------------------------

#Opens file holding current events and displays results on screen
def mainMenuViewEvents(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):

    #Checks for UpcomingEvents.txt. If file does not exist, go back to main menu.
    fileName = "UpcomingEvents.txt"
    try:
        f = open(fileName, "r")
    except FileNotFoundError:
        sendData=("\nThere are no events in your area at this time.")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #Displays each event line-by-linem then returns to main menu
    events = [x.strip() for x in f.readline().split(', ')]
    sendData=("\nCurrent events in your area:\n") 
    c.send(sendData.encode())
    while events != [""]:
        sendData=(events[0] + ": " + events[1] + " points\n")
        c.send(sendData.encode())
        events = [x.strip() for x in f.readline().split(', ')]
    mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

#--------------------------------------------------------------------------------------------

#Allows users to purchase tickets using points
def mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):

    #Attempts to open UpcomingEvents.txt. If file does not exist, return to main menu.
    fileName = "UpcomingEvents.txt"
    try:
        f = open(fileName, "r")
    except FileNotFoundError:
        sendData=("\nThere are no events in your area at this time.")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #Begins creating the event menu
    sendData=("\nHere are some events in your area:")
    c.send(sendData.encode())

    #Sets 3 lines from UpcomingEvents.txt to variables
    event1 = [x.strip() for x in f.readline().split(', ')] 
    event2 = [x.strip() for x in f.readline().split(', ')]
    event3 = [x.strip() for x in f.readline().split(', ')]

    #Creates menu items 1-3 from variables above 
    while event1 != [""]:
        if event1 != [""]:
            sendData=("\n1. " + event1[0].ljust(50) + "\t" + event1[1] + " points")
            c.send(sendData.encode())
        if event2 != [""]:
            sendData=("\n2. " + event2[0].ljust(50) + "\t" + event2[1] + " points")
            c.send(sendData.encode())
        if event3 != [""]:
            sendData=("\n3. " + event3[0].ljust(50) + "\t" + event3[1] + " points")
            c.send(sendData.encode())

        #Checks if next line is empty. If no, prints option 4. If it is empty, it skips option 4.
        finalLine = [x.strip() for x in f.readline().split(', ')]
        if finalLine != [""]:
            sendData=("\n4. More Events")
            c.send(sendData.encode())
        else:
            sendData=("\n")
            c.send(sendData.encode())

        #Prints the other options
        sendData=("\n5. Top of List")
        c.send(sendData.encode())
        sendData=("\n6. Exit\n")
        c.send(sendData.encode())

        #Gets input from client 
        sendData=("\nWhich will you choose: ")
        c.send(sendData.encode())
        option = c.recv(1024).decode()
        option=option.strip()

        #Begins process of purchasing ticket from menu item 1
        if option == '1':

            #Confirms the user chose the correct event
            sendData=("\nWould you like to purchase a ticket to " + event1[0] + " for the cost of " + event1[1] + " points?")
            c.send(sendData.encode())
            sendData=("Y or N: ")
            c.send(sendData.encode())
            choice = c.recv(1024).decode()
            choice=choice.strip()

            #If user confirms they checked correct event, sets point values to int for math purposes
            if choice =='Y' or choice == 'y':
                currentPoints = int(currentPoints)
                eventPoints = int(event1[1])

                #If user has enough points, checks user has correct email
                if currentPoints >= eventPoints:
                    sendData=("\nPlease enter your email to validate purchase: ")
                    c.send(sendData.encode())
                    validation = c.recv(1024).decode()
                    validation = validation.strip()

                    #If email is correct, checks user for valid password.
                    if email == validation:
                        sendData=("\nPlease enter your password to validate purchase: ")
                        c.send(sendData.encode())
                        validation = c.recv(1024).decode()
                        validation = validation.strip()

                        #if password is correct, begins purchase process
                        if password == validation:

                            #If accounts.txt fails to open, goes back to main menu
                            try:
                                f2 = open('accounts.txt', 'rt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Creates an updated user info with replaced current points (current points - event point cost)
                            currentPoints = str(currentPoints)
                            original = email + ", " + password + ", " + currentPoints
                            currentPoints = int(currentPoints) - eventPoints
                            currentPoints = str(currentPoints)
                            replacement = email + ", " + password + ", " + currentPoints
                            data = f2.read()
                            data = data.replace(original, replacement)
                            f2.close()

                            #If accounts.txt fails to open, go back to main menu
                            try:
                                f2 = open('accounts.txt', 'wt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Writes updated user data to accounts.txt
                            f2.write(data)
                            f2.close()

                            #Gets date and time, then writes the purchase to an accountnum-specific file, creating such file if it does not exist. 
                            today = date.today()
                            dateFormat = today.strftime("%B %d, %Y")
                            now = datetime.now()
                            timeFormat = now.strftime("%I:%M %p")
                            fileName = accountNum + "TicketHistory.txt"
                            f3 = open(fileName, "a")
                            eventWrite = str(event1[0] + " (" + event1[1] + " points) on " + dateFormat + " at " + timeFormat + "\n")
                            f3.write(eventWrite)
                            f3.close()

                            #Returns to main menu
                            sendData=("\nThank you for your purchase! Returning to main menu!")
                            c.send(sendData.encode())
                            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                        #If passwords did not match, return to main menu
                        else:
                            sendData=("\nPassword did not match. Try again.")
                            c.send(sendData.encode())
                            f.close()
                            currentPoints=str(currentPoints)
                            mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                    #If email did not match, return to main menu
                    else:
                        sendData=("\nEmail did not match. Try again.")
                        c.send(sendData.encode())
                        f.close()
                        currentPoints=str(currentPoints)
                        mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)   

                #if user does not have enough points, return to main menu
                else:
                    sendData=("\nYou don't have enough points!")
                    c.send(sendData.encode())
                    currentPoints=str(currentPoints)
                    f.close()
                    mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

            #If user chooses "N" or if invalid option, return to main menu
            else:
                f.close()
                if choice != 'N' and choice != 'n':
                    sendData=("\nInvalid Option! Please try again!")
                    c.send(sendData.encode())
                currentPoints=str(currentPoints)
                mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)       

        #Begins process of purchasing ticket from menu item 2
        if option == '2':

            #Confirms the user chose the correct event
            sendData=("\nWould you like to purchase a ticket to " + event2[0] + " for the cost of " + event2[1] + " points?")
            c.send(sendData.encode())
            sendData=("Y or N: ")
            c.send(sendData.encode())
            choice = c.recv(1024).decode()
            choice=choice.strip()

            #If user confirms they checked correct event, sets point values to int for math purposes
            if choice =='Y' or choice == 'y':
                currentPoints = int(currentPoints)
                eventPoints = int(event2[1])

                #If user has enough points, checks user has correct email
                if currentPoints >= eventPoints:
                    sendData=("\nPlease enter your email to validate purchase: ")
                    c.send(sendData.encode())
                    validation = c.recv(1024).decode()
                    validation = validation.strip()

                    #If email is correct, checks user for valid password.
                    if email == validation:
                        sendData=("\nPlease enter your password to validate purchase: ")
                        c.send(sendData.encode())
                        validation = c.recv(1024).decode()
                        validation = validation.strip()

                        #if password is correct, begins purchase process
                        if password == validation:

                            #If accounts.txt fails to open, goes back to main menu
                            try:
                                f2 = open('accounts.txt', 'rt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Creates an updated user info with replaced current points (current points - event point cost)
                            currentPoints = str(currentPoints)
                            original = email + ", " + password + ", " + currentPoints
                            currentPoints = int(currentPoints) - eventPoints
                            currentPoints = str(currentPoints)
                            replacement = email + ", " + password + ", " + currentPoints
                            data = f2.read()
                            data = data.replace(original, replacement)
                            f2.close()

                            #If accounts.txt fails to open, go back to main menu
                            try:
                                f2 = open('accounts.txt', 'wt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Writes updated user data to accounts.txt
                            f2.write(data)
                            f2.close()

                            #Gets date and time, then writes the purchase to an accountnum-specific file, creating such file if it does not exist.
                            today = date.today()
                            dateFormat = today.strftime("%B %d, %Y")
                            now = datetime.now()
                            timeFormat = now.strftime("%I:%M %p")
                            fileName = accountNum + "TicketHistory.txt"
                            f3 = open(fileName, "a")
                            eventWrite = str(event2[0] + " (" + event2[1] + " points) on " + dateFormat + " at " + timeFormat + "\n")
                            f3.write(eventWrite)
                            f3.close()

                            #Returns to main menu
                            sendData=("\nThank you for your purchase! Returning to main menu!")
                            c.send(sendData.encode())
                            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                        #If passwords did not match, return to main menu
                        else:
                            sendData=("\nPassword did not match. Try again.")
                            c.send(sendData.encode())
                            f.close()
                            currentPoints=str(currentPoints)
                            mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                    #If email did not match, return to main menu
                    else:
                        sendData=("\nEmail did not match. Try again.")
                        c.send(sendData.encode())
                        f.close()
                        currentPoints=str(currentPoints)
                        mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)   

                #if user does not have enough points, return to main menu
                else:
                    sendData=("\nYou don't have enough points!")
                    c.send(sendData.encode())
                    currentPoints=str(currentPoints)
                    f.close()
                    mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

            #If user chooses "N" or if invalid option, return to main menu
            else:
                f.close()
                if choice != 'N' and choice != 'n':
                    sendData=("\nInvalid Option! Please try again!")
                    c.send(sendData.encode())
                currentPoints=str(currentPoints)
                mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Begins process of purchasing ticket from menu item 3
        elif option == '3':

            #Confirms the user chose the correct event
            sendData=("\nWould you like to purchase a ticket to " + event3[0] + " for the cost of " + event3[1] + " points?")
            c.send(sendData.encode())
            sendData=("Y or N: ")
            c.send(sendData.encode())
            choice = c.recv(1024).decode()
            choice=choice.strip()
            
            #If user confirms they checked correct event, sets point values to int for math purposes
            if choice =='Y' or choice == 'y':
                currentPoints = int(currentPoints)
                eventPoints = int(event3[1])

                #If user has enough points, checks user has correct email
                if currentPoints >= eventPoints:
                    sendData=("\nPlease enter your email to validate purchase: ")
                    c.send(sendData.encode())
                    validation = c.recv(1024).decode()
                    validation = validation.strip()

                    #If email is correct, checks user for valid password.
                    if email == validation:
                        sendData=("\nPlease enter your password to validate purchase: ")
                        c.send(sendData.encode())
                        validation = c.recv(1024).decode()
                        validation = validation.strip()

                        #if password is correct, begins purchase process
                        if password == validation:

                            #If accounts.txt fails to open, goes back to main menu
                            try:
                                f2 = open('accounts.txt', 'rt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Creates an updated user info with replaced current points (current points - event point cost)
                            currentPoints = str(currentPoints)
                            original = email + ", " + password + ", " + currentPoints
                            currentPoints = int(currentPoints) - eventPoints
                            currentPoints = str(currentPoints)
                            replacement = email + ", " + password + ", " + currentPoints
                            data = f2.read()
                            data = data.replace(original, replacement)
                            f2.close()

                            #If accounts.txt fails to open, go back to main menu
                            try:
                                f2 = open('accounts.txt', 'wt')
                            except FileNotFoundError:
                                sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                                c.send(sendData.encode())
                                currentPoints = str(currentPoints)
                                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                            #Writes updated user data to accounts.txt
                            f2.write(data)
                            f2.close()

                            #Gets date and time, then writes the purchase to an accountnum-specific file, creating such file if it does not exist.
                            today = date.today()
                            dateFormat = today.strftime("%B %d, %Y")
                            now = datetime.now()
                            timeFormat = now.strftime("%I:%M %p")
                            fileName = accountNum + "TicketHistory.txt"
                            f3 = open(fileName, "a")
                            eventWrite = str(event3[0] + " (" + event3[1] + " points) on " + dateFormat + " at " + timeFormat + "\n")
                            f3.write(eventWrite)
                            f3.close()

                            #Returns to main menu
                            sendData=("\nThank you for your purchase! Returning to main menu!")
                            c.send(sendData.encode())
                            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                        #If passwords did not match, return to main menu
                        else:
                            sendData=("\nPassword did not match. Try again.")
                            c.send(sendData.encode())
                            f.close()
                            mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                    #If email did not match, return to main menu
                    else:
                        sendData=("\nEmail did not match. Try again.")
                        c.send(sendData.encode())
                        f.close()
                        mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)   

                #if user does not have enough points, return to main menu
                else:
                    sendData=("\nYou don't have enough points!")
                    c.send(sendData.encode())
                    f.close()
                    mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

            #If user chooses "N" or if invalid option, return to main menu
            else:
                if choice != 'N' and choice != 'n':
                    sendData=("\nInvalid Option! Please try again!")
                    c.send(sendData.encode())
                f.close()
                mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #If option 4 is chosen, prints next 3 events from UpcomingEvents.txt
        elif option == '4':
            if finalLine != [""]:
                sendData=("\nHere are some events in your area:")
                c.send(sendData.encode())    
                event1 = finalLine
                event2 = [x.strip() for x in f.readline().split(', ')]
                event3 = [x.strip() for x in f.readline().split(', ')]

            #If the final line was empty, restarts menu
            else:
                sendData=("\nInvalid option. Please try again.")
                c.send(sendData.encode())
                f.close()
                mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #If option 5 was chosen, tries to return to beginning of list by reopening UpcomingEvents.txt. If no file exists, returns to main menu
        elif option == '5':
            f.close()
            try:
                f = open(fileName, "r")
            except FileNotFoundError:
                sendData=("\nThere are no events in your area at this time.")
                c.send(sendData.encode())
                mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            sendData=("\nHere are some events in your area:")
            c.send(sendData.encode())    
            event1 = [x.strip() for x in f.readline().split(', ')]
            event2 = [x.strip() for x in f.readline().split(', ')]
            event3 = [x.strip() for x in f.readline().split(', ')]  

        #Returns to main menu if option 6 is chosen
        elif option == '6':
            f.close()
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Begins ticket purchase menu again if invalid option is chosen.
        else:
            sendData=("\nInvalid option. Please try again.")
            c.send(sendData.encode())
            f.close()
            mainMenuTicketPurchase(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            

#--------------------------------------------------------------------------------------------

#Tries to read user's ticket history from associated .txt file. If no file exists, returns user to main menu.
def mainMenuTicketHistory(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):
    fileName = accountNum + "TicketHistory.txt"
    try:
        f = open(fileName, "r")
    except FileNotFoundError:
        sendData=("\nYou have no purchased tickets.")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    history = f.read()
    sendData=("\nHere are your previous ticket purchases:\n" + history)
    c.send(sendData.encode())
    mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

#--------------------------------------------------------------------------------------------

#Allows users to enter codes for points
def mainMenuEnterCode(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):

    #Tries to open pointcodes.txt. If fails, returns users to main menu.
    try:
        f = open('pointcodes.txt', 'r')
    except FileNotFoundError:
        sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 003)")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #Gets point code input from client 
    sendData=("\nThis is where you can enter codes you find for points! Each code can only be used once!")
    c.send(sendData.encode())
    sendData=("\nPlease enter a code for points, or enter 'quit' to go back to the main menu: ")
    c.send(sendData.encode())
    codeEnter = c.recv(1024).decode()
    codeEnter = codeEnter.strip()

    #if user input "quit", return to main menu
    if codeEnter == 'quit':
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #Looks in accountnum-specific CodesUsed text file to see if the code has been used by the user already.
    code = [x.strip() for x in f.readline().split(', ')]
    try:
        fileName = accountNum + "CodesUsed.txt"
        f3 = open(fileName, "r")
        usedCode = f3.readline()
        while usedCode != "":
            if usedCode.strip() == codeEnter:
                sendData=("\nYou have already used that code. Please enter another code.") #If code has been used, restart Enter Code Menu
                c.send(sendData.encode())
                f.close()
                f3.close()
                mainMenuEnterCode(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            usedCode = f3.readline()

    #If no CodesUsed file exists for the user, continue
    except FileNotFoundError:
        pass

    #After checking for CodesUsed file, regardless of if it exists or not, adds points to user's account unless code has been used before
    finally:
        while code != [""]:
            if code[0] == codeEnter:

                #if accounts.txt does not exist, return to main menu without adding points
                try:
                    f2 = open('accounts.txt', 'r')
                except FileNotFoundError:
                    sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 004)")
                    c.send(sendData.encode())
                    mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                #Creates updated user info with currentpoints = (currentpoints + points from code)
                original = email + ", " + password + ", " + currentPoints
                currentPoints = int(currentPoints) + int(code[1])
                currentPoints = str(currentPoints)
                replacement = email + ", " + password + ", " + currentPoints
                data = f2.read()
                data = data.replace(original, replacement)
                f2.close()

                #If accounts.txt does not exist, return to main menu
                try:
                    f2 = open('accounts.txt', 'wt')
                except FileNotFoundError:
                    sendData=("\nAn error has occured. Please email sanner_justin@columbusstate.edu for troubleshooting. (ERROR CODE 002)")
                    c.send(sendData.encode())
                    currentPoints = str(currentPoints)
                    mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

                #Updates accounts.txt with the updated user info
                f2.write(data)
                f2.close()

                #Updates accountnum-specific CodesUsed.txt file to add the code used. Creates the CodesUsed text file if it does not already exist.
                fileName = accountNum + "CodesUsed.txt"
                f3 = open(fileName, "w")
                f3.write(code[0])
                f3.close()

                #Returns to main menu
                sendData=("\nPoints successfully added! Returning to main menu!")
                c.send(sendData.encode())
                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            code = [x.strip() for x in f.readline().split(', ')]
    #If code was entered incorrectly, restarts Enter Code Menu
    sendData=("\nYou have entered an incorrect code. Please try again.")
    c.send(sendData.encode())
    mainMenuEnterCode(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
        
        
#--------------------------------------------------------------------------------------------
#Displays the user info menu and gets input from client
def userInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):  #Main Menu Option 5-User Info Menu
    sendData=("\nThe available options are:\n\t1. View Information\n\t2. Edit Information\n\t3. Return to Main Menu\n")
    c.send(sendData.encode())

    #Gets input from client
    sendData=("\nWhat number will you choose? ")
    c.send(sendData.encode())
    option = c.recv(1024).decode()
    option = option.strip()

    if option == '1': #Displays the current user's info
        userInfoMenuViewInfo(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    elif option == '2': #Allows user to edit their info
        editInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    elif option == '3': #Returns to main menu
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    else: #If no valid option, restarts user info menu
        sendData=("\nYou did not enter a valid option! Please try again!")
        c.send(sendData.encode())
        userInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

#--------------------------------------------------------------------------------------------

#Displays current user's info
def userInfoMenuViewInfo(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):
    sendData=("\nHere is your current information:")
    c.send(sendData.encode())
    sendData=("\nFirst Name: " + firstName)
    c.send(sendData.encode())
    sendData=("\nLast Name: " + lastName)
    c.send(sendData.encode())
    sendData=("\nEmail: " + email)
    c.send(sendData.encode())
    sendData=("\nCurrent Points: " + currentPoints + "\n")
    c.send(sendData.encode())
    userInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
    
#--------------------------------------------------------------------------------------------

#Allows users to edit their info
def editInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr):

    #If accounts.txt does not exist, returns to main menu
    try:
        f = open('accounts.txt', 'r')
    except FileNotFoundError:
        sendData=("\nYour information cannot be edited at this time.")
        c.send(sendData.encode())
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #Checks for valid password before allowing user to change. If 'quit' is entered, returns to main menu
    sendData=("\nPlease enter your password for validation or enter 'quit' to return to main menu: ")
    c.send(sendData.encode())
    validation = c.recv(1024).decode()
    validation = validation.strip()
    if validation == 'quit':
        mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #If password matches, sets variable currentUser to a string containing current user info
    if password == validation:
        currentUser = firstName + ", " + lastName + ", " + email + ", " + password + ", " + currentPoints

        #Gets input from client to get new first name
        sendData=("\nEnter your new first name or enter 'quit' to return to main menu: ")
        c.send(sendData.encode())
        newFirst = c.recv(1024).decode()
        newFirst = newFirst.strip()
        if newFirst == 'quit':
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Gets input from client to get new last name
        sendData=("\nEnter your new last name or enter 'quit' to return to main menu: ")
        c.send(sendData.encode())
        newLast = c.recv(1024).decode()
        newLast = newLast.strip()
        if newLast == 'quit':
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Gets input from client to get new email
        sendData=("\nEnter your new email or enter 'quit' to return to main menu: ")
        c.send(sendData.encode())
        newEmail = c.recv(1024).decode()
        newEmail = newEmail.strip()
        if newEmail == 'quit':
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Checks emails in accounts.txt to make sure entered email is unique. 
        emailChecker = [x.strip() for x in f.readline().split(', ')]
        while emailChecker != [""]:
            validation = emailChecker[2]
            validActNum = emailChecker[0]

            #Allows duplicate email to pass through only if the email is associated with the current accountNum
            if validation == newEmail and validActNum != accountNum:
                sendData=("\nThis email is already in use. Please try again.")
                c.send(sendData.encode())
                f.close()
                editInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)
            emailChecker = [x.strip() for x in f.readline().split(', ')]

        #Gets user input to change password
        sendData=("\nEnter your new password or enter 'quit' to return to main menu: ")
        c.send(sendData.encode())
        newPass = c.recv(1024).decode()
        newPass = newPass.strip()
        if newPass == 'quit':
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #Gets user input to validate their new password
        sendData=("\nEnter your new password again or enter 'quit' to return to main menu: ")
        c.send(sendData.encode())
        newPassValid = c.recv(1024).decode()
        newPassValid = newPassValid.strip()
        if newPassValid == 'quit':
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #If the new passwords match, close accounts.txt, then try to open accounts.txt. If file does not exist, returns to main menu
        if newPass == newPassValid:
            f.close()
            try:
                f = open('accounts.txt', 'r')
            except FileNotFoundError:
                sendData=("\nYour information cannot be edited at this time.")
                c.send(sendData.encode())
                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

            #Creates variable newUser with previous client inputs, then sets data to update the current user info with new user info
            newUser = newFirst + ", " + newLast + ", " + newEmail + ", " + newPass + ", " + currentPoints
            data = f.read()
            data = data.replace(currentUser, newUser)
            f.close()

            #Tries to open accounts.txt. If fails, returns to main menu without updating user data
            try:
                f = open('accounts.txt', 'w')
            except FileNotFoundError:
                sendData=("\nYour information cannot be edited at this time.")
                c.send(sendData.encode())
                mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

            #Updates accounts.txt with updated user info
            f.write(data)
            f.close()

            #Updates variables to the inputed variables
            firstName = newFirst
            lastName = newLast
            email = newEmail
            password = newPass

            #Prints the updated user info and returns to main menu
            sendData=("\nInformation successfully changed! Here is your current info:")
            c.send(sendData.encode())
            sendData=("\nFirst Name: " + firstName)
            c.send(sendData.encode())
            sendData=("\nLast Name: " + lastName)
            c.send(sendData.encode())
            sendData=("\nEmail: " + email)
            c.send(sendData.encode())
            sendData=("\nCurrent Points: " + currentPoints + "\n")
            c.send(sendData.encode())
            mainMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

        #If the two new passwords did not match, restarts Edit User Info menu
        else:
            sendData=("\nYour passwords did not match. Please try again.")
            c.send(sendData.encode())
            f.close()
            editInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)

    #If input password does not match password associated with account, restarts Edit User Info Menu
    else:
        sendData=("\nYour password did not match. Please try again.")
        c.send(sendData.encode())
        f.close()
        editInfoMenu(accountNum, firstName, lastName, email, password, currentPoints, s, port, c, addr)


#--------------------------------------------------------------------------------------------

#Launches program on startup
def main():
    startup()

main()
