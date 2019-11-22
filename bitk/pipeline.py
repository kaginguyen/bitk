from threading import Thread
import configparser, os
from time import sleep



class Worker(Thread):
    def __init__(self, config): 
        Thread.__init__(self)
        self.config = list(config)
        self.counter = 0
        self.thread_name = config["name"]
        global stop_flag


    def run(self):
        while True: 
            try: 
                self.counter += 1
                sleep(1)
        
            except stop_flag == True:
                break



class Manager:

    def __init__(self, ini_file): 
        self.ini_file = ini_file
        self.execute()


    def execute(self):
        config = configparser.ConfigParser()
        config.read(self.ini_file)
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
            stop_flag = False
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')

                print(border_str)
                print("".join(list("|" + format(" " + i[0], "<{}".format(i[1])) for i in columns_config)) + "|")
                for thread in self.threads_list:
                    print("".join(list("|" + format(" " + str(thread.__dict__.get(i[2])), "<{}".format(i[1])) for i in columns_config)) + "|" )
                print(border_str)

                sleep(3) 
        except: 
            pass 

        