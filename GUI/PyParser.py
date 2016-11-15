from Tkinter import *
import tkMessageBox
import operator
import tkFont
import nltk

# Classes And Functions

# Stack Definition

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


class Node(object):
    """
    Tree node: left and right child + data which can be any object
    """

    def __init__(self, data=None, left=None, right=None):
        """
        Node Constructor
        @param data node data object
        """
        self.left = left
        self.right = right
        self.data = data


    def setRootVal(self, data):
        self.data = data

    def insertLeft(self, data, left=None, right=None):
        """
        Insert new node with data
        @param data node data object to insert
        """
        if self.left is None:
            self.left = Node(data, left, right)

    def insertRight(self, data, left=None, right=None):
        """
        Insert new node with data
        @param data node data object to insert
        """
        if self.right is None:
            self.right = Node(data, left, right)

    def print_each_level(self):
        # Start off with root node

        printTree = Toplevel(root)
        thislevel = [self]
        canvas = Canvas(printTree, width=1600, height=1600)
        canvas.pack(side="top", fill="both", expand=True)

        n = 560
        a = 5
        i = 0
        m = 0
        q = n
        # While there is another level
        while thislevel:
            nextlevel = list()

            # Print all the nodes in the current level, and store the next level in a list
            for node in thislevel:
                if (i % 2) == 0:
                    canvas_id1 = canvas.create_text(n, a + 10, anchor="nw")
                    canvas.itemconfig(canvas_id1, text=node.data)
                    n += 2 * m
                else:
                    canvas_id1 = canvas.create_text(n, a + 10, anchor="nw")
                    canvas.itemconfig(canvas_id1, text=node.data)
                    n += 2 * m
                if node.left: nextlevel.append(node.left)
                if node.right: nextlevel.append(node.right)
            i += 1
            n = q - (q / 2)
            q = n
            m = n
            a += 65
            thislevel = nextlevel



class Tree(Stack, Node):
    def var_init(self, inexp):
        for i in range(0, len(inexp)):
            try:
                inexp[i] = float(inexp[i])
            except:
                inexp[i] = inexp[i]
        return inexp

    def modifyExp(self, exp):
        for i in range(0, len(exp) - 2):
            if exp[i] == ')' and exp[i + 1] in ['+', '-', '*', '/', '%', '^']:
                if type(exp[i + 2]) is float:
                    if exp[i + 1] in ['*', '/', '%', '^']:
                        exp[i + 2:i + 2] = ['(']
                        exp[i + 4:i + 4] = [exp[i + 1]]
                        exp[i + 5:i + 5] = [1.0]
                        exp[i + 6:i + 6] = [')']
                        break
                    else:
                        exp[i + 2:i + 2] = ['(']
                        exp[i + 4:i + 4] = [exp[i + 1]]
                        exp[i + 5:i + 5] = [0.0]
                        exp[i + 6:i + 6] = [')']
                        break
            elif type(exp[i]) is float and exp[i + 1] in ['+', '-', '*', '/', '%', '^']:
                if exp[i + 2] == '(':
                    if exp[i + 1] in ['*', '/', '%', '^']:
                        exp[i:i] = ['(']
                        exp[i + 3:i + 3] = [1.0]
                        exp[i + 4:i + 4] = [')']
                        exp[i + 5:i + 5] = [exp[i + 2]]
                        break
                    else:
                        exp[i:i] = ['(']
                        exp[i + 3:i + 3] = [0.0]
                        exp[i + 4:i + 4] = [')']
                        exp[i + 5:i + 5] = [exp[i + 2]]
                        break
        return exp

    def buildTree(self, exp):
        lst = self.modifyExp(exp)
        treeStack = []
        operatorStack = Stack()
        operandStack = Stack()
        bracketsStack = Stack()

        bracketsStack.push('start')
        while not bracketsStack.isEmpty():
            for i in lst:
                if i == '(':
                    bracketsStack.push(i)
                elif type(i) is float:
                    operandStack.push(i)
                elif i in ['+', '-', '*', '/', '%', '^']:
                    operatorStack.push(i)
                elif i == ')':
                    if operandStack.isEmpty() and not operatorStack.isEmpty():
                        tTree = Node()
                        mTree = Node()
                        tTree.setRootVal(operatorStack.pop())
                        mTree = treeStack.pop()
                        tTree.insertRight(mTree.data, mTree.left, mTree.right)
                        mTree = treeStack.pop()
                        tTree.insertLeft(mTree.data, mTree.left, mTree.right)
                        binTree = tTree
                        del tTree
                        treeStack.append(binTree)
                    elif operandStack.isEmpty() and operatorStack.isEmpty():
                        bracketsStack.pop()
                    elif not operatorStack.isEmpty() and not operandStack.isEmpty():
                        tTree = Node()
                        tTree.setRootVal(operatorStack.pop())
                        tTree.insertRight(operandStack.pop())
                        tTree.insertLeft(operandStack.pop())
                        binTree = tTree
                        del tTree
                        treeStack.append(binTree)
                    bracketsStack.pop()
                    if bracketsStack.size() == 1:
                        bracketsStack.pop()
                        break
        binTree = treeStack.pop()
        binTree.print_each_level()


