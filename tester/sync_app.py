import sys
sys.path.append("../")

from bitk.pipeline import Manager 

if __name__ == '__main__':
    Manager("./test_config.ini")
