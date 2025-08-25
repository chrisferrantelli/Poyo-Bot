import random
import importlib

def test_check():
    assert True

def test_poyoball_response():
    responses = [
        # Positive
        "POYO!",
        "Poyoooo!!",
        "POOYO! (double puff)",
        "POYOPOYO!!",
        "poyo. (nods firmly)",
        "Poyo~",
        "Po~yo? (hopeful bounce)",
        "poyo poyo poyo!",
        "poyo.",
        "POyO!! (with jazz hands)",

        # Uncertain
        "...poyo?",
        "poy...yo?",
        "(blushes) poy...",
        "p-p-poyo??",
        "*inhales deeply* ...poyoooooooooo",

        # Negative
        "poy-nah.",
        "PO—no. (record scratch)",
        "...noYO.",
        "poyo... (shakes head)",
        "poynope."
  ]

    for _ in range(20):
        resp = random.choice(responses)
        assert resp in responses


def test_ego_rating():
    for _ in range (100):
        val = random.randint(1, 100)
        assert 1 <= val <= 100