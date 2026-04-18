import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ptcg-generate-decklist", description="Generate PDF Pokemon TCG deck lists from PTCGL exports."
    )
    parser.add_argument("-f", "--format", help="Standard format abbreviation (e.g., ASC)", default="POR")
    parser.add_argument("-d", "--deck-export", help="Path to Deck export", required=True)
    parser.add_argument("-p", "--player", help="Player Name", required=True)
    parser.add_argument("-v", "--verbose", action="count", default=0)

    return parser.parse_args()
