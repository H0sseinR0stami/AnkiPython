import pandas as pd
import genanki
from gtts import gTTS
import os
import re
import tempfile


# Function to extract the full answer sentence for TTS, excluding "c1::"
def extract_full_answer(cloze_text):
    return re.sub(r'{{c1::(.*?)}}', r'\1', cloze_text)


# Read the CSV file with Cloze questions and extra information
csv_file = './ankiInput/cloze_questions.csv'  # Update with the path to your CSV file
df = pd.read_csv(csv_file)
df.columns = ['ClozeQuestion', 'ExtraInformation']  # Assuming the second column is for extra information

# Create a new Anki deck with Cloze type
my_deck = genanki.Deck(
    2059400110,
    'My Cloze Deck'
)

# CSS to style the Cloze deletion text and answer text
css_style = """
<style>
.cloze {
    color: blue; /* Color for the cloze deletion on the front of the card */
}
.question {
    color: green; /* Color for the answer on the back of the card */
    style: font-family: Segoe UI;
    font-size: 35px;
    }
.extraInf {
    color: brown; /* Color for the answer on the back of the card */
    style: font-family: Segoe UI;
    font-size: 18px;
    }

</style>
"""

# Create a new Anki model for Cloze deletion
cloze_model = genanki.Model(
    1607392319,
    'Cloze Model with Answer Audio',
    fields=[
        {'name': 'Text'},
        {'name': 'AnswerAudio'},  # Field for answer audio
        {'name': 'ExtraInformation'}  # Field for extra information
    ],
    templates=[
        {
            'name': 'Cloze Card',
            'qfmt': (css_style +
                     "<div class = question>{{cloze:Text}}</div>"
                     "<br>"
                     "Type the answer: {{type:cloze:Text}}"
                     "<br>"
                     "<div class = extraInf > hint : {{ExtraInformation}}</div>"
                     ),  # Front of the card
            'afmt': (css_style +
                     "<div class = question>{{cloze:Text}}</div>"
                     "<br>"
                     "Your answer: {{type:cloze:Text}}<br>{{AnswerAudio}}"
                     "<br>"
                     "<div class = extraInf > hint : {{ExtraInformation}}</div>")  # Back of the card
        },
    ],
    model_type=genanki.Model.CLOZE
)

# Folder for temporary audio files
audio_dir = tempfile.mkdtemp()
audio_files = []

# Generate audio and flashcards
for index, row in df.iterrows():
    # Full answer text for TTS
    full_answer_text = extract_full_answer(row['ClozeQuestion'])
    # Generate audio
    tts = gTTS(text=full_answer_text, lang='en')
    audio_file = os.path.join(audio_dir, f'audio_{index}.mp3')
    tts.save(audio_file)
    audio_files.append(audio_file)

    # Create a Cloze note
    note = genanki.Note(
        model=cloze_model,
        fields=[row['ClozeQuestion'], f'[sound:audio_{index}.mp3]', row['ExtraInformation']]
    )
    my_deck.add_note(note)

# Save the deck to a file
output_file = './outoutDeck/myDeck.apkg'
genanki.Package(my_deck, media_files=audio_files).write_to_file(output_file)
print("Deck is successfully created")
