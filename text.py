t = []
s = open('supers.csv', 'r').readlines()
count = 1
for i in s:
	if count % 2 == 0:
		t.append(i.strip('"').strip('\n').strip('"').strip())
	count += 1
