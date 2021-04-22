import primitives.fromJson
import primitives.cipher


class Adapter:

   def __init__(self, user_name, exchange_name):

       self.un = user_name
       self.ens = exchange_name
       data = primitives.fromJson.load(f'../../data/users/{user_name}/config.json')
       key_secret = primitives.cipher.decrypt(f'../../data/users/{user_name}/_{user_name}.bin', data['exchanges'][exchange_name.lower()]['ln'])
       temp = __import__(exchange_name)
       print(key_secret)
       # self.exchange = temp.Adapter(key_secret[0], key_secret[1], key_secret[2])
       self.exchange = temp.Adapter(key_secret)


if __name__ == '__main__':
    d = Adapter('m', 'Bitstamp')
    print(d.__dict__) 
