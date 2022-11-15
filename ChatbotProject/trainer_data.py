import os
import pickle

if __name__ == '__main__':
    users = {}
    starters = [['Charmander', 'Squirtle', 'Bulbasaur'], ['Charmeleon', 'Wartortle', 'Ivysaur'],
                ['Charizard', 'Blastoise', 'Venusaur']]
    if os.path.isfile('Users.p'):
        users = pickle.load(open('Users.p', 'rb'))
    for trainer in users.keys():
        user_data = users[trainer]
        print(trainer)
        print('Starter : ' + starters[0][user_data[0]])
        print('Current Evolution : ' + starters[user_data[1]][user_data[0]])
        print('Number of Questions Asked : ' + str((user_data[2]) + (user_data[1] + 1)*5))
        print()