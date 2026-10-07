from logic import *


def solve(puzzle_name, people, knowledge):
    """Print the entailed kind (Knight or Knave) of each person."""
    print(puzzle_name)
    for person in people:
        knight = Symbol(f"{person} is a Knight")
        knave = Symbol(f"{person} is a Knave")
        if model_check(knowledge, knight):
            print(f"{person} is a Knight")
        elif model_check(knowledge, knave):
            print(f"{person} is a Knave")
        else:
            print(f"{person}: unknown")
    print()


# ============================================================
# Puzzle 0: A says "I am both a knight and a knave."
# ============================================================
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

knowledge0 = And(
    # A is exactly one of knight / knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # What A says
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

solve("Puzzle 0:", ["A"], knowledge0)


# ============================================================
# Puzzle 1: A says "We are both knaves." B says nothing.
# ============================================================
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

# A's statement: "We are both knaves."
statement1 = And(AKnave, BKnave)

knowledge1 = And(
    # Exactly one kind per person
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    # A's utterance
    Implication(AKnight, statement1),
    Implication(AKnave, Not(statement1)),
    # B says nothing -> no constraint
)

solve("Puzzle 1:", ["A", "B"], knowledge1)


# ============================================================
# Puzzle 2: A says "We are the same kind."
#           B says "We are of different kinds."
# ============================================================
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

same = Or(And(AKnight, BKnight), And(AKnave, BKnave))
different = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    # Exactly one kind per person
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    # A's utterance
    Implication(AKnight, same),
    Implication(AKnave, Not(same)),
    # B's utterance
    Implication(BKnight, different),
    Implication(BKnave, Not(different)),
)

solve("Puzzle 2:", ["A", "B"], knowledge2)


# ============================================================
# Bonus Puzzle 3:
#   A says either "I am a knight." or "I am a knave." (unknown which)
#   B says "A said 'I am a knave'."
#   B also says "C is a knave."
#   C says "A is a knight."
# ============================================================
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Tracks which sentence A actually uttered:
#   ASaidKnave = True  -> A said "I am a knave."
#   ASaidKnave = False -> A said "I am a knight."
ASaidKnave = Symbol("A said: I am a knave")

# A's actual utterance is true iff it matches A's real kind.
AStatement = Or(
    And(ASaidKnave, AKnave),          # A said "I am a knave" and A is a knave
    And(Not(ASaidKnave), AKnight),    # A said "I am a knight" and A is a knight
)

# B's utterance is a conjunction of two claims.
BStatement = And(ASaidKnave, CKnave)  # "A said 'I am a knave'" AND "C is a knave"

# C's utterance.
CStatement = AKnight                  # "A is a knight"

knowledge3 = And(
    # Exactly one kind per person
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave), Not(And(CKnight, CKnave)),
    # A's utterance
    Implication(AKnight, AStatement),
    Implication(AKnave, Not(AStatement)),
    # B's utterance
    Implication(BKnight, BStatement),
    Implication(BKnave, Not(BStatement)),
    # C's utterance
    Implication(CKnight, CStatement),
    Implication(CKnave, Not(CStatement)),
)

solve("Puzzle 3 (Bonus):", ["A", "B", "C"], knowledge3)