def arithmeticParse(event):
    root.iconify()
    arithWindow = Toplevel(root)
    arithWindow.geometry('1024x630+100+100')

    # Menu

    menu = Menu(arithWindow)
    arithWindow.config(menu=menu)
    arithWindow.configure(background='#093145')

    aboutMenu = Menu(menu)
    menu.add_cascade(label="About", menu=aboutMenu)
    aboutMenu.add_command(label="Software", command=aboutSoftware)
    aboutMenu.add_separator()
    aboutMenu.add_command(label="Developers", command=develepors)

    helpMenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="Arithmetic", command=arithmeticHelp)

    # Arithmetic Parser Layout

    exp = StringVar()

    arithmeticLabel = Label(arithWindow, text="Arithmetic Parser", pady=10, font=mainFont, fg="#EFD469", bg="#093145")
    arithmeticLabel.place(relx="0.25", rely="0.05")

    myLabel = Label(arithWindow, text="Enter Fully Parenthesised Arithmetic Expression ", pady=10, padx=10,
                    font=textFont, fg="white", bg="#093145")
    myEntry = Entry(arithWindow, width=50, textvariable=exp)
    myButton = Button(arithWindow, text="Generate Notations", font=textFont, fg="#093145", bg="#EFD469")
    myLabel.place(relx="0.03", rely="0.24")
    myEntry.place(relx="0.53", rely="0.27")
    myButton.place(relx="0.2", rely="0.4")

    # Function

    def expressionTree(event):
        clearButton = Button(arithWindow, text="Clear Window", font=textFont, fg="#093145", bg="#EFD469")
        clearButton.place(relx="0.6", rely="0.4")

        treeButton = Button(arithWindow, text="Print Tree", font=textFont, fg="#093145", bg="#EFD469")
        treeButton.place(relx="0.44", rely="0.4")

        expression = exp.get()
        lst = expression.split()
        parIncrement = 0
        operCount = 0
        parDecrement = 0
        minNoOfParen = 0
        for i in lst:
            if i.isalpha():
                tkMessageBox.showwarning("Ouch!", "Only Numeric Data Is Allowed")
                break
            if i == '(':
                parIncrement += 1
            elif i == ')':
                parDecrement += 1
            elif i in ['+', '-', '*', '/', '^', '%']:
                operCount += 1
                minNoOfParen += 2

        if ('{' or '[' or '}' or ']' or '<' or '>') in lst:
            tkMessageBox.showwarning("Ouch!", "Only '(' and ')' Are Allowed ")
            arithWindow.destroy()
            root.deiconify()
        if parIncrement != parDecrement or lst[0] is not '(' or minNoOfParen > (parIncrement + parDecrement):
            tkMessageBox.showwarning("Ouch!", "Invalid!\nExpression is Not Correctly Parenthesized.")
        else:
            treeLabel1 = Label(arithWindow, text="PostFix Expression", pady=5, font=textFont, fg="white", bg="#093145")
            treeLabel3 = Label(arithWindow, text="PreFix Expression", pady=5, font=textFont, fg="white", bg="#093145")
            treeLabel1.place(relx="0.27", rely="0.62")
            treeLabel3.place(relx="0.27", rely="0.72")

            # Reverse Polish Notation

            def reversePolishNotation(exp):
                for i in range(len(exp)):
                    try:
                        exp[i] = float(exp[i])
                    except:
                        exp[i] = exp[i]

                s = Stack()
                expArray = []
                for i in exp:
                    if i == '(':
                        s.push('(')
                    elif type(i) is float:
                        expArray.append(i)
                    elif i in ['+', '-', '*', '/', '^', '%']:
                        s.push(i)
                    elif i == ')':
                        for j in range(s.size() - 1, 0, -1):
                            if s.peek() in ['+', '-', '*', '/', '^', '%']:
                                expArray.append(s.pop())
                            elif s.peek() == '(':
                                s.pop()
                                break
                return expArray

            # RPN Evaluation

            def postOrderEval(exp):
                opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv,
                         '^': operator.pow, '%': operator.mod}
                eStack = Stack()
                for i in exp:
                    if type(i) is float:
                        eStack.push(i)
                    elif i in ['+', '-', '*', '/', '^', '%']:
                        operand1 = eStack.pop()
                        operand2 = eStack.pop()
                        eStack.push(opers[i](operand2, operand1))
                return eStack.peek()

            # PreFix Expression

            def preFixExpression(exp):
                exp = exp[::-1]
                for i in range(0, len(exp)):
                    if exp[i] == '(':
                        exp[i] = ')'
                    elif exp[i] == ')':
                        exp[i] = '('
                preExp = reversePolishNotation(exp)
                preExp = preExp[::-1]

                return preExp

            postFix = reversePolishNotation(lst)
            treeLabel2 = Label(arithWindow, text=postFix, pady=10, padx=10, font=textFont, fg="white", bg="#093145")
            treeLabel2.place(relx="0.6", rely="0.62")

            preFix = preFixExpression(lst)
            treeLabel4 = Label(arithWindow, text=preFix, pady=10, padx=10, font=textFont, fg="white", bg="#093145")
            treeLabel4.place(relx="0.6", rely="0.72")

            answerLabel = Label(arithWindow, text="Answer To The Expression Is ", pady=10, padx=10, font=textFont,
                                fg="white", bg="#093145")
            answer = postOrderEval(postFix)
            answerLabel1 = Label(arithWindow, text=answer, pady=5, padx=5, font=textFont, fg="white", bg="#093145")
            answerLabel.place(relx="0.26", rely="0.82")
            answerLabel1.place(relx="0.64", rely="0.82")

        def clearWindow(event):
            treeLabel2.destroy()
            answerLabel1.destroy()
            treeLabel4.destroy()

        clearButton.bind("<Button-1>", clearWindow)

        def treeGUI(event):
            treeObj = Tree()
            exp = treeObj.var_init(lst)
            treeObj.buildTree(exp)

        treeButton.bind("<Button-1>", treeGUI)

    myButton.bind("<Button-1>", expressionTree)


