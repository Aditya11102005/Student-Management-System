import mysql.connector as mydb
import time as t
from tqdm import tqdm as p


class timer:
    def executing(self):
        for i in p(range(10), colour="white", desc="Executing", leave=False, dynamic_ncols=True):          
            t.sleep(0.25)

    def loading(self):
        for i in p(range(10), colour="white", desc="  Loading", leave=False, dynamic_ncols=True):          
            t.sleep(0.25)


def setup():
    db = mydb.connect(host="localhost", user="root", password="")
    executor = db.cursor()
    try:
        executor.execute("CREATE DATABASE IF NOT EXISTS SMS")
        executor.execute("USE SMS")
        executor.execute("CREATE TABLE IF NOT EXISTS studentDetails(RollNo int(3) NOT NULL PRIMARY KEY AUTO_INCREMENT,FirstName varchar(14) NOT NULL,LastName varchar(14) NOT NULL,DOB date NOT NULL,Class int(3) NOT NULL,Gender varchar(6) NOT NULL, CHECK (Gender = 'Male or Gender = 'Female'))")
        executor.execute("INSERT INTO studentDetails(FirstName,LastName,DOB,Class,Gender) VALUES('Aditya','Bijjaragi','2005-10-11',12,'Male')")
        executor.execute("CREATE TABLE IF NOT EXISTS studentResults(RollNo int(3),Physics int(3) NOT NULL,Chemistry int(3) NOT NULL,Maths int(3) NOT NULL,English int(3) NOT NULL,CS int(3) NOT NULL,OverallPercentage decimal(4,2) NOT NULL,Month varchar(10) NOT NULL,FOREIGN KEY (RollNo) REFERENCES studentDetails(RollNo) ON DELETE CASCADE ON UPDATE CASCADE)")
        executor.execute("INSERT INTO studentResults(RollNo,Physics,Chemistry,Maths,English,CS,OverallPercentage,Month) VALUES(1,19,16,20,21,25,80.80,'April')")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Setup failed!\nError: {e}")
    db.close()


def viewStudents():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    try:
        executor.execute("SELECT * FROM studentDetails")
        result = executor.fetchall()
        if len(result) == 0:
            print("Invalid RollNo")
        else:
            timer.loading()
            print("|"+"-"*67+"|")
            for row in result:
                rno = row[0]
                Fname = row[1]
                Lname = row[2]
                dob = row[3]
                Class = row[4]
                Gender = row[5]
                print("|"+"Student Detail:"+" "*52+"|")
                print("|"+f"Roll No: {rno}\t\t\tClass: {Class}"+" "*27+"|")
                print("|"+f"First Name: {Fname}\t\tLast Name: {Lname}"+" "*16+"|")
                print("|"+f"DOB: {dob}\t\tGender: {Gender}"+" "*24+"|")
                print("|"+"-"*67+"|")
            print("|"+"_"*67+"|")
    except Exception as e:
        print(f"Error occurred while fetching student detail!\nError: {e}")
    db.close()


def addStudents():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    print("|"+"-"*67+"|")
    Fname = input("|"+"Enter first name: ")
    Lname = input("|"+"Enter last name: ")
    dob = input("|"+"Format - YYYY-MM-DD\n"+"|"+"Enter date of birth: ")
    Class = int(input("|"+"Enter class: "))
    gender = input("|"+"Enter gender: ")
    print("|"+"_"*67+"|")
    timer.executing()
    try:
        executor.execute("INSERT INTO studentDetails(FirstName,LastName,DOB,Class,Gender) VALUES(%s,%s,%s,%s,%s)",(Fname,Lname,dob,Class,gender))
        db.commit()
        print("Successfully added")
    except Exception as e:
        db.rollback()
        print(f"Failed to add student!\nError: {e}")
    db.close()


def updateStudent():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    r = int(input("Enter the roll no to be updated: "))
    executor.execute("SELECT * FROM studentDetails WHERE RollNo=%s",(r,))
    result = executor.fetchall()
    if len(result) == 0:
        print("Invalid RollNo")
    else:
        print("|"+"-"*67+"|")
        Fname = input("|"+"Enter new first name (press enter to skip): ")
        Lname = input("|"+"Enter new last name (press enter to skip): ")
        dob = input("|"+"Format: YYYY-MM-DD\n"+"|Enter new date of birth (press enter to skip): ")
        Class = input("|"+"Enter new class (press enter to skip): ")
        gender = input("|"+"Enter new gender (press enter to skip): ")
        print("|"+"_"*67+"|")
        executor.execute("SELECT * FROM studentDetails WHERE RollNo=%s",(r,))
        updating = executor.fetchone()

        if updating is None:
            print(f"No student found with Roll No {r}")
            return

        updateq = f"UPDATE studentDetails SET "
        updatel = []
        if Fname != "":
            updatel.append(f"firstName='{Fname}'")
        if Lname != "":
            updatel.append(f"lastName='{Lname}'")
        if dob != "":
            updatel.append(f"dob='{dob}'")
        if Class != "":
            try:
                cLass = int(Class)
                updatel.append(f"class={cLass}")
            except ValueError:
                print("Invalid class value, skipping update")
        if gender != "":
            updatel.append(f"gender='{gender}'")

        updateq += ", ".join(updatel)
        updateq += f" WHERE RollNo={r}"

        timer.executing()
        try:
            executor.execute(updateq)
            if executor.rowcount > 0:
                db.commit()
                print(f"Successfully updated student details with Roll No {r}")
            else:
                print(f"No rows updated for student with Roll No {r}")
        except Exception as e:
            db.rollback()
            print(f"Failed to update student with Roll No {r}!\nError: {e}")
    db.close()


