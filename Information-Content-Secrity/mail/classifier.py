# 实现一个基于朴素贝叶斯算法的文本分类学习过程
# 垃圾邮件样本:spam_100.utf8
# 正常邮件样本:ham_100.utf8
# 测试样本:test.utf8

import os
import jieba
import math

def generate_dic():
    dir = './train/'   
    filenames = os.listdir(dir)
    dic = set()   
    count = 0
    for filename in filenames:
        with open(dir+filename, 'r', encoding='utf8') as file:
            while(True):
                sentence = file.readline()
                count = count + 1
                print('processing Num:' + str(count), end='\r')
                if sentence == '':
                    break
                words_gen = jieba.cut(sentence)
                dic.update(list(words_gen))
    print()
    return list(dic) 

def to_vec(dic, full_path):
    '''step2,将每个文件进行向量化'''
    result = []
    with open(full_path, 'r', encoding='utf8') as file:
        while(True):
            vec = []
            sentence = file.readline()
            if sentence == '':
                break
            words = set(list(jieba.cut(sentence)))
            for word in dic:
                if word in words:
                    vec.append(1)
                else:
                    vec.append(0)
            result.append(vec)
    return result

def pam2vec(dic):
    dir = './train/'
    ham = to_vec(dic, dir+'ham_100.utf8')
    spam = to_vec(dic, dir+'spam_100.utf8')
    return [ham, spam]

def caculate_possibility(data):
    demension = len(data[0])
    data_len = len(data)
  
    possiblity = []
    for i in range(demension):
        single_word_total = 0
        for j in range(data_len):
            single_word_total = single_word_total + data[j][i]
        possiblity.append(single_word_total)

    total = 0
    for item in possiblity:
        total = total + item
    
    for i in range(demension):
        if possiblity[i] != 0:
            possiblity[i] = math.log10(possiblity[i]/total)
        else:
            possiblity[i] = -5
    return possiblity

def train(ham, spam):
    '''训练过程'''
    word_poss_ham = caculate_possibility(ham)
    word_poss_spam = caculate_possibility(spam)
    ham_poss = len(ham)/(len(ham)+len(spam))
    spam_poss = math.log10( 1 - ham_poss)
    ham_poss = math.log10(ham_poss)
    return [ham_poss, spam_poss, word_poss_ham, word_poss_spam]

def is_spam(factor, data_vector):
    '''分类过程'''
    ham_poss = 0
    spam_poss = 0
    general_ham_poss, general_spam_poss, word_poss_ham, word_poss_spam = factor
    for i in range(len(data_vector)):
        if data_vector[i] == 1:
            ham_poss = ham_poss + word_poss_ham[i]
            spam_poss = spam_poss + word_poss_spam[i]

    ham_poss = ham_poss + general_ham_poss
    spam_poss = spam_poss + general_spam_poss

    if ham_poss > spam_poss:
        return False
    else:
        return True

# 测试
dic = generate_dic()
ham, spam = pam2vec(dic)
print(ham)
factor = train(ham, spam)
test = to_vec(dic, './test.utf8')
count = 0
right = 0
option = 'test'
mail_type = []

if option == 'ham':
    for i in range(100):
        mail_type.append(False)
    data = ham
elif option == 'spam':
    for i in range(100):
        mail_type.append(True)
    data = spam
elif option == 'test':
    for i in range(50):
        mail_type.append(False)
    for i in range(50):
        mail_type.append(True)
    data = test
print(len(data))
count = 0
result = []
for sentence in data:
    result.append(is_spam(factor,sentence))
for i in range(100):
    if mail_type[i] == result[i]:
        count += 1
print('正确率为:',count,'\b%')