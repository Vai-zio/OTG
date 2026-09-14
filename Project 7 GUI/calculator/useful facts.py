import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import os

# TODO LIST
# [1]: Make the different types of facts work
# [2]: Isolate fact texts in seperate documents
# [3]: Make the UI colors change with what mode is selected
# [4]: Import sound effects when pressing buttons :3
# [5]: If possible make an extension for the program to speak to ChatGPT with an API
# [6]: Maybe use listbox in tkinter to communicate with ChatGPT as an input field

#  List of facts
facts = [
    "A man can be arrested in Italy for wearing a skirt in public.",
    "Did you know that there actually existed femboys in the Roman Empire?",
    "Definition: A femboy is typically a male who presents in a more feminine manner, often incorporating elements of fashion, makeup, and behavior traditionally associated with women.",
    "Historical Context: The concept of gender fluidity and androgyny has existed throughout history, with various cultures embracing different expressions of gender.",
    "Ancient Cultures: In ancient Rome, men often wore togas and tunics that could be considered gender-neutral, and some men adopted feminine styles for various reasons, including performance in theater.",
    "Kabuki Theater: In Japan, the Kabuki theater features male actors (onnagata) who play female roles, showcasing a long-standing tradition of gender performance.",
    "Victorian Era: During the Victorian era, men sometimes wore clothing that blurred gender lines, including skirts and dresses, especially in artistic circles.",
    "Modern Fashion: The rise of gender-neutral fashion in the 21st century has led to increased visibility and acceptance of femboy aesthetics in mainstream culture.",
    "Anime and Manga: Femboy characters are prevalent in anime and manga, often depicted with exaggerated feminine features and styles, contributing to the popularity of the trope.",
    "LGBTQ+ Community: Femboys are often embraced within the LGBTQ+ community, where gender expression is celebrated and diverse identities are recognized.",
    "Social Media Influence: Platforms like TikTok and Instagram have allowed femboys to showcase their style and connect with others, leading to a growing online community.",
    "Makeup and Beauty: Many femboys enjoy makeup and beauty routines, challenging traditional gender norms and promoting self-expression.",
    "Cultural Representation: Femboys can be found in various media, from music videos to fashion shows, highlighting the evolving nature of gender representation.",
    "Body Positivity: The femboy aesthetic often promotes body positivity, encouraging individuals to embrace their unique features regardless of societal standards.",
    "Subcultures: Femboys can be part of various subcultures, including goth, punk, and kawaii, each with its own distinct style and influences.",
    "Gender Identity: While some femboys identify as male, others may identify as non-binary or genderqueer, emphasizing the fluidity of gender.",
    "Fashion Icons: Celebrities like Harry Styles and Lil Nas X have challenged traditional masculinity through their fashion choices, inspiring many femboys.",
    "Art and Expression: Femboys often use fashion and art as a means of self-expression, creating a unique blend of masculine and feminine aesthetics.",
    "Community Support: Online forums and social media groups provide support and resources for femboys, fostering a sense of belonging.",
    "Cultural Misunderstanding: Despite growing acceptance, femboys can still face misunderstanding and stigma, highlighting the need for continued education and awareness.",
    "Cosplay: Femboys often participate in cosplay, dressing as characters from video games, anime, and movies, further blurring gender lines.",
    "Fashion Trends: Trends such as oversized clothing, pastel colors, and androgynous styles are often embraced by femboys, reflecting a shift in fashion norms.",
    "Influence of K-Pop: The K-Pop industry has popularized femboy aesthetics, with male idols often adopting feminine styles and makeup.",
    "Historical Figures: Some historical figures, such as the French poet Arthur Rimbaud, are often cited as early examples of gender nonconformity.",
    "Femboy vs. Crossdresser: While femboys may adopt feminine styles, they do not necessarily identify as crossdressers, who may dress in clothing typically associated with the opposite gender for various reasons.",
    "Mental Health: Embracing one's identity as a femboy can have positive effects on mental health, promoting self-acceptance and confidence.",
    "Fashion Designers: Many fashion designers are now creating lines specifically for gender non-conforming individuals, further legitimizing the femboy aesthetic.",
    "Cultural Festivals: Events like Pride parades often celebrate femboy culture, providing a platform for visibility and acceptance.",
    "Literature: Femboys have been featured in literature, often as symbols of rebellion against traditional gender roles.",
    "Influence of Drag Culture: The drag community has influenced the femboy aesthetic, with many femboys adopting elements of drag performance in their style.",
    "Gender Expression: Femboys often challenge the binary understanding of gender, promoting a more fluid and inclusive perspective.",
    "Personal Stories: Many femboys share their personal journeys online, discussing their experiences with gender identity and societal expectations."
]

# Initialize the current fact index
current_fact_index = 0

def show_next_fact():
    global current_fact_index
    # Update the text widget with the next fact
    T.delete(1.0, tk.END)  # Clear the current text
    T.insert(tk.END, facts[current_fact_index])  # Insert the next fact
    # Update the index for the next fact
    current_fact_index = (current_fact_index + 1) % len(facts)  # Loop back to the first fact

def show_selection():
    selected_value = var.get()
    label.config(text=f"Selected: {selected_value}")

root = tk.Tk()

# Specify size of window.
root.geometry("600x500")

frame = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
frame.grid(column=1, row=1, sticky="EW")
framefacts = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
framefacts.grid(column=0, row=1, sticky="EW")

# Create text widget and specify size.
T = tk.Text(framefacts, height=6, width=52)

# Create label
l = tk.Label(framefacts, text="Fb Fact Generator")
l.config(font=("Courier", 22))

# Create button for next text.
b1 = tk.Button(framefacts, text="Next", command=show_next_fact)

# Create an Exit button.
b2 = tk.Button(framefacts, text="Exit", command=root.destroy)

l.pack()
T.pack()
b1.pack()
b2.pack()

# Insert the first fact.
T.insert(tk.END, facts[current_fact_index])

# Create a variable to hold the selected value
var = tk.StringVar(value="Random facts")

# Create radio buttons
radio1 = tk.Radiobutton(frame, text="Random facts", variable=var, value="Random facts", command=show_selection)
radio2 = tk.Radiobutton(frame, text="Femboy facts", variable=var, value="Femboy facts", command=show_selection)
radio3 = tk.Radiobutton(frame, text="How to facts", variable=var, value="How to facts", command=show_selection)
radio4 = tk.Radiobutton(frame, text="Reality facts", variable=var, value="Reality facts", command=show_selection)

# Place radio buttons in the grid
radio1.grid(row=0, column=0, padx=10, pady=5)
radio2.grid(row=1, column=0, padx=10, pady=5)
radio3.grid(row=2, column=0, padx=10, pady=5)
radio4.grid(row=3, column=0, padx=10, pady=5)

# Label to display the selected option
label = tk.Label(frame, text="Selected: Random facts")
label.grid(row=4, column=0, padx=10, pady=10)

tk.mainloop()
