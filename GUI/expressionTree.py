from Tkinter import *

root = Tk()


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

    # def __repr__(self):
    # return "Node With Data: %d" % self.data

    def setRootVal(self, data):
        self.data = data

    def insertLeft(self, data, left=None, right=None):
        """
        Insert new node with data
        @param data node data object to insert
        """
        if self.left is None:
            self.left = Node(data, left, right)
            # else:
            #	self.left.insertLeft(data)

    def insertRight(self, data, left=None, right=None):
        """
        Insert new node with data
        @param data node data object to insert
        """
        if self.right is None:
            self.right = Node(data, left, right)
            # else:
            #	self.right.insertRight(data)

    def print_each_level(self):
        # Start off with root node
        thislevel = [self]
        canvas = Canvas(root, width=1200, height=1200)
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
                    #blackline = canvas.create_line(n, a+10,  q - (q / 2), a+75)
                    #blackline2 = canvas.create_line(n, a + 10 , q - (q / 2), a+75)
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

x = "( ( ( ( 4 * 7 ) + 7 ) "
lst = x.split()
for i in range(0, len(lst)):
    try:
        lst[i] = float(lst[i])
    except:
        lst[i] = lst[i]


def modifyExp(exp):
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
    print exp

modifyExp(lst)

def buildTree(lst):
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

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

xscrollbar = Scrollbar(root, orient=HORIZONTAL)
xscrollbar.pack(side=BOTTOM, fill=X)

buildTree(lst)
root.mainloop()
