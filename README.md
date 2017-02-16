# investment_lookup

The place to do lookup for relevant projects, jpm, bochk and trade_converter.

An investment instrument has multiple IDs, Bloomberg ticker, Bloomberg BBG id,
ISIN code, etc. Based on one ID we need to lookup other IDs. Also, based on the position's accounting treatment, we need to decide what id to output.



++++++++++
ver 0.15
++++++++++
1. Add support for 'Market' as a security id type. Previouly all 'Market' type security id are based on lookup, now if the security id of a 'Market' type looks like a HK equity, Geneva investment id is generated automatically.



++++++++++
ver 0.14
++++++++++
1. Bug fix: when security id is of integer form, it is read in as a float number, but we need string.

2. Add one more security in the lookup table.


++++++++++
ver 0.13
++++++++++
1. Updated portfolio code mapping to accounting treatment in function get_portfolio_accounting_treatment(), based on Kathleen's input for trustee equity portfolio code.


++++++++++
ver 0.12
++++++++++
1. Updated accounting treatment mapping in get_portfolio_accounting_treatment(), added '12404', '12528'.



++++++++++
ver 0.12
++++++++++
1. id_lookup.py updated to add more mapping from portfolio id to accounting treatment in function get_portfolio_accounting_treatment()



++++++++++
ver 0.11
++++++++++
1. Add more logging.
2. investmentLookup.xls updated.



++++++++++
ver 0.1
++++++++++
1. Migrated from jpm's id_lookup.py module.
2. Add one more parameter to the get_investment_Ids() function, the accounting treatment of the position, to handle the situation of DIF, because it contains both HTM and Trading positions.
