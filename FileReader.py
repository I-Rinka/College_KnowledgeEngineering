#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DBuilder.py
@Time    :   2020/05/01 18:18:31
@Author  :   Rinka 
@Contact :   I_Rinka@outlook.com
@License :   (C)Copyright 2019-2020, BIT_Rinka
@Desc    :   None
'''

# here put the import lib


class OneHotBuilder:
    # 常规操作：
    def __init__(self, fileName, startDate, endDate):
        """初始化完后Run一下函数"""
        # 决定OneHot是多少维的向量
        self.demension = 15000
        self.fileName = fileName
        self.startDate = startDate
        self.endDate = endDate
        # self.topList=[]
        self.oneHotDic = {}
        self.__f = open(self.fileName, "r")
        self.__dic1 = {}
        self.linkedWord = []
        self.entityWord = []
        self.__Run()

    def __str__(self):
        return "file:%s\nstart:%s\nend:%s\n" % (self.fileName, self.startDate, self.endDate)

    # 功能函数：
    # 切分词语
    # 输出格式：[[词1,词性],[词2,词性]]
    def __GetWord(self, line):
        """输入：文件读入的一行字符串|返回值：二维列表，二维列表的第二个属性为词性"""
        # line = self.__f.readline()
        splt = line.split('  ')
        out = []
        for v in splt:
            if v[0] == '[':
                out.append([v[1:v.find('/')], v[v.find('/'):]])
            else:
                out.append([v[0:v.find('/')], v[v.find('/'):]])
            # out.append([v[0:v.find('/')], v[v.find('/'):]])
        return out

    # 输出格式：[[词1,词2],[词1,词2]]
    def __GetEntityWord(self, line):
        """得到命名实体|输入：文件读入的一行字符串|返回值：二维列表"""
        out = []
        # line = self.__f.readline()
        prePosition = line.find('[')
        while prePosition != -1:
            Position = line[prePosition:].find(']')
            if Position == -1:
                break
            Position = Position+prePosition
            if Position+3 >= len(line):
                break
            if 'nt' in line[Position+1:Position+3]:
                splt = line[prePosition:Position].split('  ')
                t = []
                for v in splt:
                    if v[0] == '[':
                        t.append(v[1:v.find('/')])
                    else:
                        t.append(v[0:v.find('/')])
                out.append(t)
            prePosition = line[Position:].find('[')
            if prePosition != -1:
                prePosition += Position
        return out

    # 得到所有紧挨着的词语
    # 输出格式：[[词1,词2],[词1,词2]]
    def __GetLinkedWord(self, processedWord):
        out = []
        i = 0
        while (i+1) < len(processedWord):
            if '/n' in processedWord[i][1] and '/n' in processedWord[i+1][1]:
                t = []
                # judge = 0
                while (i+1) < len(processedWord):
                    if '/n' in processedWord[i][1]:
                        t.append(processedWord[i][0])
                    else:
                        break
                    i += 1
                out.append(t)
            i += 1
        return out

    # 建立字典(字典需要用已有的，输入的二元组也是已有的)，统计词频
    # 更新词典
    def __UpdateDic(self, Dic, wordList):
        for word in wordList:
            if '/n' in word[1]:
                if not word[0] in Dic:
                    Dic[word[0]] = 1
                else:
                    Dic[word[0]] = Dic[word[0]]+1
        return Dic

    # 此对象执行的主体
    def __Run(self):
        switch = False
        switch2 = False
        while True:
            line = self.__f.readline()
            # 输入输出停止/起始判断，通过两个开关来决定当前的状态
            if line.startswith(self.startDate) and switch == False:
                switch = True
            if line.startswith(self.endDate):
                switch2 = True
            elif switch2:
                break

            # 开始处理读入数据，以后添加扩展就在这里
            if switch:
                t = self.__GetWord(line)  # 得到了可区分词性的二维列表
                self.__UpdateDic(self.__dic1, t)
                t2 = self.__GetLinkedWord(t)
                t3 = self.__GetEntityWord(line)
                self.linkedWord.extend(t2)
                self.entityWord.extend(t3)

        self.topList = list(self.__dic1.items())
        self.topList.sort(
            key=lambda parameter_list: parameter_list[1], reverse=True)
        ran = min(self.demension-1, len(self.topList))
        for i in range(ran):
            self.oneHotDic[self.topList[i][0]] = i
        self.oneHotDic['UNKNOWN'] = ran
        return

    def GetDemension(self, word):
        """输入：需要得到对应onehot向量下标的字符|返回：onehot向量的维度"""
        if word in self.oneHotDic:
            return self.oneHotDic[word]
        else:
            return self.oneHotDic['UNKNOWN']


p1 = OneHotBuilder(
    R'data/1998-01-2003版-带音.txt', "19980101", "19980120")
# print(p1.oneHotDic)
# print(p1.GetDemension('UNKNOWN'))
# for i in range(100):
#     print(p1.topList[i])
# print(p1.linkedWord)
print(p1.linkedWord)
print('\n')
print('\n')
print('\n')
print(p1.entityWord)