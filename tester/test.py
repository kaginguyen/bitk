import psycopg2

def db_connect(db_setting):
    db_setting = db_setting.split("|")
    if db_setting[0].split(":")[0] == 'postgresql':
        db_conn = psycopg2.connect(dbname = db_setting[0].split(":")[1],
                                    host = db_setting[1].split(":")[0],
                                    port = db_setting[1].split(":")[1],
                                    user = db_setting[2].split(":")[0],
                                    password = db_setting[2].split(":")[1])
    
    return db_conn


with db_connect("postgresql:futbin_db|163.172.175.100:5432|postgres:megane123").cursor() as cur: 
    cur.execute("SELECT * FROM futbin_sch.player_index")
    data = cur.fetchall()

print(data) 