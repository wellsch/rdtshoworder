from textbased_dance import Dance
from textbased_dancer import Dancer


def add_edges(dances: set['Dance']):
    for dance_1 in dances:
        for dance_2 in dances:
            if dance_1.name != dance_2.name and len(dance_1.dancers.intersection(dance_2.dancers)) > 0:
                dance_1.add_nbr(dance_2)

def weight_dances(dances: set['Dance']):
    for dance in dances:
        dance.calc_weight()


file = open("dances.txt")

dances = set()
all_dancers = {}

magic_mike = None
olivia = None

for line in file:
    [name, dancers_str] = line.split(":")
    dancers_names = set(dancers_str.strip().split(","))
    dancers = set()
    for dancer in dancers_names:
        if dancer in all_dancers:
            all_dancers[dancer].add_dance()
        else:
            all_dancers[dancer] = Dancer(dancer)
        dancers.add(all_dancers[dancer])
    dance = Dance(name, dancers)
    dances.add(dance)
    if (name == "Sol Jazz"):
        dance.schedule_dance()
        dances.remove(dance)
        for dancer in dancers:
            dancer.time_since_last_dance = 0
    if (name == "Magic Mike"):
        magic_mike = dance
    if (name == "Olivia Contemp"):
        olivia = dance

add_edges(dances)
weight_dances(dances)

num_dance = 0

while len(dances) != 0:
    if num_dance == 13:
        magic_mike.schedule_dance()
        dances.remove(magic_mike)
        # olivia.schedule_dance()
        num_dance += 1
        # dances.remove(olivia)
        weight_dances(dances)
        continue
    max_dance = max(dances)
    if max_dance.weight == - float('inf'):
        print("All remaining dances share a member with this dance")
    max_dance.schedule_dance()
    dances.remove(max_dance)
    weight_dances(dances)
    for dancer in all_dancers.values():
        dancer.time_since_last_dance += 1
    num_dance += 1
