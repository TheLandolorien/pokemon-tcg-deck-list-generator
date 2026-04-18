# Pokémon TCG Deck List Generator

Generate PDF Pokemon TCG deck lists from PTCGL exports.

## ⚡️ Quick Start

Ensure [Python](https://www.python.org/downloads) and [Python Poetry](https://python-poetry.org/docs/#installation) are installed.

Dependency installation is managed via `poetry`. Once cloned, you can install dependencies from the project root:

```shell
poetry install
```

Once dependencies are installed, you can run the `ptcg-generate-decklist` command with our information like this:

```shell
poetry run ptcg-generate-decklist -p "First Last" -i 1234567 -b 2000-01-01 -a Junior
```

And boom! You're ready to generate your Pokémon TCG Deck Lists via CLI! 🎉

## 🪪 License

This tool is [MIT licensed](./LICENSE).
