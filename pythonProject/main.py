from random import randint

# отели = синяя группа
# рестораны = красная группа
# аптеки и больницы = зеленая группа

# карта, у каждого номера своя локация, группа, цена, аренда и владелец.
dict_levels = {
    0: ['Старт'],
    1: ['rixos', 'blue', 2000000, 500000, None],
    2: ['sema_hospital', 'green', 5000000, 1000000, None],
    3: ['paul_restaurant', 'red', 1000000, 100000, None],
    4: ['movenpick', 'blue', 1500000, 70000, None],
    5: ['mamma_mia', 'red', 700000, 50000, None],
    6: ['kfc', 'red', 1000000, 50000, None],
    7: ['arbat_hotel', 'blue', 1200000, 100000, None],
    8: ['esentai_apartments', 'blue', 2500000, 300000, None],
    9: ['queens_hospital', 'green', 500000, 50000, None],
    10: ['palm_hotel', 'blue', 1000000, 200000, None],
    11: ['dental_clinic', 'green', 500000, 50000, None],
    12: ['burger_king', 'red', 2500000, 400000, None],
    13: ['mayo_clinic', 'green', 3000000, 300000, None],
    14: ['eye_clinic', 'green', 900000, 100000, None],
    15: ['mc_donalds', 'red', 1000000, 300000, None]
}

# класс игроков
#####################################################################################
class Player:
    def __init__(self, name, pos, balance, first_lap):
        self.name = name
        self.pos = pos
        self.balance = balance
        self.first_lap = first_lap
        self.locations_blue = []
        self.locations_green = []
        self.locations_red = []
        self.triple_rent_blue = False
        self.triple_rent_green = False
        self.triple_rent_red = False

    def greetings(self):
        print(f'Всем привет, меня зовут {self.name}.')
    def buy(self):
        if self.balance >= dict_levels[self.pos][2]:
            self.balance -= dict_levels[self.pos][2]
            if dict_levels[self.pos][1] == 'blue':
                self.locations_blue.append([dict_levels[self.pos][0], dict_levels[self.pos][1]])
            elif dict_levels[self.pos][1] == 'red':
                self.locations_red.append([dict_levels[self.pos][0], dict_levels[self.pos][1]])
            else:
                self.locations_green.append([dict_levels[self.pos][0], dict_levels[self.pos][1]])
            dict_levels[self.pos][4] = self.name
            print(f'Поздравляем {self.name} вы купили {dict_levels[self.pos][0]}!\nОстаток средств: {self.balance}')
        else:
            print(f'Недастаточно средств...')
#####################################################################################

