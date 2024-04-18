from random import choice, randint
from collections import OrderedDict
from statistics import mean

from preferences import*
from generator import RandGen
from user import User
from product import Product

class Review(User, Product):
    def __init__(self, users, products):
        self.R = React()
        super().__init__()
        self.users = users
        self.products = products
        self.reviews = {}
        self.avgRating = {}
        self.reviewFile = 'reviews.txt'

        self.reviewType = {
            'USER ID': '',
            'RATING': '',
            'COMMENT': '',
        }

    def volume(self):
        return len(self.reviews)
    
    def delByUserID(self, userID):
        try:
            for key, value in self.reviews.items():
                for key2, value2 in value.items():
                    if value2['USER ID'] == userID:
                        del self.reviews[key][key2]
                        text = 'deleted user data in reviews'
                        self.R.printActionTaken(text)
                        return 1
        except Exception as e:
            text = 'deleting user data in reviews'
            self.R.printException(text, e)
        return -1

    def delByProductID(self, productID):
        try:
            for key in self.reviews.keys():
                if key == productID:
                    del self.reviews[key]
                    text = 'deleted product data in reviews'
                    self.R.printActionTaken(text)
                    return 1
        except Exception as e:
            text = 'deleting product data in reviews'
            self.R.printException(text, e)
        return -1

    def __giveAvgRating(self):
        try:
            for key, value in self.reviews.items():
                rating = []
                for v in value.values():
                    rating.append(int(v['RATING']))
                self.avgRating[key] = round(mean(rating), 2)
        except Exception as e:
            text = 'calculating average rating'
            self.R.printException(text, e)

    def __genReview(self):
        review = {
            f'r{i + 1}':
            {
                'USER ID': choice(self.users.giveListUser()),
                'RATING': RandGen(1, 1).number(),
                'COMMENT': RandGen(1, 50).comment(),
            } for i in range(randint(1, 10))
        }
        return review

    def generate(self):
        try:
            self.reviews = {
                choice(self.products.giveListProduct()): 
                self.__genReview() for _ in range(nReviews)
            }
            self.reviews = OrderedDict(sorted(self.reviews.items()))
            self.__giveAvgRating()
            return 1
        except Exception as e:
            self.R.printException('generating reviews', e)
        return -1
    
    def read(self):
        try:
            with open(self.reviewFile, 'r') as file:
                for line in file:
                    if line == '\n':
                        continue
                    i = line.index(': ')
                    key = line[:i]
                    value = line[i+1:].strip().split('\t')
                    item = {}
                    for line2 in value:
                        item2 = {}
                        i2 = line2.index(': ')
                        key2 = line2[:i2].strip()
                        value2 = line2[i2+1:].strip().split('| ')
                        for line3 in value2:
                            i3 = line3.index(': ')
                            key3 = line3[:i3].strip()
                            value3 = line3[i3+1:].strip()
                            item2[key3] = value3
                        item[key2] = item2
                    self.reviews[key] = item
            self.__giveAvgRating()
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('reviews')
        except Exception as e:
            self.R.printException('loading reviews', e)
        return -1

    def save(self):
        try:
            with open(self.reviewFile, 'w') as file:
                for key, value in self.reviews.items():
                    item = ''
                    for key2, value2 in value.items():
                        if isinstance(value2, dict):
                            item2 = ''
                            for key3, value3 in value2.items():
                                item2 += f'{key3}: {value3} | '
                            item += f'{key2}: {item2[:-2]}\t'
                        else:
                            item += f'{key2}: {value2[:-1]}\t'
                    file.write(f'{key}: {item}\n\n')
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('users')
        except Exception as e:
            self.R.printException('saving to reviews', e)
        return -1

    def add(self):
        try:
            self.R.printRequest('add')
            item = self.reviewType.copy()
            text = '\t\tpass PROD ID: '
            id = input(text).strip()
            if self.products.existsProduct(id):
                for key in item:
                    text = f'\t\tpass {key}: '
                    if key == 'RATING':
                        value = int(input(text))
                        while not 0<=value<=10:
                            self.R.printIncorrectItem('RATING')
                            value = int(input(text))
                    else:
                        value = input(text).strip()
                    item[key] = value
                    if key == 'USER ID':
                        if not self.users.existsUser(item[key]):
                            self.R.printIncorrectItem('user ID')
                            return -1
                print(item)
                text = 'ADD to reviews?'
                if self.R.printTakeAction(text) == 'y':
                    keys = list(self.reviews.keys())
                    if id in keys:
                        last = list(self.reviews[id].keys())[-1]
                        new = f'{last[0]}{int(last[1:]) + 1}'
                        self.reviews[id][new] = item
                    else:
                        self.reviews[id] = {'r1': item}
                        print(self.reviews[id])
                    self.__giveAvgRating()
                    self.R.printActionTaken('added')
                    return 1
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            else:  
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            self.R.printException('adding to reviews', e)
            return -1

    def delete(self):
        try:
            self.R.printRequest('delete')
            text = '\t\tpass product ID: '
            id = input(text).strip().lower()
            try:
                item = self.reviews[id].copy()
                print(item)
                text = f'DELETE from reviews?'
                if self.R.printTakeAction(text) == 'y':
                    del self.reviews[id]
                    self.__giveAvgRating()
                    text = 'deleted review from reviews'
                    self.R.printActionTaken(text)
                    return 1
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            except KeyError:
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            text = 'deleting review from reviews'
            self.R.printException(text, e)
        return -1

    def modify(self):
        try:
            self.R.printRequest('modify')
            text = '\t\tpass product ID: '
            id = input(text).strip().lower()
            try:
                item = self.reviews[id].copy()
                print(item)
                text = '\t\tplease select review to modify: '
                key = input(text).strip().lower()
                try:
                    item[key]
                    text = '\t\tplease select value to modify: '
                    key2 = input(text).strip().upper()
                    try:
                        item[key][key2]
                        text = f'\t\tpass {key2}: '
                        if key2 == 'RATING':
                            value = int(input(text))
                            if not 0 <= value <= 10:
                                self.R.printIncorrectItem('rating')
                                value = int(input(text))
                        else:
                            value = input(text).strip()
                        item[key][key2] = value
                        print(item)
                        text = f'MODIFY {key2} item?'
                        if self.R.printTakeAction(text) == 'y':
                            self.reviews[id][key][key2] = value
                            self.__giveAvgRating()
                            self.R.printActionTaken('modified')
                            print(self.reviews[id])
                            return 1
                        else:
                            self.R.printActionTaken('cancelled')
                            return 0
                    except KeyError:
                        self.R.printIncorrectItem('item')
                except KeyError:
                    self.R.printIncorrectItem('review')
            except KeyError:
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            self.R.printException('modifying reviews', e)
        return -1

    def __printItem(self, id):
        value = self.reviews[id]
        item = ''
        for key2, value2 in value.items():
            item2 = ''
            for key3, value3 in value2.items():
                key3Text = f'{bcolors.OKGREEN}{key3}{bcolors.ENDC}'
                item2 += f'{key3Text}: {value3} | '
            key2Text = f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
            item += f'{key2Text}: {item2[:-2]}\t'
        keyText = f'{bcolors.OKBLUE}{id}{bcolors.ENDC}'
        text = 'AVG RATING:'
        ratingText = f'{bcolors.OKLEMON} {text} {bcolors.ENDC}'
        ratingValue = self.avgRating[id]
        rating = f'{ratingText}{ratingValue}'
        print(f'\t\t{keyText}: {item}\t{rating}\n')

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.reviews.keys():
                self.__printItem(key)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing reviews', e)
        return -1
    
    def sort(self):
        try:
            self.R.printRequest('sort by')
            review = self.reviewType
            sortable = [key for key in review.keys()
                         if not isinstance(review[key], dict)]
            sortable.append('AVG RATING')
            print(f'\t\t{' | '.join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                if sortType == 'AVG RATING':
                    value = OrderedDict(sorted(self.avgRating.items(), 
                                            key=lambda v: float(v[1])))
                    for i, (k, v) in enumerate(value.items()):
                        kText = f'{bcolors.OKBLUE}{k}{bcolors.ENDC}'
                        print(f'\t\t{i + 1}. {kText}: {v}\n')
                else:
                    for i, (key, value) in enumerate(self.reviews.items()):
                        item = ''
                        value = {k: v[sortType]
                                for k, v in value.items()}
                        try:
                            value = OrderedDict(sorted(value.items(), 
                                                    key=lambda v: float(v[1])))
                        except:
                            value = OrderedDict(sorted(value.items(), 
                                                    key=lambda v: v[1]))
                        for key2, value2 in value.items():
                            key2Text = f'{bcolors.OKGREEN}{key2}{bcolors.ENDC}'
                            item += f'{key2Text}: {value2} | '
                        keyText = f'{bcolors.OKBLUE}{key}{bcolors.ENDC}'
                        text = 'AVG RATING:'
                        ratingText = f'{bcolors.OKLEMON} {text} {bcolors.ENDC}'
                        ratingValue = self.avgRating[key]
                        rating = f'{ratingText}{ratingValue}'
                        print(f'\t\t{i + 1}. {keyText}: {item[:-2]}\t{rating}\n')
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('item')
        except Exception as e:
            self.R.printException('sorting reviews', e)
        return -1
    
    def filter(self):
        try:
            self.R.printRequest('filter by id')
            text = '\t\tpass product ID: '
            key = input(text).strip().lower()
            try:
                self.__printItem(key)
                self.R.printActionTaken('finished')
                return 1
            except KeyError:
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            self.R.printException('filtering reviews', e)
        return -1