# Functions

def aboutSoftware():
    tkMessageBox.showinfo("About Software", "String and Arithmetic Parser In Python!\n\tVersion 1.0")


def develepors():
    tkMessageBox.showinfo("Developers", "\tMeghna Singh\t\n\tPrerna Arora\t\n\tAnand Sethi\t")


def arithmeticHelp():
    help_arithWindow = Toplevel(root)
    help_arithWindow.title("Arithmetic Guide")
    help_arithWindow.geometry('900x400+150+150')
    help_arithWindow.configure(background="#093145")

    topFrame = Frame(help_arithWindow)
    topFrame.pack()
    topFrame.configure(background="#093145")
    bottomFrame = Frame(help_arithWindow)
    bottomFrame.pack(side=BOTTOM)

    head_font = tkFont.Font(family="Trebuchet MS", size=27, weight="bold")
    arithHeadLabel = Label(topFrame, text="Arithmetic Guide", font=head_font, bg="#093145", fg="#EFD469")
    arithHeadLabel.pack()

    b_font = ("Verdana", 10, "bold")

    bLabel = Label(topFrame,
                   text="Arithmetic parser shows the post fix notation and evaluates the answer of the given fully  parenthesized expression.",
                   font=b_font, bg="#093145", fg="white", padx=10, pady=10)
    bLabel.pack()

    S = Scrollbar(bottomFrame)
    T = Text(bottomFrame, height=500, width=900, fg="white", bg="#093145")
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    sub_heading = """

    HOW TO USE ARITHMETIC PARSER:"""

    quote = """


    Insert a fully parenthesized expression in the first entry box. Don't forget to add space between the 
    operators, operands and parenthesis. After that click on 'Generate Expression Tree' and get the 
    required parsed expression.
    
    In infix arithmetic expressions, operators are placed between two operands-- as shown in the examples 
    below:

        2 + 3    or    1 + ( 2 + 3 ) * ( 4 * 5 )    
        
    FULLY PARENTHESIZED ARITHMETIC EXPRESSION: 
    
    
    A fully parenthesized expression is a method of writting arithmetic expressions in which parentheses
    are placed around each pair of operands and its associated operator. A fully parenthesized arithmetic
    expression is an infix arithmetic expression where every operator and its arguments are contained in 
    parentheses, as seen in following:
        
        ( 2 + 3 )    or    ( 1 + ( 2 + 3 ) * ( 4 * 5 ) )
        
    Note that a fully parenthesized expression explicitly details the order in which the operators are to
    be applied. Consequently, in the evaluation of such expressions,operator precedence and associativity
    don't really matter at all.


    For Example :

    ( ( 5 + 5) * ( 9 * 3 ) )

    The above example gives the output :

    *
    +
    5
    5
    *
    9
    3

    And evaluates to : 270


            """
    T.insert(0.0, sub_heading)
    T.insert(END, quote, welcomeFont)