# класс кубика
#####################################################################################
class Cube:
    def __init__(self, name):
        self.name = name

    def tell_to_throw(self, player):
        global queue_counter
        # спрашиваем участника хочет ли он бросить кубик
        decision = input(f'Хэй {player.name} пришла твоя очередь, кинуть кубик?(да/нет)')
        if decision.lower() == 'да':
            self.throw(player)
            queue_counter += 1
            # ставим что игрок бросил кубик
            player.first_lap = False
        else:
            print(f'Вы пропустили свою очередь {player.name}...')
            queue_counter += 1

    def throw(self, player):
        global queue
        # получение случайного результата через RANDINT
        outcome = randint(1, 3)
        player.pos = (player.pos + outcome) % 16
        print(f'Хэй {player.name} тебе выпало число {outcome}, теперь ты на локации {player.pos}...')
        # прибовления денег за прохождения карты, каждый круг по 500000 (не включая первого).
        if player.pos == 0 and player.first_lap == False:
            player.balance += 500000
            print(f'Ты прошёл круг теперь твой баланс: {player.balance}.(+500k)')
        else:
            if dict_levels[player.pos][4] == None:
                want_to_buy = input(f'{player.name}, желаешь ли ты купить {dict_levels[player.pos][0]} за {dict_levels[player.pos][2]}?(да/нет)')
                if want_to_buy.lower() == 'да':
                    player.buy()
            else:
                if dict_levels[player.pos][4] == player.name:
                    print('Вы попали на свою территорию!')
                    # если человек попал на свою купленную локацию то он может утроить арендную плату за 500000
                    if dict_levels[player.pos][1] == 'blue':
                        if len(player.locations_blue) == 3:
                            triple_rent = input('Хотите ли утроить цену аренды для всех своих гостиниц? (за 500000), (да/нет)')
                            if triple_rent.lower() == 'да':
                                if player.balance - 500000 >= 0:
                                    player.balance -= 500000
                                    player.triple_rent_blue = True
                                    print('Цены утроены!')
                                else:
                                    print('Не достаточно средств')
                    elif dict_levels[player.pos][1] == 'red':
                        if len(player.locations_red) == 3:
                            triple_rent = input('Хотите ли утроить цену аренды для всех своих ресторанов?')
                            if triple_rent.lower() == 'да':
                                if player.balance - 500000 >= 0:
                                    player.balance -= 500000
                                    player.triple_rent_red = True
                                    print('Цены утроены!')
                                else:
                                    print('Не достаточно средств')
                    else:
                        if len(player.locations_green) == 3:
                            triple_rent = input('Хотите ли утроить цену аренды для всех своих больниц?')
                            if triple_rent.lower() == 'да':
                                if player.balance - 500000 >= 0:
                                    player.balance -= 500000
                                    player.triple_rent_green = True
                                    for i in range(1, 16):
                                        if dict_levels[i][1] == 'green':
                                            dict_levels[i][3] *= 3
                                    print('Цены утроены!')
                                else:
                                    print('Не достаточно средств')

                else:
                    print(f'Вы попали на территорию {dict_levels[player.pos][4]}...')
                    if player.balance - dict_levels[player.pos][3] >= 0:
                        player.balance -= dict_levels[player.pos][3]
                        print(f'С вас сняли {dict_levels[player.pos][3]} за аренду, ваш баланс: {player.balance}')
                        for i in queue:
                            if i.name == dict_levels[player.pos][4]:
                                i.balance += dict_levels[player.pos][3]
                                print(f'{i.name} А вам заплатили: {dict_levels[player.pos][3]} у вас: {i.balance}')
                    else:
                        print(f'Вам нужно было заплатить {dict_levels[player.pos][3]} а у вас {player.balance}.\nВы банкрот! К сожалению вы выбили из игры...')
                        for i in range(1, 16):
                            if dict_levels[i][4] == player.name:
                                dict_levels[i][4] = None
                        queue.remove(player)
                        del player
#####################################################################################

# правила и приветствие игроков
print("""Приветствую всех в нашей мини манаполии от Арыстана Кайрбаева!
Сегодня мы узнаем кто из вас лучший финансист, и стратег.
У нас в городе есть 15 мест где вам предстоит побывать а может и купить их...
В начале у каждого из вас будет по 2 миллиона тенге, распорядитесь ими с умом и постарайтесь купить как можно больше участок одного цвета.
У каждого из вас будет очередь броска, вам может выпасть 1, 2 или 3.\n""")

# регистрация игроков, установим что это их первый круг и не стоит давать им по 500000
player1 = Player(input('Имя игрока 1: '), 0, 2000000, True)
player2 = Player(input('Имя игрока 2: '), 0, 2000000, True)
player3 = Player(input('Имя игрока 3: '), 0, 2000000, True)

# создание магического кубика
magic_cube = Cube('Магический кубик')

# знакомство игроков
player1.greetings()
player2.greetings()
player3.greetings()

# очередь ходов
queue = [player1, player2, player3]
queue_counter = 0

# игровой цикл
while (player1.balance >= 0) or (player2.balance >= 0) or (player3.balance >= 0):
    if len(queue) > 1:
        magic_cube.tell_to_throw(queue[queue_counter % len(queue)])
        print('\n')
    else:
        print(f'Игра окончена! Победил {queue[0].name}!')
        break