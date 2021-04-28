import primitives.fromJson
import primitives.cipher


class Adapter:

    def __init__(self, user_name, exchange_name):

        self.un = user_name
        self.en = exchange_name
        self.data = primitives.fromJson.load(f'../../data/users/{user_name}/config.json')
        temp_keys = primitives.cipher.decrypt(f'../../data/users/{user_name}/_{user_name}.bin', self.data['exchanges'][exchange_name.lower()]['ln'])
        key_secret = {'key': temp_keys[-2], 'secret': temp_keys[-1]}
        if len(temp_keys) == 3:
            key_secret.update({'user': temp_keys[0]})
        temp_exchange = __import__(exchange_name)
        self.exchange = temp_exchange.Adapter(**key_secret)

    def balances(self):
        return self.exchange.balances(self.data['currencies'])



if __name__ == '__main__':
    test = Adapter('m', 'Bitstamp')
    # print(test.__dict__) 
    print(test.balances()) 
