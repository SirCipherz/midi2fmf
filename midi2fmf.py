#!/usr/bin/python3
from mido import MidiFile
from sys import argv
import math

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

def number_to_note(number: int) -> tuple:
        octave = number // NOTES_IN_OCTAVE
        note = NOTES[number % NOTES_IN_OCTAVE]

        return note, octave

mid = MidiFile(argv[1], clip=True)

notes = ""
bpm = 130

for msg in mid:
        msg_dict = msg.dict()

        if msg_dict["type"] == "set_tempo":
                bpm = math.floor(60000000 / msg_dict["tempo"])

        if msg_dict["type"] == "note_on" and msg_dict["time"] > 0.007:
                pause = str(round(3 / msg_dict["time"]))
                notes = notes + pause + "P, "

        if msg_dict["type"] == "note_off" and msg_dict["time"] > 0.007:
                pause = str(round(3 / msg_dict["time"]))
                note = number_to_note(msg_dict["note"])

                notes = notes + pause + note[0] + str(note[1]) + ", "

notes = notes[:-2]

format = """Filetype: Flipper Music Format
Version: 0
BPM: """ + str(bpm) + """
Duration: 12
Octave: 5
Notes: """ + notes

print(format)
