from __future__ import print_function
import sys, random, enchant, shelve, tempfile, uuid, datetime
from PyQt5 import QtWidgets, QtCore, QtGui

def roll_board():
    """roll_board is a function which creates an array
    of range 0,16 containing the standard boggle dice randomized
    in location and value as list "board". It also formats a list
    to add brackets around each letter to create "fboard". Finally
    the roll_board function prints out the board, formatted. It also
    replaces the Qu die with a % if it rolls that (after printing)."""
    board = [random.choice(["A","E","A","N","E","G"]),random.choice(["A","H","S","P","C","O"]),random.choice(["A","S","P","F","F","K"]),random.choice(["O","B","J","O","A","B"]),random.choice(["I","O","T","M","U","C"]),random.choice(["R","Y","V","D","E","L"]),random.choice(["L","R","E","I","X","D"]),random.choice(["E","I","U","N","E","S"]),random.choice(["W","N","G","E","E","H"]),random.choice(["L","N","H","N","R","Z"]),random.choice(["T","S","T","I","Y","D"]),random.choice(["O","W","T","O","A","T"]),random.choice(["E","R","T","T","Y","L"]),random.choice(["T","O","E","S","S","I"]),random.choice(["T","E","R","W","H","V"]),random.choice(["N","U","I","H","M","Qu"])]
    random.shuffle(board)
    fboard = []
    for index in range(0,16):
        fboard.append("["+board[index]+"]")
    print("{:<5} {:<5} {:<5} {:<5}".format(fboard[0],fboard[1],fboard[2],fboard[3]))
    print("{:<5} {:<5} {:<5} {:<5}".format(fboard[4],fboard[5],fboard[6],fboard[7]))
    print("{:<5} {:<5} {:<5} {:<5}".format(fboard[8],fboard[9],fboard[10],fboard[11]))
    print("{:<5} {:<5} {:<5} {:<5}".format(fboard[12],fboard[13],fboard[14],fboard[15]))
    for i in range(0,16):
        if board[i] == "Qu":
            board[i] = "%"
    print()
    return board

def get_input():
    """get_input is a function which uses the assignment
    specified formatting in order to compile a list of the player's
    answers to the boggle board to then be computed. It exits upon
    the entry of the word 'X'. It also formats all the input as Uppercase
    and replaces the string QU with % (which is my currently operating solution
    for the QU problem. This all is stored in returned formatted words ("fword")"""
    print("Start typing your words! (press enter after each word and enter 'X' when done):")
    entry = "go"
    global words
    words = []
    while entry != "X" and entry != "x":
        entry = raw_input(">")
        if(entry != "X" and entry != "x"):
            words.append(entry)
    fwords = []
    counter = 0
    for word in words:
        fwords.append(word.upper())
    for word in fwords:
        fwords[counter] = word.replace("QU","%")
        counter = counter + 1
    #for word in fwords:
        #print(word)
    return fwords

def check_word(word,depth,board,used,position):
    """check_word is a recursive function which takes as parameters
    "word" - the word being checked
    "depth" - the character to check in the word
    "board" - the boggle board to use
    "used" - an array of used positions
    "position" - the current position checking from
    Given all of these the function then recursively checks
    in a depth first pattern if the word is in the boggle board.
    It returns a boolean True if found, False if otherwise."""
    if position == 0:
        adjacents = [1,4,5]
    elif position < 3:
        adjacents = [-1,1,3,4,5]
    elif position == 3:
        adjacents = [-1,3,4]
    elif position == 4 or position == 8:
        adjacents = [-4,-3,1,4,5]
    elif position == 5 or position == 6 or position == 9 or position == 10:
        adjacents = [-5,-4,-3,-1,1,3,4,5]
    elif position == 7 or position == 11:
        adjacents = [-5,-4,-1,3,4]
    elif position == 12:
        adjacents = [-4,-3,1]
    elif position < 15:
        adjacents = [-5,-4,-3,-1,1]
    else:
        adjacents = [-5,-4,-1]

    result = False;
    if depth == len(word):
        return True
    for adjacent in adjacents:
        #print("Checking neighbor "+str(adjacent))
        if position+adjacent > 15 or position+adjacent < 0:
            #print("Blank")
            continue
        if board[position+adjacent] == word[depth] and used[position+adjacent] == False:
            #print("found a letter!"+word[depth])
            used[position+adjacent] = True;
            result = check_word(word,depth+1,board,used,position+adjacent)
            if result == True:
                break
        #else:
            #print("Not the right letter!")
    used[position] = False
    return result

