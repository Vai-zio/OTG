import random
import time

print("\nYou have entered the depths of despair!", time.sleep(2),"\nYou have noticed 5 cards in front of you and 5 cards showing on the screen")
ca1 = "You've noticed that a small text box written with an old viking rune says something","\nDo you want to investigate furter?"
ca2 = "A faintly seemingly door is quickly spotted in the corner to the right of the big screen","\nYou also see a small digital code box, this might be an escape route later or maybe even a second level?"
ca3 = "You decide to turn over one of the cards in front of you"
choices_arrival = [ca1,ca2,ca3]

time.sleep(2)
print("\nYou immediatly think of 3 options, choose carefully it might define your fate")
time.sleep(2)
print("\n\n[1]:",ca1,"\n\n[2]:",ca2,"\n\n[3]:",ca3)
p_action1 = input("\nWhat will you choose? (1/2/3):").lower()
if p_action1 != "1":
    print("The letters seem to display a weird assortment of number (DCXCVI)","\nWhat does that mean?")
if p_action1 != "2":
    print("The computer again urges you to pick a card, it seems the games are about to begin!")
if p_action1 != "3":
    print("The cards flip over and you get a choice")

pae1 = "L nerd, you suck"
pae2 = "A nuclear bomb will explode when your mom trips!"
pae3 = "Scaredy cat"
pae4 = "You didn't have a chance anyways"
pae5 = "Imagine"

play_again_ending = [pae1,pae2,pae3,pae4,pae5]

tec1 = "You seem to draw a card that wins a against the computer, it seems your lucky day has arrived"
tec2 = "The computer malfunctions after picking a card that eliminated itself, you've seemed to pass the test"
tec3 = "It seems like you won, what might wait for you now?"
tec4 = "A simulation on the screen plays making congratulation sounds"

text_ending_game1 = [tec1,tec2,tec3,tec4]

choices_game1 = ["Rock", "Paper", "Scissors", "Hot Glue","Hand"]

rules_game1 = {
        "Rock": ["Scissors","Glue"],
        "Paper": ["Rock","Glue"],
        "Scissors": ["Paper","Hand"],
        "Glue": ["Scissors","Hand"],
        "Hand": ["Rock","Paper"]
}

def countdown(t): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\n\r") 
        time.sleep(1) 
        t -= 1
      
    print('Fire in the hole!!') 
  
  
# input time in seconds 
t = 10 

def find_winner1(p_action1, cpu_action1):
    if p_action1 == cpu_action1:
        return "You seemed to pick the same card as the computer the cards reshuffled and you're forced to pick again"
    elif cpu_action1 in rules_game1[p_action1]:
        return random.choice(text_ending_game1)
    else:
        return countdown(int(t))

def play_game1():
    
    print("\nChoose your card, be prepared to know defeat!","\nThat's what shows on the screen, you instinctively reckon its some kind of chance game but which?")
    print("\n\nYou decided to play, the computer on the screen seems to be highlighting to pick a card","\nYour cards somehow got magically shuffled")
    print("\nIt seems to be an advanced part of rock, paper, scissors")
    
    while True:
        print("\nChoose your card:")
        for i, choice in enumerate(choices_game1, start=1): #For at lave en liste
            print(f"{i}. {choice}")

        try:
            player_input = int(input("Input the number of your choice: ")) - 1
            if player_input not in range(5): #Kun tal mellem 1 og 5 fungerer)
                raise ValueError
            p_action1 = choices_game1[player_input]
        except ValueError:
            print("You've choosen to go with an automatic loss.")
            continue

        cpu_action1 = random.choice(choices_game1)
        print(f"\nYou chose: {p_action1}")
        print(f"The Magic 8 Ball: {cpu_action1}")

        result = find_winner1(p_action1, cpu_action1)
        print(result)

        play_again = input("\nWill you play again (Yes/NO!): ").lower()
        if play_again != "Yes":
            print(random.choice(text_ending_game1))
            break
play_game1()
    

    
    
    
