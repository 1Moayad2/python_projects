##################
import sqlite3
import re
import random
import time, datetime
import os
##################
db = sqlite3.connect("app.db")
cr = db.cursor()
cr.execute("create table if not exists users (name text, date_birth integers, country text, mark integer, runtimequiz float, user_id integer)")

#########################
mark = 0
num = 1
#########################
def quiz(NOQ, CDM) :
    """
       NOQ :
            number of questions 'to printing'
       CDM :
            count down minute
    """

    global mark, num, time_quiz

    start = time.time()
    DT = datetime.datetime.now()
    COUNT_DOWN = datetime.datetime(DT.year, DT.month, DT.day, DT.hour, DT.minute + CDM)
    delta = datetime.timedelta(microseconds=-0.000001)

    qs = ["question1? ", "question2? "] # all questions
    shuffle = qs.copy()
    random.shuffle(shuffle)
    for number_question in range(NOQ) :
        time_stop = COUNT_DOWN - datetime.datetime.now()
        if time_stop < delta :
            print ("timeing is stopped!, and", end=" ")
            break
        print (f"\nThe time remaining is {time_stop}")
        print (f"\nquestion {num}")
        answer = input(shuffle[number_question])
        print ()
        num += 1
        if shuffle[0] == qs[0] or shuffle[1] == qs[0] and answer == "yes":
            mark += 1
        elif shuffle[0] == qs[1] or shuffle[1] == qs[1] and answer == "no":
            mark += 2

    print ("questions is stop")
    print ("I wish you success\n")
    end = time.time()
    time_quiz = "{:.1f}".format(end - start)



def login() :

    name = input("Enter your f_name, m_name, l_name: ").strip().lower()
    age = input("Enter your date-birth, example => 1982/12/25 : ").strip()
    country = input("Enter your country: ").strip().lower()

    search = re.search("^\w{3,9}\s\w{3,9}\s\w{3,9}$", name)
    search2 = re.search("^/?\d{4}[/|\s]\d{1,2}[/|\s]\d{1,2}$", age)
    search3 = re.search("^\w{4,12}$", country)

    if search and search2 and search3 :
        cr.execute(f"select name from users where name = '{name}'")
        result = cr.fetchone()
        if result != None :
            print ("You recorded in the exam, O", name.split()[0])
        else:
            def add_id() :
                uid = random.randint(100000000, 999999999)
                cr.execute(f"select user_id from users where user_id = '{uid}'")
                R = cr.fetchone()
                if R != None :
                    add_id()
                else:
                    quiz(2, 1)
                    cr.execute(f"insert into users values(?, ?, ?, ?, ?, ?)", (name, age, country, mark, time_quiz, uid))
                    db.commit()
            add_id()
    else:
        os.system("clear")
        print ("Please enter information in the correct form")
        print ("Please try again:")
        login()



def fetchallinfo() :

    op = input("\nDo you want to print tags?, Y_yes / N_no? ").strip().lower()
    if op == "y" or op == "yes":
        time.sleep(1)
        os.system("clear")
        cr.execute("select name, mark from users order by mark desc")
        result = cr.fetchall()
        print (f"We are {len(result)} student") 
        print ("Print all tags :\n\n")
        count = 1
        print ("Rank         Name                    Mark \n")
        for rows in result:
            print ("-" *43)
            print (r"#{} {} {} / 3".format(str(count).zfill(2), ''.join(rows[0]).rjust(len(rows[0]) + 3).ljust(33), rows[1]))
            count += 1
        print ()
        option = input("Do you want to deep_search for a specific person?, Y_yes / N_no? ").strip().lower()
        if option == "y" or option == "yes":
            Deep_search = input("enter all name to search it: ").strip().lower()
            cr.execute(f"select * from users where name = '{Deep_search}'")
            result = cr.fetchone()
            if result == None :
                print (f"\nNo named is '{Deep_search}' in school")
            else:
                a = result[1].replace(" ", "/")
                print (f"\nname => {result[0]}, date-birth => {a[1:] if a[0] == '/' else a}, country => {result[2]}, mark => {result[3]}, run-time => {result[4]}, id => {result[5]}")
        else:
            print ()
        db.close()
    else:
        db.close()
        print ()

login()
fetchallinfo()
