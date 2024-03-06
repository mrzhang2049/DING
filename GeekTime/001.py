tr = '999'
print(f'''
H 
       OIP{tr}
''')
print('s' in 'sx')

print('qw' * 3)

print(['6', 'DF', 67])

print([x for x in range(1, 10)])

dicx = {"av": 1, "bx": 123}
print(dicx.keys())
dicx["av"] = 999
dicx["df"] = 899
dicx.setdefault("af", "ppp")
newDIx = {"av": 888, "F#": 2058}
dicx |= newDIx
for key, val in dicx.items():
    print(key, val)