def check_list(board,fwords):
    """check_list is a function which takes in a board and a formatted list
    of words to check. It calls check_word and assumes that there is a public
    list "words" containing the list of corresponding words to fwords. It
    first performs checking to make sure the word is not a duplicate,
    then of appropriate length, then checks to see if it exists in the board
    and is a valid dictionary word and calculates the results."""
    used = []
    d = enchant.Dict("en_US")
    for i in range(0,16):
        used.append(False)
    position = 0
    counter = 0
    result = False
    score = 0
    for word in fwords:

        skip = False
        if counter > 0:
            for i in range(0,counter):
                if word == fwords[i]:
                    print("The word "+words[counter]+" has already been used.")
                    skip = True
        if skip:
            counter = counter + 1
            continue
        length = len(word)
        if length < 3:
            print("The word "+words[counter]+" is too short.")
            counter = counter + 1
            continue

        elif length < 5:
            value = 1
        elif length < 6:
            value = 2
        elif length < 7:
            value = 3
        elif length < 8:
            value = 5
        else:
            value = 11

        for position in range(0,16):
            if board[position] == word[0]:
                depth = 1
                used[position] = True
                result = check_word(word,depth,board,used,position)
            if result:
                if d.check(words[counter]):
                    print("The word "+words[counter]+" is worth "+str(value)+" point",end='')
                    if value == 1:
                        print(".")
                    else:
                        print("s.")
                    score = score + value
                else:
                    print("The word "+words[counter]+" is ... not word.")
                break

        if not result:
            print("The word "+words[counter]+" is not present.")
        counter = counter + 1
        result = False
        i = 0
        for n in used:
            used[i] = False
            i = i+1
    return score

def play_boggle():
    """play_boggle is the driver function to execute a boggle game. It calls roll_board,
    get_input, and check_list then prints your score and passes it through as a return
    value for further use."""
    board = roll_board()
    fwords = get_input()
    score = check_list(board,fwords)
    print("Your total score is "+str(score)+" point",end='')
    if score == 1:
        print("!")
    else:
        print("s!")
    return score

def format_words(words):
    """formats words for dictionary checking"""
    fwords = []
    counter = 0
    for word in words:
        fwords.append(word.upper())
    for word in fwords:
        fwords[counter] = word.replace("QU","%")
        counter += 1;
    return fwords

class BoggleWindow(QtWidgets.QMainWindow):
    """ Boggle window contains the components for the game
    and launches the window, as well as poling for an initial
    load window."""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        popup = StartScreen()
        choice = popup.exec_()
        if choice == QtWidgets.QMessageBox.Yes:
            self.setup()
            self.loadGame()
        else:
            self.setup()


    def setup(self):
        self.setWindowTitle('Boggle Game')
        self.setToolTip("Let's Play Boggle!")

        self.boggle_game = BoggleGame(self)
        self.setCentralWidget(self.boggle_game)

        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(QtWidgets.qApp.quit)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)
        file_menu.addAction("Save",self.saveGame)
        file_menu.addAction("Load",self.loadGame)

        self.show()

    def closeEvent(self, event):
        popup = QuitMessage()
        reply = popup.exec_()
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def saveGame(self):
        s = shelve.open('boggle.save')
        ids = open("boggle.ids", "a")
        uid = str(uuid.uuid4())
        ids.write(uid+"\n")
        ids.close()
        s[uid] = {"when": datetime.datetime.now(), "title": datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "uid": uid, "letters": self.boggle_game.board.letters, "words": self.boggle_game.list.words, "text": self.boggle_game.input.text(), "time": self.boggle_game.timer.time.remainingTime(), "ticker": self.boggle_game.timer.ticker.remainingTime(), "display": self.boggle_game.timer.display.intValue()}
        s.close()

    def loadGame(self):
        global suid
        try:
            s = shelve.open('boggle.save')
        except:
            print("No Saves to Load")
            return
        dialog = LoadDialog(self,s)
        dialog.exec_()
        self.boggle_game.board.letters = s[suid]["letters"]
        self.boggle_game.board.update()
        self.boggle_game.list.words = s[suid]["words"]
        self.boggle_game.list.update()
        self.boggle_game.input.setText(s[suid]["text"])
        self.boggle_game.input.setReadOnly(False)
        self.boggle_game.timer.time.stop()
        self.boggle_game.timer.time.start(s[suid]["time"])
        self.boggle_game.timer.ticker.stop()
        self.boggle_game.timer.ticker.start(s[suid]["ticker"])
        self.boggle_game.timer.display.display(s[suid]["display"])

