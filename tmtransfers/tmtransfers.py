#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Web Scraping Transfermarkt Transfer Data

Web scrapes league transfer data from Transfermarkt. Results can be
exported as comma-separated value (CSV) files. Also includes a
a function for cleaning resultant dataframes.

Importing as a module provides the following functions:

    * scrape_transfermarkt
    * tidy_transfers
"""

import numpy as np
import pandas as pd

from tmtransfers import helpers


# Exported functions
def scrape_transfermarkt(
    league_name,
    league_id,
    season_id,
    base="https://transfermarkt.com",
    window="",
    loans="3",
    internal="0",
    write=False
):
    """Web scrapes Transfermarkt for the specified transfer activity in the
    given league and season. Returns scraped data as a Pandas dataframe.

    Args:
        league_name (str): League name as shown in a Transfermarkt url.
        league_id (str): Unique league identifier on Transfermarkt.
        season_id (str): First calendar year of the season, e.g. "2020" for
            the 2020/21 season.
        base (str): Transfermarkt base url.
        window (str): "s" or "w" for summer/winter windows, respectively;
            "" for both.
        loans (str): "0" to exclude loans, "1" to include loans, "2" for
            loans only, "3" to exclude players returning from loan.
        internal (str): "0" to exclude movements within clubs, "1" to
            include.
        write (bool): True to export data as a CSV.
        
    Returns:
        pd.DataFrame
    """

    season = str(season_id)
    windows = {
        "s": "summer",
        "w": "winter"
    }

    if window:
        url = base + (
            f"/{league_name}/transfers/wettbewerb/{league_id}/plus/?"
            f"saison_id={season_id}&s_w={window}&leihe={loans}"
            f"&intern={internal}"
        )
        soup = helpers._get_soup(url)
        transfers_df = helpers._get_transfers(soup)
        transfers_df['window'] = windows[window]
    else:
        df_list = []
        for k in windows.keys():
            url = base + (
                f"/{league_name}/transfers/wettbewerb/{league_id}/plus/?"
                f"saison_id={season_id}&s_w={k}&leihe={loans}"
                f"&intern={internal}"
            )
            soup = helpers._get_soup(url)
            df = helpers._get_transfers(soup)
            df['window'] = windows[k]
            df_list.append(df)
        transfers_df = (pd.concat(df_list, ignore_index=True)
            .sort_values(by=['club', 'window'], ignore_index=True)
        )

    transfers_df['league'] = league_name
    transfers_df['season'] = season
    
    if write:
        helpers._export_csv(transfers_df, league_name, season)

    return transfers_df


def tidy_transfers(dataframe):
    """Cleans a dataframe of web scraped transfer records.
 
    Loan status is extracted from `fee`. Unknown and non-applicable numeric
    fields are set to `NaN`, string fields to an empty string.

    Args:
        dataframe (pd.DataFrame): Dataframe of transfer records.

    Returns:
        pd.DataFrame
    """

    def format_fees_and_loans(df):
        """Helper function to parse fees and set loan statuses."""

        if pd.isna(df.fee):
            return df

        df.fee = df.fee.lower()
        fee_string = lambda s: df.fee.startswith(s)

        if fee_string("end of loan"):
            df.fee = "$0"
            df.is_loan = True
            df.loan_status = "end of loan"
        elif fee_string("loan fee"):
            df.fee = df.fee.replace("loan fee:", '')
            df.is_loan = True
            df.loan_status = "loan with fee"
        elif fee_string("loan transfer"):
            df.fee = "$0"
            df.is_loan = True
            df.loan_status = "free loan"
        elif fee_string("free transfer"):
            df.fee = "$0"

        return df


    def value_as_numeric(val):
        """Helper function to convert a currency string to a numeric type."""

        if pd.isna(val) or val == '-' or val == '?':
            return np.nan
        
        # Hack to get around some entries using comma decimal separators
        val = val[1:].lower().replace(',', '.')
        if val[-1] == 'm':
            val = pd.to_numeric(val[:-1]) * 1e6
        elif val[-3:] == 'th.':
            val = pd.to_numeric(val[:-3]) * 1e3
        else:
            val = pd.to_numeric(val, errors='coerce')

        return val
    
    dataframe = (dataframe.assign(is_loan = False, loan_status = '')
        .apply(format_fees_and_loans, axis=1)
        .assign(
            market_value = lambda df: df.market_value.apply(value_as_numeric),
            fee = lambda df: df.fee.apply(value_as_numeric)
        )
    )
    dataframe.age = pd.to_numeric(dataframe.age, errors='coerce')
    dataframe.season = pd.to_datetime(dataframe.season).dt.year
    for col in ['nationality', 'position', 'short_pos', 'dealing_club', 'dealing_country']:
        dataframe[col].fillna('', inplace=True)
    dataframe.league = dataframe.league.str.replace('-', ' ').str.title()    
    
    return dataframe
