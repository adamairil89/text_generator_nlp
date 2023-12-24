import streamlit as st
import random
from nltk import bigrams, trigrams
import os
from sklearn.base import defaultdict

# Create a placeholder for model
model = defaultdict(lambda: defaultdict(lambda: 0))

def read_and_combine_txt_files(folder_path):
    """Reads all TXT files within a folder, combines their contents, and returns the combined text."""

    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r") as file:
                    combined_text += file.read() + "\n"  # Add a newline between files
            except FileNotFoundError:
                print(f"Warning: File not found: {file_path}")
            except UnicodeDecodeError:
                print(f"Warning: Encoding error while reading: {file_path}")

    return combined_text

# Specify the folder containing the TXT files
folder_path = "song_lyrics"  # Replace with the actual folder path

# Read and combine the text from all TXT files in the folder
text = read_and_combine_txt_files(folder_path)

# Split the text into sentences
sentences = text.split(".")

# Count frequency of co-occurrence [w1, w2, w3]
for sentence in sentences:
    for w1, w2, w3 in trigrams(sentence.split(), pad_right=True, pad_left=True):
        model[(w1, w2)][w3] += 1

# Transform counts to probabilities
for w1_w2 in model:
    total_count = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_count

def generate_sentence(text):
    """Generates a sentence using the model."""
    sentence_finished = False

    while not sentence_finished:
        # Select a random probability threshold
        r = random.random()
        accumulator = .0

        for word in model[tuple(text[-2:])].keys():
            accumulator += model[tuple(text[-2:])][word]
            if accumulator >= r:
                text.append(word)
                break

        if text[-2:] == [None, None]:
            sentence_finished = True

    return ' '.join([t for t in text if t])

# Streamlit app
st.title("Sentence Generator")

user_text = st.text_input("Enter few words:")  # Prompt for user input

if st.button("Generate texts"):
    text = user_text.split() # Split the input text into words
    generated_sentence = generate_sentence(text)
    st.divider()
    st.write("Text generated using bi-gram:")
    st.write(generated_sentence)
    st.session_state.user_text = ""

