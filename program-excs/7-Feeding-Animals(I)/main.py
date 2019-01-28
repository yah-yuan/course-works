def main():
    num = input()
    num = int(num)
    person = []
    animal = []
    time = 0
    for _ in range(num):
        animal.append([])
    for _ in range(8):
        s = input()
        s = s.split(' ')
        n = []
        for i in s:
            n.append(int(i))
        person.append(n)
    
    for i in range(num):
        for p in person:
            animal[i].append(p[i])
    
    for i in range(num):
        time += min(animal[i])
    print(time)

try: 
    while True:
        main()
except:
    pass