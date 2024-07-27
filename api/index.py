from flask import Flask, jsonify
import random
import pyaudio
import wave
from openai import OpenAI
from flask_cors import CORS
from dotenv import load_dotenv
import os
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
load_dotenv()
OPEN_API_KEY = os.getenv('OPEN_API_KEY')
COUPLED = ""
SOUND_REFERENCE = {
    'S': 'SH',
    'F': 'TH',
    'L': 'R',
    'B': 'V',
    'P': 'F',
    'T': 'D'
}
PRONUNCIATION = {
    "sunday": "sʌn.deɪ",
    "free": "friː",
    "love": "lʌv",
    "boat": "boʊt",
    "pen": "pen",
    "tree": "triː"
}
LETTERS = ['S', 'F', 'L', 'B', 'P', 'T']
EXAMPLE = {
    'S': 'sunday',
    'F': 'free',
    'L': 'love',
    'B': 'boat',
    'P': 'pen',
    'T': 'tree'
}

REMEDY = {
    'P': ['Put your lips together to make the sound. Vocal cords dont vibrate for voiceless sounds.'],
    'B': ['Put your lips together to make the sound. '],
    'M': ['Put your lips together to make the sound. Air flows through your nose.'],
    'W': ['Put your lips together and shape your mouth like you are saying "oo".'],
    'F': ['Place your bottom lip against your upper front teeth. Top teeth may be on your bottom lip.'],
    'V': ['Place your bottom lip against your upper front teeth. Top teeth may be on your bottom lip.'],
    'S': ["Keep your teeth close together to make the sound. The ridge right behind your two front teeth is involved. The front of your tongue is used. Vocal cords don't vibrate for voiceless sounds."],
    'Z': ['Keep your teeth close together to make the sound. The ridge right behind your two front teeth is involved. The front of your tongue is used.'],
    'th': ['Place your top teeth on your bottom lip and let your tongue go between your teeth for the sound. The front of your tongue is involved.'],
    'TH': ['Place your top teeth on your bottom lip and let your tongue go between your teeth for the sound (as in thin). The front of your tongue is involved. The front of your tongue is used.'],
    'NG': ['Air flows through your nose.'],
    'SING': ['Air flows through your nose.'],
    'L': ['The ridge right behind your two front teeth is involved. The front of your tongue is used.'],
    'T': ["The ridge right behind your two front teeth is involved. The front of your tongue is used. Vocal cords don't vibrate for voiceless sounds."],
    'D': ['The ridge right behind your two front teeth is involved. The front of your tongue is used.'],
    'CH': ['The front-roof of your mouth is the right spot for the sound.'],
    'J': ['The front-roof of your mouth is the right spot for the sound. The front of your tongue is used.'],
    'SH': ['The front-roof of your mouth is the right spot for the sound. The front of your tongue is used.'],
    'ZH': ['The front-roof of your mouth is the right spot for the sound. The front of your tongue is used.'],
    'K': ["The back-roof of your mouth is the right spot for the sound. The back of your tongue is used. Vocal cords don't vibrate for voiceless sounds."],
    'G': ['The back-roof of your mouth is the right spot for the sound. The back of your tongue is used.'],
    'R': ['The back-roof of your mouth is the right spot for the sound. The back of your tongue is used.'],
    'Y': ['The front of your tongue is used.'],
    'CH': ['The front of your tongue is used.'],
    'H': ['Your lungs provide the airflow for every sound, especially this one.']
}


def check(word_given, word_recieved, check_for):
        for i in range(len(word_recieved)):
              if word_recieved[i]=='.' or word_recieved[i]=='\n' or word_recieved[i]==' ' or word_recieved[i]=='!':
                    word_recieved=word_recieved[0:i]
                    break
        print(word_given,word_recieved,check_for)
        if word_recieved[0:len(SOUND_REFERENCE[check_for])] == SOUND_REFERENCE[check_for]:
            #print(word_recieved[len(SOUND_REFERENCE[check_for]):],word_given[len(check_for):])
            if word_recieved[len(SOUND_REFERENCE[check_for]):]==word_given[len(check_for):]:

                 return 20
            else:
                 return 0

            #return [0,REMEDY[check_for]]
        elif word_recieved[0:len(check_for)]==word_given[0:len(check_for)]:
            if word_recieved[len(check_for):]==word_given[len(check_for):]:
                 return 100
            else:
                 return 75
        else:
            # print('dasd')
            return 0


@app.route('/record', methods=["GET"])
def record():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    client = OpenAI(api_key=OPEN_API_KEY)

    audio_file = open("output.wav", "rb")
    transcript = client.audio.translations.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    print(transcript.upper())
    percentage = check(EXAMPLE[COUPLED].upper(), transcript.upper(), COUPLED.upper())

    print(percentage)
    word_percentage = {
        "transcript": transcript,
        "percentage": percentage
    }
    return jsonify(word_percentage)


@app.route("/remedy/<int:averagePercentage>", methods=["GET", "POST"])
def remedy(averagePercentage):
    if (averagePercentage<=50):
        result = {
            "remedy":REMEDY[COUPLED]
        }
    else:
        result = {
            "remedy":""
        }

    return jsonify(result)


@app.route("/generate_word", methods=["GET"])
def generate_word():
    global COUPLED
    COUPLED = ""
    COUPLED = random.choice(LETTERS)

    word_data = {
        "word1": EXAMPLE[COUPLED],
        "letter": COUPLED,
        "pronunciation": PRONUNCIATION[EXAMPLE[COUPLED[0]]]

    }
    print(COUPLED)
    return jsonify(word_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
