import logging
import sys
import os
from pathlib import Path
from collections import namedtuple

from PyPDFForm import PdfWrapper, RawElements

import pokemon_tcg_deck_list_generator.cli as cli

DeckListField = namedtuple(typename="DeckListField", field_names=["name", "x", "y", "text", "size"])

logging.basicConfig(stream=sys.stdout, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SRC_PATH, PACKAGE_NAME = os.path.split(os.path.dirname(__file__))
PACKAGE_PATH = Path(SRC_PATH) / PACKAGE_NAME
OUTPUT_DIR = Path(os.path.dirname(SRC_PATH)) / "output"
Path.mkdir(OUTPUT_DIR, exist_ok=True)


def run() -> None:
    args = cli.parse_args()

    logger.setLevel(logging.WARNING - args.verbose * 10)

    write_fields(player_name=args.player, format=args.format)


def write_fields(player_name: str, format: str) -> None:
    format = format.upper()
    fields = [
        DeckListField(name="Player Name", x=93, y=713, text=player_name, size=10),
    ]
    title = f"{player_name} Deck List - {format}"

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