def deleteStudent():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    r = int(input("NOTE:You can not delete student with rollno 1\nEnter the roll number: "))
    executor.execute("SELECT * FROM studentDetails WHERE RollNo=%s",(r,))
    deleting = executor.fetchone()

    if deleting is None:
        print(f"No student found with Roll No {r}")
        return
    
    conform = input(f"Do you really want to delete the student data with roll number {r}?(y/n): ")
    if conform == "y":
        timer.executing()
        executor.execute("DELETE FROM studentDetails WHERE RollNo=%s",(r,))
        db.commit()
        print("Successfully deleted student")
    elif conform == "n":
        db.rollback()
        print("On your request we are not deleting the data")
    else:
        print("Failed to delete student")
    db.close()


def viewMarks():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    try:
        timer.loading()
        executor.execute("SELECT sd.RollNo,sd.FirstName,sd.LastName,sr.Physics,sr.Chemistry,sr.Maths,sr.English,sr.CS,sr.OverallPercentage,sr.Month FROM studentDetails sd,studentResults sr WHEREsd.RollNo = sr.RollNo")
        result = executor.fetchall()
        for row in result:
            rno = row[0]
            Fname = row[1]
            Lname = row[2]
            Physics = row[3]
            Chemistry = row[4]
            Maths = row[5]
            English = row[6]
            Cs = row[7]
            Percentage = row[8]
            Months = row[9]
            print("|"+"Student Score:"+" "*53+"|")
            print("|"+f"First Name: {Fname}\t\tLast Name: {Lname}"+" "*16+"|")
            print("|"+f"Roll No: {rno}\t\t\tCS: {Cs}"+" "*30+"|")
            print("|"+f"Physics: {Physics}\t\t\tChemistry: {Chemistry}"+" "*23+"|")
            print("|"+f"Maths: {Maths}\t\t\tEnglish: {English}"+" "*25+"|")
            print("|"+f"Percentage: {Percentage}\t\tMonth: {Months}"+" "*20+"|")
            print("-"*69)
        print("|"+"_"*67+"|")
    except Exception as e:
        print(f"Error occurred while fetching student detail!\nError: {e}")
    db.close()


def addMarks():
    db = mydb.connect(host="localhost", user="root", password="",database="SMS")
    executor = db.cursor()
    print("|"+"_"*67+"|")
    r = int(input("Enter the student rollno: "))
    executor.execute("SELECT * FROM StudentDetails where RollNo=%s",(r,))
    result = executor.fetchall()
    if len(result) == 0:
        print("Student does not exist, first add the student details.")
    else:
        print("Enter marks as per subject")
        p = int(input("|"+"Physics: "))
        c = int(input("|"+"Chemistry: "))
        m = int(input("|"+"Maths: "))
        e = int(input("|"+"English: "))
        cs = int(input("|"+"CS: "))
        mt = input("|"+"Enter the month of test: ")
        print("|"+"_"*67+"|")
        per = ((p+c+m+e+cs)/125)*100
        percentage = round(per,2)
        timer.executing()
        try:
            executor.execute("INSERT INTO studentResults(RollNo,Physics,Chemistry,Maths,English,CS,OverallPercentage,Month) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(r,p,c,m,e,cs,percentage,mt))
            db.commit()
            print("Successfully added")
        except Exception as e:
            db.rollback()
            print(f"Failed to add student!\nError: {e}")
    db.close()


setup()


print("*"*69)
print("|"+" "*20,"Student Management System"+" "*20,"|")
print("*"*69)
x = ""
while x == "":
    print("|"+"-"*67+"|")
    print("|"+" "*20,"1. View student details"+" "*22,"|")
    print("|"+" "*20,"2. Add student details"+" "*23,"|")
    print("|"+" "*20,"3. Update student details"+" "*20,"|")
    print("|"+" "*20,"4. Delete student details"+" "*20,"|")
    print("|"+" "*20,"5. View student marks"+" "*24,"|")
    print("|"+" "*20,"6. Add student marks"+" "*25,"|")
    print("|"+"_"*67+"|")
    c = int(input("|"+"Enter your choice: "))
    if c == 1:
        viewStudents()
    elif c == 2:
        addStudents()
    elif c == 3:
        updateStudent()
    elif c == 4:
        deleteStudent()
    elif c == 5:
        viewMarks()
    elif c == 6:
        addMarks()
    else:
        print("|"+"Invalid input\n"+"|"+"Try Again...")

    x = input("|"+"Press ENTER to continue: ")
