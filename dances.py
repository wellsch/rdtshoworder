from typing import Dict, List, Set, Tuple
from dance import Dance
from dancer import Dancer

def process_dances(dances: Dict[str, List[str]]) -> Tuple[Set['Dance'], Dict[str, 'Dancer']]:
    all_dancers = {}
    all_dances = set()
    
    for dance in dances.items():
        [name, dancer_names] = dance
        
        dancers = set()
        for dancer in dancer_names:
            if dancer in all_dancers:
                all_dancers[dancer].add_dance()
            else:
                all_dancers[dancer] = Dancer(dancer)
            dancers.add(all_dancers[dancer])
        dance = Dance(name, dancers)
        all_dances.add(dance)

    return (all_dances, all_dancers)