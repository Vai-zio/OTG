import random

# Generer et tilfældigt tal mellem 1 og 100
number_to_guess = random.randint(1, 100)

# Spørg spilleren om deres gæt
guess = int(input("Gæt et tal mellem 1 og 100: "))

# Tjek om gættet er korrekt
if guess < number_to_guess:
    print("For lavt!")
elif guess > number_to_guess:
    print("For højt!")
else:
    print("Tillykke! Du gættede rigtigt!")
