# -*- coding: utf_8 -*-
import os
import socket
from mutagen.id3 import ID3

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
    id3 = ID3(path)
    strip = len(stripPath)
    data = {"path": f[strip:]}
    if "TIT2" in id3:
        data["title"] = id3["TIT2"].text[0]
    else:
        data["title"] = "UNKNOWN"
    if "TPE1" in id3:
        data["artist"] = id3["TPE1"].text[0]
    else:
        data["artist"] = "UNKNOWN"
    if "TALB" in id3:
        data["album"] = id3["TALB"].text[0]
    else:
        data["album"] = "UNKNOWN"
    data["hash"] = genHash(path, id3.size)
    return data
    
def genHash(path, header_size):
    sha = hashlib.sha256()
    source = open(path, 'rb')
    head = source.read(3)
    if head == "ID3":
        source.seek(header_size)
    else:
        source.seek(0)
    # Skip null padding
    buf = source.read(1)
    while buf != "\xFF":
        buf = source.read(1)
    source.seek(-1, 1)
    for i in xrange(0,10):
        try:
            buf = source.read(10240)
            if (i==0 and buf[0] != "\xFF"):
                import pdb; pdb.set_trace()
                print "Uh-oh!"
            sha.update(buf)
        except:
            break
    source.close()
    return sha.hexdigest()

def storeData(cur, data, host):
    try:
        cur.execute("insert into description "
                         "(id, artist, title, album) "
                         "values (?,?,?,?)",(
                         data["hash"],
                         data["artist"],
                         data["title"],
                         data["album"]))
        cur.execute("insert into files (id, path, host) values (?,?,?)",[
                      data["hash"],
                      data["path"].decode('utf8'),
                      host])
    except sqlite3.IntegrityError:
        pass
    except Exception, e:
        import pdb; pdb.set_trace()
        print e

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
        try:
            data = getData(f, options.directory)
            storeData(cur, data, options.host)
        except Exception,e:
            db.commit()
            print "Skipping..."
            pprint(data)
            print "\t\t%s" % e
            pprint(findMatch(cur, data))
            #storeError(cur, data, e)
        # pprint(data)
    db.commit()

