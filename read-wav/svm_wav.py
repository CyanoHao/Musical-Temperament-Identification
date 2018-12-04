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
	wavefile = wave.open(filename, 'r') # open for reading
	
	#读取wav文件的四种信息的函数。期中numframes表示一共读取了几个frames。
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

	cent_hist = list(float(0) for _ in range(1200))

	# 取 110 Hz 到 1760 Hz 转换成音分（A4 上下各 2 个八度）
	for i in range(frames_per_block):
		freq_in_hertz = freqs[i] * framerate
		if freq_in_hertz >= 110 and freq_in_hertz <= 1760:
			cent = ratio_to_cent(freq_in_hertz / 440)
			cent_hist[cent] += spectum[i]

	# normalize cent_hist
	cent_hist_total = float(0)
	for i in range(len(cent_hist)):
		cent_hist_total += cent_hist[i]

	for i in range(len(cent_hist)):
		cent_hist[i] = cent_hist[i]/cent_hist_total

	'''
	fig, ax = plt.subplots()
	ax.plot(list(range(1200)), cent_hist)
	plt.show()
	print(cent_hist_total)
	'''
	return cent_hist
#训练集文件名和测试集文件名
filename_list = ['girigiri-十二平均律.wav', 'girigiri-五度相生律.wav', 'girigiri-纯律.wav', '歌唱祖国-十二平均律.wav', '歌唱祖国-五度相生律.wav', '歌唱祖国-纯律.wav', 'alphabet-十二平均律.wav', 'alphabet-五度相生律.wav', 'alphabet-纯律.wav','燕园情-十二平均律.wav', '燕园情-五度相生律.wav', '燕园情-纯律.wav']
filename_list_testing = ['girigiri-十二平均律.wav', 'girigiri-五度相生律.wav', 'girigiri-纯律.wav', '歌唱祖国-十二平均律.wav', '歌唱祖国-五度相生律.wav', '歌唱祖国-纯律.wav', 'alphabet-十二平均律.wav', 'alphabet-五度相生律.wav', 'alphabet-纯律.wav','燕园情-十二平均律.wav', '燕园情-五度相生律.wav', '燕园情-纯律.wav']
#分段个数
training_segment = 3
testing_segment = 2
segment = training_segment + testing_segment

training_data = [0] * len(filename_list) * training_segment
training_label = [0] * len(filename_list) * training_segment

for i in range(len(filename_list)):
	for j in range(training_segment):
		training_data[i * training_segment + j] = read_wave(filename_list[i], float(j)/float(segment), float(j + 1)/float(segment))
		training_label[i * training_segment + j] = i % 3

testing_data = [0] * len(filename_list_testing) * testing_segment
testing_label = [0] * len(filename_list_testing) * testing_segment
for i in range(len(filename_list_testing)):
	for j in range(testing_segment):
		testing_data[i * testing_segment + j] = read_wave(filename_list_testing[i], float(training_segment + j)/float(segment), float(training_segment + j + 1)/float(segment))
		testing_label[i * testing_segment + j] = i % 3

clf = svm.SVC(gamma='scale')
clf.fit(training_data, training_label)

correct_count = 0
predict = clf.predict(testing_data)
print (predict)

for i in range(len(filename_list_testing) * 2):
	if(predict[i] == testing_label[i]):
		print('correct')
		correct_count += 1
print('correct count',correct_count)

