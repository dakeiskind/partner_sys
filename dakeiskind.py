__author__ = 'dAKE'


def write():
    with open("D:\CodeStore\PyCharm\partner_sys\world.txt", mode='a') as file:
        print("begin...")
        # print(file.read())
        file.write("\nblahblah....\n")
        print("end...")

    # print("begin...")
    # f = open(r"D:/CodeStore/PyCharm/partner_sys/world.txt", mode='a', encoding="UTF-8")
    # f.write("blahblah...")
    # f.close()
    # print("end...")


write()

