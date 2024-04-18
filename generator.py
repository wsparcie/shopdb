from random import randint, choice

class RandGen:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.length = randint(start, stop)

    def __genString(self, ifLetters, ifUppers, ifDigits, ifSymbols, ifSpaces):
        argSum = ifLetters + ifUppers + ifDigits + ifSymbols

        self.ifLetters = ifLetters
        self.ifUppers = ifUppers
        self.ifDigits = ifDigits
        self.ifSymbols = ifSymbols
        self.ifSpaces = ifSpaces

        self.chars = {
            'vowels': 'aeiou',
            'consonants': 'bcdfghjklmnprstwz',
            'digits': '0123456789',
            'symbols': '!@#$&*.?',
            'spaces': ifSpaces,
            'vowelConsonant': 'aeiou' + 'bcdfghjklmnprstwz',
            'digitSymbolSpace': '0123456789' + '!@#$&*.?',
        }

        self.factors = {
            'letters': 0,
            'uppers': 2,
            'digits': argSum - ifDigits,
            'symbols': argSum - ifSymbols,
            'spaces': argSum,
        }

        self.ifSpaces = ifSpaces if ifSpaces else 0

        self.word = ' '

        for index in range(self.length):
            conds = self.__genCond(argSum, index)
            self.__genChar(conds, index)
        return self.word[1:]

    def __genCond(self, argSum, index):
        vergeCond = argSum < index < self.length - argSum

        symbolCond = spaceCond = True
        for char in self.word[-randint(argSum, argSum + 1):]:
            if char in self.chars['symbols']:
                symbolCond = False
                break
        for char in self.word[-randint(argSum+1, argSum + 2):]:
            if char in self.chars['spaces']:
                spaceCond = False
                break

        letters = 1
        if not (argSum == 1 and self.ifUppers):
            cond = self.word[-1] in self.chars['digitSymbolSpace']
            uppers = vergeCond and cond
        else:
            uppers = 1
        if not (argSum in (1, 2) and self.ifDigits):
            digits = vergeCond
        else:
            digits = 1
        if not (argSum in (1, 2) and self.ifSymbols):
            symbols = vergeCond and symbolCond
        else:
            symbols = 1
        spaces = self.length - 3 > index > 2 and spaceCond

        lettersRand = randint(0, self.factors['letters'])
        uppersRand = randint(0, self.factors['uppers'])
        digitsRand = randint(0, self.factors['digits'])
        symbolsRand = randint(0, self.factors['symbols'])
        spacesRand = randint(0, self.factors['spaces'])

        upperCond = index == 0 or (uppers and not uppersRand)
        conds = {
            'ifLetters': 
            self.ifLetters and letters and not lettersRand,
            'ifUppers': 
            self.ifUppers and upperCond,
            'ifDigits': 
            self.ifDigits and digits and not digitsRand,
            'ifSymbols': 
            self.ifSymbols and symbols and not symbolsRand,
            'ifSpaces': 
            self.ifSpaces and spaces and not spacesRand,
        }
        return conds

    def __genChar(self, conds, index):
        if index % 2:
            vowConCond = choice(self.chars['vowels'])
        else:
            vowConCond = choice(self.chars['consonants'])

        if conds['ifSpaces']:
            self.word += choice(self.chars['spaces'])
        elif conds['ifUppers']:
            if self.stop != 1:
                char = vowConCond
            else:
                char = choice(self.chars['vowelConsonant'])
            char = char.upper()
            self.word += char
        elif conds['ifDigits']:
            self.word += choice(self.chars['digits'])
        elif conds['ifSymbols']:
            self.word += choice(self.chars['symbols'])
        elif conds['ifLetters']:
            if self.stop != 1:
                char = vowConCond
            else:
                char = choice(self.chars['vowelConsonant'])
            self.word += char

    def name(self):
        return self.__genString(1, 1, 0, 0, '')
    
    def number(self):
        return self.__genString(0, 0, 1, 0, '')
    
    def email(self):
        stVal = self.__genString(1, 0, 0, 0, '_')
        ndVal = RandGen(3,6).__genString(1, 0, 0, 0, '')
        result = f'{stVal}@{ndVal}.com'
        return result
    
    def phrase(self):
        return self.__genString(1, 1, 0, 0, ' ')
    
    def password(self):
        return self.__genString(1, 1, 1, 1, '')
    
    def price(self):
        genVal = self.__genString(0, 0, 1, 0, '')
        fractVal = RandGen(2,2).number()
        result = round(float(f'{genVal}.{fractVal}'), 2)
        return result
    
    def comment(self):
        sentences = [f'{self.phrase()}. ' 
                     for _ in range(randint(1,10))]
        result = ''.join(sentences)
        return result
    
    def postalcode(self):
        stVal = RandGen(2,2).number()
        ndVal = RandGen(3,3).number()
        result = f'{stVal}-{ndVal}'
        return result