for m in girigiri
do
	for t in 十二平均律 五度相生律 纯律
	do
		timidity $m.mid -Z $t.txt -Ow -o $m-$t.wav
		ffmpeg -i $m-$t.wav $m-$t.flac
	done
done