def stringHelp():
    help_stringWindow = Toplevel(root)
    help_stringWindow.title("String Guide")
    help_stringWindow.geometry('900x400+150+150')
    help_stringWindow.configure(background="#093145")

    topFrame = Frame(help_stringWindow)
    topFrame.pack()
    topFrame.configure(background="#093145")
    bottomFrame = Frame(help_stringWindow)
    bottomFrame.pack(side=BOTTOM)

    head_font = tkFont.Font(family="Trebuchet MS", size=27, weight="bold")
    headLabel = Label(topFrame, text="String Guide", font=head_font, bg="#093145", fg="#EFD469")
    headLabel.pack()

    b_font = ("Verdana", 10, "bold")
    secondLabel = Label(topFrame,
                        text="String parser shows the parse tree of the given sentence with the help of given grammar.",
                        font=b_font, bg="#093145", fg="white", padx=10, pady=10)
    secondLabel.pack()

    S = Scrollbar(bottomFrame)
    T = Text(bottomFrame, height=500, width=900, bg="#093145", fg="white")
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    sub_heading1 = """
    
    HOW TO USE STRING PARSER: """

    quote1 = """


    A String Parser is basically used to make a parse tree from a given grammar and sentence. First ,
    enter a meaningful sentence in English. In the next entry box that says "Enter Your Grammar" enter
    the complete grammar as explained in the example below. The grammar consists of production rule that
    consists of terminals and non terminals.

    Terminal symbols are literal symbols which may appear in the outputs of the  production  rules  of  a 
    formal grammar and which cannot be changed using the rules of the  grammar.  Applying  the  rules 
    recursively to a source string of symbols will usually terminate in a final output string consisting
    only of terminal symbols.

    Nonterminal symbols are those symbols which can be replaced. They may also be called simply syntactic 
    variables. A formal grammar includes a start symbol, a designated member of the set of nonterminals 
    from which all the strings in a language may be derived by successive applications of the production
    rules.
    
    In fact, the language defined by a grammar is precisely the set of terminal strings that can be so 
    derived. A grammar is defined by production rules (or just 'productions') that specify which symbols
    may replace which other symbols; these rules may be used to generate strings, or to parse them. Each
    such rule has a head, or left-hand side, which consists of the string that may be replaced, and a
    body, or right-hand side, which consists of a string that may replace it. Rules are often written in
    the form head ->  body; e.g., the rule a -> b specifies that a can be replaced by b.

    For Example :

    Sentence : 
    I shot an elephant in my pajamas
    
    Grammar:
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | 'I'
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'elephant' | 'pajamas'
    V -> 'shot'
    P -> 'in'  

    Another Example,

    Sentence : 
    The dog chased a cat
    
    Grammar:
    S -> NP VP
    PP -> P NP
    NP -> Det N | NP PP
    VP -> V NP | VP PP
    Det -> 'a' | 'The' |'the'
    N -> 'dog' | 'cat'
    V -> 'chased' | 'sat'
    P -> 'on' | 'in'

    
    Here the words S,NP,VP etc are the part of POS TAG LIST.
    The list is as :
    No.     Tag     Description
    1.      CC      Coordinating conjunction
    2.      CD      Cardinal number
    3.      DT      Determiner
    4.      EX      Existential there
    5.      FW      Foreign word
    6.      IN      Preposition or subordinating conjunction
    7.      JJ      Adjective
    8.      JJR     Adjective, comparative
    9.      JJS     Adjective, superlative
    10.     LS      List item marker
    11.     MD      Modal
    12.     NN      Noun, singular or mass
    13.     NNS     Noun, plural
    14.     NNP     Proper noun, singular
    15.     NNPS    Proper noun, plural
    16.     PDT     Predeterminer
    17.     POS     Possessive ending
    18.     PRP     Personal pronoun
    19.     PRP$    Possessive pronoun
    20.     RB      Adverb
    21.     RBR     Adverb, comparative
    22.     RBS     Adverb, superlative
    23.     RP      Particle
    24.     SYM     Symbol
    25.     TO      to
    26.     UH      Interjection
    27.     VB      Verb, base form
    28.     VBD     Verb, past tense
    29.     VBG     Verb, gerund or present participle
    30.     VBN     Verb, past participle
    31.     VBP     Verb, non-3rd person singular present
    32.     VBZ     Verb, 3rd person singular present
    33.     WDT     Wh-determiner
    34.     WP      Wh-pronoun
    35.     WP$     Possessive wh-pronoun
    36.     WRB     Wh-adverb
	
            """
    T.insert(0.0, sub_heading1)
    T.insert(END, quote1, welcomeFont)


