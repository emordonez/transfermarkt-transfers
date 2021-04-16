# Transfermarkt Transfer Data

## Code

| Label             | Description                                                     |
|-------------------|-----------------------------------------------------------------|
| `club`            | Club involved in the transfer, i.e. the buyer/seller            |
| `name`            | Player’s name                                                   |
| `age`             | Player’s age at the date of the transfer                        |
| `nationality`     | Player’s nationality per FIFA international eligibility         |
| `position`        | Player’s position                                               |
| `short_pos`       | Abbreviated `position`, e.g. CF for centre-forward              |
| `market_value`    | Transfermarkt’s estimated market value of the player            |
| `dealing_club`    | Other club involved in the transfer, i.e. the seller/buyer      |
| `dealing_country` | Country in which the `dealing_club` competes                    |
| `fee`             | Transfer fee in euros                                           |
| `movement`        | In or out                                                       |
| `window`          | Summer or winter                                                |
| `league`          | `club`’s league                                                 |
| `season`          | First year of the season of the transfer, e.g. 2020 for 2020/21 |
| `is_loan`         | Indicator for a loan transfer                                   |
| `loan_status`     | Additional details if a loan transfer                           |

## Missing data

### How to interpret null values

* `age`, `nationality`, `position`, and `short_pos` are empty when they aren't listed on Transfermarkt.
* `market_value` and `fee` are empty if they're unknown or not applicable.
Transfermarkt market value is based on community estimates, so market values are generally more available in higher rated leagues and as time goes on.
Fees are unknown if they have been undisclosed or not reported, and not applicable for certain kinds of player movement, e.g. retirements and bans.
  * 0 is _not_ recommended as a fill-in, to avoid confusion with free transfers and loans that have a known fee of 0.
  * Check `dealing_club` and `dealing_country` for the things like retirements and bans.
* `dealing_club` and `dealing_country` are empty if they aren't listed on Transfermarkt.
`dealing_country` is also empty for the special movements like retirements and bans (check `dealing_club` for specifics).
* `loan_status` is a computed column that is empty only if `is_loan` is false.
It can be safely filled however you wish.

### Null counts

Nonzero null counts out of 134,437 records in the data:

* `age` = 41
* `nationality` = 28
* `position` = `short_pos` = 3
* `market_value` = 51,499
* `dealing_country` = 7,306
* `fee` = 34,629
* `loan_status` = 92,725

## Missing leagues

Transfermarkt does not provide data (not sure why) for

* the 2011/12 Russian Premier Liga season,
* the 1992/93 and 1993/94 Belgian Jupiler Pro League seasons,
* or the 1992/93&ndash;2002/03 Scottish Premiership seasons.

The corresponding CSVs are empty.
