---
title: Cards
emoji: ⚡
colorFrom: gray
colorTo: pink
sdk: streamlit
sdk_version: 1.15.2
app_file: app.py
pinned: false
license: apache-2.0
---

# cards: prototype UIs for ML cards

> ### 🌱 Just sprouting!
> This project is in the very beginning stages of development. It's not well tested and is only intended to be used as a demo.

## Installation

``` shell
git clone https://github.com/codesue/cards.git
cd cards
pip install -r requirements.txt
```

NOTE: It's not possible to install model-card-toolkit on an M1 machine due to
an [ml-metadata incompatibility](https://github.com/google/ml-metadata/issues/143).
Most MCT functionality needed for this app is implemented in `placeholder_mct_lib.py`
and will be used if MCT isn't installed.

## Running the app

```shell
python run.py
```

## Working in a notebook

If you prefer to work in a notebook and don't mind ~~living dangerously~~ creative
workarounds, check out `dev.ipynb`. 
