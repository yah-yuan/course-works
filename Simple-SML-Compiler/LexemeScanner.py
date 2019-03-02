# !/usr/bin/python
# -*- coding: UTF-8 -*-

'''
:
Standard ML 词法分析器
'''
'''
创建时间 ：Tue Dec  5 16:17:15 CST 2017
作者：张
注释：

注释 ① 
  词素信息的存储结构如下：
    文本结构
       |
     行结构
       |
    词素信息
注释 ②
  使用isinstance()方法判断对象是否为一个类的实例
注释 ③
  python可变对象的传递，一律引用，需使用copy.copy()函数
  虽然之前的问题并不是由这一特性引起的
注释 ④
  在某种情况下（不确定具体原因），类的新实例会拥有前一个该类实例的属性，因此在有多个实例的类的构造函数中应初始化属性？
'''

import sys

class LexemeStruct(object):
    '''单个词素数据结构'''
    # 行信息存在上一级结构中
    lexemeBegin = 0
    lexemeEnd = 0
    lexemeString = ''
    type = ''

    def __init__(self,lexemeBegin,lexemeEnd,lexemeString,type):
        self.lexemeBegin = lexemeBegin
        self.lexemeEnd = lexemeEnd
        self.lexemeString = lexemeString
        self.type = type

class ResultStruct(object):
    '''文本结构'''
    numberOfLines = 0
    line_list = []
    def __init__(self):
        pass

    def AddNewLine(self,line):
        if isinstance(line,LineStruct):
            self.line_list.append(line)
            self.numberOfLines += 1
        else:
            sys.exit()

class LineStruct(object):
    '''行结构'''
    mySerial = 0
    numberOfLexemes = 0
    lexeme_list = []
    def __init__(self,mySerial):
        self.lexeme_list = []
        self.numberOfLexemes = 0
        self.mySerial = mySerial
    
    def AddNewLexeme(self,lexeme):
        if isinstance(lexeme,LexemeStruct):
            self.lexeme_list.append(lexeme)
            self.numberOfLexemes += 1
        else:
            print '非法词素结构信息'
            sys.exit()

class OriginText(object):
    text_list = []
    filePath = ''
    numberOfLines = 0
    def __init__(self,path):
        self.filePath = path
        try:
            text = open(path)
            self.text_list = text.readlines()
        except IOError,e:
            print e
            sys.exit()
        finally:
            text.close()
        self.numberOfLines = len(self.text_list)


class SML_data(object):
    '''静态数据'''
    reserveNumber = '0123456789'
    reserveHexNumber = '0123456789abcdefg'
    reserveLetter = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    reserveWords = ('val','fun','if','then','else','let','end','datatype','andalso','orelse')
    reserveSingleOperator = ('=',':','"','(',')','>','<','~','.','^','*','-','+','[',']','{','}','/','@',';',',','#')
    reserveDoubleOperator = ('<>','::','=>','>=','<=')
    reserveOperateButLetters = ('div','mod','andalso','orelse','handle','raise','of')
   