class LoadDialog(QtWidgets.QDialog):
    """Load dialogue uses a passed in shelf to grab all the saved states
    it then sets the suid to represent the state to load."""
    def __init__(self, parent, s):
        QtWidgets.QDialog.__init__(self, parent)
        self.setup(s)

    def setup(self, s):
        global suid
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        keys = []
        try:
            ids = open("boggle.ids", "r")
        except:
            print("Error!! .ids file deleted or no files ever saved!!")
            return
        for line in ids.readlines():
            keys.append(line.rstrip())
        self.text = QtWidgets.QLabel("Please select a file to load: ")
        self.list = QtWidgets.QListWidget(self)
        self.grid.addWidget(self.text,1,1,1,1)
        self.grid.addWidget(self.list,2,1,4,1)
        self.allFiles = []
        for key in keys:
            print(s[key])
            print(type(s[key]))
            self.allFiles.append(s[key])
        self.allFiles = sorted(self.allFiles, key=lambda k: k['when'], reverse=True)
        self.list.itemClicked.connect(self.item_click)
        for save in self.allFiles:
            self.list.addItem(save["title"])

    def item_click(self, item):
        global suid
        suid = self.allFiles[self.list.row(item)]["uid"]
        self.close()

class BoggleGame(QtWidgets.QWidget):
    """BoggleGame contains the actual components and serves
    as the windows main component."""
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        self.board = BoggleBoard(self)
        self.list = TextList(self)
        self.input = InputBox(self)
        self.timer = BoggleTimer(self)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.board, 1, 1, 4, 4)
        self.grid.addWidget(self.list, 1, 5, 4, 1)
        self.grid.addWidget(self.input, 5, 1, 1, 5)
        self.grid.addWidget(self.timer, 5, 5, 1, 1, QtCore.Qt.AlignRight)

        self.input.returnPressed.connect(self.make_message())
        self.input.returnPressed.connect(self.input.setup)
        self.timer.time.timeout.connect(self.stoptime)

    def stoptime(self):
        """ evaluation execution """
        global words
        words = self.list.words
        self.timer.time.stop()
        self.input.setReadOnly(True)
        score = check_list(self.board.letters,format_words(self.list.words))
        popup = ScoreScreen(score)
        reply = popup.exec_()
        if reply == QtWidgets.QMessageBox.Yes:
            self.board.letters = roll_board()
            self.board.update()
            self.list.setup()
            self.input.setText("")
            self.input.setReadOnly(False)
            self.timer.restart()

    def make_message(self):
        def message():
            self.list.addWord(self.input.text())
        return message

