import pyodbc
 
conn = pyodbc.connect(r'DBQ=C:\Users\piquard\Documents\eparts.accdb')
cursor = conn.cursor()
cursor.execute('select * from drumFr')
    
for row in cursor.fetchall():
    print (row)

cursor = conn.cursor()
cursor.execute('select * from drumFr')
   
for row in cursor.fetchall():
    print (row)
