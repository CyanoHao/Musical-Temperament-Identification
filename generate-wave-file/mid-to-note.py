import mido

mid = mido.MidiFile('alphabet.mid')

notelist = []

for msg in mid:
	if isinstance(msg, mido.messages.messages.Message):
		d = msg.dict()
		if d['type'] == 'note_on':
			notelist.append(d['note'])

print(notelist)