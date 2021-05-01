import copy
import random


class Subject:
    def __init__(self, data_cell):
        self.gems_found = 0
        self.data_cell = data_cell
        self.moves = ""

    def get_fitness(self):
        moves_count = len(self.moves) // 2
        fitness = self.gems_found * 1000 + (500 - moves_count)   # funkcia na vypocet fitness jedinca
        return fitness


class World:
    def __init__(self, grid, x, y, num_of_gems):
        self.grid = copy.deepcopy(grid)
        self.y = y      # aktualna pozicia panacika
        self.x = x      # aktualna pozicia panacika
        self.num_of_gems = num_of_gems


# vrati list pociatocnych jedincov
def initialization(count):
    subjects = []
    for i in range(count):
        data_cell = []
        for i in range(64):
            data_cell.append(random.randint(0, 255))
        subj = Subject(data_cell)
        subjects.append(subj)
    return subjects


# cyklicka inkrementacia
# vracia cislo novej instrukcie
def increment(instruction):
    number = instruction + 1
    if number > 255:            # 0 <= instrukcia <= 255
        number = 0
    return number


# cyklicka dekrementacia
# vracia cislo novej instrukcie
def decrement(instruction):
    number = instruction - 1
    if number < 0:
        number = 255            # 0 <= instrukcia <= 255
    return number


# pohyb panacika po mape
# vracia: -1 ak vysiel z mapy, 0 ak sa pohol na prazdne miesto, 1 ak nasiel poklad
def move(world, instruction):
    direction = instruction & 3  # pohyb sa rozlisuje podla poslednych 2 bitov
    if direction == 0:      # hore
        world.y -= 1
    elif direction == 1:    # dole
        world.y += 1
    elif direction == 2:    # doprava
        world.x += 1
    elif direction == 3:    # dolava
        world.x -= 1

    if world.x > 6 or world.y > 6 or world.x < 0 or world.y < 0:    # ak mimo mapy
        return -1

    if world.grid[world.y][world.x] == 1:
        world.grid[world.y][world.x] = 0
        return 1

    return 0


# instrukcia na vypis
# vrati znak pohybu: H, D, P alebo L
def print_instruction(instruction):
    number = instruction & 3    # pohyb sa rozlisuje podla poslednych 2 bitov
    directions = "HDPL"
    return directions[number]


# virtualny stroj
# vypocita subjectu jeho fitness, priradi mu pohyby
def virtual_machine(subject, world):
    instructions = subject.data_cell.copy()     # skopirovanie datovej bunky s instrukciami
    grid = copy.deepcopy(world.grid)
    tmp_wrld = World(grid, world.x, world.y, world.num_of_gems)   # vytvorenie docasneho sveta aby sa neprepisal povodny
    subject.moves = ""      # vynulovanie pohybov jedinca
    subject.gems_found = 0     # vynulovanie poctu najdenych pokladov jedinca
    act_address = 0
    i = 0

    while i < 500 and act_address < 64 and subject.gems_found < world.num_of_gems:
        operation = instructions[act_address] >> 6       # operacia: prve 2 bity
        address = instructions[act_address] & 63         # adresa: poslednych 6 bitov
        if operation == 0:      # inkrementacia
            instructions[address] = increment(instructions[address])
        elif operation == 1:    # dekrementacia
            instructions[address] = decrement(instructions[address])
        elif operation == 2:    # skok
            act_address = address - 1  # -1 lebo po podmienke bude zase +1
        elif operation == 3:    # vypis/pohyb
            subject.moves += print_instruction(instructions[address]) + " "    # pridanie znaku do pola pohybov jedninca
            mov_check = move(tmp_wrld, instructions[address])       # vykonanie pohybu v docasnom svete
            if mov_check == -1:     # pohyb mimo mapu
                act_address = 64    # skok na konecnu instrukciu
            elif mov_check == 1:    # panacik nasiel poklad
                subject.gems_found += 1
        act_address += 1    # presun na dalsiu instrukciu
        i += 1


# vrati jeden zvoleny subject na zaklade rulety
# parameter je list usporiadanych subjektov podla fitness (vzostupne)
def select_parent_roulette(subjects):
    num_of_subjects = len(subjects)
    roulette_size = (num_of_subjects + 1) * num_of_subjects // 2
    selection = random.randint(0, roulette_size - 1)
    sum = 0
    for i in range(num_of_subjects + 1):
        sum += i
        if sum > selection:
            return subjects[i - 1]


