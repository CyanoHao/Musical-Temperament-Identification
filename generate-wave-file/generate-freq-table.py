import math

# 纯律 just intonation
ji_table = [
	1,     # C
	16/15, # D♭-
	9/8,   # D
	6/5,   # E♭
	5/4,   # E
	4/3,   # F
	45/32, # F♯+
	3/2,   # G
	8/5,   # A♭
	5/3,   # A
	16/9,  # B♭-
	15/8,  # B
]

# 五度相生律 Pythagorean tuning
pt_table = [
	1,          # C
	3**7/2**11, # C♯
	3**2/2**3,  # D
	2**5/3**3,  # E♭
	3**4/2**6,  # E
	2**2/3,     # F
	3**6/2**9,  # F♯
	3/2,        # G
	3**8/2**12, # G♯
	3**3/2**4,  # A
	2**4/3**2,  # B♭
	3**5/2**7,  # B
]

# 十二平均律 equal temperament
et_table = list(map(lambda x: 2**(x/12), range(12)))

def generate_freq_table(table, filename):
	with open(filename, 'w') as file:
		for tone in range(128):
			# MIDI 的音从 C-1 开始
			group = -1 + math.floor(tone / 12)
			base = 440 / table[9] * 2**(group - 4)
			file.write("{0}\n".format(round(base * table[tone % 12] * 1000)))

if __name__ == '__main__':
	generate_freq_table(ji_table, "ji.txt")
	generate_freq_table(pt_table, "pt.txt")
	generate_freq_table(et_table, "et.txt")