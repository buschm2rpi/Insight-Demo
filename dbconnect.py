import mysql.connector
from pandas import read_sql

def getSchema(dbinfo):
    cnx = getConnection(columns,dbinfo)
    cursor = cnx.cursor()
    query = ("SHOW columns from "+dbinfo['table'])
    cursor.execute(query)

    schema=[]
    for row in cursor:
        schema.append((row[0],row[1]))

    cursor.close()
    cnx.close()

    return schema

def getColumnItems(columns,dbinfo):
    cnx = getConnection(columns,dbinfo)
    cursor = cnx.cursor()
    query = constructQuery(columns,dbinfo)
    cursor.execute(query)
    #print(cursor.)
    items=[i for i in cursor]
    #uniqueItems=set([i[1] for i in items])

    cursor.close()
    cnx.close()
    
    return items

def getDFfromDB(columns,dbinfo):
    cnx = getConnection(columns,dbinfo)
    query = constructQuery(columns,dbinfo)
    return read_sql(query, cnx, index_col='id')

def constructQuery(columns,dbinfo):
    query="SELECT id"
    for column in columns:
        query = query + ", " + column
    query = query + " FROM "+dbinfo['table']
    print(query)
    return query

def getConnection(columns,dbinfo):
    return mysql.connector.connect(user=dbinfo['user'], 
                                  password=dbinfo['passwd'],
                                  database=dbinfo['database'])

def getDictA2B(fileA):
    B = dict()
    f = open(fileA)
    f.readline() # skip over the header
    line = f.readline().rstrip()
    while line != "":
        data = line.split('"')
        B[data[1]]=data[3]
        line = f.readline().rstrip()
    return B

#################

if __name__ == "__main__":
    config={
        'user':'mbusch',
        'passwd':open("password.txt").readline().rstrip(),
        'database':'insightdb',
        'table':'926969878_T_ONTIME'}

    # for testing
    cnx = mysql.connector.connect(user=config['user'], 
                                      password=config['passwd'],
                                      database=config['database'])


    schema = getSchema(config)
    idx_list=[1,2,3]
    columns = []
    for i in idx_list:
        columns.append(str(schema[i][0]))
    print(columns)
    items = getColumnItems(columns,config)

