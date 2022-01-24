# -----------------------------------------------------------------
# Assignment 3: Student Enrollment System usinf linked chains and a priority queue
#
# File: enrollStudent.py
#
# Author: Siddharth Chhatbar
# -----------------------------------------------------------------

class StudentNode:
    def __init__(self, id, faculty, first, last):
        assert (type(id) == str), ("Error: ID should be 'str' object")
        self.id = id
        self.faculty = faculty
        self.first = first
        self.last = last
        self.next = None
        self.previous = None
    
    # Setters
    def setID(self, id):
        '''
        Sets the student ID according to the given ID
        Returns: None
        '''
        assert (type(id) == str), ("Error: ID should be 'str' object")
        self.id = id
    
    def setFac(self, faculty):
        '''
        Sets the Faculty abbreviation according to the given Faculty
        Returns: None
        '''
        self.faculty = faculty
    
    def setFirstName(self, first):
        '''
        Sets the student's First name according to the given first
        Returns: None
        '''
        self.first = first
    
    def setLastName(self, last):
        '''
        Sets the student's Last name according to the given last
        Returns: None
        '''
        self.last = last
    
    def setNext(self, next):
        '''
        Sets next as the next node
        Returns: None
        '''
        self.next = next
    
    def setPrev(self, previous):
        '''
        Sets previous as the previous node
        Returns: None
        '''
        self.previous = previous

    # Getters
    def getID(self):
        '''
        Accessor for student ID
        Returns: str
        '''
        return self.id
    
    def getFac(self):
        '''
        Accessor for Faculty
        Returns: str
        '''
        return self.faculty 
    
    def getFirstName(self):
        '''
        Accessor for student's First name
        Returns: str
        '''
        return self.first 
    
    def getLastName(self):
        '''
        Accessor for student's Last name
        Returns: str
        '''
        return self.last
    
    def getNext(self):
        '''
        Accessor for next node
        Returns: memory location
        '''
        return self.next 
    
    def getPrev(self):
        '''
        Accessor for previous node
        Returns: momory location
        '''
        return self.previous  

class EnrollTable:
    def __init__(self, capacity):
        assert (capacity <= 51), ('Error: Max capacity of 51 allowed')
        self.capacity = capacity
        self.enrollment_table = [None for x in range(self.capacity)]
        self.table_size = 0
    
    def cmputIndex(self, studentID):
        '''
        Gererating index from given ID
        Returns: int
        '''
        index = 0 
        studentID = int(studentID)
        for i in range(3):
            num = studentID % 100
            studentID = studentID // 100
            if i == 0:
                index = num**2
            else:
                index += num
        index = index % self.capacity
        return index

    def insert(self, item):
        '''
        Inserting item in enrollment table
        Returns: None
        '''
        if self.isEnrolled(item.getID()):
            print('Error: ' +  item.getFirstName() + ' ' + item.getLastName() + ' (ID: ' + item.getID() + ') already enrolled.')
        else:
            index = self.cmputIndex(item.getID())
            if self.enrollment_table[index] == None:
                self.enrollment_table[index] = item
            else:
                current = self.enrollment_table[index]
                while current.getNext() != None:
                    current = current.getNext()
                current.setNext(item)

            self.table_size += 1                

    def remove(self, item):
        '''
        Removing item from enrollment table
        Returns: None
        '''
        index = self.cmputIndex(item.getID())
        if self.size() == 0:
            raise Exception('List is Empty')

        current = self.enrollment_table[index]
        previous = None
        found = False
        while current != None and not found:
            if current.getID() == item.getID():
                found = True
            else:
                previous = current
                current = current.getNext()
        if not found:
            raise Exception('Item not in list')
        else:
            if previous == None: 
                self.enrollment_table[index] = current.getNext()
            else:
                previous.setNext(current.getNext())
            self.table_size = self.table_size -1

    def isEnrolled(self, studentID):
        '''
        Reports if the ID is present in enrollment table or not
        Returns: bool
        '''
        index = self.cmputIndex(studentID)
        current = self.enrollment_table[index]
        while current != None:
            if current.getID() == studentID:
                return True
            if current.getID() > studentID:
                return False
            else:
                current = current.getNext()
        return False

    def size(self):
        '''
        Reports the size of the enrollment table
        Returns: int
        '''
        return self.table_size

    def isEmpty(self):
        '''
        Reports if enrollment table is empty or not
        Returns: bool
        '''
        return self.size() == 0

    def __str__(self):
        string = '['
        for i in range(self.size()):
            if self.enrollment_table[i] != None:
                current = self.enrollment_table[i]
                string += str(i) + ': '
                while current != None:
                    info = current.getID() + ' ' + current.getFac() + ' ' +  current.getFirstName() + ' ' + current.getLastName() 
                    if current.getNext() != None:
                        string = string + info + ', '
                    elif current.getNext() == None:
                        string += info + ', '
                    current = current.getNext()
                string += '\n'
        if len(string) != 1:
            string = string[0:len(string) - 3] + ']'
        else:
            string += ']'
        return string

class PriorityQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
    
    def enqueue(self, item):
        '''
        Enqueues the item in a Priority Queue
        Returns: None
        '''
        faculty_priority = {"SCI" : 4, "ENG" : 3, "BUS" : 2, "ART" : 1, "EDU" : 0}
        if self.size() == 0: 
            self.head = item
            self.tail = item
        
        else:
            current = self.head
            count = 0
            while current != None:
                current_faculty = faculty_priority[current.getFac()]
                item_faculty = faculty_priority[item.getFac()]
                if current_faculty < item_faculty and count == 0:
                    enqueue = current
                    count += 1
                current = current.getNext()
            
            if current_faculty < item_faculty:
                if enqueue.getPrev() == None:
                    item.setNext(enqueue)
                    enqueue.setPrev(item)
                    self.head = item

                else:
                    item.setNext(enqueue)
                    item.setPrev(enqueue.getPrev())
                    enqueue.getPrev().setNext(item)
                    enqueue.setPrev(item)

            elif current_faculty >= item_faculty:
                self.tail.setNext(item)
                item.setPrev(self.tail)
                self.tail = item
        
        self.count += 1
                
    def dequeue(self):
        '''
        Dequeues the first element from the Priority Queue
        Returns: StudentNode
        '''
        if self.isEmpty():
            raise Exception('Queue is empty')
        else:
            current = self.head
            self.head = self.head.getNext()
            current.setNext(None)
            
        self.count -= 1
        return current

    def size(self):
        '''
        Reports the size of the Priority Queue
        Returns: int
        '''
        return self.count

    def isEmpty(self):
        '''
        Reports if the Priority Queue is empty or not
        Returns: bool
        '''
        return self.count == 0

    def __str__(self):
        string = '['
        current = self.head
        while current != None:
            info = current.getID() + ' ' + current.getFac() + ' ' +  current.getFirstName() + ' ' + current.getLastName()
            string += info + ',\n'
            current = current.getNext()
        if len(string) != 1:
            string = string[:len(string)-2] + ']'
        else:
            string += ']'
        return string
