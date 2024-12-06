# Chase's 2024 Advent of Code Solutions

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Creating New Solutions

Use the setup script to create the directory structure and files for a new day:

```bash
python create_daily_assets.py --day XX  # where XX is the day number (1-25)
```

This will:

- Create empty `input.txt` and `test.txt` files within directory `inputs/XX`
- Copy the solution template from `solutions/00.py` to `solutions/XX.py`

## Running Solutions

```bash
python -m solutions.XX --test  # to run with test input
python -m solutions.XX        # to run with real input
```

where `XX` is the zero-padded day number (01-25)