class SML_Scanner(SML_data):
    '''分析器'''
    lexemeBegin = None
    forward = None
    endOfBuff = None
    currentLine = None
    list_originText = []
    currentLineResult = None
    scannerResult = None
    numberOfLines = 0
    commenting = False
    stringing = False
    lines = 0
    filePath = ''

    def __init__(self,textObj):
        if isinstance(textObj,OriginText):
            pass
        else:
            print '传入非法内容'
            sys.exit()
        self.numberOfLines = textObj.numberOfLines
        self.list_originText = textObj.text_list
        self.filePath = textObj.filePath

    def Scan(self):
        self.scannerResult = ResultStruct()
        for lines in range(self.numberOfLines):
            '''分析每一行的情况'''
            self.currentLine = self.list_originText[lines]
            self.currentLineResult = LineStruct(lines)
            self.lexemeBegin = 0
            self.forward = 0
            self.endOfBuff = len(self.currentLine) - 1
            while True:
                if self.commenting:
                    flag = self.CommentScanner()
                else:
                    flag = self._WhatIsIt()
                if flag == 'LINE_END':
                    break
            self.scannerResult.AddNewLine(self.currentLineResult)
        return self.scannerResult
            
    def _WhatIsIt(self):
        '''判断出一个词素类型：标识符identity（分为变量variable和数字number）还是操作符operation
        这里开始时lexemeBegin == forward'''
        while True:
            '''判断是否是个空格'''
            if self.lexemeBegin == self.endOfBuff:
                return 'LINE_END'
            elif(self.currentLine[self.lexemeBegin] == ' '):
                self.lexemeBegin += 1
                self.forward += 1
            else:
                break

        if self.currentLine[self.lexemeBegin] in self.reserveLetter:
            self.VariableScanner()

        elif self.currentLine[self.lexemeBegin] in self.reserveNumber:
            self.NumberScanner()

        else:
            if self.OperatorScanner() == 'LINE_END':
                return 'LINE_END'

    def VariableScanner(self):
        '''标识符中的变量名扫描器'''
        while True:
            if self.forward >= self.endOfBuff:
                '''触行尾结束词素'''
                break
            elif self.currentLine[self.forward] in self.reserveLetter:
                '''字母继续读取'''            
                if self.currentLine[self.forward] == '_':
                    '''下划线处理'''
                    if self.lexemeBegin == self.forward:
                        if self.currentLine[self.forward + 1] == ' ':
                            #这是一个通配符，暂时算一个变量
                            self.forward += 1
                        else :
                            self.ErrorReport('不合法的变量（以 _ 开头）')
                    else:
                        self.forward += 1
                self.forward += 1
            elif self.currentLine[self.forward] in self.reserveNumber:
                '''数字继续读取'''
                self.forward += 1
            elif self.currentLine[self.forward] == ' ':
                '''空格结束词素'''
                break
            elif self.currentLine[self.forward] == '.':
                ''''.'结束词素'''
                break
            else:
                '''其他所有符号结束词素'''
                #这里要判断这些符号是否是可以合法结束数字词素的符号
                break
        
        '''标识符词素类型认定'''
        if self.currentLine[self.lexemeBegin : self.forward] in ('true','false'):
            '''布尔类型'''
            self.SaveALexeme('bool')
            self.lexemeBegin = self.forward

        elif self.currentLine[self.lexemeBegin : self.forward] in self.reserveOperateButLetters:
            '''字母形式的运算符'''
            self.SaveALexeme('operator')
            self.lexemeBegin = self.forward

        elif self.currentLine[self.lexemeBegin : self.forward] in self.reserveWords:
            '''保留的关键字'''
            self.SaveALexeme('keywords')
            self.lexemeBegin = self.forward

        else:
            '''变量'''
            self.SaveALexeme('variable')
            self.lexemeBegin = self.forward
    
    def NumberScanner(self):
        '''标识符中的数字扫描器'''
        usingNumberList = self.reserveNumber
        floatNumber = False
        wordNumber = False
        hexNumber = False
        messege = {'hex':None,'word':None,'float':None}
        while True:
            if self.currentLine[self.forward] == '0':
                '''对0x,0w,0wx,形式的数字的特殊判别'''
                if self.lexemeBegin == self.forward:
                    if self.currentLine[self.forward + 1] == 'x':
                        usingNumberList = self.reserveHexNumber
                        hexNumber = True
                        self.forward += 2
                    elif self.currentLine[self.forward + 1] == 'w':
                        wordNumber = True
                        if self.currentLine[self.forward + 2] == 'x':
                            usingNumberList = self.reserveHexNumber
                            hexNumber = True
                            self.forward += 3
                        else:
                            self.forward += 2
                    else :
                        self.forward += 1
                else :
                    self.forward += 1
            elif self.currentLine[self.forward] == '.':
                '''小数点判断'''
                if floatNumber == True:
                    self.ErrorReport('不合法的数字')
                else:
                    floatNumber = True
                    self.forward += 1
            elif self.currentLine[self.forward] in usingNumberList:
                '''合法的数字'''
                self.forward += 1
            elif self.currentLine[self.forward] in self.reserveLetter:
                self.ErrorReport('错误的数字或变量名')
            elif self.forward >= self.endOfBuff:
                '''触行尾结束词素'''
                break
            elif self.currentLine[self.forward] == ' ':
                '''空格结束词素'''
                break
            else:
                '''其他所有符号结束词素'''
                #这里要判断这些符号是否是可以合法结束数字词素的符号
                break
        
        '''词素分割完成，开始类型认定'''
        if floatNumber == True:
            self.SaveALexeme('real')
        else:
            self.SaveALexeme('int')
        self.lexemeBegin = self.forward
    
    def OperatorScanner(self):
        '''符号判断'''
        while True:
            if self.forward == self.lexemeBegin :
                '''从第一个符号开始判断'''
                if self.forward >= self.endOfBuff:
                    '''行尾结束'''
                    break
                elif self.currentLine[self.forward] not in self.reserveSingleOperator:
                    self.ErrorReport('符号不存在')
                elif self.currentLine[self.forward] == '#':
                    if self.currentLine[self.forward + 1] == '"':
                        '''#作为字符标志'''
                        self.forward += 1
                        self.SaveALexeme('operator')
                        self.lexemeBegin = self.forward
                        break
                    elif self.currentLine[self.forward + 1] in self.reserveLetter:
                        '''作为函数取值符号'''
                        self.forward += 1
                        self.SaveALexeme('dictionary')
                        self.lexemeBegin = self.forward
                        break
                    else :
                        self.ErrorReport('#号 使用不合法')
                elif self.currentLine[self.forward] == '"':
                    self.StringScanner()
                    return 0
                elif self.currentLine[self.forward:(self.forward + 2)] == '(*':
                    self.forward += 2
                    break
                else :
                    '''其他符号'''
                    self.forward += 1
            else :
                try:
                    a = self.currentLine[self.forward]
                except IndexError:
                    a = 1
                if self.forward >= self.endOfBuff:
                    '''行尾结束'''
                    break
                
                elif self.currentLine[self.forward] in self.reserveSingleOperator:

                    self.forward += 1
                elif self.currentLine[self.forward] in self.reserveLetter:
                    '''字母结束'''
                    break
                elif self.currentLine[self.forward] in self.reserveNumber:
                    '''数字结束'''
                    break
                elif self.currentLine[self.forward] == ' ':
                    '''空格结束'''
                    break
                else :
                    self.ErrorReport('无法识别的符号')

        '''符号认定'''
        if self.forward == self.lexemeBegin:
            pass
        elif self.forward == (self.lexemeBegin + 1):
            self.SaveALexeme('operator')
            self.lexemeBegin = self.forward

        elif self.forward == (self.lexemeBegin + 2) :
            if self.currentLine[self.lexemeBegin:self.forward] in self.reserveDoubleOperator:
                self.SaveALexeme('operator')
                self.lexemeBegin = self.forward

            elif self.currentLine[self.lexemeBegin:self.forward] == '(*':
                if self.CommentScanner() == 'LINE_END':
                    return 'LINE_END'
                else:
                    return 0
            else:
                self.ErrorReport('二元符号不存在')
        else:
            self.ErrorReport('符号不存在（超长）')

    def CommentScanner(self):
        '''已经找到了一个(:,检测:)或下一个(:'''
        self.commenting = True
        # 问题：转义字符未处理
        while True:
            if self.currentLine[self.forward:(self.forward + 2)] == '*)':
                self.forward += 2
                self.commenting = False
                break
            elif self.currentLine[self.forward:(self.forward + 2)] == '(*':
                self.lexemeBegin = self.forward
                self.forward += 2
                if self.CommentScanner() == 'LINE_END':
                    self.commenting = True
                    return 'LINE_END'
                self.commenting = True
            elif self.forward >= self.endOfBuff:
                break
            else:
                self.forward += 1
            
        '''认定'''
        self.SaveALexeme('comments')
        if self.forward >= self.endOfBuff:
            return 'LINE_END'

    def StringScanner(self):
        '''字符串判断'''
        # 这里问题：a.转义字符 b.换行
        isStringStart = False
        isStringEnd = False
        while True:
            if self.currentLine[self.forward] == '"':
                if isStringStart == False:
                    '''字符串开头'''
                    isStringStart = True
                    self.forward += 1
                else:
                    if self.currentLine[self.forward - 1] == '\\':
                        self.forward += 1
                    else:
                        self.forward += 1
                        isStringEnd = True
                        break
            else:
                self.forward += 1

        self.SaveALexeme('string')
        self.lexemeBegin =self.forward

    def SaveALexeme(self,type):
        '''保存一个识别到的词素'''
        savingLexeme = LexemeStruct(self.lexemeBegin,self.forward,self.currentLine[self.lexemeBegin:self.forward],type)
        self.currentLineResult.AddNewLexeme(savingLexeme)

    def ErrorReport(self,errorMessege):
        '''产生词素报错'''
        raise LexemeError(self.filePath,self.scannerResult.numberOfLines,self.lexemeBegin,errorMessege)
        
class LexemeError(Exception):
    '''词素分析异常'''
    lexemeBegin = 0
    line = 0
    errorMessege = ''
    fileName = ''
    def __init__(self,fileName,line,lexemeBegin,errorMessege):
        self.lexemeBegin = lexemeBegin
        self.line = line
        self.errorMessege = errorMessege
        self.fileName = fileName
    def __str__(self):
        errorReporting = '\n Scanner error had happend in: ' + self.fileName + ' at:'
        errorReporting = errorReporting + '\n  line: ' + repr(self.line + 1) + '\tlocation: ' + repr(self.lexemeBegin)
        errorReporting = errorReporting + '\n  Error: ' + self.errorMessege
        return errorReporting

def main():
    text = OriginText('test.sml')
    test = SML_Scanner(text)
    result = test.Scan()
    for line in result.line_list:
        for lexeme in line.lexeme_list:
            if lexeme.type != 'comments':
                print 'line ',line.mySerial,': ',lexeme.lexemeString,'\t',lexeme.type

if __name__ == '__main__':
    main()