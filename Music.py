import sys
import subprocess

print("Bienvenue dans le programme d'enregistrement et de transcription musicale !")
print("Ce programme va enregistrer votre audio, détecter les notes, et permettre la lecture via MIDI avec l'instrument de votre choix.")

packages = {
    "pyaudio": "pyaudio",
    "wave": None,  # Module standard de Python
    "threading": None,  # Module standard de Python
    "librosa": "librosa",
    "numpy": "numpy",
    "time": None,  # Module standard de Python
    "mido": "mido",
    "rtmidi": "python-rtmidi",
    "pydub": "pydub"
}

def install_and_import(package, module=None):
    if module is None:
        module = package
    try:
        __import__(module)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[module] = __import__(module)

# Exécute la fonction pour chaque paquet requis
for module, package in packages.items():
    if package is not None:  # Seulement installer s'il n'est pas un module standard
        install_and_import(package, module)

import wave
import threading
import time
from mido import Message
from pydub import AudioSegment
from pydub.playback import play

# Paramètres d'enregistrement
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 500
WAVE_OUTPUT_FILENAME = "output.wav"

# Initialiser PyAudio
p = pyaudio.PyAudio()
is_recording = True

def stop_recording():
    global is_recording
    input("Appuyez sur Entrée pour arrêter l'enregistrement...")
    is_recording = False

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Enregistrement en cours... (Appuyez sur Entrée pour arrêter)")
frames = []

thread = threading.Thread(target=stop_recording)
thread.start()

while is_recording:
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Enregistrement terminé, fichier sauvegardé sous : {WAVE_OUTPUT_FILENAME}")

# Lecture du fichier WAV original
audio = AudioSegment.from_file(WAVE_OUTPUT_FILENAME)
play(audio)

# MIDI output
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

# Liste étendue d'instruments avec option de sortie
instruments = {
    0: "Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    3: "Honky-tonk Piano",
    4: "Electric Piano 1",
    5: "Electric Piano 2",
    6: "Harpsichord",
    7: "Clavi",
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)",
    28: "Electric Guitar (muted)",
    29: "Overdriven Guitar",
    30: "Distortion Guitar",
    31: "Guitar harmonics",
    32: "Acoustic Bass",
    33: "Electric Bass (finger)",
    34: "Electric Bass (pick)",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "SynthStrings 1",
    51: "SynthStrings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "Synth Brass 1",
    63: "Synth Brass 2",
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
    80: "Lead 1 (square)",
    81: "Lead 2 (sawtooth)",
    82: "Lead 3 (calliope)",
    83: "Lead 4 (chiff)",
    84: "Lead 5 (charang)",
    85: "Lead 6 (voice)",
    86: "Lead 7 (fifths)",
    87: "Lead 8 (bass + lead)",
    88: "Pad 1 (new age)",
    89: "Pad 2 (warm)",
    90: "Pad 3 (polysynth)",
    91: "Pad 4 (choir)",
    92: "Pad 5 (bowed)",
    93: "Pad 6 (metallic)",
    94: "Pad 7 (halo)",
    95: "Pad 8 (sweep)",
    96: "FX 1 (rain)",
    97: "FX 2 (soundtrack)",
    98: "FX 3 (crystal)",
    99: "FX 4 (atmosphere)",
    100: "FX 5 (brightness)",
    101: "FX 6 (goblins)",
    102: "FX 7 (echoes)",
    103: "FX 8 (sci-fi)",
    104: "Sitar",
    105: "Banjo",
    106: "Shamisen",
    107: "Koto",
    108: "Kalimba",
    109: "Bagpipe",
    110: "Fiddle",
    111: "Shanai",
    112: "Tinkle Bell",
    113: "Agogo",
    114: "Steel Drums",
    115: "Woodblock",
    116: "Taiko Drum",
    117: "Melodic Tom",
    118: "Synth Drum",
    119: "Reverse Cymbal",
    120: "Guitar Fret Noise",
    121: "Breath Noise",
    122: "Seashore",
    123: "Bird Tweet",
    124: "Telephone Ring",
    125: "Helicopter",
    126: "Applause",
    127: "Gunshot"
}

# Détection de note
y, sr = librosa.load(WAVE_OUTPUT_FILENAME, sr=None)
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
note_dict = {}

for i in range(pitches.shape[1]):
    pitch = pitches[:, i].argmax()
    if magnitudes[pitch, i] > 15: # Magnitude supérieur à 15
        note = librosa.hz_to_midi(pitches[pitch, i])
        note_name = librosa.midi_to_note(int(note))
        if note_name in note_dict:
            note_dict[note_name] += 1
        else:
            note_dict[note_name] = 1

filtered_notes = [note for note, count in note_dict.items() if count > 2]
print("Notes détectées :", filtered_notes)

while True:  # Boucle pour choisir l'instrument et jouer les notes
    print("Liste des instruments disponibles (ou tapez -1 pour sortir):")
    for num, name in instruments.items():
        print(f"{num}: {name}")
    instr_choice = int(input("\nEntrez le numéro de l'instrument désiré: "))

    if instr_choice == -1:
        print("Sortie du programme.")
        break

    midiout.send_message(Message('program_change', program=instr_choice).bytes())

    # Jouer les notes détectées
    for note_name in filtered_notes:
        note_midi = librosa.note_to_midi(note_name)
        message = Message('note_on', note=note_midi, velocity=64)
        midiout.send_message(message.bytes())
        time.sleep(0.25)  # Durée de chaque note pendant 0.25 seconde
        message = Message('note_off', note=note_midi)
        midiout.send_message(message.bytes())

midiout.close_port()
print("Playback terminé.")

