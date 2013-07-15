# -*- coding: utf_8 -*-
import sqlite3
from  optparse import OptionParser

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-t", "--thumb_file", dest="thumbs", help="List of thumbs-up songs", default="thumbs.list")
    parser.add_option("-D", "--database", dest="database", help="Database to store results", default="plapal.sqlite")
    (options, args) = parser.parse_args()

    db = sqlite3.connect(options.database)
    cur = db.cursor()
    thumbs = open(options.thumbs, "r")
    import pdb; pdb.set_trace()
    for line in iter(thumbs.readline, ''):
        try:
            (artist, title, album) = line.strip().split("|",3)
            cur.execute("update description set rating=5 where artist like ? and title like ? and album like ?", 
                        [artist.decode('utf8'), title.decode('utf8'), album.decode('utf8')])
        except Exception, e:
            import pdb; pdb.set_trace()
            print e
        print ("%s %s" % (artist, album))
    db.commit()



