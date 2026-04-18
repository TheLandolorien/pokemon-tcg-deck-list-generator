import pokemon_tcg_deck_list_generator.cli as cli


def run() -> None:
    args = cli.parse_args()

    print(args.format, args.deck_export)
