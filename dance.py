from dancer import Dancer

class Dance:
    def __init__(self, name, dancers: set['Dancer']):
        self.nbrs: set['Dance'] = set()
        self.degree = 0
        self.name = name
        self.dancers = dancers
        self.weight = 0

    def add_nbr(self, dance: 'Dance'):
        self.nbrs.add(dance)
        self.degree += 1

    def remove_nbr(self, nbr: 'Dance'):
        self.nbrs.remove(nbr)
        self.degree -= 1

    def calc_weight(self):
        self.weight = len(self.nbrs) * 2
        # self.weight = 0
        for dancer in self.dancers:
            # self.weight += dancer.dances - dancer.dances_done
            if dancer.time_since_last_dance == 0:
                self.weight = - float('inf')
    
    def calc_weight_greedy(self):
        self.weight = 0
        for dancer in self.dancers:
            if dancer.time_since_last_dance == 0:
                self.weight = float('inf')
            if dancer.time_since_last_dance == 1:
                self.weight += 1
    
    def qcs(self):
        qcs = 0
        instants = 0
        for dancer in self.dancers:
            if dancer.time_since_last_dance == 1:
                instants += 1
            if dancer.time_since_last_dance == 2:
                qcs += 1
        return qcs, instants

    def schedule_dance(self):
        print(f"Scheduled: {self}")
        for dancer in self.dancers:
            dancer.schedule_dance()
        for nbr in self.nbrs:
            nbr.remove_nbr(self)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: 'Dance'):
        return self.weight == other.weight
    
    def __gt__(self, other: 'Dance'):
        return self.weight > other.weight
    
    def __lt__(self, other: 'Dance'):
        return self.weight < other.weight
    
    def __ge__(self, other: 'Dance'):
        return self.weight >= other.weight
    
    def __le__(self, other: 'Dance'):
        return self.weight <= other.weight
    
    def __str__(self):
        dancers = set()
        for dancer in self.dancers:
            dancers.add(str(dancer))
        return f"{self.name}: {dancers}"