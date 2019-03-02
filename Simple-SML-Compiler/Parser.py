# !/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Standard ML 语法分析器
创建时间: Thu Jan  4 16:43:48 CST 2018
作者: 张
注释:
① 目前可以识别的文法:
  DEFINE => 'val' variable '=' TYPE (':' TYPE)
  TYPE => EXPRESSION | string | NUMBER | COMPARE
  EXPRESSION => EXPRESSION ('+' | '-') SECDEXPR | SECDEXPR | '#' string | COMPARE 
  SECDEXPR => SECDEXPR ('*' | '/' | 'div') THIRDEXPR | THIRDEXPR
  THIRDEXPR => '~' FOURTHEXPR | FOURTHEXPR
  FOURTHEXPR => '(' EXPRESSION ')' | variable |NUMBER
  NUMBER => real | int
  COMPARE => EXPRESSION compareOp EXPRESSION
  FUNCTION => 'fun' operater EXPRESSION | '(' EXPRESSION ')' | variable | LIST
  JUDGEMENT => 

② 还无法识别的文法:

  TUPLE => '(' (variable,number,string,LIST) (','(variable,number,string))* ')'
  TUPLE_ELEMENT => variable | number | string | LIST
  LIST => '[' variable (',' variable) ']' | '[' int (',' int) ']' 
  LIST => '[' string (',' string) ']' | '[' TUPLE (',' TUPLE) ']' | '[' real (',' real) ']' 
  FUNCTION => 
