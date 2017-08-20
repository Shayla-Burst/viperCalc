__author__ = 'shaylamarie'
from tkinter import * #Imports GUI packages.
import platform #Imports tools for testing user's operating system

nums = [] #List used to store calculator input as strings for later use of eval() (eval() is totally safe to use in this program since user input is highly controlled
ifFunctionsOpen = False

def numPress(num, display): #Function to store number button presses, update display screen, and update the current number (more on that in CurrentNum class)
    if ((display["text"] == "0")):
        display["text"] = num

    else:
        display["text"] += num

    if (CurrentNum.returnCurrent() == "0"):
        CurrentNum.overwrite(num)
    else:
        CurrentNum.add(num)


def negPress(display): #Function for the negative NEG button press, prevents error-inducing input.
    if ("-" in CurrentNum.returnCurrent()):
        return
    else:
        CurrentNum.add("-")

    if (display["text"] == "0"):
        display["text"] = "NEG"
    else:
        display["text"] += "NEG"

def clearPress(output, display): #Clears display and all variables used in calculation
    output["text"] = ""
    display["text"] = "0"
    CurrentNum.clear()
    ParenthStorage.clear()
    nums.clear()

def decPress(display, output): #Function for decimal button press, prevents error-inducing input.
    if ("." in CurrentNum.returnCurrent()):
        return
    if(output["text"] != ""):
        display["text"] = output["text"]
        CurrentNum.overwrite(output["text"])
        nums.clear()
    if(display["text"] == "0"):
        display["text"] = "."
        CurrentNum.overwrite(".")
    else:
        display["text"] += "."
        CurrentNum.add(".")


def opPress(op, display, output): #Handles the press of the basic operation buttons (plus, minus, multiply, divide, power)
    if(output["text"] != ""):
        display["text"] = output["text"]
        CurrentNum.overwrite(output["text"])
        nums.clear()



    if(display["text"] == "0"):
        return

    if ("NEG" in display["text"]):
        display["text"] = display["text"].replace("NEG", "-")


    if (ParenthStorage.isGoing() == True):
        if (CurrentNum.returnCurrent() != "0"):
            ParenthStorage.add(CurrentNum.returnCurrent())
        ParenthStorage.add(op)


    else:
        if (CurrentNum.returnCurrent() != "0"):
            nums.append(CurrentNum.returnCurrent())
        if (op != "**"):
            nums.append(op)


    if((op == "**") & (ParenthStorage.isGoing() == False)):
        nums.append(op)

    if(op == "**"):
        display["text"] += "^"
    else:
        display["text"] += op


    CurrentNum.clear()

def parenth(display, par): #Handles presses of the parentheses buttons.

    if (display["text"] == "0"):
        if (par == "("):
            display["text"] = par
        if (par == ")"):
            return
    elif (display["text"][(len(display["text"]) - 1)] == "."):
        return
    else:
        display["text"] += par

    if (par == "("):
        ParenthStorage.begin()

        if (CurrentNum.returnCurrent() != "0"):
            nums.append(CurrentNum.returnCurrent())

        CurrentNum.clear()
    if (par == ")"):
        ParenthStorage.end(CurrentNum.returnCurrent())
        CurrentNum.clear()


def delete(display): #Handles press of the delete button, is a "backspace" function.
    displayLastDigit = display["text"][len(display["text"]) - 1]
    if ((displayLastDigit == "*") or (displayLastDigit == "+") or (displayLastDigit == "-") or(displayLastDigit == "/")):
        display["text"] = display["text"][:-1]
        nums.pop()
    if ((displayLastDigit == ")") or (displayLastDigit == "(")):
        display["text"] = display["text"][:-1]
        nums[-1] = nums[-1][:-1]
    if (displayLastDigit == "G"):
        display["text"] = display["text"][:-3]
        CurrentNum.delete(3)
    else:
        for i in range(10):
            if (displayLastDigit == str(i)):
                display["text"] = display["text"][:-1]
                CurrentNum.delete(1)
                if (len(nums[-1]) == 1):
                    nums.pop()
                else:
                    nums[-1] = nums[-1][:-1]


def functionsPress(functButton, display, equals, root): #Handles the press and toggle function of th FUNCTIONS button. Expands window to show functions, and then regresses window back to original size on toggle
    if (functButton["bg"] == "white"):
        root.geometry("600x400")
        functionsInit(display, equals, root)
        functButton.config(bg = "light green")

    else:
        root.geometry("300x400")
        functButton.config(bg = "white")


