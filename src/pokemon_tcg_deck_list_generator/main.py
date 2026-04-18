from pathlib import Path

import pokemon_tcg_deck_list_generator.cli as cli


def run() -> None:
    args = cli.parse_args()

    deck_list_template_path = Path("assets") / f"{args.format}.pdf"

    print(deck_list_template_path, args.deck_export)
