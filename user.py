from collections import OrderedDict

from preferences import*
from generator import RandGen

class User():
    def __init__(self):
        self.R = React()
        self.userFile = 'users.txt'
        self.users = {}

        self.userType = dict.fromkeys(self.__genUser())
        self.addressType = dict.fromkeys(self.__giveAddressType())

    def existsUser(self, userID):
        return userID in self.users

    def volume(self):
        return len(self.users)
    
    def giveDictUser(self):
        return self.users
    
    def giveListUser(self):
        return list(self.users.keys())

    @staticmethod
    def __giveAddressType():
        addressType = {
            'POST CODE': RandGen(2, 2).postalcode(),
            'COUNTRY': RandGen(5, 10).name(),
            'STATE': RandGen(5, 15).name(),
            'CITY': RandGen(5, 20).name(),
            'ST NUMBER': RandGen(1,1).number(),
        }
        return addressType

    def __genUser(self):
        user = {
            'NAME': RandGen(3, 9).name(),
            'SURNAME': RandGen(5, 15).name(),
            'PHONE': RandGen(9, 9).number(),
            'EMAIL': RandGen(8, 16).email(),
            'ADDRESS': self.__giveAddressType(),
        }
        return user

    def generate(self):
        try:
            self.users = {
                f'u{i + 1}': self.__genUser() 
                for i in range(nUsers)
            }
            return 1
        except Exception as e:
            self.R.printException('generating users', e)
        return -1

    def read(self):
        try:
            with open(self.userFile, 'r') as file:
                for line in file:
                    if line == '\n':
                        continue
                    i = line.index(': ')
                    key = line[:i]
                    value = line[i+1:].strip().split('\t')
                    item = {}
                    for line2 in value:
                        i2 = line2.index(': ')
                        key2 = line2[:i2]
                        value2 = line2[i2+1:].strip()
                        if key2 == 'ADDRESS':
                            value2 = value2.split('| ')
                            item2 = {}
                            for line3 in value2:
                                i3 = line3.index(': ')
                                key3 = line3[:i3]
                                value3 = line3[i3+1:].strip()
                                item2[key3] = value3
                            item[key2] = item2
                        else:
                            item[key2] = value2
                    self.users[key] = item
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('users')
        except Exception as e:
            self.R.printException('loading users', e)
        return -1

    def save(self):
        try:
            with open(self.userFile, 'w') as file:
                for key, value in self.users.items():
                    item = ''
                    for key2, value2 in value.items():
                        if key2 == 'ADDRESS':
                            item2 = ''
                            for key3, value3 in value2.items():
                                item2 += f'{key3}: {value3} | '
                            item += f'{key2}: {item2[:-2]}\t'
                        else:
                            item += f'{key2}: {value2}\t'
                    file.write(f'{key}: {item}\n\n')
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('users')
        except Exception as e:
            self.R.printException('saving to users', e)
        return -1

    def add(self):
        try:
            self.R.printRequest('add')
            item = self.userType.copy()
            for key in item:
                if key == 'ADDRESS':
                    item2 = self.addressType.copy()
                    for key2 in self.addressType:
                        text = f'\t\tpass {key2}: '
                        item2[key2] = input(text).strip()
                    item[key] = item2
                else:
                    text = f'\t\tpass {key}: '
                    item[key] = input(text).strip()
            print(item)
            text = 'ADD to users?'
            if self.R.printTakeAction(text) == 'y':
                last = list(self.users.keys())[-1]
                new = f'{last[0]}{int(last[1:]) + 1}'
                self.users[new] = item
                self.R.printActionTaken('added')
                return 1
            else:
                self.R.printActionTaken('cancelled')
                return 0
        except Exception as e:
            self.R.printException('adding to users', e)
        return -1

    def delete(self):
        try:
            self.R.printRequest('delete')
            text = '\t\tpass user ID: '
            id = input(text).strip().lower()
            try: 
                item = self.users[id].copy()
                print(item)
                text = f'DELETE from users?'
                if self.R.printTakeAction(text) == 'y':
                    del self.users[id]
                    text = 'deleted user in users'
                    self.R.printActionTaken(text)
                    return id
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            except KeyError:
                self.R.printIncorrectItem('user ID')
        except Exception as e:
            text = 'deleting user from users'
            self.R.printException(text, e)
        return -1

    def modify(self):
        try:
            self.R.printRequest('modify')
            text = '\t\tpass user ID: '
            id = input(text).strip().lower()
            try:
                item = self.users[id].copy()
                print(item)
                text = '\t\tplease select value to modify: '
                key = input(text).strip().upper()
                try:
                    item[key]
                    if key == 'ADDRESS':
                        text = '\t\tplease select item to modify: '
                        key2 = input(text).strip().upper()
                        item[key][key2]
                        value = input(f'\t\tpass {key2}: ').strip()
                        item[key][key2] = value
                        print(item)
                        text = f'MODIFY {key2} item?'
                        if self.R.printTakeAction(text) == 'y':
                            self.users[id][key][key2] = value
                            self.R.printActionTaken('modified')
                            print(self.users[id])
                            return 1
                        else:
                            self.R.printActionTaken('cancelled')
                            return 0
                    else:
                        text = f'\t\tpass {key}: '
                        value = input(text).strip()
                        item[key] = value
                        print(item)
                        text = f'MODIFY {key} item?'
                        if self.R.printTakeAction(text) == 'y':
                            self.users[id][key] = value
                            self.R.printActionTaken('modified')
                            print(self.users[id])
                            return 1
                        else:
                            self.R.printActionTaken('cancelled')
                            return 0
                except KeyError:
                    self.R.printIncorrectItem('item')
            except KeyError:
                self.R.printIncorrectItem('user ID')
        except Exception as e:
            self.R.printException('modifying users', e)
        return -1

    def __printItem(self,id):
        value = self.users[id]
        item = ''
        for key2, value2 in value.items():
            if key2 == 'ADDRESS':
                item2 = ''
                for key3, value3 in value2.items():
                    key3Text = f'{bcolors.OKGREEN}{key3}{bcolors.ENDC}'
                    item2 += f'{key3Text}: {value3} | '
                key2Text = f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
                item += f'{key2Text}: {item2[:-2]}\t'
            else:
                key2Text= f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
                item += f'{key2Text}: {value2}\t'
        keyText = f'{bcolors.OKBLUE}{id}{bcolors.ENDC}'
        print(f'\t\t{keyText}: {item}\n')

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.users.keys():
                self.__printItem(key)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing users', e)
        return -1
    
    def sort(self):
        try:
            self.R.printRequest('sort by')
            user = self.__genUser()
            sortable = [key for key in user.keys() 
                        if not isinstance(user[key], dict)]
            print(f'\t\t{' | '.join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                value = {k: v[sortType]
                          for k, v in self.users.items()}
                try:
                    value = OrderedDict(sorted(value.items(), 
                                            key = lambda v: float(v[1])))
                except:
                    value = OrderedDict(sorted(value.items(), 
                                            key = lambda v: v[1]))
                for i, (key, value) in enumerate(value.items()):
                    keyText = f'{bcolors.OKBLUE}{key}{bcolors.ENDC}'
                    valueText = f'{bcolors.OKCYAN}{value}{bcolors.ENDC}'
                    print(f'\t\t{i + 1}. {keyText}: {valueText}\n')
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('item')
        except Exception as e:
            self.R.printException('sorting users', e)
        return -1
    
    def filter(self):
        try:
            self.R.printRequest('filter by id')
            text = '\t\tpass user ID: '
            key = input(text).strip().lower()
            try:
                self.__printItem(key)
                self.R.printActionTaken('finished')
                return 1
            except KeyError:
                self.R.printIncorrectItem('user ID')
        except Exception as e:
            self.R.printException('filtering users', e)
        return -1