def functionsInit(display, equals, root): #Initializes the GUI of the extra functions shown by use of the FUNCTIONS button.
        functButtonFrame = Frame(root, width = 290, height = 390, bd = 6, bg = "black", highlightbackground = "white", relief = SUNKEN)
        functButtonFrame.place(width = 290, height = 385, x = 305, y = 5)

        sciNoLabelFrame = LabelFrame(functButtonFrame, text = "Scientific Notation", fg = "white", bg = "black", width = 275, height = 60)
        sciNoLabelFrame.grid(row = 0, column = 0)
        sciNoLabelFrame.grid_propagate(False)

        sciNoButton = Button(sciNoLabelFrame, text = "x 10^", height = 1, width = 3, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: sciNo(display, equals))
        sciNoButton.place(height = 30, width = 60, x = 10, y = 8)
        sciNoButton.config(font = ("Sans", 10))

        convertToSciButton = Button(sciNoLabelFrame, text = "Convert to Sci", height = 1, width = 12, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: toSci(display, equals))
        convertToSciButton.place(height = 30, width = 110, x = 90, y = 8)
        convertToSciButton.config(font = ("Sans", 10))


def sciNo(display, equals): #Handles the scientific notation (x 10^) button, and prevents error-inducing input.
    if (display["text"] == "0"):
        return
    if (CurrentNum.returnCurrent() == "0"):
        return
    display["text"] += " x 10^"
    nums.append(CurrentNum.returnCurrent())
    CurrentNum.clear()
    nums.append("* 10 **")

def toSci(display, equals): #Handles Number to Scientific Notation button press, prevents error-inducing input, begins the entry for it to be later stored in nums[]
    if ("toSci(" in display["text"] == True):
        return
    display["text"] = "toSci("
    ParenthStorage.beginToSci()

def numToSciConvert(num): #Handles converting numbers to scientific notation, without the use of "e".
    decPos = 0
    exponent = 0
    numDecimal = ""
    numString = num[4:(len(num) - 1)]
    if ("." in numString):
        decPos = numString.index(".")
        if (numString[0] == "."):
            numString = numString[1:(len(numString))]
            for i in range(len(numString)):
                if (numString[i] == "0"):
                    exponent -= 1
                if (numString[i] != "0"):
                    numDecimal += numString[i]

                    if (len(numDecimal) == 1):
                        numDecimal += "."
                        exponent -= 1
    if((numString[0] != "0") & (numString[0] != ".")):
        exponent = (len(numString) - 1)
        for i in range(len(numString)):
            if (numString[i] != "0"):
                numDecimal += numString[i]
                if (len(numDecimal) == 1):
                    numDecimal += "."

    return numDecimal + " x 10^" + str(exponent)

def equalsPress(output, display): #Solves the entered problem
    parenCount = 0
    equationString = ""

    if ("NEG" in display["text"]):
        display["text"] = display["text"].replace("NEG", "-")

    if(display["text"][-1] != ")"):
        if (CurrentNum.returnCurrent() != "0"):
            nums.append(CurrentNum.returnCurrent())

    for i in range(len(nums)):
        if ("SCI" in nums[i]):
           nums[i] = numToSciConvert(nums[i])
           output["text"] = nums[i]

        if (i < len(nums)):
            equationString += nums[i] + " "

        elif (i == len(nums)):
            equationString += nums[i]

    answer = eval(equationString)
    answer = '{:.19f}'.format(answer) #Gets rid of constant e in expression, gives full decimal up to 19 places
    answerString = str(answer)
    if ("." in answerString): #Gets rid of any unneeded zeroes at end of decimal
        for i in range (len(answerString)):
            if ((answerString[-1] == "0") & (answerString[-2] != ".")):
                answerString = answerString[0:-1]
    else:
        answerString = str(answer)

    output["text"] = answerString
    CurrentNum.clear()
    nums.clear()


class CurrentNum(): #This class handles keeping track of the current number (the number between the previous operation key and the next. Mainly exists for preventing error-inducing input.
    currentNumber = "0"

    def add(num):
        if ((CurrentNum.currentNumber == "0") or ((CurrentNum.currentNumber == "0") & (num == "-"))):
            CurrentNum.currentNumber = num
        else:
            CurrentNum.currentNumber += num

    def overwrite(num):
        CurrentNum.currentNumber = num

    def returnCurrent():
        return CurrentNum.currentNumber

    def delete(num):
        CurrentNum.currentNumber = CurrentNum.currentNumber[:-num]

    def clear():
        CurrentNum.currentNumber = "0"


