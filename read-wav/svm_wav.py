from sklearn import svm
import math
import collections

import wave
import numpy as np
import math

import matplotlib.pyplot as plt

def ratio_to_cent(num):
	decpart = num - math.floor(num)
	cent = int(round(decpart * 1200))
	if cent == 1200:
		cent = 0
	return cent

def read_wave(filename, start = 0, end = 1):
	#读取wav文件，我这儿读了个自己用python写的音阶的wav
	wavefile = wave.open(filename, 'r') # open for writing
	
	#读取wav文件的四种信息的函数。期中numframes表示一共读取了几个frames，在后面要用到滴。
	nchannels = wavefile.getnchannels()
	sample_width = wavefile.getsampwidth()
	framerate = wavefile.getframerate()
	numframes = wavefile.getnframes()
	
	bytes_per_frame = nchannels * sample_width

	# print("channel",nchannels)
	# print("sample_width",sample_width)
	# print("framerate",framerate)
	# print("numframes",numframes)

	# 每个 block 3 秒钟，频谱分辨率为 1/3 Hz	
	frames_per_block = int(framerate * 3)
	blocks = int(numframes / frames_per_block)

	freqs = np.fft.fftfreq(frames_per_block)
	spectum = list(0 for _ in range(frames_per_block))
	spectum = np.array(freqs)

	# 对每个 block 做 FFT，将所得频谱叠加
	for _ in range(int(blocks * start), int(blocks * end)):
		amps = list(0 for _ in range(frames_per_block))
		buffer = wavefile.readframes(frames_per_block)
		for j in range(frames_per_block):
			ch0 = buffer[bytes_per_frame * j:bytes_per_frame * j + sample_width]
			amps[j] = int.from_bytes(ch0, byteorder = 'little', signed = True)

		data = np.array(amps)
		w = np.fft.fft(data)
		spectum += np.abs(w)

		# # Find the peak in the coefficients
		# idx = np.argmax(np.abs(w))
		# freq = freqs[idx]
		# freq_in_hertz = abs(freq * framerate)
		# print(freq_in_hertz)

	cent_hist = list(0 for _ in range(1200))

	# 取 110 Hz 到 1760 Hz 转换成音分（A4 上下各 2 个八度）
	for i in range(frames_per_block):
		freq_in_hertz = freqs[i] * framerate
		if freq_in_hertz >= 110 and freq_in_hertz <= 1760:
			cent = ratio_to_cent(freq_in_hertz / 440)
			cent_hist[cent] += spectum[i]

	# fig, ax = plt.subplots()
	# ax.plot(list(range(1200)), cent_hist)
	# plt.show()

	return cent_hist

filename_list = ['girigiri-十二平均律.wav', 'girigiri-五度相生律.wav', 'girigiri-纯律.wav', '歌唱祖国-十二平均律.wav', '歌唱祖国-五度相生律.wav', '歌唱祖国-纯律.wav', 'alphabet-十二平均律.wav', 'alphabet-五度相生律.wav', 'alphabet-纯律.wav']
filename_list_testing = ['燕园情-十二平均律.wav', '燕园情-五度相生律.wav', '燕园情-纯律.wav']
segment = 20
training_data = [0] * len(filename_list) * (segment - 2)
training_label = [0] * len(filename_list) * (segment - 2)

for i in range(len(filename_list)):
	for j in range(segment - 2):
		training_data[i * (segment - 2) + j] = read_wave(filename_list[i], float(j)/float(segment), float(j + 1)/float(segment))
		training_label[i * (segment - 2) + j] = i % 3

testing_data = [0] * len(filename_list_testing)
for i in range(len(filename_list_testing)):
	testing_data[i] = read_wave(filename_list_testing[i], 0, 1)

clf = svm.SVC(gamma='scale')
clf.fit(training_data, training_label)

for i in range(len(filename_list_testing)):
	print (clf.predict([testing_data[i]]))

