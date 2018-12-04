from sklearn import svm
import math
import collections
from read-wav import read-wav.py

training_data = [read_wave('歌唱祖国-十二平均律.wav'), read_wave('歌唱祖国-五度相生律.wav'), read_wave('歌唱祖国-纯律.wav'), read_wave('alphabet-十二平均律.wav'), read_wave('-五度相生律.wav'), read_wave('alphabet-纯律.wav')]
training_label = [0,1,2,0,1,2]
testing_data =[read_wave('燕园情-十二平均律.wav'), read_wave('燕园情-五度相生律.wav'), read_wave('燕园情-纯律.wav')]

clf = svm.SVC(gamma='scale')
clf.fit(training_data, training_label)
for i in range(3):
	print (clf.predict([testing_data[i]]))