'''

import LexemeScanner
import sys

class SML_data(object):
    '''sml静态数据''' 
    pass

class Tree(object):
    son_list = []
    son_number = 0
    level = 0
    grammar = ''
    string = ''
    type = ''

    def __init__(self, grammar, string = None, type = None):
        if grammar in ('[Expression 1st]', '[Expression 2nd]', '[Expression 3rd]', '[Expression 4th]'):
            grammar = '[Expression]'
        self.son_list = []
        self.son_number = 0
        self.level = 0
        self.grammar = grammar
        self.string = string
        self.type = type

    def append(self, son):
        if son.son_number == 1 and son.grammar == '[Expression]':
            self.son_list.append(son.son_list[0])
            self.son_number += 1
        else:
            son.levelup()
            self.son_list.append(son)
            self.son_number += 1

    def levelup(self):
        self.level += 1
        if self.son_number != 0:
            for son in self.son_list:
                son.levelup()
        return True

    def __str__(self):
        res = '   ' * self.level + '|-- '
        if self.grammar == 'lexeme':
            res += '\'' + self.string + '\'' + ' (type: ' + repr(self.type) + ')'
            res += '\n'
        else:
            res += self.grammar
            res += '\n'
            for son in self.son_list:
                res += '%s' % son
        return res

class Lexeme(LexemeScanner.LexemeStruct):
    '''一个单个词素'''
    line = 0
    serial = 0
    def __init__(self,serial,line,lexeme):
        self.line = line
        self.serial = serial
        self.type = lexeme.type
        self.lexemeBegin = lexeme.lexemeBegin
        self.lexemeEnd = lexeme.lexemeEnd
        self.lexemeString = lexeme.lexemeString

class SML_Parser(object):
    '''分析器,维护一个成员为lexeme的list'''
    now = 0
    total = 0
    lexeme_list = []
    result = None
    type = None
    cache = None
    tree = None # 用于存放非终结符的生成树,函数本身只返回布尔值
    variable_list = {}
    asl_tree = None
    param = None # 用于记录函数的参数名

    def __init__(self,result):
        '''初始化,建立维护的输入词素列表'''
        self.lexeme_list = []
        self.now = 0
        total = 0
        for line in result.line_list:
            lineNumber = line.mySerial
            for lexeme in line.lexeme_list:
                if lexeme.type == 'comments':
                    continue
                newLexeme = Lexeme(total, lineNumber, lexeme)
                self.lexeme_list.append(newLexeme)
                total += 1
        self.total = total
        self.asl_tree = Tree('[ASL_root]')

    def ErrorReport(self,help):
        '''直接结束此次语法分析并报告错误'''
        raise ParserError(self.cache.line ,
            self.cache.lexemeBegin ,
            self.cache.lexemeString ,
            help)

    '''以下是维护词素表的方法'''
    def increase(self,number = 1):
        '''词素指针增'''
        self.now += number
        if self.now < self.total:
            self.cache = self.lexeme_list[self.now]
        else :
            self.cache = Lexeme(0,0,LexemeScanner.LexemeStruct(0,0,'',''))

    def recovery(self,save):
        '''词素指针还原'''
        self.now = save
        self.cache = self.lexeme_list[self.now]

    def Start(self):
        '''开始分析'''
        self.cache = self.lexeme_list[0]
        while True:
            begin = self.now
            '''每次成功识别一个文法,将now置于下一条语句的开始'''
            if self.Declare():
                self.asl_tree.append(self.tree)
                if self.now == self.total:
                    break
            elif self.FunDeclare():
                self.asl_tree.append(self.tree)
                if self.now == self.total:
                    break
            else:
                self.ErrorReport('无法识别的语句')
        return True

    def Declare(self):
        '''DEFINE => 'val' variable '=' TYPE (':' TYPE)
           TYPE => EXPRESSION | string | NUMBER | COMPARE
           NUMBER => real | int'''
        save = self.now
        tree = Tree('[Declare]')
        variable = ''

        if not self.cache.lexemeString == 'val':
            self.now = save
            return False
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))

        self.increase()

        if not self.cache.type == 'variable':
            self.ErrorReport('可能需要一个合法的标识符')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        variable = self.cache.lexemeString
        self.increase()

        if not self.cache.lexemeString == '=':
            self.ErrorReport('可能需要一个"="')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if self.Expression():
            tree.append(self.tree)
            self.variable_list[variable] = self.type
        elif self.Compare():
            tree.append(self.tree)
            self.variable_list[variable] = self.type
        elif self.cache.type in ('string'):
            self.type = self.cache.type
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.variable_list[variable] = self.cache.type
            self.increase()
        else: 
            self.ErrorReport('不合法的变量声明')

        if self.cache.lexemeString == ':':
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            if self.cache.lexemeString == self.type:
                tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                self.increase()
            else:
                self.ErrorReport('与声明的类型不一致')

        self.tree = tree
        self.type = None
        return True

    def FunDeclare(self):
        save = self.now
        tree = Tree('[FunDeclare]')
        name = ''
        param = ''

        if not self.cache.lexemeString == 'fun':
            return False
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if not self.cache.type == 'variable':
            self.ErrorReport('函数不合法')
        tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
        name = self.cache.lexemeString
        self.variable_list[name] = ('fun' , self.type)
        self.increase()

        if not self.cache.type == 'variable':
            self.ErrorReport('函数不合法')
        tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
        param = self.cache.lexemeString
        self.param = param
        self.increase()

        if not self.cache.lexemeString == '=':
            self.ErrorReport('函数不合法')
        tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
        self.increase()

        if self.Jugement():
            tree.append(self.tree)
        elif self.Expression():
            tree.append(self.tree)
        else:
            self.ErrorReport('函数不合法')

        self.param = None
        self.type = None
        self.tree = tree
        return True

    def Jugement(self):
        tree = Tree('[Judgment]')

        if not self.cache.lexemeString == 'if':
            return False
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if not self.Compare():
            self.ErrorReport('不合法的条件语句')
        tree.append(self.tree)
        self.type = None
        
        if not self.cache.lexemeString == 'then':
            self.ErrorReport('不合法的条件语句')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if self.Expression():
            tree.append(self.tree)
        elif self.Jugement():
            tree.append(self.tree)
        else:
            self.ErrorReport('不合法的条件语句')
        
        if not self.cache.lexemeString == 'else':
            self.ErrorReport('不合法的条件语句')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()
        if self.Jugement():
            tree.append(self.tree)
        elif self.Expression():
            tree.append(self.tree)
        else:
            self.ErrorReport('不合法的条件语句')
        
        self.tree = tree
        return True
        

    def Expression(self):
        '''EXPRESSION => EXPRESSION ('+' | '-') SECDEXPR | SECDEXPR | '#' string | COMPARE'''
        save = self.now
        tree = Tree('[Expression 1st]')
        end = False #如果不能继续向下推导,置true
        comp = False

        if self.cache.lexemeString == '#':
            tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
            self.increase()
            if self.cache.type == 'string':
                if len(self.cache.lexemeString) != 3:
                    self.ErrorReport('不是一个单个的字符')
                tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                self.type = self.cache.type
                end = True
                self.increase()
            else :
                self.ErrorReport('期望一个字符串')

        elif self.cache.type == 'string':
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.type = self.cache.type
            self.increase()
            # 暂时认为字符串是不可操作的
            end = True

        elif self.Compare():
            tree.append(self.tree)
            comp = True
        elif self.Expression2nd():
            tree.append(self.tree)
        else:
            self.ErrorReport('不是一个表达式')
        
        '''消除左递归'''
        if not end:
            if self.cache.lexemeString in ('+','-'):
                if self.type == 'bool':
                    self.ErrorReport('bool值无法进行这样的运算')
                tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                self.increase()
                if self.Expression2nd():
                    tree.append(self.tree)
                else :
                    self.ErrorReport('不合法的表达式')

            if self.type == 'bool':
                if self.cache.lexemeString in ('andalso', 'orelse'):
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                    self.increase()
                    if self.Expression():
                        tree.append(self.tree)
                    else:
                        self.ErrorReport('表达式不全')

        self.tree = tree
        return True

    def Expression2nd(self):
        '''SECDEXPR => SECDEXPR ('*' | '/' | 'div') THIRDEXPR | THIRDEXPR'''
        save = self.now
        flag = False
        tree = Tree('[Expression 2nd]')

        if self.Expression3rd():
            tree.append(self.tree)
        else:
            return False

        if self.cache.lexemeString == '*':
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            flag = True
        elif self.cache.lexemeString == '/':
            if self.type != 'real':
                self.ErrorReport('不合法的变量类型,期望real')
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            flag = True
        elif self.cache.lexemeString == 'div':
            if self.type != 'int':
                self.ErrorReport('不合法的变量类型,期望int')
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            flag = True

        if flag:
            if self.Expression3rd():
                tree.append(self.tree)
            else :
                self.ErrorReport('不合法的表达式')
        
        self.tree = tree
        return True


    def Expression3rd(self):
        '''右结合运算'''
        '''THIRDEXPR => '~' FOURTHEXPR| THIRDEXPR ('andalso' | 'orelse') FOURTHEXPR | FOURTHEXPR'''
        save = self.now
        tree = Tree('[Expression 3rd]')
        end = False

        if self.cache.lexemeString == '~':
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            if self.Expression4th():
                tree.append(self.tree)
                end = True
            else:
                self.ErrorReport('期望一个合法的表达式')
        elif self.Expression4th():
            tree.append(self.tree)
        else:
            return False

        self.tree = tree
        return True

    def Expression4th(self):
        '''FOURTHEXPR => '(' EXPRESSION ')' | variable |NUMBER | 
           NUMBER => real | int '''

        save = self.now
        tree = Tree('[Expression 4th]')
        tmp = None

        if self.cache.type == 'variable':
            try:
                tmp = self.variable_list[self.cache.lexemeString]
            except KeyError:
                if self.cache.lexemeString == self.param:
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.type))
                    self.increase()
                else:
                    self.ErrorReport('未声明的变量名')
            if tmp:
                if tmp[0] == 'fun':
                    self.FuncTranse()
                    tree.append(self.tree)

                elif self.type:
                    try:
                        tmp = self.variable_list[self.cache.lexemeString]
                    except KeyError:
                        self.ErrorReport('未声明的变量名')
                    if tmp == self.type:
                        tree.append(Tree('lexeme', self.cache.lexemeString, self.type))
                        self.increase()
                    else:
                        self.ErrorReport('变量类型有误')
                else:
                    try:
                        tmp = self.variable_list[self.cache.lexemeString]
                    except KeyError:
                        self.ErrorReport('未声明的变量名')
                    self.type = self.variable_list[self.cache.lexemeString]
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.type))
                    self.increase()

        elif self.cache.type == 'real':
            if self.type:
                if self.type != 'real':
                    self.ErrorReport('不合法的变量类型')
            else:
                self.type = self.cache.type
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()

        elif self.cache.type == 'int':
            if self.type:
                if self.type != 'int':
                    self.ErrorReport('不合法的变量类型')
            else:
                self.type = self.cache.type
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
        elif self.cache.type == 'bool':
            if self.type:
                if self.type != 'bool':
                    self.ErrorReport('不合法的变量类型')
            else:
                self.type = self.cache.type
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()

        elif self.cache.lexemeString == '(':
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
            if not self.Expression():
                self.ErrorReport('不合法的表达式')
            tree.append(self.tree)
            if not self.cache.lexemeString == ')':
                self.ErrorReport('期望一个 ")" ')
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
        else:
            return False

        self.tree = tree
        return True


    def FuncTranse(self):
        type = self.variable_list[self.cache.lexemeString][1]
        tree = Tree('[FuncTranse]')

        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if not self.cache.lexemeString == '(':
            self.ErrorReport('不合法的调用')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        if not self.Expression():
            self.ErrorReport('不合法的调用')
        tree.append(self.tree)

        if not self.cache.lexemeString == ')':
            self.ErrorReport('不合法的调用')
        tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
        self.increase()

        self.tree = tree
        return True

    def Compare(self):
        '''COMPARE => identity compareOp identity'''
        save = self.now
        tree = Tree('[Compare]')
        type = None
        tmp = None

        if self.cache.type == 'variable':
            try:
                tmp = self.variable_list[self.cache.lexemeString]
            except KeyError:
                if self.cache.lexemeString == self.param:
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.type))
                    self.increase()
                else:
                    self.ErrorReport('未声明的变量名')
            if tmp:
                if tmp[0] == 'fun':
                    type = tmp[1]
                    self.FuncTranse()
                    tree.append(self.tree)
                else:
                    type = tmp
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                    self.increase()

        elif self.cache.type in ('int, float'):
            type = self.cache.type
            tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
            self.increase()
        else:
            return False

        if self.cache.lexemeString in ('<', '<>', '>', '<=', '>=', '='):
            tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
            self.increase()
        else:
            self.recovery(save)
            return False

        if self.cache.type == 'variable':
            try:
                tmp = self.variable_list[self.cache.lexemeString]
            except KeyError:
                if self.cache.lexemeString == self.param:
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.type))
                    self.increase()
                else:
                    self.ErrorReport('未声明的变量名')

            if tmp:
                if tmp[0] == 'fun':
                    if not type:
                        pass
                    elif not type == tmp[1]:
                        self.ErrorReport('变量类型错误')
                    self.FuncTranse()
                    tree.append(self.tree)
                else:
                    try:
                        tmp = self.variable_list[self.cache.lexemeString]
                    except KeyError:
                        self.ErrorReport('未声明的变量名')
                    if not type:
                        pass
                    elif not type == tmp[1]:
                        self.ErrorReport('变量类型错误')
                    tree.append(Tree('lexeme', self.cache.lexemeString, self.cache.type))
                    self.increase()

        elif self.cache.type in ('int, float'):
            if not type:
                pass
            elif not type == self.cache.type:
                self.ErrorReport('变量类型错误')
            tree.append(Tree('lexeme',self.cache.lexemeString, self.cache.type))
            self.increase()
        else:
            self.ErrorReport('不合法的判断句式')

        self.type = 'bool'
        self.tree = tree
        return True
        

class ParserError(Exception):
    line = 0
    place = 0
    lexeme = ''
    help = ''
    def __init__(self, line, place, lexeme, help):
        self.line = line
        self.place = place
        self.lexeme = lexeme
        self.help = help

    def __str__(self):
        info = '\n Parser error raised at: \n'
        info += '\tline ' + repr(self.line + 1) + '\n'
        info += '\tposition ' + repr(self.place) + '\n'
        info += '\tlexeme IS ' + self.lexeme + '\n'
        info += self.help + '\n'
        return info

def main():
    text = LexemeScanner.OriginText('test.sml')
    scanner = LexemeScanner.SML_Scanner(text)
    lexemes = scanner.Scan()
    parser = SML_Parser(lexemes)
    parser.Start()
    print parser.asl_tree

if __name__ == '__main__':
    main()