class ParenthStorage(): #Handles the behavior and storage of parentheses. Coded to handle multiple parentheses. Stores entire parentheses statement into nums[]
    parenStatement = "" #Initialize the parentheses statement for later storage.
    parenGoing = False #For testing whether a parentheses statement is currently going.
    openPars = 0 #Keeps count of open parentheses statements.

    def begin():
        if (ParenthStorage.openPars == 0):
            ParenthStorage.parenStatement = "("
            ParenthStorage.openPars += 1
            ParenthStorage.parenGoing = True

        else:
            ParenthStorage.parenStatement += "("
            ParenthStorage.openPars += 1

    def beginToSci():
        if (ParenthStorage.parenGoing == True):
            if (ParenthStorage.openPars >= 1):
                ParenthStorage.parenStatement += "SCI("
                ParenthStorage.openPars += 1
                ParenthStorage.sciGoin = True
        else:
            ParenthStorage.parenStatement = "SCI("
            ParenthStorage.parenGoing = True
            ParenthStorage.openPars += 1
            ParenthStorage.sciGoin = True


    def add(numOrOp):
        if (((ParenthStorage.openPars >= 1) & (CurrentNum.returnCurrent() != "0"))):
            ParenthStorage.parenStatement += numOrOp + " "

    def end(currentNum):
        if (CurrentNum.returnCurrent() != "0"):
            ParenthStorage.parenStatement += currentNum + ")"

        else:
            ParenthStorage.parenStatement += ")"

        ParenthStorage.openPars -= 1

        if (ParenthStorage.openPars == 0):
            nums.append(ParenthStorage.parenStatement)
            ParenthStorage.parenStatement = ""
            ParenthStorage.parenGoing = False


    def isGoing():
        return ParenthStorage.parenGoing

    def get():
        return ParenthStorage.parenStatement

    def clear():
        ParenthStorage.parenStatement = ""


