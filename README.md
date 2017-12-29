# investment_lookup

The place to do lookup for relevant projects, jpm, bochk and trade_converter.

An investment instrument has multiple IDs, Bloomberg ticker, Bloomberg BBG id,
ISIN code, etc. Based on one ID we need to lookup other IDs. Also, based on the position's accounting treatment, we need to decide what id to output.



++++++++++
ver 0.2@2017-12-29
++++++++++
1. Changed get_investment_Ids() function in id_lookup.py, remove the condition to check the length of the security id, when the security id type is "Market" and starts with "HK". Because previously those security ID always has length 8, such as "HK 00700", "HK 03480", but then "HK 2025" appears. So this checking is removed.



++++++++++
ver 0.1901@2017-10-23
++++++++++
1. changed get_portfolio_accounting_treatment() to make accounting treatment for in house fund "HTM" (previously it was "trading").



++++++++++
ver 0.19@2017-10-20
++++++++++
1. changed get_portfolio_accounting_treatment() to add in house fund portfolio id.



++++++++++
ver 0.18@2017-08-18
++++++++++
1. changed portfolio id for china life overseas passive accounts.
2. changed portfolio accounting treatment to HTM for 12094, so that it can return the geneva investment id for the portfolio's only position, the private equity holding.



++++++++++
ver 0.17@2017-08-16
++++++++++
1. The id_lookup module now uses standard logging, get logger via:

	logger = logging.getLogger(__name__)


++++++++++
ver 0.16
++++++++++
1. Fixed the test case failures caused by the last update.

2. Updated investLookup.xls for an additional entry.



++++++++++
temporary change
++++++++++
1. Change the get_investment_id_from_isin() function, so that when the portfolio accounting treatment is 'HTM', it returns both geneva investment id (isin + 'HTM') and the ISIN code. This is because HTM portfolios can contain AFS positions, those positions' investment id is just the isin code, therefore we need to return isin code as well to match those positions. However, if a HTM portfolio contain the same bond (say isin = XS123) as both a HTM position and an AFS position, i.e., it has two positions, one is 'XS123 HTM' with no ISIN code and the other 'XS123' with ISIN code, then this approach will fail. But we haven't observed such things happening in the HTM portfolios.

2. For DIF fund, the same bond can appear in both the HTM and AFS section, but there are two position files for DIF, one for HTM position and one for AFS position, so the above approach won't break DIF reconciliation.



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
