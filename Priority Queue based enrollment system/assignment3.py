# -----------------------------------------------------------------
# Assignment 3: Student Enrollment System usinf linked chains and a priority queue
#
# File: assignment3.py
#
# Author: Siddharth Chhatbar
# -----------------------------------------------------------------

import enrollStudent

def enroll_file(table):
    '''
    Writing the information of enrolled students in a file
    Returns: None
    '''
    table = str(table)
    file = open('enrolled.txt', 'w')    
    file.write(table)
    file.close()

def waitlist_file(queue):
    '''
    Appending the priority queue of students to a file
    Returns: None
    '''
    queue = str(queue)
    file = open('waitlist.txt','a')
    file.write(queue + '\n\n')
    file.close()

def enroll(student_list):
    '''
    -> Enrolling students in the program
    -> Creating a Priority Queue for the remaining students
    Returns: EnrollTable, ProrityQueue
    '''
    enrollment_table = enrollStudent.EnrollTable(51)
    student_priority = enrollStudent.PriorityQueue()

    for i in range(len(student_list)):
        student = student_list[i]
        student = student.split()
        student_info = enrollStudent.StudentNode(student[0], student[1], student[2], student[3])
        if i < 50:
            enrollment_table.insert(student_info)
        else:
            student_priority.enqueue(student_info)
    
    enroll_file(enrollment_table)
    waitlist_file(student_priority)
    print('Enrolled:')
    print(enrollment_table)
    print()
    print('Waitlist:')
    print(student_priority)
    print()
    return enrollment_table,student_priority

def read():
    '''
    MAIN FUNCTION FOR OPTION 'R'
    -> Reads student data from given file
    -> Calls the enroll(student_list) function
    Returns: EnrollTable, ProrityQueue
    '''
    valid = False
    while not valid:
        try:
            filename = input('Please enter a filename for student records: ')
            file = open(filename, 'r')
            valid = True
        except  FileNotFoundError:
            print('Error: File Not Found.')
        
        student_list = file.read().split('\n')
        table,queue = enroll(student_list)
        file.close()
        return table,queue

def drop_student(student_list, table, queue):
    '''
    -> Drops the students from given file
    -> Enrolls the students according to PriorityQueue
    Returns: None
    '''
    for i in range(len(student_list)):
        student = student_list[i]
        student = student.split()
        student_info = enrollStudent.StudentNode(student[0], student[1], student[2], student[3])
        try:
            table.remove(student_info)
        except Exception as ItemNotFound:
            print("WARNING: " + student[2] + ' ' + student[3] + ' (ID: ' + student[0] + ') is not currently enrolled and cannot be dropped.')
        if table.size() < 50:
            try:
                table.insert(queue.dequeue())
            except Exception as EmptyQueue:
                print(EmptyQueue)
    
    waitlist_file(queue)
    print()
    print('Waitlist:')
    print(queue)
    print()


def drop(table, queue):
    '''
    MAIN FUNCTION FOR OPTION 'D'
    -> Reads student data from given file
    -> Calls the drop_student(student_list, table, queue) function
    Returns: None
    '''
    valid = False
    while not valid:
        try:
            filename = input('Please enter a filename for student records: ')
            file = open(filename, 'r')
            valid = True
        except  FileNotFoundError:
            print('Error: File Not Found.')
        
        student_list = file.read().split('\n')
        drop_student(student_list,table,queue)
        file.close()

def main():
    valid = False
    table,queue = None,None
    while not valid:
        choice = input('Would you like to register or drop students [R/D]: ')
        if choice == 'Q':
            print('Exiting...\nGoodbye...')
            valid = True
        elif choice == 'R':
            table, queue = read()

        elif choice == 'D':
            drop(table, queue)
        else:
            print('Invalid input.')

main()