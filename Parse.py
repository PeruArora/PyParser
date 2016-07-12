import nltk
import sys
import operator 


choice = int(raw_input(' 1. String Parser\n 2. Arithmetic Parser\n Enter Your Choice: '))

# String Parser
if choice == 1 :
    
    sentence = raw_input("Enter Your Sentence: ")
    words = sentence.split()
    
    try:
        #Fetching the user input grammar
        grammar_path = nltk.data.load("input_grammar.cfg")

        ch_parser = nltk.ChartParser(grammar_path)

        for tree in ch_parser.parse(words):
            print tree
        tree.draw()
    
    except:
        fin = open("input_grammar.cfg", "a")
        fin.write("\n")
        print "Enter Your Grammar: "

    # To take grammar as an input from the user

        while 1:
            try:
                line = sys.stdin.readline()
                fin.write(line)
            except KeyboardInterrupt:
                break
        fin.close()
        
        #Fetching the user input grammar
        grammar_path = nltk.data.load("input_grammar.cfg")

        ch_parser = nltk.ChartParser(grammar_path)

        for tree in ch_parser.parse(words):
            print tree
        tree.draw()


# Arithmetic Parser
elif choice == 2:
    
    # Stack Defination
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
            return self.items[len(self.items)-1]

        def size(self):
            return len(self.items)


    
    # Binary Tree Defination
    class BinaryTree:

        def __init__(self,rootObj):
            self.key = rootObj
            self.leftChild = None
            self.rightChild = None

        def insertLeft(self,newNode):

            if isinstance(newNode, BinaryTree):
                t = newNode
            else:
                t = BinaryTree(newNode)
    
            if self.leftChild is not None:
                t.left = self.leftChild

            self.leftChild = t
    
        def insertRight(self,newNode):
            if isinstance(newNode,BinaryTree):
                t = newNode
            else:
                t = BinaryTree(newNode)

            if self.rightChild is not None:
                t.right = self.rightChild
            self.rightChild = t

        def isLeaf(self):
            return ((not self.leftChild) and (not self.rightChild))

        def getRightChild(self):
            return self.rightChild

        def getLeftChild(self):
            return self.leftChild

        def setRootVal(self,obj):
            self.key = obj

        def getRootVal(self,):
            return self.key
        
        def postorder(self):
            if self.leftChild:
                self.leftChild.postorder()
            if self.rightChild:
                self.rightChild.postorder()
            print(self.key)
            
        def postordereval(self):
            opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}
            res1 = None
            res2 = None
            if self.leftChild:
                res1 = self.leftChild.postordereval()  #// \label{peleft}
            if self.rightChild:
                res2 = self.rightChild.postordereval() #// \label{peright}
            if res1 and res2:
                return opers[self.key](res1,res2) #// \label{peeval}
            else:
                return self.key


     # Arithmetic Parsing
    def buildParseTree(fpexp):
        fplist = fpexp.split()
        pStack = Stack()
        eTree = BinaryTree('')
        pStack.push(eTree)
        currentTree = eTree
        for i in fplist:
            if i == '(':
                currentTree.insertLeft('')
                pStack.push(currentTree)
                currentTree = currentTree.getLeftChild()
            elif i not in ['+', '-', '*', '/', ')']:
                currentTree.setRootVal(int(i))
                parent = pStack.pop()
                currentTree = parent
            elif i in ['+', '-', '*', '/']:
                currentTree.setRootVal(i)
                currentTree.insertRight('')
                pStack.push(currentTree)
                currentTree = currentTree.getRightChild()
            elif i == ')':
                currentTree = pStack.pop()
            else:
                raise ValueError
        return eTree
    
    expression = raw_input("Enter Fully Paranthesized Arithmetic Expression: ")
    
    # Checking Validity of Expression Entered
    
    lst = expression.split()
    parIncrement=0
    parDecrement=0
    for i in lst:
        if i=='(':
            parIncrement+=1
        elif i==')':
            parDecrement+=1

    if parIncrement != parDecrement:
        print ("Invalid!\n\t\t**** Expression is Not Correctly Parenthesized. ****")
        exit(0)
        
        
    pt = buildParseTree(expression)
    pt.postorder()
    print "Ans is: "
    print pt.postordereval()

else:
    print "\n\t\t Invalid Choice!"
    
