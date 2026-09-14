import random

print("\nYou have entered the depths of despair!", "\nYou have noticed 5 cards in front of you and 5 cards showing on the screen")
ca1 = "You've noticed that a small text box written with an old viking rune says something","\nDo you want to investigate furter?"
ca2 = "A faintly seemingly door is quickly spotted in the corner to the right of the big screen","\nYou also see a small digital code box, this might be an escape route later or maybe even a second level?"
ca3 = "You decide to turn over one of the cards in front of you"
choices_arrival = [ca1,ca2,ca3]
print("\nYou immediatly think of 3 options, choose carefully it might define your fate")
print("\n\n[1]:",ca1,"\n\n[2]:",ca2,"\n\n[3]:",ca3)
pc1 = input("\nWhat will you choose? (1/2/3):").lower()
if pc1 != "1":
    print("The letters seem to display a weird assortment of number (DCXCVI)","\nWhat does that mean?")

cg1 = ["Rock", "Paper", "Scissors", "Hot Glue","Hand"]

rg1 = {
        "Rock": ["Scissors","Glue"],
        "Paper": ["Rock","Glue"],
        "Scissors": ["Paper","Hand"],
        "Glue": ["Scissors","Hand"],
        "Hand": ["Rock","Paper"]
}
print("Choose your card, be prepared to know defeat!","\nThat's what shows on the screen, you instinctively reckon its some kind of chance game but which?")


def g1():
    print("\n\nYou decided to play, the computer on the screen seems to be highlighting to pick a card","\nYour cards somehow got magically shuffled")
    print("It seems to be an advanced part of rock, paper, scissors")
    
    while True:
        print("\nChoose your card:")
        for in1, choiceg1 in enumerate(choices, start=1): #For at lave en liste (fandt det ved hjælp af github)
            print(f"{in1}. {choiceg1}")

            try:
                pi1 = int(input("Input the number of your choice: ")) - 1
                if pi1 not in range(5): #Kun tal mellem 1 og 5 fungerer
                    raise V_E1 #ValueError1
                pc1 = cg1[pi1]
            except V_E1:
                print("You've choosen to go with an automatic loss, a simple trapdoor beneath you opens and you fall to your death")
                continue

        cpuc1 = random.choice(cg1)
        print(f"\nYou chose: {pc1}")
        print(f"The Magic 8 Ball screen chose: {cpuc1}")
        
def fw1(pc1, cpuc1): #fw1 as in find_winner of game 1
    if pc1 == cpuc1:
        return "You seemed to pick the same card as the computer the cards reshuffled and you're forced to pick again"
    
    elif cpuc1 in rg1[pc1]:
        return random.choice(teg1)#Text ending game 1
    

    
    
    
