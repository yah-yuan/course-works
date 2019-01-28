def main():
    animal = []
    person = []

    animal_num = input()
    animal_num = animal_num.split(' ')
    person_num = int(animal_num[0])
    animal_num = int(animal_num[1])

    for _ in range(person_num):
        s = input()
        s = s.split(' ')
        person.append([])
        for pref in s:
            person[-1].append(int(pref))

    for _ in range(animal_num):
        animal.append([])
        for __ in range(person_num):
            if person[_] == 1:
                animal[-1].append(__)
    
    print(animal)

main()