class Calc(Frame):

    def __init__(self): #Initializes initUI.
        super().__init__()
        self.initUI()

    def initUI(self): #The user interface method. Initializes
        root = RootWindow.root #Pushes main window over to this class.

        opScreen = Frame(root, width = 290, height = 75, bd = 4, bg = "light blue", relief = SUNKEN) #"screen" for displaying current input.
        opScreen.grid(pady = 5, padx = 5, row = 0, column = 2, columnspan = 3)
        opScreen.grid_propagate(False)


        displayNums = Label(opScreen, text = "0", bg = "light blue") #Numbers and operations that are displayed in opScreen
        displayNums.grid(row = 0, column = 0)
        displayNums.grid_propagate(False)
        displayNums.config(font = ("Courier", 18))


        equalsFrame = Frame(root, width = 290, height = 40, bd = 6, bg = "light blue", highlightbackground = "light green", relief = SUNKEN)  #Display screen for answers.
        equalsFrame.place(height = 40, width = 290, x = 5, y = 85)

        equalsSignFrame = Frame(equalsFrame, width = 30, height = 30, bd = 0, bg = "light blue", highlightbackground = "light green") #invisible frame to hold equals signifier on the answer screen.
        equalsSignFrame.grid(padx = 0, pady = 0, row = 0, column = 0)
        equalsSignFrame.grid_propagate(False)

        equalsSignLabel = Label(equalsSignFrame, height = 0, width = 0, text = "=", bg = "light blue") #Equals sign on answer screen. Does not change.
        equalsSignLabel.grid(row = 0, column = 0, padx = 0, pady = 0)
        equalsSignLabel.grid_propagate(False)
        equalsSignLabel.config(font = ("Arial Bold", 20))

        equalsLabel = Label(equalsFrame, text = "", bg = "light blue", fg = "black") #Displays answers.
        equalsLabel.grid(row = 0, column = 1)
        equalsLabel.grid_propagate(False)
        equalsLabel.config(font = ("Courier", 15))


        calcButtonFrame = Frame(root, width = 290, height = 250, bd = 6, bg = "black", highlightbackground = "white", relief = SUNKEN) #Frame to hold the buttons of the calculator.
        calcButtonFrame.place(width = 290, height = 250, x = 5, y = 140)

        numDecimal = Button(calcButtonFrame, text = ".", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: decPress(displayNums, equalsLabel)) #Decimal button
        numDecimal.grid(row = 5, column = 0, padx = 5, pady = 5)
        numDecimal.config(font = ("Sans", 10))

        numButtons = [] #Creates list for buttons
        for i in range(10): #Since there wisll be ten number keys, 0-10. Sets and initializes number keys to save code space.
            numButtons.append(Button(calcButtonFrame, text = str(i), height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda i = i: numPress(str(i), displayNums))) #Adds new button to list, with i being the number put on the button and sent to numPress()
            if (i == 0):
                numButtons[i].grid(row = 5, column = 1, padx = 5, pady = 5)
            if ((i == 1) or (i == 2) or (i == 3)):
                numButtons[i].grid(row = 2, column = i - 1, padx = 5, pady = 5)
            if ((i == 4) or (i == 5) or (i == 6)):
                numButtons[i].grid(row = 3, column = i - 4, padx = 5, pady = 5)
            if ((i == 7) or (i == 8) or (i == 9)):
                numButtons[i].grid(row = 4, column = i - 7, padx = 5, pady = 5)
            numButtons[i].config(font = ("Sans", 10))

        numNeg = Button(calcButtonFrame, text = "NEG", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: negPress(displayNums)) #Negative number button.
        numNeg.grid(row = 5, column = 2, padx = 5, pady = 5)
        numNeg.config(font = ("Sans", 10))

        numAdd = Button(calcButtonFrame, text = "+", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: opPress("+", displayNums, equalsLabel)) #Plus sign button.
        numAdd.grid(row = 2, column = 3, padx = 5, pady = 5)
        numAdd.config(font = ("Sans", 10))

        numSub = Button(calcButtonFrame, text = "-", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: opPress("-", displayNums, equalsLabel)) #Minus sign button.
        numSub.grid(row = 3, column = 3, padx = 5, pady = 5)
        numSub.config(font = ("Sans", 10))

        numMult = Button(calcButtonFrame, text = "*", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: opPress("*", displayNums, equalsLabel)) #Multiplication button.
        numMult.grid(row = 4, column = 3, padx = 5, pady = 5)
        numMult.config(font = ("Sans", 10))

        numDiv = Button(calcButtonFrame, text = "/", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: opPress("/", displayNums, equalsLabel)) #Division button
        numDiv.grid(row = 5, column = 3, padx = 5, pady = 5)
        numDiv.config(font = ("Sans", 10))

        numPower = Button(calcButtonFrame, text = "POW", height = 1, width = 9, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: opPress("**", displayNums, equalsLabel)) #Power/exponent button.
        numPower.grid(row = 4, column = 4)
        numPower.config(font = ("Sans", 10))

        equalsButton = Button(calcButtonFrame, text = "=", height = 1, width = 9, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: equalsPress(equalsLabel, displayNums)) #Equals button to solve problem.
        equalsButton.grid(row = 6, column = 4)
        equalsButton.config(font = ("Sans", 10))

        clearButton = Button(calcButtonFrame, text = "CLEAR", height = 1, width = 9, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: clearPress(equalsLabel, displayNums)) #Clears display and all working variables pertaining to current problem.
        clearButton.grid(row = 5, column = 4)
        clearButton.config(font = ("Sans", 10))

        deleteButton = Button(calcButtonFrame, text = "DEL", height = 1, width = 9, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: delete(displayNums)) #Delete/backspace button.
        deleteButton.grid(row = 2, column = 4)
        deleteButton.config(font = ("Sans", 10))

        leftParenth = Button(calcButtonFrame, text = "(", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: parenth(displayNums, "(")) #Left parentheses button.
        leftParenth.grid(row = 6, column = 0)
        leftParenth.config(font = ("Sans", 10))

        rightParenth = Button(calcButtonFrame, text = ")", height = 1, width = 2, bd = 4, bg = "black", fg = "white", highlightbackground = "white", highlightthickness = 4, command = lambda: parenth(displayNums, ")")) #Right parentheses button.
        rightParenth.grid(row = 6, column = 1)
        rightParenth.config(font = ("Sans", 10))

        functions = Button(calcButtonFrame, text = "FUNCTIONS", height = 1, width = 9, bd = 4, bg = "white", fg = "black", highlightbackground = "white", highlightthickness = 4, command = lambda: functionsPress(functions, displayNums, equalsLabel, root)) #Functions button to display further calculator operations.
        functions.grid(row = 3, column = 4)
        functions.config(font = ("Sans", 10))

class RootWindow(): #creates main window in a class, so global variables can be avoided
    root = Tk(className = 'ViperCalc')
    root.geometry("300x400")
    root.configure(background = "black")
    if (platform.system() == "Windows"): #Makes sure a usable icon is loaded for the host OS, three most popular OSs are included.
        root.iconbitmap("vipercalc-logo-square.ico")
    if (platform.system() == "Linux"):
        root.iconbitmap("vipercalc-logo-square.png")
    if (platform.system() == "Mac OS X"):
        root.iconbitmap("vipercalc-logo-square.icns")


def main(): #Initializes window when called below, keeps it running.
    root = RootWindow.root
    Calc()
    root.mainloop()

main() #initializes main function and starts program
