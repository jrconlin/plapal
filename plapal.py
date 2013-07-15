# -*- coding: utf_8 -*-
import os
import socket
import id3reader

import sqlite3
import hashlib
from pprint import pprint
from  optparse import OptionParser

def listDirectory(directory, fileExtList):
    content = [os.path.normcase(f)
                for f in os.listdir(directory)]
    fileList = []
    for f in content:
        fullPath = os.path.join(directory, f)
        if os.path.isfile(fullPath):
            if os.path.splitext(f)[1] in fileExtList:
                fileList.append(fullPath)
            next
        if os.path.isdir(fullPath):
            fileList = fileList + listDirectory(fullPath, fileExtList)
            next
    return fileList

def getData(path, stripPath=""):
    id3 = id3reader.Reader(f)
    strip = len(stripPath)
    return {"title": id3.getValue("title"),
            "artist": id3.getValue("performer"),
            "album": id3.getValue("album"),
            "genre": id3.getValue("genre"),
            "hash": genHash(path),
            "path": f[strip:]}


def genHash(path):
    sha = hashlib.sha256()
    source = open(path, 'rb')
    for i in xrange(0,10):
        try:
            buf = source.read(10240)
            sha.update(buf)
        except:
            break
    source.close()
    return sha.hexdigest()

def storeData(cur, data, host):
    cur.execute("insert into description "
                         "(id, artist, title, album, genre) "
                         "values (?,?,?,?,?)",(
                         data["hash"],
                         data["artist"],
                         data["title"],
                         data["album"],
                         data["genre"]))
    cur.execute("insert into files (id, path, host) values (?,?,?)",[
                      data["hash"],
                      data["path"].decode('utf8'),
                      host])

def findMatch(cur, data):
    cur.execute("select * from files where id = ?", [data["hash"]])
    return cur.fetchone()

def storeError(cur, data, error):
    cur.execute("insert into errors (id, path, error) values (?,?,?)",
                (data["hash"], data["path"], error));


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory", help="Directory to scan", default="/media/music/")
    parser.add_option("-D", "--database", dest="database", help="Database to store results", default="plapal.sqlite")
    parser.add_option("-H", "--host", dest="host", help="Host name", default=socket.gethostname())
    (options, args) = parser.parse_args()

    
    db = sqlite3.connect(options.database)
    cur = db.cursor()
    print "Gathering Files from %s:%s" % (options.host, options.directory)
    files = listDirectory(options.directory, [".mp3"])
    print "Storing music..."
    for f in files:
        data = getData(f, options.directory)
        try:
            storeData(cur, data, options.host)
        except Exception,e:
            db.commit()
            print "Skipping..."
            pprint(data)
            print "\t\t%s" % e
            pprint(findMatch(cur, data))
            import pdb;pdb.set_trace()
            #storeError(cur, data, e)
        # pprint(data)
    db.commit()

