# SQL
## This repository contains a walk- through of a project done with Python for SQL.
### This project consisted in writing Python scripts that obtain information from previously searched and downloaded files and dump it into SQLite databases, which the scripts also create. There are three different scripts:
- The first one, which is called clinvar_citations.py, is meant to upload information from ClinVar on scientific articles related to the variants. That information can be found on the file "var_citations.txt". 
- The second script (clinvar_stats.py) loads ClinVar data from the statistics of variants per gene, which is contained in "var_summary.txt".
- Finally, civic.py is responsible for loading CIViC variant information, similar to that loaded from ClinVar with clinvar_parser.py. In this case, the data is obtained from two different files, being "01-    Dec-2023-VariantSummaries" and "01-Dec-2023-ClinicalEvidenceSummaries".