# vrati jeden nahodne zvoleny subject z lepsej polovice
# parameter je list usporiadanych subjektov podla fitness (vzostupne)
def select_parent_random(subjects):
    num_of_subjects = len(subjects)
    selection = random.randint(num_of_subjects // 2, num_of_subjects - 1)
    return subjects[selection]


# vrati list novych subjectov
# subjects: list usporiadanych subjektov podla fitness (vzostupne)
# elitism_percentage: urcuje aka cast subjectov bude pridana neskor z predoslej generacie
#                     podla neho sa zisti kolko sa ma vytvorit novych subjectov
# is_roulette: urcuje, ci vyber rodica bude ruleta alebo nahodny
def crossover(subjects, elitism_percentage, is_roulette):
    new_generation = []
    new_generation_part = (100 - elitism_percentage) / 100
    num_of_crossovers = round((len(subjects) * new_generation_part)) // 2
    for i in range(num_of_crossovers):
        # vyber rodicov
        if is_roulette:
            parent1 = select_parent_roulette(subjects)
            parent2 = select_parent_roulette(subjects)
        else:
            parent1 = select_parent_random(subjects)
            parent2 = select_parent_random(subjects)

        cross_point = random.randint(0, 64)
        data_cell1 = parent1.data_cell[0:cross_point]
        data_cell1 += parent2.data_cell[cross_point:]
        children1 = Subject(data_cell1)
        new_generation.append(children1)
        data_cell2 = parent2.data_cell[0:cross_point]
        data_cell2 += parent1.data_cell[cross_point:]
        children2 = Subject(data_cell2)
        new_generation.append(children2)
    return new_generation


# nahodna zmena datovych buniek subjectov
# subjects: list subjectov
# probability: percentualna sanca ze dojde k mutacii
def mutation(subjects, probability):
    for i in range(len(subjects)):
        number = random.randint(0, 99)
        if probability > number:
            for j in range(len(subjects[i].data_cell)):
                # ak dojde k mutacii tak kazda bunka jedinca sa zmeni s pravdepodobnostou 1 ku 20
                if random.randint(1, 20) == 1:
                    subjects[i].data_cell[j] = subjects[i].data_cell[j] & random.randint(0, 255)


def main():
    grid = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    world = World(grid, 3, 6, 5)
    num_of_populations = int(input("Pocet generacii: "))
    mutation_probability = int(input("Pravdepodobnost mutacie: "))
    generation_size = int(input("Pocet jedincov v generacii: "))
    elitism_percentage = int(input("Percento elitarstva: "))
    is_roulette = False
    if input("Moznost krizenia (Ruleta: r   Nahodne: n): ") == 'r':
        is_roulette = True

    # inicializacia
    new_generation = initialization(generation_size)
    subjects = []
    population = 0      # cislo aktualnej populacie
    all_gems = False
    best_subject = new_generation[0]

    while True:
        if population == num_of_populations:
            print("POPULACIA CISLO", population - 1)
            print("BEST:", best_subject.moves)
            print("Pocet populacii dosiahol pozadovanu hodnotu")
            cont = input("Pokracovat y/n: ")
            if cont == 'y':
                num_of_populations += int(input("Pocet dalsich populacii: "))
            else:
                break
        subjects = new_generation
        # vlozenie kazdeho subjectu do stroja
        for i in range(generation_size):
            virtual_machine(subjects[i], world)

        # usporiadanie subjectov podla fitness (vzostupne)
        subjects.sort(key=lambda x: x.get_fitness())
        if best_subject.get_fitness() < subjects[-1].get_fitness():
            best_subject = subjects[-1]
        if best_subject.gems_found == world.num_of_gems:
            all_gems = True
            break

        # zistenie a vypisanie priemerjnej percentualnej uspesnosti jedincov
        sum_fitness = 0
        for i in subjects:
            sum_fitness += i.get_fitness()
        print(str(round(100 / 5484 * sum_fitness / generation_size, 2)) + "%")

        # vznik novych jedincov krizenim
        new_generation = crossover(subjects, elitism_percentage, is_roulette)
        # mutacia novych jedincov
        mutation(new_generation, mutation_probability)
        # doplnenie najlepsich jedincov z predoslej generacie
        new_generation_size = len(new_generation)
        for i in range(generation_size - new_generation_size):      # elitarstvo
            new_generation.append(subjects[-1-i])
        population += 1

    if all_gems:
        print("POPULACIA CISLO", population)
        print("FUNKCNY JEDINEC:", best_subject.moves)


main()
