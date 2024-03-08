#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

### IMPORTANTE: Los scripts se deben ejecutar desde la ruta que se guardan.

# This script generates a 'citations' table for uploading ClinVar sci-articles citations related to variants from a non-compressed text file.


import sys, os
import sqlite3

try:
	# Trying to load a newer version
	import pysqlite3
	if pysqlite3.sqlite_version_info > sqlite3.sqlite_version_info:
		del sqlite3
		import pysqlite3 as sqlite3
	else:
		del pysqlite3
except:
	pass

if sqlite3.sqlite_version_info < (3, 37, 0):
	raise AssertionError("Este programa necesita una versión de SQLite igual o superior a 3.37.0")

# For compressed input files
import gzip
import re

CLINVAR_TABLE = [

    ''' 
    CREATE TABLE IF NOT EXISTS citations (
        allele_id INTEGER NOT NULL,
        citation_source TEXT NOT NULL,
        citation_id TEXT NOT NULL
    ) STRICT
    
    '''
    ,

    ''' 
    CREATE INDEX IF NOT EXISTS idx_citations_allele_id ON citations(allele_id)
    
    '''
    ,
    '''
    CREATE INDEX IF NOT EXISTS idx_citations_citation_id ON citations(citation_id)
    
    '''
]

def open_citations_db(db_file):
    if not os.path.exists(db_file):
        db = sqlite3.connect(db_file, isolation_level=None)
        cur = db.cursor()
        try:
            cur.execute("PRAGMA journal_mode=WAL")
        except sqlite3.Error as e:
            print("An error occurred: {}".format(str(e)), file=sys.stderr)
        finally:
            cur.close()
        db.close()
    
    db = sqlite3.connect(db_file)

    cur = db.cursor() # Conexión a la base de datos SQLite
    try:
        cur.execute("PRAGMA synchronous = normal;")
        cur.execute("PRAGMA FOREIGN_KEYS=ON")
        for tableDecl in CLINVAR_TABLE:
            cur.execute(tableDecl)
    except sqlite3.Error as e:
        print("An error occurred: {}".format(str(e)), file=sys.stderr)
    finally:
        cur.close()
    return db

def store_citations_file(db, citations_file):
    with open(citations_file, "rt", encoding="utf-8") as cf:
        cur = db.cursor()
        headerMapping = None
        with db:
            for line in cf:
                wline = line.rstrip("\n")
                if (headerMapping is None) and (wline.startswith('#')):
                    wline = wline.lstrip("#")
                    columnNames = re.split(r"\t", wline)
                    headerMapping = {}
                    for columnId, columnName in enumerate(columnNames):
                        headerMapping[columnName] = columnId
                else:
                    columnValues = re.split(r"\t", wline)
                    for iCol, vCol in enumerate(columnValues):
                        if len(vCol) == 0 or vCol == "-":
                            columnValues[iCol] = None
                    allele_id = int(columnValues[headerMapping["AlleleID"]])
                    citation_source = columnValues[headerMapping["citation_source"]]
                    citation_id = columnValues[headerMapping["citation_id"]]
                    cur.execute("""
                        INSERT INTO citations(
                            allele_id, 
                            citation_source, 
                            citation_id) 
                        VALUES(?,?,?)
                    """, (allele_id, citation_source, citation_id))
        cur.close()
		
# Cerrar la conexión con la base de datos
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {0} {{db_file}} {{citations_file}}".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    db_file = sys.argv[1]
    citations_file = sys.argv[2]
    db = open_citations_db(db_file)
    try:
        store_citations_file(db, citations_file)
    finally:
        db.close()	
#store_clinvar_file()
#conn.close()

