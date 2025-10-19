from textbased_dance import Dance
from textbased_dancer import Dancer


def add_edges(dances: set['Dance']):
    for dance_1 in dances:
        for dance_2 in dances:
            if dance_1.name != dance_2.name and len(dance_1.dancers.intersection(dance_2.dancers)) > 0:
                dance_1.add_nbr(dance_2)

def weight_dances(dances: set['Dance']):
    for dance in dances:
        dance.calc_weight_greedy()


file = open("2025dances.txt")

dances = set()
all_dancers = {}

rhea_jazz = None
annabelle = None
sol = None

for line in file:
    [name, dancers_str] = line.split(":")
    dancers_names = set(dancers_str.strip().split(","))
    dancers = set()
    for dancer in dancers_names:
        dancer_str = dancer.strip()
        if dancer_str in all_dancers:
            all_dancers[dancer_str].add_dance()
        else:
            all_dancers[dancer_str] = Dancer(dancer_str)
        dancers.add(all_dancers[dancer_str])
    dance = Dance(name, dancers)
    if name == "Avery Contemporary":
        dance.schedule_dance()
    elif name == "Sol Contemporary":
        sol = dance
    else:
        dances.add(dance)
    
    if name == "Rhea Jazz":
        rhea_jazz = dance
    elif name == "Annabelle Contemporary":
        annabelle = dance

add_edges(dances)
weight_dances(dances)

num_dance = 0
qcs = 0
instants = 0

while len(dances) != 0:
    if len(dances) == 12:
        min_dance = rhea_jazz
    elif len(dances) == 11:
        min_dance = annabelle
    else:
        min_dance = min(dances)
    if min_dance.weight == float('inf'):
        print("All remaining dances share a member with this dance")
        new_qcs, new_instants = min_dance.qcs()
        qcs += new_qcs
        instants += 1
    else:
        qcs += min_dance.weight
    min_dance.schedule_dance()
    dances.remove(min_dance)
    weight_dances(dances)
    for dancer in all_dancers.values():
        dancer.time_since_last_dance += 1
    num_dance += 1

sol.schedule_dance()

print("Quick Changes: " + str(qcs))
print("Instants: " + str(instants))
