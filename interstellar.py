import math
import numpy as np
# Librosa for audio
import librosa


def doit(pitches, magnitudes, reverse_bit_stream, symbol_flip, symbol_length):
	out_freq = []
	in_tone = False

	# find the frequency at each point in the track
	for i in range(0, magnitudes.shape[1]):
		index = magnitudes[:, i].argmax()
		pitch = pitches[index,i]
		pitch = math.floor(pitch)
		if (pitch == 0):
			in_tone = False
		elif(not in_tone):
			in_tone = True
			out_freq.append(pitch)
			# print(i, " ", pitch)

	out_freq = np.asarray(out_freq)

	# print(out_freq.size)

	out_bits = []

	# classify the frequencies into high(1) and low(0)
	for i in out_freq:
		if (i > 150 and i < 250):
			out_bits.append(0)
		if (i > 350 and i < 450):
			out_bits.append(1)

	if (reverse_bit_stream):
		out_bits.reverse()

	out_bits = np.asarray(out_bits)

	print(out_bits)

	out_ordered_bits = out_bits

	if (symbol_flip):
		out_lsb_bits = []
		# re-arrange the bits from msb to lsb order?
		for i in range(0, math.floor(out_bits.size / symbol_length)):
			base = i * symbol_length
			for x in range(0, symbol_length):
				offset = base + ((symbol_length - 1)-x)
				out_lsb_bits.append(out_bits[offset])

		out_ordered_bits = np.asarray(out_lsb_bits)

	# print(out_lsb_bits.size)

	out_bytes = []
	out_str = ""

	# convert each byte into a character, then to a string
	for i in range(0, math.floor(out_ordered_bits.size / symbol_length)):
		base = i * symbol_length
		char = "0b"
		for x in range(0, symbol_length):
			offset = base + x
			char = char + str(out_ordered_bits[offset])
		out_bytes.append(int(char, 2))
		out_str = out_str + chr(int(char, 2))

	# print(out_bytes)
	print(out_str, end='')
	print()
	print()
	print("-----------------------------------")
	print()


audio_path = '/Users/grant/Desktop/interstellar.wav'
y, sr = librosa.load(audio_path, sr=None)

pitches, magnitudes = librosa.piptrack(y, sr, n_fft=3500, fmin=200, fmax=600)

doit(pitches, magnitudes, False, True, 8)
doit(pitches, magnitudes, False, True, 7)
doit(pitches, magnitudes, False, True, 6)
doit(pitches, magnitudes, False, False, 8)
doit(pitches, magnitudes, False, False, 7)
doit(pitches, magnitudes, False, False, 6)
doit(pitches, magnitudes, True, True, 8)
doit(pitches, magnitudes, True, True, 7)
doit(pitches, magnitudes, True, True, 6)
doit(pitches, magnitudes, True, False, 8)
doit(pitches, magnitudes, True, False, 7)
doit(pitches, magnitudes, True, False, 6)