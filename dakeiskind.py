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

if __name__ == 'main':
    print 'This is main process.\n'
    print 'amend.'
    write()


class DakeTestBranch(object):
    def __init__(self):
        super(DakeTestBranch, self).__init__()

    def test(self):
        pass

    def dake(self):
        pass