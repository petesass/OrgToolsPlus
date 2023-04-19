import tkinter as tk
import random
import mido

window = tk.Tk()
window.title("MIDI Melody Generator")
window.geometry("600x400")

title_label = tk.Label(window, text="MIDI Melody Generator", font=("Arial", 24))
title_label.pack()

options_frame = tk.Frame(window)
options_frame.pack()

tempo_label = tk.Label(options_frame, text="Tempo (BPM):")
tempo_label.grid(row=0, column=0)
tempo_scale = tk.Scale(options_frame, from_=40, to=200, orient=tk.HORIZONTAL)
tempo_scale.set(120)
tempo_scale.grid(row=0, column=1)

length_label = tk.Label(options_frame, text="Length (bars):")
length_label.grid(row=1, column=0)
length_scale = tk.Scale(options_frame, from_=4, to=32, orient=tk.HORIZONTAL)
length_scale.set(8)
length_scale.grid(row=1, column=1)

key_label = tk.Label(options_frame, text="Key:")
key_label.grid(row=2, column=0)
key_listbox = tk.Listbox(options_frame, height=12, selectmode=tk.MULTIPLE)
keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for key in keys:
    key_listbox.insert(tk.END, key)
key_listbox.selection_set(0)
key_listbox.grid(row=2, column=1)

mode_label = tk.Label(options_frame, text="Mode:")
mode_label.grid(row=3, column=0)
mode_listbox = tk.Listbox(options_frame, height=2)
modes = ["Major", "Minor"]
for mode in modes:
    mode_listbox.insert(tk.END, mode)
mode_listbox.selection_set(0)
mode_listbox.grid(row=3, column=1)

composer_label = tk.Label(options_frame, text="Composer:")
composer_label.grid(row=4, column=0)
composer_listbox = tk.Listbox(options_frame, height=4)
composers = ["Bach", "Mozart", "Chopin", "Random"]
for composer in composers:
    composer_listbox.insert(tk.END, composer)
composer_listbox.selection_set(3)
composer_listbox.grid(row=4, column=1)

generate_button = tk.Button(window, text="Generate", font=("Arial", 16))
generate_button.pack()

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NUMBERS = {name: i for i, name in enumerate(NOTE_NAMES)}
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]
CHORDS = {
    (0, 4): [0], # I
    (5, 9): [5], # V
    (7, 11): [7], # vii°
    (2, 5): [2], # ii
    (3 ,7): [3], # iii
    (9 ,12): [9], # vi
    (11 ,14): [11], # vii°
    (4 ,8): [4], # IV+
}
CHORD_PROGRESSIONS = {
    "Major": [
        [(0,), (5,), (9,), (5,), (0,), (5,), (9,), (5,),], # I-V-vi-V-I-V-vi-V
        [(0,), (5,), (9,), (4,), (0,), (5,), (9,), (4,),], # I-V-vi-IV-I-V-vi-IV
        [(0,), (4,), (5,), (0,), (9,), (4,), (5,), (9,),], # I-IV-V-I-vi-IV-V-vi
        [(0,), (4,), (2,), (5,), (9,), (2,), (5,), (0,),], # I-IV-ii-V-vi-ii-V-I
    ],
    "Minor": [
        [(9,), (2,), (5,), (9,), (3,), (7,), (11,), (3,)], # vi-ii-V-vi-iii-vii°-I-iii        
        [(9,), (2,), (5,), (9,), (3,), (7,), (0, 4), (3,)], # vi-ii-V-vi-iii-vii°-I+-iii
        [(9,), (2,), (5,), (9,), (11,), (5,), (0, 4), (11,)], # vi-ii-V-vi-I-V-I+-I
        [(9,), (7,), (11,), (9,), (2,), (7,), (11,), (2,)], # vi-vii°-I-vi-ii-vii°-I-ii
    ],
}
def generate_melody():
    tempo = tempo_scale.get()
    length = length_scale.get()
    key = key_listbox.get(key_listbox.curselection()[0])
    mode = mode_listbox.get(mode_listbox.curselection()[0])
    composer = composer_listbox.get(composer_listbox.curselection()[0])

    midi_file = mido.MidiFile()
    midi_file.ticks_per_beat = 480
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

    scale = MAJOR_SCALE if mode == "Major" else MINOR_SCALE
    tonic = NOTE_NUMBERS[key]
    notes = [tonic + note for note in scale] + [tonic + 12]
    octave = 4
    velocity = 64
    time = 0

    if composer == "Random":
        composer = random.choice(list(CHORD_PROGRESSIONS.keys()))
    progression = random.choice(CHORD_PROGRESSIONS[composer])

    for bar in range(length):
        chord = progression[bar % len(progression)]
        chord_notes = [notes[note] + octave * 12 for note in chord]

        for beat in range(4):
            subdivision = random.randint(1, 4)
            duration = midi_file.ticks_per_beat // subdivision

            if random.random() < 0.8:
                note = random.choice(chord_notes)
            else:
                note = random.choice(notes) + octave * 12

            if note > 84:
                octave -= 1
                note -= 12
            elif note < 48:
                octave += 1
                note += 12

            track.append(mido.Message("note_on", note=note, velocity=velocity, time=time))
            track.append(mido.Message("note_off", note=note, velocity=velocity, time=duration))
            time = 0

    track.append(mido.MetaMessage("end_of_track"))

    midi_file.save("temp.mid")

def play_melody():
    import pygame

    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load("temp.mid")
    pygame.mixer.music.play()

generate_button.config(command=generate_melody)

play_button = tk.Button(window, text="Play", font=("Arial", 16))
play_button.pack()

play_button.config(command=play_melody)

window.mainloop()
