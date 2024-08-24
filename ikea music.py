from mido import MidiFile, MidiTrack, Message, MetaMessage

# Define note durations (in ticks) for each beat (quarter note)
note_durations = {
    1: 480,  # whole note
    2: 240,  # half note
    4: 120,  # quarter note
    8: 60,   # eighth note
    16: 30,  # sixteenth note
}

# Define the music
music_notes = [
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
    # Cmaj7
    [("E4", 4), ("G4", 4), ("B4", 4), ("C5", 4)],
    # Fmaj7
    [("F4", 4), ("A4", 4), ("C5", 4), ("E5", 4)],
    # Am7
    [("E4", 4), ("G4", 4), ("A4", 4), ("C5", 4)],
    # G
    [("D4", 4), ("G4", 4), ("B4", 4), ("G4", 4)],
]

# Create a new MIDI file
mid = MidiFile()

# Create a new track
track = MidiTrack()
mid.tracks.append(track)

# Set tempo (120 BPM)
ticks_per_beat = mid.ticks_per_beat
microseconds_per_beat = int(1e6 / 12)  # microseconds per beat
track.append(MetaMessage('set_tempo', tempo=microseconds_per_beat))

# Add notes to the track
time = 0
for measure in music_notes:
    for note, duration in measure:
        note_value, octave = note[:-1], int(note[-1])
        note_number = 12 + 12 * (octave - 4) + ("C C#D D#E F F#G G#A A#B".index(note_value) // 2)
        track.append(Message('note_on', note=note_number, velocity=64, time=time))
        time += note_durations[duration]
        track.append(Message('note_off', note=note_number, velocity=64, time=time))

# Save the MIDI file
mid.save('ikea_music.mid')
