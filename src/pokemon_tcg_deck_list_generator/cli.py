import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ptcg-generate-decklist", description="Generate PDF Pokemon TCG deck lists from PTCGL exports."
    )
    parser.add_argument("-f", "--format", help="Standard format abbreviation (e.g., ASC)", default="POR")
    parser.add_argument("-p", "--player-name", help="Player Name", required=True)
    parser.add_argument("-i", "--player-id", help="Player ID", required=True)
    parser.add_argument("-b", "--player-dob", help="Player's Date of Birth", required=True)
    parser.add_argument("-a", "--player-division", help="Player's Age Division", default="Masters")
    parser.add_argument("-v", "--verbose", action="count", default=0)

    return parser.parse_args()
