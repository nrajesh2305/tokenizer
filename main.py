from tokenizerP import *
import time
import random
import pyttsx3

python_categorized, python_total = process_file("test.txt")

random_phrases = [
    "ACCESSING THE MAINFRAME", "DEPLOYING ENEMY VEHICLES", 
    "LAUNCHING A TROJAN MALWARE", "BYPASSING FIREWALL", 
    "UPLOADING THE VIRUS", "OVERRIDING SECURITY PROTOCOLS", 
    "FIREWALL DISABLED", "HOST UNREACHABLE", "TRIANGULATING POSITION", 
    "TROJAN MALWARE DEPLOYED"
]

print("As a result of reading your file, we have displayed the full content above, \nwe will be cleaning it up before tokenization begins, press (o) to go forward:")
choice1 = input("")
for i in range(10):
    time.sleep(1)
    if(i == 0):
        continue
    print(f"Cleaning... {i * 10}%")

clean_code_and_ignore_comments("test.txt")

choice = input("Would you like to see the tokenized version y/n?\n")
print("Regardless whatever you mean by that, clear or not, I am gonna show the Python Tokenized Table.")

for i in range(10):
    print(random_phrases[random.randint(0, len(random_phrases) - 1)] + "...")
    time.sleep(random.randint(1, 3))

if python_categorized:
    display_table(python_categorized, python_total)

time.sleep(5)
print("YOU THOUGHT I WAS DONE, HAHAHA. ONE LAST CHANCE")
time.sleep(10)

for i in range(10):
    print(random_phrases[random.randint(0, len(random_phrases) - 1)] + "...")
    time.sleep(random.randint(1, 3))

print("Fine I'm done, you win. Or do you?")