class BoggleBoard(QtWidgets.QWidget):
    """The boggle grid."""
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        self.letters = []
        self.letters = roll_board()
        #get a board from the boggle function loaded in letters
        #make labels out of the board and store them in labels
        self.labels = []
        for letter in self.letters:
            if letter == '%':
                letter = "Qu"
            self.labels.append(QtWidgets.QLabel(letter))
            if letter == "Qu":
                letter = '%'
        for label in self.labels:
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            label.setStyleSheet("border:1px solid rgb(180, 180, 180); font: bold 48px arial, sans-serif; color: blue") #isn't this cool!? CSS in a python program!
        self.setFixedSize(500,500)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.labels[0], 1, 1, 1, 1)
        self.grid.addWidget(self.labels[1], 1, 2, 1, 1)
        self.grid.addWidget(self.labels[2], 1, 3, 1, 1)
        self.grid.addWidget(self.labels[3], 1, 4, 1, 1)
        self.grid.addWidget(self.labels[4], 2, 1, 1, 1)
        self.grid.addWidget(self.labels[5], 2, 2, 1, 1)
        self.grid.addWidget(self.labels[6], 2, 3, 1, 1)
        self.grid.addWidget(self.labels[7], 2, 4, 1, 1)
        self.grid.addWidget(self.labels[8], 3, 1, 1, 1)
        self.grid.addWidget(self.labels[9], 3, 2, 1, 1)
        self.grid.addWidget(self.labels[10], 3, 3, 1, 1)
        self.grid.addWidget(self.labels[11], 3, 4, 1, 1)
        self.grid.addWidget(self.labels[12], 4, 1, 1, 1)
        self.grid.addWidget(self.labels[13], 4, 2, 1, 1)
        self.grid.addWidget(self.labels[14], 4, 3, 1, 1)
        self.grid.addWidget(self.labels[15], 4, 4, 1, 1)

    def update(self):
        counter = 0
        for letter in self.letters:
            if letter == '%':
                letter = "Qu"
            self.labels[counter].setText(letter)
            if letter == "Qu":
                letter = '%'
            counter += 1

class TextList(QtWidgets.QTextEdit):
    """The inputted words"""
    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self, parent)
        self.setup()


    def setup(self):
        self.words = []
        self.setFixedSize(300,500)
        self.text = ""
        self.setReadOnly(True)
        self.setText(self.text)

    def addWord(self, word):
        if(word == ""):
            return
        self.words.append(word)
        self.text = ""
        for word in self.words:
            self.text = self.text + word + "\n"
        self.setText(self.text)

    def update(self):
        self.text = ""
        for word in self.words:
            self.text = self.text + word + "\n"
        self.setText(self.text)

class InputBox(QtWidgets.QLineEdit):
    """ The box for new inputs """
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.setup()

    def setup(self):
        self.setText("")
        self.setFixedWidth(690);
        #set action on enter to addWord(maybe located in container)

class BoggleTimer(QtWidgets.QWidget):
    """All timer logic and display"""
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self,parent)
        self.setup()

    def setup(self):

        self.time = QtCore.QTimer()
        self.ticker = QtCore.QTimer()
        self.ticker.start(1000)
        self.time.start(180000)
        self.display = QtWidgets.QLCDNumber()
        self.display.setSegmentStyle(self.display.Flat)
        self.display.setStyleSheet("color: black;") #isn't this cool!? CSS in a python program!
        self.display.display(180)
        self.ticker.timeout.connect(self.ticktime)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.display.setFixedWidth(100)
        self.grid.addWidget(self.display,1,1,1,1)
        #self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #set event - on update change display
        #set event - on zero turn off input and evaluate

    def ticktime(self):
        self.display.display(self.display.intValue() - 1)
        if(self.display.intValue() != 0):
            self.ticker.start(1000)
        else:
            self.ticker.stop()

    def restart(self):
        self.time.start(180000)
        self.ticker.start(1000)
        self.display.display(180)

#below are various dialogues for different circumstances
class ScoreScreen(QtWidgets.QMessageBox):
    def __init__(self,score):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Time's Up!\nScore: "+str(score)+"\nWould you like to play again?")
        self.addButton(self.No)
        self.addButton(self.Yes)

class StartScreen(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Welcome to boggle! Would you like to load a saved game?")
        self.addButton(self.No)
        self.addButton(self.Yes)

class QuitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Do you really want to quit?")
        self.addButton(self.No)
        self.addButton(self.Yes)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = BoggleWindow()
    app.exec_()