def quit(event):
    answer = tkMessageBox.askyesno("Seriously?", "Are You Sure?")
    if answer > 0:
        root.destroy()


def stringParse(event):
    root.iconify()
    stringWindow = Toplevel(root)
    stringWindow.geometry('1070x630+100+100')
    stringWindow.configure(background="#093145")

    # Menu

    menu = Menu(stringWindow)
    stringWindow.config(menu=menu)

    aboutMenu = Menu(menu)
    menu.add_cascade(label="About", menu=aboutMenu)
    aboutMenu.add_command(label="Software", command=aboutSoftware)
    aboutMenu.add_separator()
    aboutMenu.add_command(label="Developers", command=develepors)

    helpMenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="String", command=stringHelp)

    # String Layout

    sentence = StringVar()

    stringLabel = Label(stringWindow, text="String Parser", padx=20, pady=10, font=mainFont, fg="#EFD469", bg="#093145")
    sentencelabel = Label(stringWindow, text="Enter Your Sentence ", pady=10, padx=10, font=textFont, fg="white",
                          bg="#093145")
    grammarLabel = Label(stringWindow, text="Enter Your Grammar ", pady=10, padx=10, font=textFont, fg="white",
                         bg="#093145")
    sentenceEntry = Entry(stringWindow, width=82, textvariable=sentence)
    grammarText1 = Text(stringWindow, height=5, width=65)
    grammarText2 = Text(stringWindow, height=5, width=65)
    parseTree = Button(stringWindow, text="Generate Parse Tree", font=textFont, fg="#093145", bg="#EFD469", bd=4)
    parseTree2 = Button(stringWindow, text="Generate Second Parse Tree", font=textFont, fg="#093145", bg="#EFD469",
                        bd=4)
    quitButton = Button(stringWindow, text="Go Back", width=17, font=textFont, fg="#093145", bg="#EFD469", bd=4)

    stringLabel.place(relx="0.32", rely="0.04")
    sentencelabel.place(relx="0.05", rely="0.28")
    sentenceEntry.place(relx="0.32", rely="0.31")
    grammarLabel.place(relx="0.05", rely="0.42")
    grammarText1.place(relx="0.32", rely="0.45")
    grammarText2.place(relx="0.32", rely="0.65")
    parseTree.place(relx="0.12", rely="0.80")
    parseTree2.place(relx="0.12", rely="0.89")
    quitButton.place(relx="0.68", rely="0.80")

    # Main Operation

    def stringParser(event):
        senten = sentence.get()
        word = senten.split(".")
        first_sen = word[0].split()
        second_sen = word[1].split()

        def firstParseTree(first_sen):
            grammar1 = grammarText1.get("0.0", END)
            grammarPath1 = nltk.grammar.CFG.fromstring(grammar1, encoding='utf-8')

            ch_parser1 = nltk.ChartParser(grammarPath1)

            for tree in ch_parser1.parse(first_sen):
                print tree
            tree.draw()

        firstParseTree(first_sen)

    def stringParser2(event):
        senten = sentence.get()
        word = senten.split(".")
        first_sen = word[0].split()
        second_sen = word[1].split()

        def secondParseTree(second_sen):
            grammar2 = grammarText2.get("0.0", END)
            grammarPath2 = nltk.grammar.CFG.fromstring(grammar2, encoding='utf-8')

            ch_parser2 = nltk.ChartParser(grammarPath2)

            for tree in ch_parser2.parse(second_sen):
                print tree
            tree.draw()

        secondParseTree(second_sen)

    parseTree.bind("<Button-1>", stringParser)
    parseTree2.bind("<Button-1>", stringParser2)

    # Quit Button 

    def goBack(event):
        stringWindow.destroy()
        root.deiconify()

    quitButton.bind("<Button-1>", goBack)


