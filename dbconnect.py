import mysql.connector

def getSchema(dbinfo):
    cnx = mysql.connector.connect(user=dbinfo['user'], 
                                  password=dbinfo['passwd'],
                                  database=dbinfo['database'])
    cursor = cnx.cursor()

    #query = ("SELECT column(1) FROM "+database+"."+table)
            # "WHERE hire_date BETWEEN %s AND %s")

    query = ("SHOW columns from "+dbinfo['table'])

    cursor.execute(query)

    schema=[]
    for row in cursor:
        schema.append((row[0],row[1]))

    cursor.close()
    cnx.close()

    return schema

def getColumnItems(columns,dbinfo):
    cnx = mysql.connector.connect(user=dbinfo['user'], 
                                  password=dbinfo['passwd'],
                                  database=dbinfo['database'])
    cursor = cnx.cursor()

    query="SELECT id"
    for column in columns:
        query = query + ", " + column
    query = query + " FROM "+dbinfo['table']
    print query
    cursor.execute(query)
    
    items=[i for i in cursor]
    #uniqueItems=set([i[1] for i in items])
    return items

#################
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
print columns
items = getColumnItems(columns,config)
