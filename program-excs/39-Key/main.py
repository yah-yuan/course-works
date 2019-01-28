def main():
    num = input()
    num = int(num)
    store = list(0 for _ in range(num))
    length = num
    s = input()
    s = s.split()
    loc = []
    for item in s:
        loc.append(int(item))
    for i in range(len(loc)):
        num = i+1
        pos = loc[i] - 1
        while True:
            if not pos < length:
                store.append(0)
                length += 1
            if store[pos] == 0:
                store[pos] = num
                break
            pos += 1
    print(length)
    for item in store:
        print(item,end='')
        if not store.index(item) == length - 1:
            print(' ',end='')
    print()

main()