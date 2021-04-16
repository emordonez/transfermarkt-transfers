# Transfermarkt Transfers (tmtransfers)

All soccer/football club transfers from 1992/93&ndash;2020/21 for 10 of the top European leagues, namely

1. ENG :england: Premier League
2. ESP :es: La Liga
3. GER :de: Bundesliga
4. ITA :it: Serie A
5. FRA :fr: Ligue 1
6. POR :portugal: Primeira Liga
7. NLD :netherlands: Eredivisie
8. RUS :ru: Premier Liga
9. BEL :belgium: Jupiler Pro League
10. SCO :scotland: Scottish Premiership

Data were obtained by web scraping league transfer data from [Transfermarkt](https://www.transfermarkt.com/).

## Data

All data are provided in the `data` directory and grouped into season subdirectories.
**Feel free to use this dataset for your own purposes!**
Consult the [README](./data/README.md) for metadata and caveats.

## Usage

If you'd like to scrape and clean the data yourself, you can use the Python script provided by `tmtransfers`.

### Setup and running the script

Clone this repository and open a terminal in the cloned folder.
First ensure all dependencies are met:

```bash
pip install -r requirements.txt
```

The module can now be run as a script from the top directory:

```bash
python -m tmtransfers
```

This launches a series of text prompts.
You should see the following output to start:

```text
Select currency (default is euro):
[1] EUR €
[2] GBP £
[3] USD $
===>
```

Follow the prompts to input your desired league parameters.
Scraped data will then be written to CSVs in a created `data` directory.

As an example, an output CSV for the Premier League's 2020/21 season with the default options and before cleaning should look like:

| club       | name                 | age | nationality | position           | short_pos | market_value | dealing_club    | dealing_country | fee           | movement | window | league         | season |
|------------|----------------------|-----|-------------|--------------------|-----------|--------------|-----------------|-----------------|---------------|----------|--------|----------------|--------|
| Arsenal FC | Thomas Partey        | 27  | Ghana       | Defensive Midfield | DM        | €40.00m      | Atlético Madrid | Spain           | €50.00m       | in       | summer | premier-league | 2020   |
| Arsenal FC | Gabriel              | 22  | Brazil      | Centre-Back        | CB        | €20.00m      | LOSC Lille      | France          | €26.00m       | in       | summer | premier-league | 2020   |
| Arsenal FC | Pablo Marí           | 26  | Spain       | Centre-Back        | CB        | €4.80m       | Flamengo        | Brazil          | €5.00m        | in       | summer | premier-league | 2020   |
| Arsenal FC | Rúnar Alex Rúnarsson | 25  | Iceland     | Goalkeeper         | GK        | €1.20m       | Dijon           | France          | €2.00m        | in       | summer | premier-league | 2020   |
| Arsenal FC | Cédric Soares        | 28  | Portugal    | Right-Back         | RB        | €8.00m       | Southampton     | England         | free transfer | in       | summer | premier-league | 2020   |

**Note:** If you run the script again and scrape data for the same league and same season, the existing CSV will be overwritten.
Be sure to move or rename existing files if you need them as is before running the script again.

### Using the module

If you'd like to use this module elsewhere, install it from the top directory with

```bash
pip install .
```

It provides two functions, `scrape_transfermarkt` and `tidy_transfers`.
Use them like so:

```python
import pandas
import tmtransfers

# Web scrape data for a league not explicitly given in the script
# Returns a Pandas dataframe
df = tmtransfers.scrape_transfermarkt(
        league_name='championship',
        league_id='GB2',
        season_id='2005',
        write=True)

# Clean the data
# Returns another Pandas dataframe
tidy_df = tmtransfers.tidy_transfers(df)
```

See the documentation in `tmtransfers.py` for more details.

**Note:** These functions have been tested for only the above leagues through the listed seasons.
You'll have to browse Transfermarkt for what to input to scrape other countries and leagues.

## Source

All data are scraped from [Transfermarkt](https://www.transfermarkt.com/) according to their [terms of use](https://www.transfermarkt.com/intern/anb).
