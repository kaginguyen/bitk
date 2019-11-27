from threading import Thread, Event 
import configparser, os
from time import sleep
import psycopg2



class Worker(Thread):
    def __init__(self, config): 
        Thread.__init__(self)
        
        self._stop_flag = Event()

        self.config = list(config)
        self.thread_name = config["name"]
        self.source_setting = config["source"].split("|")
        self.pull_script = config["pull"]
        self.dest_setting = config["dest"].split("|")
        self.push_script = config["push"]
        self.initial_timestamp = config["initial_timestamp"] 

        config = configparser.ConfigParser()
        config.read("./local.ini")
        if config["Local Setting"][config["name"]] == None: 
            config["Local Setting"][config["name"]] = self.initial_timestamp 
        else: 
            self.initial_timestamp = config["Local Setting"][config["name"]]


    def db_connect(self, db_setting, script):
        if db_setting[0].split(":")[0] == 'postgresql':
            db_conn = psycopg2.connect(dbname = db_setting[0].split(":")[1],
                                        host = db_setting[1].split(":")[0],
                                        port = db_setting[1].split(":")[1],
                                        user = db_setting[2].split(":")[0],
                                        password = db_setting[2].split(":")[1],)
            
            with db_conn.cursor() as cur:
                cur.execute(script)
                result = cur.fetchall()

        elif db_setting[0].split(":")[0] == 'mysql':
            pass 
        
        return result


    def pull(self): 
        # Script formatting will go into this part 
        

        result = db_connect(self.source_setting, self.pull_script)
        
        return result 

    
    def push(self, data): 
        # INSERT script formatting wil go into this part 
        
        db_connect(self.dest_setting, self.push_script)

        return None 


    def run(self):

        while not self.stop_flag.is_set():
            self._stop_flag.wait(5) 
            data = pull()
            push(data) 

            



class Manager:

    def __init__(self, ini_file): 
        self.ini_file = ini_file
        self.execute()


    def execute(self):
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        
        if os.path.exists("./local.ini") == False: 
            local_config = configparser.ConfigParser()
            local_config.add_section("Local Setting")
            for i in config.sections():
                local_config["Local Setting"][config[i]["name"]] = config[i]["initial_timestamp"]
                
            

        
        self.threads_list = []

        for i in config.sections():
            self.threads_list.append(Worker(config[i])) 
        
        for i in self.threads_list:
            i.start()

        # Configuring settings for the management board 
        columns_config = [
                            ["Thread", 15, "_name"],
                            ["Name", 20, "thread_name"],
                            ["Config", 70, "config"],
                            ["Counter", 10, "counter"]
                        ]

        border_str = "".join(list("+" + "-"*(i[1]) for i in columns_config)) + "+"

        try: 
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')

                print(border_str)
                print("".join(list("|" + format(" " + i[0], "<{}".format(i[1])) for i in columns_config)) + "|")
                for thread in self.threads_list:
                    print("".join(list("|" + format(" " + str(thread.__dict__.get(i[2])), "<{}".format(i[1])) for i in columns_config)) + "|" )
                print(border_str)

                sleep(4) 

        except KeyboardInterrupt: 
            for i in self.threads_list:
                i._stop_flag.set()
                i.join()
                print("Thread {} has stopped".format(i.thread_name))



        