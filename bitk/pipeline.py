from threading import Thread, Event 
import configparser, os
from time import sleep
from bitk.pgsql import PostgreSQLConnector



class Worker(Thread):
    def __init__(self, config): 
        Thread.__init__(self)
        self.config = list(config)
        self.counter = 0
        self.thread_name = config["name"]
        self.stop_flag = Event()


    def run(self):
        while not self.stop_flag.is_set():
            self.counter += 1
            self.stop_flag.wait(4)



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
                i.stop_flag.set()
                i.join()
                print("Thread {} has stopped".format(i.thread_name))



        