from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
statement_A0 = And(
    AKnave,
    AKnight,
)
knowledge0 = And(
    # A is a knight or a knave.
    Or(AKnight, AKnave),
    # A is not both a knight and a knave.
    Not(And(AKnight, AKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_A0, AKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_A0), AKnave),
)

# Puzzle 1
# A says "We are both knaves."
statement_A1 = And(
    AKnave,
    BKnave,
)
# B says nothing.
knowledge1 = And(
    # A is a knight or a knave.
    Or(AKnight, AKnave),
    # A is not both a knight and a knave.
    Not(And(AKnight, AKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_A1, AKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_A1), AKnave),
    # B is a knight or a knave.
    Or(BKnight, BKnave),
    # B is not both a knight and a knave.
    Not(And(BKnight, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
statement_A2 = And(
    Biconditional(AKnight, BKnight),
    Biconditional(AKnave, BKnave),
)
# B says "We are of different kinds."
statement_B2 = And(
    Biconditional(AKnight, BKnave),
    Biconditional(AKnave, BKnight),
)
knowledge2 = And(
    # A is a knight or a knave.
    Or(AKnight, AKnave),
    # A is not both a knight and a knave.
    Not(And(AKnight, AKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_A2, AKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_A2), AKnave),
    # B is a knight or a knave.
    Or(BKnight, BKnave),
    # B is not both a knight and a knave.
    Not(And(BKnight, BKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_B2, BKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_B2), BKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
statement_A3_0 = AKnight
statement_A3_1 = AKnave
statement_A3 = Or(statement_A3_0, statement_A3_1)
# B says "A said 'I am a knave'."
# B says "C is a knave."
statement_B3 = And(statement_A3_1, CKnave)
# C says "A is a knight."
statement_C3 = AKnight
knowledge3 = And(
    # A is a knight or a knave.
    Or(AKnight, AKnave),
    # A is not both a knight and a knave.
    Not(And(AKnight, AKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_A3, AKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_A3), AKnave),
    # B is a knight or a knave.
    Or(BKnight, BKnave),
    # B is not both a knight and a knave.
    Not(And(BKnight, BKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_B3, BKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_B3), BKnave),
    # C is a knight or a knave.
    Or(CKnight, CKnave),
    # C is not both a knight and a knave.
    Not(And(CKnight, CKnave)),
    # Telling the truth leads to being a knight. Being a knight leads to lying.
    Biconditional(statement_C3, CKnight),
    # Lying leads to being a knave. Being a knave leads to lying.
    Biconditional(Not(statement_C3), CKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
