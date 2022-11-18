

import sys
# script that reads lines from jfreechart csv file and gets each metric value
# and puts in corresponding array

def getMetric():
    try:
        filename = sys.argv[1]
    except:
        print("please enter a valid file")

    NOCom = []
    NCLOC = []
    DCP = []

    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            tab = line.split(",")
            NOCom.append(int(tab[1]))
            NCLOC.append(int(tab[2]))
            DCP.append(float(tab[3]))


def main():
    getMetric()


if __name__ == "__main__":
    main()
