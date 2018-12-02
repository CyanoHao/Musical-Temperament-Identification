import math

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
midi_num_of_A = 69

#ABCDEFG对应的音级
pitch_to_tone_table = [
0,2,3,5,7,8,10
]

#燕园情简谱
yyq_num = [
3,3,3,3,3,3,2,3,-5,-5,-5,-5,-5,-5,-5,-5,3,3,3,3,3,3,2,3,5,5,5,5,5,5,3,5,6,6,6,6,6,6,5,6,1,1,1,1,1,1,1,1,
-6,-5,-6,1,2,1,2,3,2,2,2,2,2,2,2,2,3,3,3,3,3,3,2,3,-5,-5,-5,-5,-5,-5,-5,-5,3,3,3,3,3,3,2,3,5,5,5,5,5,5,3,5,
6,6,6,6,6,6,5,6,1,1,1,1,1,1,1,1,-6,-5,-6,1,2,1,2,3,1,1,1,1,1,1,1,1,6,6,6,6,4,4,1,6,5,5,5,5,3,3,3,1,
2,2,2,3,2,2,2,1,3,3,3,3,3,3,1,1,6,6,6,6,4,4,1,6,5,5,5,5,3,3,3,3,2,2,2,1,2,2,2,3,2,2,2,2,2,2,-5,-5,
3,3,3,3,1,1,-5,5,3,3,3,3,3,3,3,3,4,4,4,5,6,6,6,5,4,4,4,4,4,4,-6,-6,3,3,3,3,2,2,6,1,3,3,3,3,2,2,2,3,
2,2,2,1,2,2,2,3,1,1,1,1,1,1,1,1,6,6,6,6,6,6,1,6,5,5,5,5,5,5,1,1,6,6,6,6,6,6,4,6,5,5,5,5,5,5,-5,-5,
3,3,3,4,2,2,-6,1,2,2,2,3,5,5,5,5,5,1,1,6,6,6,6,6,1,6,5,5,5,5,5,5,1,1,
6,6,6,6,6,6,4,6,5,5,5,5,5,5,-5,-5,3,3,3,5,2,2,-6,1,2,2,2,2,3,3,3,3,1,1,1,1,1,1
]

def generate_freq_table(filename, num_notation, pitch_of_one ):
	with open(filename, 'w') as file:
		for num in num_notation:
			midi_num = midi_num_of_A
			if num < 0:
				midi_num -= 12
				num = -num
			pitch = num + pitch_of_one - 1
			while pitch >= 7:
				midi_num += 12
				pitch -= 7
			midi_num += pitch_to_tone_table[pitch]
			file.write("{0},".format(midi_num))

if __name__ == '__main__':
	generate_freq_table("yyq_midi.txt", yyq_num, G )