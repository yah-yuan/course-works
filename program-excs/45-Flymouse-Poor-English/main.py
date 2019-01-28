def proc():
    a = input()
    a = int(a)
    for _ in range(a):
        stri = input()
        if not stri[0].istitle():
            stri = stri[0].upper() + stri[1:]
        str_split = stri.split(' ')
        # tmp = str_split[0]
        # str_split.remove(str_split[0])
        leng = len(str_split)
        for i in range(leng):
            word = str_split[i]
            if len(word) == 1:
                continue
            if not word[1:].islower():
                word = word[0] + word[1:].lower()
                str_split[i] = word
        # str_split.insert(0,tmp)
        s = ' '
        stri = s.join(str_split)
        print(stri)

proc()