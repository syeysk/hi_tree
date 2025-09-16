import sqlite3

c = sqlite3.connect(':memory:')
cu = c.cursor()
try:
    for i in cu.execute('CREATE VIRTUAL TABLE testrtree USING rtree(id,minX,maxX,minY,maxY);'):
        print(i)
    
    print('supported')
except Exception as error:
    print('not supported:', error)
