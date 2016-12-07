# investment_lookup

The place to do lookup for relevant projects, jpm, bochk and trade_converter.

An investment instrument has multiple IDs, Bloomberg ticker, Bloomberg BBG id,
ISIN code, etc. Based on one ID we need to lookup other IDs. Also, based on the position's accounting treatment, we need to decide what id to output.



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
