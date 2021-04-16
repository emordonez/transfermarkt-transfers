"""Helper functions, not meant for export."""

from pathlib import Path
import requests

from bs4 import BeautifulSoup
import pandas as pd


# Dataframe column names
CLUB = "club"
NAME = "name"
AGE = "age"
NATIONALITY = "nationality"
POSITION = "position"
SHORT_POS = "short_pos"
MARKET_VALUE = "market_value"
DEALING_CLUB = "dealing_club"
DEALING_COUNTRY = "dealing_country"
FEE = "fee"
MOVEMENT = "movement"

COLUMN_HEADERS = [
    CLUB,
    NAME,
    AGE,
    NATIONALITY,
    POSITION,
    SHORT_POS,
    MARKET_VALUE,
    DEALING_CLUB,
    DEALING_COUNTRY,
    FEE,
    MOVEMENT
]


def _export_csv(df, league_name, season_id):
    """Exports a league dataframe to the corresponding season's folder."""

    output_file = f"{league_name}.csv"
    output_dir = Path(f"data/{season_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / output_file, index=False, encoding='utf-8')


def _get_soup(url):
    """Makes an http request and returns the html as BeautifulSoup."""

    headers = {'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
        'like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    )}
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        print("Failed with input url: " + url)

    return BeautifulSoup(response.content, 'lxml')


def _get_transfers(soup):
    """Parses transfer data from BeautifulSoup and writes them to a dataframe."""

    clubs = [tag.text for tag in soup.find_all('div', {'class': 'table-header'})][1:]
    tables = [tag.findChild() for tag in soup.find_all('div', {'class': 'responsive-table'})]
    tables_in = tables[::2]
    tables_out = tables[1::2]
    tables.clear()

    df_list = []
    for (club, table_in, table_out) in zip(clubs, tables_in, tables_out):
        df_list.append(_table_to_df(club, table_in, "in"))
        df_list.append(_table_to_df(club, table_out, "out"))

    if not df_list:
        return pd.DataFrame(columns=COLUMN_HEADERS)

    return pd.concat(df_list, ignore_index=True)


def _parse_hyphenated_string(s):
    """Parses a hyphenated range into a list of integers."""

    # In: "2004-2007"
    # Out: [2004, 2005, 2006, 2007]
    list_of_lists = [list(range(*[int(second) + int(first) 
        for second, first in enumerate(substring.split('-'))])) 
        if '-' in substring else [int(substring)]
        for substring in s.split()]
    
    return [item for sublist in list_of_lists for item in sublist]


def _table_to_df(club, table, movement=None):
    """Creates a dataframe of transfer data read from an html table."""

    age_class = 'alter-transfer-cell'
    nationality_class = 'nat-transfer-cell'
    position_class = 'pos-transfer-cell'
    shortpos_class = 'kurzpos-transfer-cell'
    marketvalue_class = 'mw-transfer-cell'
    dealingclub_class = 'verein-flagge-transfer-cell'
    fee_class = 'rechts'

    data = {header: [] for header in COLUMN_HEADERS}

    def update_data(key, tag, image=False):
        """Helper function to update data dict."""

        if not tag:
            data[key].append(None)
        elif not image and tag.get_text():
            data[key].append(tag.get_text(strip=True))
        elif image and tag.get('alt'):
            data[key].append(tag.get('alt'))
        else:
            data[key].append(None)

    trs = table.find_all('tr')
    for tr in trs[1:]:
        data[CLUB].append(club)
        data[MOVEMENT].append(movement)
        tds = tr.find_all('td')
        if len(tds) == 1:
            return
        for td in tds:
            td_class = td.get('class')
            if td_class:
                if age_class in td_class:
                    update_data(AGE, td)
                elif nationality_class in td_class:
                    td_child = td.findChild()
                    update_data(NATIONALITY, td_child, image=True)
                elif position_class in td_class:
                    update_data(POSITION, td)
                elif shortpos_class in td_class:
                    update_data(SHORT_POS, td)
                elif marketvalue_class in td_class:
                    update_data(MARKET_VALUE, td)
                elif dealingclub_class in td_class:
                    td_country = td.find('img')
                    td_club = td.find('a')
                    update_data(DEALING_COUNTRY, td_country, image=True)
                    update_data(DEALING_CLUB, td_club)
                elif fee_class in td_class:
                    update_data(FEE, td)
            else:
                td_child = td.findChild()
                update_data(NAME, td_child)

    return pd.DataFrame.from_dict(data)
