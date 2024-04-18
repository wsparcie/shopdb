from random import choice, randint
from collections import OrderedDict

from preferences import*
from user import User
from product import Product

class Order(User, Product):
    def __init__(self, users, products):
        self.R = React()
        super().__init__()
        self.users = users
        self.products = products
        self.orders = {}

        self.orderFile = 'orders.txt'
        self.totalPrice = {}
        
        self.orderType = {
            'USER ID': '',
            'PROD ID': {},
        }

    def volume(self):
        return len(self.orders)
    
    def delByUserID(self, userID):
        try:
            for key, value in self.orders.items():
                if value['USER ID'] == userID:
                    item = self.orders[key].copy()
                    del self.orders[key]
                    keys = [key for key in item['PROD ID'].keys()]
                    values = [value['QUANTITY'] for value in item['PROD ID'].values()]
                    quantity = {k: v for k, v in zip(keys, values)}
                    for k, v in quantity.items():
                        self.products.updateStock(k, int(v))
                    self.__giveTotalPrice()
                    self.R.printActionTaken('deleted user data in orders')
                    return 1
        except Exception as e:
            self.R.printException('deleting user data in orders', e)
        return -1
    
    #def delByProductID(self, productID):

    def __updatePrice(self, quantity, id):
        try:
            price = self.products.giveDictProduct()[id]['PRICE']
            value = round(float(price) * quantity, 2)
            return value
        except Exception as e:
            self.R.printException('updating products price', e)
        return -1


    def __giveTotalPrice(self):
        try:
            for key, value in self.orders.items():
                price = []
                value2 = value['PROD ID']
                for value3 in value2.values():
                    value4 = value3['PRICE']
                    price.append(float(value4))
                self.totalPrice[key] = round(sum(price), 2)
        except Exception as e:
            text = 'calculating total price'
            self.R.printException(text, e)

    def __giveCartType(self, productID):
        try:
            text = '\t\tpass quantity: '
            quantity = int(input(text))
            stock = int(self.products.giveDictProduct()[productID]['STOCK'])
            while not 0 <= quantity <= stock:
                if quantity > 0:
                    self.R.printIncorrectItem(f'stock ({stock} pieces)')
                else:
                    self.R.printIncorrectItem('quantity')
                quantity = int(input(text))
            cartType = {
                    'QUANTITY': quantity,
                    'PRICE': round(float(
                        self.products.giveDictProduct()[productID]['PRICE'])
                        * quantity, 2),
            }
            return cartType
        except Exception as e:
            self.R.printException('while adding to cart', e)
        return -1

    def __genCart(self, productID):
        cart = {
            'QUANTITY': (quantity := randint(1,10)),
            'PRICE': round(float(
                self.products.giveDictProduct()[productID]['PRICE'])
                  * quantity, 2),
        }
        return cart

    def __genOrder(self):
        usersList = self.users.giveListUser()
        productsList = self.products.giveListProduct()
        values = {
                (productID := 
                 choice(productsList)):
                   self.__genCart(productID)
                for _ in range(randint(1,2))
        }
        order = {
            'USER ID': choice(usersList),
            'PROD ID': values,
            }
        return order

    def generate(self):
        try:
            self.orders = {
                f'o{i + 1}': self.__genOrder()
                  for i in range(nOrders)
            }
            self.__giveTotalPrice()
            return 1
        except Exception as e:
            self.R.printException('generating orders', e)
        return -1
    
    def read(self):
        try:
            with open(self.orderFile, 'r') as file:
                for line in file:
                    if line == '\n':
                        continue
                    i = line.index(': ')
                    key = line[:i].strip()
                    value = line[i+1:].strip().split('\t')
                    item = {}
                    for line2 in value:
                        i2 = line2.index(': ')
                        key2 = line2[:i2].strip()
                        value2 = line2[i2+1:].strip()
                        item2 = {}
                        if key2 == 'PROD ID':
                            for line3 in value2.split('| '):
                                i3 = line3.index(': ')
                                key3 = line3[:i3].strip()
                                value3 = line3[i3+1:].strip().split('; ')
                                item3 = {}
                                for line4 in value3:
                                    i4 = line4.index(': ')
                                    key4 = line4[:i4].strip()
                                    value4 = line4[i4+1:].strip()
                                    item3[key4] = value4
                                item2[key3] = item3
                            item[key2] = item2
                        else:
                            item[key2] = value2
                    self.orders[key] = item
            self.__giveTotalPrice()
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('orders')
        except Exception as e:
            self.R.printException('loading orders', e)
        return -1

    def save(self):
        try:
            with open(self.orderFile, 'w') as file:
                for key, value in self.orders.items():
                    item = ''
                    for key2, value2 in value.items():
                        if key2 == 'PROD ID':
                            item2 = ''
                            for key3, value3 in value2.items():
                                item3 = ''
                                for key4, value4, in value3.items():
                                    item3 += f'{key4}: {value4}; '
                                item2 += f'{key3}: {item3[:-2]} | '
                            item += f'{key2}: {item2[:-2]}'
                        else:
                            item += f'{key2}: {value2}\t'
                    file.write(f'{key}: {item}\n\n')
            return 1
        except FileNotFoundError:
            self.R.printFileNotFound('orders')
        except Exception as e:
            self.R.printException('saving to orders', e)
        return -1

    def add(self):
        try:
            self.R.printRequest('add')
            item = self.orderType.copy()
            key = 'USER ID'
            id = input('\t\tpass USER ID: ').strip()
            if self.users.existsUser(id):
                coll = {}
                quantity = {}
                item[key] = id
                key = 'PROD ID'
                while True:
                    id = input('\t\tpass PROD ID: ')
                    if self.products.existsProduct(id):
                        cart = self.__giveCartType(id)
                        coll[id] = cart
                        quantity[id] = cart['QUANTITY']
                        text = 'ADD another product?'
                        status = self.R.printTakeAction(text)
                        if status != 'y':
                            break
                    else:
                        self.R.printIncorrectItem('product ID')
            else:
                self.R.printIncorrectItem('user ID')
                return -1
            item[key] = coll
            print(item)
            text = 'ADD to orders?'
            if self.R.printTakeAction(text) == 'y':
                last = list(self.orders.keys())[-1]
                new = f'{last[0]}{int(last[1:]) + 1}'
                self.orders[new] = item
                for k, v in quantity.items():
                    self.products.updateStock(k, -int(v))
                    self.__giveTotalPrice()
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
            text = '\t\tpass order ID: '
            id = input(text).strip().lower()
            try:
                item = self.orders[id].copy()
                print(item)
                text = f'DELETE from orders?'
                if self.R.printTakeAction(text) == 'y':
                    del self.orders[id]
                    keys = [key for key in item['PROD ID'].keys()]
                    values = [value['QUANTITY'] for value in item['PROD ID'].values()]
                    quantity = {k: v for k, v in zip(keys, values)}
                    for k, v in quantity.items():
                        self.updateStock(k, int(v))
                    self.__giveTotalPrice()
                    text = 'deleted order from orders'
                    self.R.printActionTaken(text)
                    return 1
                else:
                    self.R.printActionTaken('cancelled')
                    return 0
            except KeyError:
                self.R.printIncorrectItem('order ID')
        except Exception as e:
            text = 'deleting order from orders'
            self.R.printException(text, e)

    def modify(self):
        try:
            self.R.printRequest('modify')
            text = '\t\tpass order ID: '
            id = input(text).strip().lower()
            try:
                item = self.orders[id].copy()
                print(item)
                text = '\t\tplease select item to modify: '
                key = input(text).strip().upper()
                try:
                    item[key]
                    if key == 'PROD ID':
                        text = '\t\tplease select product to modify: '
                        key2 = input(text).strip().lower()
                        item[key][key2]
                        try:
                            text = '\t\tplease select value to modify: '
                            key3 = input(text).strip().upper()
                            try:
                                item[key][key2][key3]
                                text = f'\t\tpass {key3}: '
                                if key3 == 'QUANTITY':
                                    quantity = int(item[key][key2][key3])
                                    stock = int(self.products.giveDictProduct()[key2]['STOCK'])
                                    value = int(input(text))
                                    while not 0 <= value <= quantity + stock:
                                        if value > 0:
                                            self.R.printIncorrectItem(f'stock ({stock} pieces)')
                                        else:
                                            self.R.printIncorrectItem('quantity')
                                        value = int(input(text))
                                    newPrice = self.__updatePrice(value, key2)
                                    item[key][key2]['PRICE'] = newPrice
                                elif key3 == 'PRICE':
                                    value = round(float(input(text)), 2)
                                    while value < 0:
                                        self.R.printIncorrectItem('price')
                                        value = round(float(input(text)), 2)
                                else:
                                    value = input(text).strip()
                                item[key][key2][key3] = value
                                print(item)
                                text = f'MODIFY {key3} item?'
                                if self.R.printTakeAction(text) == 'y':
                                    self.orders[id][key][key2][key3] = value
                                    if key3 == 'QUANTITY':
                                        quantity -= int(value)
                                        self.products.updateStock(key2, quantity)
                                    self.__giveTotalPrice()
                                    self.R.printActionTaken('modified')
                                    print(self.orders[id])
                                    return 1
                                else:
                                    self.R.printActionTaken('cancelled')
                                    return 0
                            except KeyError:
                                self.R.printIncorrectItem('item')
                        except KeyError:
                            self.R.printIncorrectItem('product ID')
                    else:
                        value = input(f'\t\tpass {key}: ').strip()
                        item[key] = value
                        print(item)
                        text = f'MODIFY {key} item?'
                        if self.R.printTakeAction(text) == 'y':
                            self.orders[id][key] = value
                            self.R.printActionTaken('modified')
                            print(self.orders[id])
                            return 1
                        else:
                            self.R.printActionTaken('cancelled')
                            return 0
                except KeyError:
                    self.R.printIncorrectItem('item')
            except:
                self.R.printIncorrectItem('order ID')
        except Exception as e:
            self.R.printException('modifying reviews', e)
        return -1
    
    def __printItem(self, id):
        value = self.orders[id]
        item = ''
        for key2, value2 in value.items():
            if key2 == 'PROD ID':
                item2= ''
                for key3, value3 in value2.items():
                    item3 = ''
                    for key4, value4 in value3.items():
                        key4Text = f'{bcolors.OKLIME}{key4}{bcolors.ENDC}'
                        item3 += f'{key4Text}: {value4}; '
                    key3Text = f'{bcolors.OKLEMON}{key3}{bcolors.ENDC}'
                    item2 += f'{key3Text}: {item3[:-2]} | '
                key2Text = f'{bcolors.OKGREEN}{key2}{bcolors.ENDC}'
                item += f'{key2Text}: {item2[:-2]}\t'
            else:
                key2Text = f'{bcolors.OKCYAN}{key2}{bcolors.ENDC}'
                item += f'{key2Text}: {value2}\t'
        keyText = f'{bcolors.OKBLUE}{id}{bcolors.ENDC}'
        text = 'TOTAL PRICE:'
        priceText = f'{bcolors.OKLEMON} {text} {bcolors.ENDC}'
        priceValue = self.totalPrice[id]
        price = f'{priceText}{priceValue}'
        print(f'\t\t{keyText}: {item}\t{price}\n')

    def list(self):
        try:
            self.R.printRequest('list')
            for key in self.orders.keys():
                self.__printItem(key)
            self.R.printActionTaken('finished')
            return 1
        except Exception as e:
            self.R.printException('listing orders', e)
        return -1
    
    def sort(self):
        try:
            self.R.printRequest('sort by')
            order = self.__genOrder()
            sortable = [key for key in order.keys() 
                        if not isinstance(order[key], dict)]
            sortable.append('TOTAL PRICE')
            print(f'\t\t{' | '.join(sortable)}')
            text = '\t\tchoose item to sort by: '
            sortType = input(text).strip().upper()
            if sortType in sortable:
                if sortType == 'TOTAL PRICE':
                    value = OrderedDict(sorted(self.totalPrice.items(), 
                                            key=lambda v: float(v[1])))
                    for i, (k, v) in enumerate(value.items()):
                        kText = f'{bcolors.OKBLUE}{k}{bcolors.ENDC}'
                        print(f'\t\t{i + 1}. {kText}: {v}\n')
                else:
                    value = {k: v[sortType] 
                            for k, v in self.orders.items()}
                    try:
                        value = OrderedDict(sorted(value.items(), 
                                                key=lambda v: float(v[1])))
                    except:
                        value = OrderedDict(sorted(value.items(), 
                                                key=lambda v: v[1]))
                    for i, (key, value) in enumerate(value.items()):
                        keyText = f'{bcolors.OKBLUE}{key}{bcolors.ENDC}'
                        valueText = f'{bcolors.OKCYAN}{value}{bcolors.ENDC}'
                        text = 'TOTAL PRICE:'
                        priceText = f'{bcolors.OKLEMON} {text} {bcolors.ENDC}'
                        priceValue = self.totalPrice[key]
                        price = f'{priceText}{priceValue}'
                        print(f'\t\t{i + 1}. {keyText}: {valueText}\t{price}\n')
                self.R.printActionTaken('finished')
                return 1
            else:
                self.R.printIncorrectItem('item')
        except Exception as e:
            self.R.printException('sorting orders', e)
        return -1

    def filter(self):
        try:
            self.R.printRequest('filter by id')
            text = '\t\tpass order ID: '
            key = input(text).strip().lower()
            try:
                self.__printItem(key)
                self.R.printActionTaken('finished')
                return 1
            except KeyError:
                self.R.printIncorrectItem('order ID')
        except Exception as e:
            self.R.printException('filtering orders', e)
        return -1