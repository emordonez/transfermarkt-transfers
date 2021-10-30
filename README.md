# Transfermarkt Transfers (tmtransfers)

All soccer/football club transfers from 1992/93&ndash;2020/21 for 10 of the top European leagues, namely

1. Premier League :england:
2. La Liga :es:
3. Bundesliga :de:
4. Serie A :it:
5. Ligue 1 :fr:
6. Primeira Liga :portugal:
7. Eredivisie :netherlands:
8. Premier Liga* :ru:
9. Jupiler Pro League* :belgium:
10. Scottish Premiership* :scotland:

Data were obtained by web scraping league transfer data from [Transfermarkt](https://www.transfermarkt.com/).

\* _Transfermarkt does not provide data for the 2011/12 Premier Liga season, the 1992/93 and 1993/94 Jupiler Pro League seasons, or the 1992/93&ndash;2002/03 Scottish Premiership seasons._

## Data

All data are provided in the `data` directory and grouped into season subdirectories.
**Feel free to use this dataset for your own purposes!**
You can clone it or [download it via DownGit](https://downgit.github.io/#/home?url=https://github.com/emordonez/transfermarkt-transfers/tree/master/data).
Consult the [README](./data/README.md) for more information.

## Usage

If you'd like to pull the raw data directly from the source or scrape data for other countries and leagues, you can use the Python script provided by `tmtransfers`.

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
