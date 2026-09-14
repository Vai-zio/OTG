import random

# Valgmuligheder
choices = ["Rock", "Scissors", "Paper", "Monkey", "Banana"]

# Resultatregler for den udvidede version
rules = {
    "Rock": ["Scissors", "Monkey"],
    "Scissors": ["Paper", "Monkey"],
    "Paper": ["Rock", "Banana"],
    "Monkey": ["Paper", "Banana"],
    "Banana": ["Rock", "Scissors"]
}

# Funktion til at finde vinderen
def find_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Draw!"
    elif computer_choice in rules[player_choice]:
        return "That's right you win!"
    else:
        return "Bonk, you lose!"

# Spil loop
def play_game():
    print("Welcome to the abriaviated version of rock, paper and scissors but with monkeys")
    
    while True:
        print("\nChoose your card:")
        for i, choice in enumerate(choices, start=1): #For at lave en liste
            print(f"{i}. {choice}")

        try:
            player_input = int(input("Input the number of your choice: ")) - 1
            if player_input not in range(5): #Kun tal mellem 1 og 5 fungerer)
                raise ValueError
            player_choice = choices[player_input]
        except ValueError:
            print("You've choosen to go with an automatic loss.")
            continue

        computer_choice = random.choice(choices)
        print(f"\nYou chose: {player_choice}")
        print(f"The Magic 8 Ball: {computer_choice}")

        result = find_winner(player_choice, computer_choice)
        print(result)

        play_again = input("\nWill you play again (Yes/NO!): ").lower()
        if play_again != "Yes":
            print("L nerd you suck")
            break

# Start spillet
play_game()
