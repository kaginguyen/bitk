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

        saving_config = configparser.ConfigParser()
        saving_config.read("./local.ini")
        self.initial_timestamp = saving_config["Local Setting"][self.config["name"]]


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
        # Config here is the config of users 
        config = configparser.ConfigParser()
        config.read(self.ini_file)
        
        # saving_config is the ini file that saves the latest timestamp when running
        # base timestamp from config file is only for starting
        if os.path.exists("./local.ini") == False: 
            saving_config = configparser.ConfigParser()
            saving_config.add_section("Local Setting")

            for i in config.sections():
                saving_config["Local Setting"][config[i]["name"]] = config[i]["initial_timestamp"]
                
            with open("./local.ini", "w") as file: 
                saving_config.write(file)

        elif os.path.exists("./local.ini") == True:
            saving_config = configparser.ConfigParser()
            saving_config.read("./local.ini")
            
            for i in config.sections():
                thread_name = config[i]["name"]
                if config[i]["initial_timestamp"] > saving_config["Local Setting"][thread_name]
                    saving_config["Local Setting"][thread_name] = config[i]["initial_timestamp"]

        
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



        