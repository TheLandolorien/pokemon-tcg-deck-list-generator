import logging
import sys
import os
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
OUTPUT_DIR = Path(os.path.dirname(SRC_PATH)) / "output"
Path.mkdir(OUTPUT_DIR, exist_ok=True)


def run() -> None:
    args = cli.parse_args()

    logger.setLevel(logging.WARNING - args.verbose * 10)

    player_fields = {k.replace("player_", ""): v for k, v in vars(args).items() if k not in ["format", "verbose"]}
    write_fields(format=args.format, player=Player(**player_fields))


def write_fields(format: str, player: Player) -> None:
    format = format.upper()
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
    title = f"{player.name} Deck List - {format}"

    decklist_template_path = PACKAGE_PATH / "assets" / "lists" / f"{format}.pdf"
    logger.debug(f"Template Path: {decklist_template_path}")

    font_path = PACKAGE_PATH / "assets" / "fonts" / "OpenSans_Condensed-Regular.ttf"
    logger.debug(f"Font Path: {font_path}")

    decklist = PdfWrapper(str(decklist_template_path), title=title, need_appearances=True)
    decklist.register_font("helvetica", str(font_path))
    logger.info(f"Registered Fonts: {decklist.fonts}")

    content = [
        RawElements.RawText(
            text=field.text, font="helvetica", font_size=field.size, page_number=1, x=field.x, y=field.y
        )
        for field in fields
    ]

    decklist.draw(content)

    output_file_path = OUTPUT_DIR / f"{title}.pdf"
    decklist.write(str(output_file_path))
