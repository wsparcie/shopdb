from collections import OrderedDict

from generator import RandGen
from preferences import*

class Product():
    def __init__(self):
        self.R = React()
        self.productFile = 'products.txt'
        self.products = {}

        self.productType = dict.fromkeys(self.__genProduct())

    def existsProduct(self, productID):
        return productID in self.products

    def volume(self):
        return len(self.products)
    
    def giveDictProduct(self):
        return self.products
    
    def giveListProduct(self):
        return list(self.products.keys())

    def giveProdPrice(self, pId):
        return round(float(self.products[pId]['PRICE']), 2)
    
    def updateStock(self, id, quantity):
        value = int(self.products[id]['STOCK'])
        value += quantity
        self.products[id]['STOCK'] = value
        if value < 0:
            self.R.printIncorrectItem(' stock')
            text = f'{abs(value)} items missing'
            print(f'\t\t{text}')
            return -1
        else:
            self.R.printActionTaken('stock updated')
            return 1
    
    def __genProduct(self):
        product = {
            'NAME': RandGen(10, 20).phrase(),
            'BRAND': RandGen(5, 10).name(),
            'TYPE': RandGen(5, 10).phrase(),
            'DESC': RandGen(10, 100).comment(),
            'STOCK': RandGen(1, 2).number(),
            'PRICE': RandGen(1, 4).price(),
        }
        return product

    def generate(self):
        try:
            self.products = {
                f'p{i + 1}': self.__genProduct() 
                for i in range(nProducts)
            }
            return 1
        except Exception as e:
            self.R.printException('generating products', e)
        return -1

    def read(self):
        try:
            with open(self.productFile, 'r') as file:
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
                        item[key2] = value2
                    self.products[key] = item
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('products')
        except Exception as e:
            self.R.printException('loading products', e)
        return -1

    def save(self):
        try:
            with open(self.productFile, 'w') as file:
                for key, value in self.products.items():
                    item = ''
                    for key2, value2 in value.items():
                        item += f'{key2}: {value2}\t'
                    file.write(f'{key}: {item}\n\n')
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('products')
        except Exception as e:
            self.R.printException('saving to products', e)
        return -1

    def add(self):
        try:
            self.R.printRequest('add')
            item = self.productType.copy()
            for key in item:
                text = f'\t\tpass {key}: '
                if key == 'STOCK':
                    value = int(input(text))
                    while value < 0:
                        self.R.printIncorrectItem('stock')
                        value = int(input(text))
                elif key == 'PRICE':
                    value = round(float(input(text)), 2)
                    while value < 0:
                        self.R.printIncorrectItem('price')
                        value = round(float(input(text)), 2)
                else:
                    value = input(text).strip()
                item[key] = value
            print(item)
            text = 'ADD to products?'
            if self.R.printTakeAction(text) == 'y':
                last = list(self.products.keys())[-1]
                new = f'{last[0]}{int(last[1:]) + 1}'
                self.products[new] = item
                self.R.printActionTaken('added')
                return 1
            else:
                self.R.printActionTaken('cancelled')
                return 0
        except Exception as e:
            self.R.printException('adding to products', e)
        return -1
    
    def delete(self):
        try:
            self.R.printRequest('delete')
            text = '\t\tpass product ID: '
            id = input(text).strip().lower()
            try: 
                item = self.products[id].copy()
                print(item)
                text = f'DELETE from products?'
                if self.R.printTakeAction(text) == 'y':
                    del self.products[id]
                    text = 'deleted product from products'
                    self.R.printActionTaken(text)
                    return id
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            except KeyError:
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            text = 'deleting product from products'
            self.R.printException(text, e)

    def modify(self):
        try:
            self.R.printRequest('modify')
            text = '\t\tpass product ID: '
            id = input(text).strip().lower()
            try:
                item = self.products[id].copy()
                print(item)
                text = '\t\tplease select value to modify: '
                key = input(text).strip().upper()
                try:
                    item[key]
                    text = f'\t\tpass {key}: '
                    if key == 'STOCK':
                        value = int(input(text))
                        while value < 0:
                            self.R.printIncorrectItem('stock')
                            value = int(input(text))
                    elif key == 'PRICE':
                        value = round(float(input(text)), 2)
                        while value < 0:
                            self.R.printIncorrectItem('price')
                            value = round(float(input(text)), 2)
                    else:
                        value = input(text).strip()
                    item[key] = value
                    print(item)
                    text = f'MODIFY {key} item?'
                    if self.R.printTakeAction(text) == 'y':
                        self.products[id][key] = value
                        self.R.printActionTaken('modified')
                        print(self.products[id])
                        return 1
                    else:
                        self.R.printActionTaken('cancelled')
                        return 0
                except KeyError:
                    self.R.printIncorrectItem('item')
            except KeyError:
                self.R.printIncorrectItem('product ID')
        except Exception as e:
            self.R.printException('modifying products', e)
        return -1
    
    def __printItem(self, id):
        value = self.products[id]
        item = ''
        for key2, value2 in value.items():
            key2Text= f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
            item += f'{key2Text}: {value2}\t'
        keyText = f'{bcolors.OKBLUE}{id}{bcolors.ENDC}'
        print(f'\t\t{keyText}: {item}\n')

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.products.keys():
                self.__printItem(key)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing users', e)
        return -1
    
    def sort(self):
        try:
            self.R.printRequest('sort by')
            product = self.__genProduct()
            sortable = [key for key in product.keys() 
                        if not isinstance(product[key], dict)]
            print(f'\t\t{' | '.join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                values = {k: v[sortType]
                           for k, v in self.products.items()}
                try:
                    values = OrderedDict(sorted(values.items(), 
                                            key=lambda v: float(v[1])))
                except:
                    values = OrderedDict(sorted(values.items(), 
                                            key=lambda v: v[1]))
                for i, (key, value) in enumerate(values.items()):
                    keyText = f'{bcolors.OKBLUE}{key}{bcolors.ENDC}'
                    valueText = f'{bcolors.OKCYAN}{value}{bcolors.ENDC}'
                    print(f'\t\t{i + 1}. {keyText}: {valueText}\n')
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('item')
        except Exception as e:
            self.R.printException('sorting products', e)
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
            self.R.printException('filtering products', e)
        return -1