# Window Initialize

root = Tk()
root.title("PyParser")
root.geometry('1060x630+120+50')
root.configure(background='#093145')

mainFont = tkFont.Font(family="Trebuchet MS", size=36, weight="bold")
subFont = ("Trebuchet MS", 24)
largeFont = ("Didot", 14, "bold")
welcomeFont = ("Verdana", 16)
textFont = ("Calibri", 15)

welcomeLabel = Label(root, text="Welcome To PyParser", font=mainFont, fg="#ffffff", bg='#093145')
subLabel = Label(root, text="Choose The Type", font=subFont, fg="#ffffff", bg='#093145')
arithButton = Button(root, text="Arithmetic Parser", font=largeFont, height=2, width=20, bg="#EFD469", relief=RAISED,
                     bd=4)
stringButton = Button(root, text="String Parser", font=largeFont, height=2, width=20, bg="#EFD469", relief=RAISED, bd=4)
exitButton = Button(root, text="Exit", font=largeFont, height=2, width=20, bg="#CD594A", relief=RAISED, bd=4)

welcomeLabel.place(relx=0.25, rely=0.18)
subLabel.place(relx=0.37, rely=0.35)
arithButton.place(relx=0.2, rely=0.55)
stringButton.place(relx=0.6, rely=0.55)
exitButton.place(relx=0.3999, rely=0.75)

# Linking Buttons

exitButton.bind("<Button-1>", quit)
arithButton.bind("<Button-1>", arithmeticParse)
stringButton.bind("<Button-1>", stringParse)

# Menu

menu = Menu(root)
root.config(menu=menu)

aboutMenu = Menu(menu)
menu.add_cascade(label="About", menu=aboutMenu)
aboutMenu.add_command(label="Software", command=aboutSoftware)
aboutMenu.add_separator()
aboutMenu.add_command(label="Developers", command=develepors)

helpMenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label="Arithmetic", command=arithmeticHelp)
helpMenu.add_separator()
helpMenu.add_command(label="String", command=stringHelp)

root.mainloop()
