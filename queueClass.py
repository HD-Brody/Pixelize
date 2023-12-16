# Problem Solving with Algorithms and Data Structure
# http://interactivepython.org/courselib/static/pythonds/BasicDS/queues.html

class Queue:
    ''' Implementation of an abstract data type/structure Queue,
        using physical implementation of a list data type.'''
    def __init__(self):
        ''' Creates a new stack that is empty.
        It needs no parameters and returns an empty stack.'''
        self.items = []

    def enqueue(self, item):
         ''' Adds a new item to the back of the queue.
            It needs the item and returns nothing. '''
         self.items.insert(0,item)

    def dequeue(self):
         ''' removes the top item from the queue.
            It needs no parameters and returns the item. Teh queue is modified.'''
         return self.items.pop()

    def peek(self):
         ''' Returns the top item from the queue but does not remove it.
            It needs no parameters. The queue is not modified.'''
         return self.items[len(self.items)-1]

    def size(self):
         ''' Returns the number of items on the queue.
            It needs no parameters and returns an integer.'''
         return len(self.items)

    def isEmpty(self):
         ''' tests to see whether the queue is empty.
            It needs no parameters and returns a boolean value.'''
         return self.items == []
