from collections import Counter
import copy
import random
import sys

# use variables just to avoid duplicating strings and making silly typos or something
Copy_Plant = "Copy Plant"
Cyber_Valley = "Cyber Valley"
Dandylion = "Dandylion"
Gigaplant = "Gigaplant"
Lonefire_Blossom = "Lonefire Blossom"
Nettles = "Nettles"
Tytannial = "Tytannial, Princess of Camellias"
D_D_R = "D.D.R. - Different Dimension Reincarnation"
Foolish_Burial = "Foolish Burial"
Giant_Trunade = "Giant Trunade"
Gold_Sarcophagus = "Gold Sarcophagus"
Heavy_Storm = "Heavy Storm"
Hidden_Armory = "Hidden Armory"
Miracle_Fertilizer = "Miracle Fertilizer"
One_for_One = "One for One"
Super_Solar_Nutrient = "Super Solar Nutrient"
Supervise = "Supervise"
Raigeki_Break = "Raigeki Break"

# Only consider cards that are relevant for combos (makes deck size math easier)
# MRK = "Mark of the Rose"
# MCT = "Mind Control"
# BRC = "Brain Control"
# USG = "Upstart Goblin"
# TRR = "Threatening Roar"


key_card_ratios = {
    # Pretty much locked
    Copy_Plant: 1, Nettles: 1,
    Lonefire_Blossom: 2, Gigaplant: 2, Tytannial: 1,
    One_for_One: 1, Foolish_Burial: 1,
    Dandylion: 2,
    Gold_Sarcophagus: 2,
    Hidden_Armory: 3, Supervise: 3,
    Heavy_Storm: 1, Giant_Trunade: 1,
    # Up in the air
    Cyber_Valley: 2,
    Super_Solar_Nutrient: 2,
    Miracle_Fertilizer: 2,
    D_D_R: 2,
    Raigeki_Break: 2,
}

# NB: Redundant combos are OK here since we're handling double-counting
combos = [
    (Lonefire_Blossom, Supervise),
    (Lonefire_Blossom, Hidden_Armory, Heavy_Storm),
    (Lonefire_Blossom, Hidden_Armory, Giant_Trunade),
    (Foolish_Burial, Super_Solar_Nutrient),
    (Foolish_Burial, Super_Solar_Nutrient, Hidden_Armory),
    (Foolish_Burial, Super_Solar_Nutrient, Supervise),
    (Foolish_Burial, Miracle_Fertilizer, Hidden_Armory),
    (Foolish_Burial, Miracle_Fertilizer, Supervise),
    (Gold_Sarcophagus, D_D_R, Supervise),
    (Gold_Sarcophagus, Hidden_Armory, Supervise),
    (Gold_Sarcophagus, Hidden_Armory, D_D_R),
    (Gold_Sarcophagus, Hidden_Armory, Hidden_Armory),
    (Gold_Sarcophagus, D_D_R, Dandylion, Super_Solar_Nutrient),
    (Super_Solar_Nutrient, Copy_Plant, Supervise),
    (Super_Solar_Nutrient, Nettles, Supervise),
    (One_for_One, Dandylion, Super_Solar_Nutrient),
    (One_for_One, Dandylion, Lonefire_Blossom),
    (One_for_One, Super_Solar_Nutrient, Supervise, Gigaplant),
    (One_for_One, Super_Solar_Nutrient, Supervise, Tytannial),
    (One_for_One, Super_Solar_Nutrient, Supervise, Cyber_Valley),
    (One_for_One, Super_Solar_Nutrient, Hidden_Armory, Gigaplant),
    (One_for_One, Super_Solar_Nutrient, Hidden_Armory, Tytannial),
    (One_for_One, Super_Solar_Nutrient, Hidden_Armory, Cyber_Valley),
    (One_for_One, Super_Solar_Nutrient, Hidden_Armory, Lonefire_Blossom),
    (One_for_One, Super_Solar_Nutrient, Hidden_Armory, Nettles),
    (Raigeki_Break, Dandylion, Super_Solar_Nutrient)
]


def how_many_combos(hand):
    n_combos = 0
    for combo in combos:
        contains_combo = not Counter(combo) - Counter(hand)
        if contains_combo:
            n_combos += 1
    return n_combos


def monte_carlo(org_deck, hand_size, n_iter):
    totals = {n: 0 for n in range(len(combos))}
    for i in range(n_iter):
        deck = copy.deepcopy(org_deck)
        random.shuffle(deck)
        hand = deck[:hand_size]
        n_combos = how_many_combos(hand)
        totals[n_combos] += 1
        if n_combos > 0:
            print(f"  - Iter {i}: {n_combos} combos: {hand}")  # sanity checking
    return totals


def generate_deck(n_upstarts):
    key_cards = sum([[name] * n for name, n in key_card_ratios.items()], [])  # sum -> combine list of lists
    min_size = len(key_cards)
    deck_size = 40 - n_upstarts
    n_others = deck_size - min_size
    if n_others < 0:
        raise ValueError(f"Invalid number of Upstart Goblin. {n_upstarts} Upstarts would "
                         f"result in a deck size of {deck_size}, but {min_size} cards are "
                         f"needed to have the necessary key cards.")
    deck = key_cards + (["Other"] * n_others)
    return deck


def main():
    combos_per_hand = {}
    for n in [0, 1, 2, 3]:
        print(f"Generating 10000 sample hands for {n} Upstart Goblin...")
        deck = generate_deck(n_upstarts=n)
        combos_per_hand[f"{n} Upstarts"] = monte_carlo(deck, hand_size=6, n_iter=100000)
    print(combos_per_hand)


if __name__ == '__main__':
    main()

