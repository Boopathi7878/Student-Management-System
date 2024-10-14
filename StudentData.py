import pymongo #MongoDb Implementation
from pymongo import MongoClient
from bson import ObjectId #BSON For Encryption
from pprint import pprint

class Subject: #Class For Subject Information
    def __init__(self, subject_name, status):
        self.subject_name = subject_name
        self.status = status

    def to_dict(self): #Which returns the Value Of Subject
        return {
            "SubjectName": self.subject_name,
            "Status": self.status
        }

class Student: #Details Of Student
    def __init__(self, student_id, name, class_name, semester, result, subjects, phone_number, enroll_number, id_number):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.semester = semester
        self.result = result
        self.subjects = subjects
        self.phone_number = phone_number
        self.enroll_number = enroll_number
        self.id_number = id_number

    def to_dict(self): #Which Stores in this format to MongoDB
        subject_dicts = [subject.to_dict() for subject in self.subjects]
        return {
            "StudentId": self.student_id,
            "Name": self.name,
            "ClassName": self.class_name,
            "Semester": self.semester,
            "Result": self.result,
            "Subjects": subject_dicts,
            "PhoneNumber": self.phone_number,
            "EnrollNumber": self.enroll_number,
            "IdNumber": self.id_number
        }

def get_student_collection(): #Retrieves The Data From MongoDB Collection Named "StudentDetails"
    client = MongoClient("mongodb://localhost:27017")
    db = client.College
    return db.Students

# Create operation
def create_student(collection, student):
    collection.insert_one(student.to_dict())
    print("Student created successfully!")

# Read operation
def read_student(collection, student_id):
    student = collection.find_one({"StudentId": student_id})
    if student:
        pprint(student)
    else:
        print("Student not found.")

# Update operation
def update_student(collection, student_id, updated_student):
    collection.update_one({"StudentId": student_id}, {"$set": updated_student.to_dict()})
    print("Student record updated successfully!")

# Delete operation
def delete_student(collection, student_id):
    collection.delete_one({"StudentId": student_id})
    print("Student deleted successfully!")

def main(): #Main Function To Get The student Collection
    collection = get_student_collection()

    while True: #Executes While Above Codes Are Succeeded
        print("\n---- Student Management System ----")
        print("1. Add Student")
        print("2. View Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            # Create Student
            student_id = input("Enter Student Id: ")
            name = input("Enter Name: ")
            class_name = input("Enter Class: ")
            semester = int(input("Enter Semester: "))
            result = input("Enter Result (Pass/Fail): ")

            subject_count = int(input("Enter the number of subjects: "))
            subjects = [] #List To Store The subjects User entered
            for _ in range(subject_count):
                subject_name = input("Enter Subject Name: ")
                status = input("Enter Status (All Clear/Arrear): ")
                subjects.append(Subject(subject_name, status))

            phone_number = input("Enter Phone Number: ")
            enroll_number = input("Enter Enrollment Number: ")
            id_number = input("Enter ID Number: ")

            student = Student(student_id, name, class_name, semester, result, subjects, phone_number, enroll_number, id_number)
            create_student(collection, student)

        elif choice == '2':
            # Read Student
            student_id = input("Enter Student Id to view: ")
            read_student(collection, student_id) #Retrieves the Information Of student By ID 

        elif choice == '3':
            # Update Student
            student_id = input("Enter Student Id to update: ")
            name = input("Enter Name: ")
            class_name = input("Enter Class: ")
            semester = int(input("Enter Semester: "))
            result = input("Enter Result (Pass/Fail): ")

            subject_count = int(input("Enter the number of subjects: "))
            subjects = []
            for _ in range(subject_count):
                subject_name = input("Enter Subject Name: ")
                status = input("Enter Status (All Clear/Arrear): ")
                subjects.append(Subject(subject_name, status))

            phone_number = input("Enter Phone Number: ")
            enroll_number = input("Enter Enrollment Number: ")
            id_number = input("Enter ID Number: ")

            updated_student = Student(student_id, name, class_name, semester, result, subjects, phone_number, enroll_number, id_number)
            update_student(collection, student_id, updated_student)

        elif choice == '4':
            # Delete Student
            student_id = input("Enter Student Id to delete: ")
            delete_student(collection, student_id)

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
