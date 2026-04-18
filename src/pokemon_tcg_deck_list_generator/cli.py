import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ptcg-generate-decklist", description="Generate PDF Pokemon TCG deck lists from PTCGL exports."
    )
    parser.add_argument("-f", "--format", help="Standard format abbreviation (e.g., ASC)")
    parser.add_argument("-d", "--deck-export", help="Path to Deck export", required=True)

    return parser.parse_args()
