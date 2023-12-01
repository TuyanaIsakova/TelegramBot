x = "100 hotel"
money = 0
reason = ""
for i in x.split():
    try:
        money = int(i)
    except Exception as e:
        reason = ''.join(i)

print(x.split())
print(f"Money: {money}")
print(f"Payment reason: {reason}")

x = ['a', 'b', 'c']
y = 'abc'
d = ' '.join([i for i in x])
print(d)