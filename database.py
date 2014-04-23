#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys


def setupDB():
    try:
        con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
        
        with con:
    
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Writers")
            cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
                    Name VARCHAR(25))")
            cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
            cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
            cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
            cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
            cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")

            cur.execute("SELECT * FROM Writers")

            rows = cur.fetchall()

            for row in rows:
                print row
    
    except mdb.Error, e:
        
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        
        if con:
            con.close()