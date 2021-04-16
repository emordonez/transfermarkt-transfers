#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tmtransfers import tmtransfers
from tmtransfers.helpers import _parse_hyphenated_string


if __name__ == "__main__":
    """Runs the module as a script."""
    
    # Currency choice determines which version of Transfermarkt is
    #   requested.
    # Main site denominates in euros, UK site in pounds, and US site
    #   in dollars.
    print('\n'.join((
        "\nSelect currency (default is euro):",
        "[1] EUR €",
        "[2] GBP £",
        "[3] USD $"
    )))
    while True:
        options = list(range(1, 4))
        try:
            localization = int(input("===> ") or 1)
            options.index(localization)
            break
        except ValueError:
            print("Error: Please input one of 1, 2, or 3.")
            continue

    print('\n'.join((
        "\nSelect league(s), e.g. '1', '3 5', '6-10' (default is top 5):",
        "[1]  ENG Premier League",
        "[2]  ESP La Liga",
        "[3]  GER Bundesliga",
        "[4]  ITA Serie A",
        "[5]  FRA Ligue 1",
        "[6]  POR Primeira Liga",
        "[7]  NLD Eredivisie",
        "[8]  RUS Premier Liga",
        "[9]  BEL Jupiler Pro League",
        "[10] SCO Scottish Premiership"
    )))
    while True:
        options = list(range(1, 11))
        try:
            choices = _parse_hyphenated_string(input("===> "))
            if not choices:
                leagues = list(range(1, 6))
                break
            elif not all(league in options for league in choices):
                print(f"Error: Please input within the range 1-{len(options)}.")
                continue
        except ValueError:
            print(f"Error: Please input within the range 1-{len(options)}.")
            continue

        leagues = choices
        break

    # English top-flight data are no longer available pre-1992/93 (?)
    print('\n'.join((
        "\nEnter desired seasons as years (default is current season).",
        "Years should be input as the first calendar year in a season, e.g. '2015' for the 2015/16 season.",
        "You can input both indiviudal years and year ranges, e.g. '1992 2004-2007'."
    )))
    while True:
        valid_seasons = list(range(1992, 2021))
        try:
            choices = _parse_hyphenated_string(input("===> "))
            if not choices:
                seasons = [2020]
                break
            elif not all(season in valid_seasons for season in choices):
                print("Error: Seasons are limited to the range 1992-2020.")
                continue
        except ValueError:
            print("Error: Seasons are limited to the range 1992-2020.")
            continue
        
        seasons = choices
        break
        
    print('\n'.join((
        "\nSelect transfer window (default is both):",
        "[1] Both",
        "[2] Summer",
        "[3] Winter"
    )))
    while True:
        options = list(range(1, 4))
        try:
            window = int(input("===> ") or 1)
        except ValueError:
            print("Error: Please input one of 1, 2, or 3.")
            continue
        if window not in options:
            print("Error: Please input one of 1, 2, or 3.")
            continue
        elif window == 1:
            window = ""
        elif window == 2:
            window = "s"
        elif window == 3:
            window = "w"
        break

    print('\n'.join((
        "\nSelect how to handle loan transfers (default is without players back from loan):",
        "[1] Exclude loans",
        "[2] Include loans",
        "[3] Loans only",
        "[4] Without players back from loan"
    )))
    while True:
        options = list(range(1, 5))
        try:
            loans = int(input("===> ") or 4)
        except ValueError:
            print("Error: Please input one of 1, 2, 3, or 4.")
            continue
        if loans not in options:
            print("Error: Please input one of 1, 2, 3, or 4.")
            continue
        else:
            loans -= 1
            break

    print("\nExclude player movements within clubs (Y/n)?")
    while True:
        options = ['y', 'n', 'yes', 'no']
        choice = input("===> ").lower()
        if not choice:
            internal = 0
            break
        if choice not in options:
            print("Please enter y/n.")
            continue
        elif choice == 'y' or choice == 'yes':
            internal = 0
        elif choice == 'n' or choice == 'no':
            internal = 1
        break

    print("\nClean the data with tidy_transfers (Y/n)?")
    while True:
        options = ['y', 'n', 'yes', 'no']
        choice = input("===> ").lower()
        if not choice:
            clean = True
            break
        if choice not in options:
            print("Please enter y/n.")
            continue
        elif choice == 'y' or choice == 'yes':
            clean = True
        elif choice == 'n' or choice == 'no':
            clean = False
        break

    sites = {
        1: "https://transfermarkt.com",
        2: "https://www.transfermarkt.co.uk",
        3: "https://www.transfermarkt.us"
    }
    base = sites[localization]
    league_ids = {
        1: "GB1",
        2: "ES1",
        3: "L1",
        4: "IT1",
        5: "FR1",
        6: "PO1",
        7: "NL1",
        8: "RU1",
        9: "BE1",
        10: "SC1"
    }
    league_names = {
        1: "premier-league",
        2: "laliga",
        3: "1-bundesliga",
        4: "serie-a",
        5: "ligue-1",
        6: "primeira-liga",
        7: "eredivisie",
        8: "premier-liga",
        9: "jupiler-pro-league",
        10: "scottish-premiership" 
    }
    loans = str(loans)
    internal = str(internal)

    print(f"\nNow scraping data for {len(leagues)} league(s) over {len(seasons)} season(s).")
    i = 1
    n = len(leagues) * len(seasons)
    for season in seasons:
        print(f"Scraping the {season}/{str(season + 1)[-2:]} season:")
        for k in leagues:
            league_name = league_names[k]
            league_id = league_ids[k]
            season_id = str(season)

            print('\x1b[2K' + "Requesting...", end='\r', flush=True)
            _ = tmtransfers.scrape_transfermarkt(
                league_name=league_name,
                league_id=league_id,
                season_id=season_id,
                base=base,
                window=window,
                loans=loans,
                internal=internal,
                clean=clean,
                write=True
                )
            print(f"({i}/{n}) Done with: {league_id + ' ' + league_name}")
            
            i += 1

    print("\nDone!\n")
