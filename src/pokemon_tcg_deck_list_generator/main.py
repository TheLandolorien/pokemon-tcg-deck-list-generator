import logging
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from collections import namedtuple

from PyPDFForm import PdfWrapper, RawElements

import pokemon_tcg_deck_list_generator.cli as cli

DeckListField = namedtuple(typename="DeckListField", field_names=["name", "x", "y", "text", "size"])
Player = namedtuple(typename="Player", field_names=["name", "id", "dob", "division"])

logging.basicConfig(stream=sys.stdout, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SRC_PATH, PACKAGE_NAME = os.path.split(os.path.dirname(__file__))
PACKAGE_PATH = Path(SRC_PATH) / PACKAGE_NAME
ROOT_DIR = Path(os.path.dirname(SRC_PATH))
OUTPUT_DIR = ROOT_DIR / "output"
Path.mkdir(OUTPUT_DIR, exist_ok=True)


def run() -> None:
    args = cli.parse_args()

    logger.setLevel(logging.WARNING - args.verbose * 10)

    player_fields = {
        k.replace("player_", ""): v
        for k, v in vars(args).items()
        if k in ["player_name", "player_id", "player_dob", "player_division"]
    }
    player = Player(**player_fields)
    font_path = PACKAGE_PATH / "assets" / "fonts" / "OpenSans_Condensed-Regular.ttf"
    logger.debug(f"Font Path: {font_path}")

    format = args.format.upper()
    title = f"{player.name} Deck List - {format}"
    decklist_template_path = PACKAGE_PATH / "assets" / "lists" / f"{format}.pdf"

    decklist = PdfWrapper(str(decklist_template_path), title=title, need_appearances=True)
    decklist.register_font("helvetica", str(font_path))
    logger.info(f"Registered Fonts: {decklist.fonts}")

    write_player_fields(pdf=decklist, player=player)
    write_deck_fields(pdf=decklist, deck_path=args.deck_filename, has_regulation=args.has_regulation)

    output_file_path = OUTPUT_DIR / f"{title}.pdf"
    decklist.write(str(output_file_path))


def write_player_fields(pdf: PdfWrapper, player: Player) -> None:
    division_y = 649
    if player.division == "Senior":
        division_y = 662.5
    elif player.division == "Junior":
        division_y = 676
    player_birthdate = datetime.strptime(player.dob, "%Y-%m-%d")

    fields = [
        DeckListField(name="Player Name", x=95, y=713, text=player.name, size=10),
        DeckListField(name="Player ID", x=285, y=713, text=player.id, size=10),
        DeckListField(name="Player Birth Month", x=497, y=713, text=str(player_birthdate.month).zfill(2), size=10),
        DeckListField(name="Player Birth Day", x=524, y=713, text=str(player_birthdate.day).zfill(2), size=10),
        DeckListField(name="Player Birth Year", x=552, y=713, text=player_birthdate.year, size=10),
        DeckListField(name="Player Division", x=376.5, y=division_y, text="x", size=9),
    ]

    content = [
        RawElements.RawText(
            text=field.text, font="helvetica", font_size=field.size, page_number=1, x=field.x, y=field.y
        )
        for field in fields
    ]

    pdf.draw(content)


def write_deck_fields(pdf: PdfWrapper, deck_path: str, has_regulation: bool = False) -> None:
    deck_export_path = ROOT_DIR / deck_path

    assert deck_export_path.exists(), f"{deck_export_path} does not exist"

    deck_list = deck_export_path.read_text().split("\n")

    pokemon = []
    trainers = []
    energy = []
    on_trainers = False
    on_energy = False

    for line in deck_list[1:]:
        if not line:
            continue

        if line.startswith("Trainer: "):
            on_trainers = True
            continue

        if line.startswith("Energy: "):
            on_trainers = False
            on_energy = True
            continue

        if on_energy:
            energy.append(line)
        elif on_trainers:
            trainers.append(line)
        else:
            pokemon.append(line)

    write_pokemon_list(pdf=pdf, pokemon=pokemon, has_regulation=has_regulation)
    write_trainer_list(pdf=pdf, trainers=trainers)
    write_energy_list(pdf=pdf, energy=energy)


def write_pokemon_list(pdf: PdfWrapper, pokemon: list[str], has_regulation: bool) -> None:
    pokemon_content = []
    card_pattern = re.compile(r"([1-9]{1,2}) (.+) ([A-Z]{3}) ([0-9]{1,3})(.*)")

    card_count_x = 274
    card_name_x = 300
    card_set_x = 475
    card_number_x = 515
    card_regulation_x = 555
    card_field_y = 586
    for card in pokemon:
        logger.info(f"Processing Pokémon Card: {card}")
        match = card_pattern.match(card)
        card_count, card_name, card_set, card_number = match.group(1, 2, 3, 4)  # type: ignore
        logger.debug(f"Card Matches: {match.groups()}")  # type: ignore
        card_regulation = None
        if has_regulation:
            card_regulation = match.group(5)[1]  # type: ignore

        pokemon_content.append(
            RawElements.RawText(
                text=card_count, font="helvetica", font_size=10, page_number=1, x=card_count_x, y=card_field_y
            )
        )
        pokemon_content.append(
            RawElements.RawText(
                text=card_name, font="helvetica", font_size=10, page_number=1, x=card_name_x, y=card_field_y
            )
        )
        pokemon_content.append(
            RawElements.RawText(
                text=card_set, font="helvetica", font_size=10, page_number=1, x=card_set_x, y=card_field_y
            )
        )
        pokemon_content.append(
            RawElements.RawText(
                text=card_number, font="helvetica", font_size=10, page_number=1, x=card_number_x, y=card_field_y
            )
        )
        if card_regulation:
            pokemon_content.append(
                RawElements.RawText(
                    text=card_regulation,
                    font="helvetica",
                    font_size=10,
                    page_number=1,
                    x=card_regulation_x,
                    y=card_field_y,
                )
            )
        card_field_y -= 13.1

    pdf.draw(pokemon_content)


def write_trainer_list(pdf: PdfWrapper, trainers: list[str]) -> None:
    trainer_content = []
    card_pattern = re.compile(r"([1-9]{1,2}) (.+) [A-Z]{3} [0-9]{1,3}")

    card_count_x = 274
    card_name_x = 300
    card_field_y = 410
    for card in trainers:
        logger.info(f"Processing Trainer Card: {card}")
        card_count, card_name = card_pattern.match(card).group(1, 2)  # type: ignore

        trainer_content.append(
            RawElements.RawText(
                text=card_count, font="helvetica", font_size=10, page_number=1, x=card_count_x, y=card_field_y
            )
        )
        trainer_content.append(
            RawElements.RawText(
                text=card_name, font="helvetica", font_size=10, page_number=1, x=card_name_x, y=card_field_y
            )
        )
        card_field_y -= 13.1

    pdf.draw(trainer_content)


def write_energy_list(pdf: PdfWrapper, energy: list[str]) -> None:
    energy_content = []
    card_pattern = re.compile(r"([1-9]{1,2}) (.+) [A-Z]{3} [0-9]{1,3}")

    card_count_x = 274
    card_name_x = 300
    card_field_y = 129
    for card in energy:
        logger.info(f"Processing Energy Card: {card}")
        card_count, card_name = card_pattern.match(card).group(1, 2)  # type: ignore

        energy_content.append(
            RawElements.RawText(
                text=card_count, font="helvetica", font_size=10, page_number=1, x=card_count_x, y=card_field_y
            )
        )
        energy_content.append(
            RawElements.RawText(
                text=card_name, font="helvetica", font_size=10, page_number=1, x=card_name_x, y=card_field_y
            )
        )
        card_field_y -= 13.1

    pdf.draw(energy_content)
