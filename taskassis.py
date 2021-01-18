#This will create a to-do list based on voice commands with functionalities

#importing modules
import speech_recognition as sr
import pyttsx3
import sys
import  os.path
from os import path
from datetime import date

#function for speaking
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate',170)
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.say(text)
    engine.runAndWait()

#function for hearing voice
def hear():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        #voice = r.listen(source)
        r.pause_threshold=1
        voice = r.listen(source, timeout=6)
        try:
            txt = r.recognize_google(voice)
            return txt
        except sr.UnknownValueError:
            speak("Sorry, I haven't heard it. Speak again.")
            hear()
        except TypeError:
            speak("Please speak clearly")
            hear()
        except sr.RequestError and Exception as e:
            speak("Seems you are out of network. Check your internet connectivity please")
            exit()

#function for help
def help():
    speak("Here are the commands in case you wanna know how this works!")
    print("Usage:-")
    print('''
    Here are the keywords should use in your command and functions I do:
     add/do                       # Add a new todo
     list/remaining               # Show remaining todos
     delete/remove                # Delete a todo
     done/complete/completed      # Complete a todo
     help/use                     # Show usage
     report/information/info      # Statistics
     exit/quit/cancel             #terminates the program''')

#add a task
def add(task):
    speak(f"You have said:{task}")
    f = open("todo.txt", "a")
    f.write(task+"\n")
    f.close()
    speak(f"Added todo {task}")
    print(f"Added todo {task}\n")

#done
def done(n):
    try:
        f = open("todo.txt","r")
        task = f.readlines()
        f.close()
        t = task[int(n)-1].rstrip("\n")
        f = open("todo.txt","w")
        for each in task:
            if each.rstrip("\n") != t:
                f.write(each)
        f.close()
        today = date.today()
        d = open("done.txt","a")
        d.write(today.strftime("%d-%m-%Y")+" "+t+"\n")
        d.close()
        speak(f"Congrats! You have completed:{t}")
        print(f"Congrats! You have completed:{t}\n")
    except IndexError:
        speak("This number of task doesn't exists")

#list of tasks
def list():
    try:
        f = open("todo.txt","r")
        list = f.readlines()
        f.close()
        for count,line in enumerate(list,1):
            print(str(count)+". "+line.rstrip("\n"))
        print("\n")
    except Exception as e:
        speak("Looks like your todo list empty")
        print("Your list is empty")
    
#lists of completed tasks
def list_c():
    try:
        f = open("done.txt","r")
        list = f.readlines()
        f.close()
        for count, line in enumerate(list,1):
            print(str(count)+". "+line.rstrip("\n"))
        print("\n")
    except Exception as e:
        speak("Looks like your done list empty")
        print("Your list is empty")
#report of tasks
def report():
    try:
        f = open("todo.txt","r")
        todo = f.readlines()
        f.close()
        d = open("done.txt","r")
        done = d.readlines()
        d.close()
        speak(f"Completed tasks: {len(done)}")
        print(f"Completed tasks: {len(done)}")
        speak(f"Pending tasks: {len(todo)}")
        print(f"Pending tasks: {len(todo)}")
        print("\n")
    except Exception as e:
        speak("Looks like there's nothing in your list to report for")
        speak("Add tasks first")
        print("Nothing to report")

#function for deleting task
def delete(n):
    try:
        f = open("todo.txt","r")
        lines = f.readlines()
        line = lines[int(n-1)]
        speak(f"Deleted todo:{line}")
        print(f"Deleted todo:{line}\n")
        del line
        f.close()
    except Exception as e:
        speak("Looks like your list is empty for deletion")
        speak("Add tasks first")
        print("Nothing to delete")

#function for exit
def stop(name):
    speak(f"Bye, Bye {name}")
    exit()
#function for recognizing commands
def rec(data):
    if "add" in data:
        speak("What do you want me to add?")
        data = hear()
        add(data)
    elif "done" in data or "complete" in data or"completed" in data:
        f= open("todo.txt","r")
        lines = f.readlines()
        f.close()
        if lines != []:
            speak("Here's the list")
            list()
            speak("Which number of task you have done?Type a number")
            try:
                n = int(input("Enter here: "))
            except ValueError or Exception as e:
                speak("Enter a integer number not a word or string")
                n = int(input("Enter here: "))
            done(n)
        else:
            speak("OOPS! You have nothing to complete!")
    elif "help" in data or "use" in data:
        help()
    elif "report" in data or "info" in data or "information" in data:
        report()
    elif "delete" in data or "remove" in data:
        f = open("todo.txt", "r")
        lines = f.readlines()
        f.close()
        if lines != []:
            speak("Here's the list")
            list()
            speak("Which number of task you have to delete?Type a number")
            try:
                n = int(input("Enter here: "))
            except ValueError or Exception as e:
                speak("Enter a integer number not a word or string")
                n = int(input("Enter here: "))
            delete(n)
        else:
            speak("OOPS! You have nothing to delete!")
    elif "list" in data or "remaining" in data :
        speak("Here's the list of pending todos")
        list()
        speak("Here's the list of completed todos with date of completion")
        list_c()
    elif "exit" in data or "quit" in data or "cancel" in data:
        stop(name)
    else:
        speak("I can't work over this!Sorry!")
        help()
        speak("What do you want me to do?")
        data = hear()
        rec(data)

#driver code
speak("Hello! I am your assistant to remind you your daily tasks!")
#user name
speak("Introduce yourself please! What is your good name?")
txt = hear()
words = len(txt.split())
if (words == 1):
    name = txt
else:
    speak("Sorry, there's too much you have speak. Enter your name here")
    name = input("Enter your name:  ")
speak("Hello" + str(name))
#how this works
help()
#start operations
speak("What do you want me to do???")
data = hear()
print(data)
rec(data)
#iteration
while(1):
    speak("Anything next?")
    data = hear()
    print(data)
    if data == None or data == "None":
        speak("Sorry, I haven't heard it. Speak Again.")
        data = hear()
    rec(data)
