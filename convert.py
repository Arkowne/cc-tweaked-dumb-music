import mido
import math
import sys

def main():
    # Vérification des arguments
    if len(sys.argv) != 4:
        print("Usage: python midi2bin.py INFILE.mid OUTFILE.bin TEMPO")
        sys.exit(1)

    MIDI_FILE = sys.argv[1]
    OUTPUT_BIN = sys.argv[2]
    try:
        BPM = float(sys.argv[3])
    except ValueError:
        print("Le tempo (BPM) doit être un nombre.")
        sys.exit(1)

    # Paramètres fixes ou à adapter si besoin
    NOTE_MIN = 56           # Première note (A0)
    NOTE_MAX = 92           # Dernière note (36 notes au total)
    NOTES = list(range(NOTE_MIN, NOTE_MAX + 1))

    SUBDIV_PER_MEASURE = 24 # Nombre de subdivisions par mesure
    BEATS_PER_MEASURE = 4   # Nombre de temps par mesure (ex: 4/4 = 4)

    delay = round((60 / BPM) / SUBDIV_PER_MEASURE, 3)

    # Variables calculées
    NOTE_COUNT = len(NOTES)             
    BYTE_COUNT = math.ceil(NOTE_COUNT / 8)
    beat_sec = 60 / BPM
    measure_sec = beat_sec * BEATS_PER_MEASURE
    step_sec = measure_sec / SUBDIV_PER_MEASURE

    # Lecture MIDI
    mid = mido.MidiFile(MIDI_FILE)
    total_time = mid.length
    steps = int(total_time / step_sec) + 1
    timeline = [set() for _ in range(steps)]

    current_notes = set()
    current_time = 0
    step_idx = 0

    for msg in mid:
        current_time += msg.time
        while step_idx < steps and (step_idx * step_sec) < current_time:
            timeline[step_idx] = set(current_notes)
            step_idx += 1
        if msg.type == 'note_on' and msg.velocity > 0:
            current_notes.add(msg.note)
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            current_notes.discard(msg.note)

    while step_idx < steps:
        timeline[step_idx] = set(current_notes)
        step_idx += 1

    # Écriture binaire
    with open(OUTPUT_BIN, 'wb') as f:
        for notes_on in timeline:
            bits = 0
            byte_list = []
            for i, n in enumerate(NOTES):
                if n in notes_on:
                    bits |= (1 << (7 - (i % 8)))
                if (i + 1) % 8 == 0 or i == len(NOTES) - 1:
                    byte_list.append(bits)
                    bits = 0
            f.write(bytearray(byte_list))

    print(f"Conversion binaire terminée ! Résultat dans {OUTPUT_BIN}")
    print(f"Tempo: {BPM} BPM, subdivisions par mesure: {SUBDIV_PER_MEASURE}, durée subdivision: {step_sec:.4f}s")
    print(f"Delay : {delay}")

if __name__ == "__main__":
    main()
