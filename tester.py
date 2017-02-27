__author__ = 'chenqi'

import re, datetime
from partner_sys import utils

def tester():

    str = 'dake_1983-01'

    # regex = re.compile(r'^[\da-zA-Z]+[\d+[a-zA-Z]+[\da-zA-Z]*]')
    regex = re.compile(r'[\dA-Za-z]+[\dA-Za-z_]*')

    m = regex.match(str)
    print(m)
    print(m.group())
    print(m.span())
    print(regex.findall(str))

    # add something
    print 'master finished here'

tester()

print(datetime.date.today())

# # test properties copy
# c = Contact()
# c.name = 'contact_01'
# c.title = 'no title'
# c.tel = '110'
# c.mobile = '13800138000'
# c.idCard = 'mei you'
# c.email = '1@1.com'
# c.idCopy = 'ye mei you'
# print(utils.to_json(c))
#
# p = Potential()
# p.zh_name = u'供应商_01'
# p.en_name = 'partner_01'
# p.ceo = 'Whoever'
# p.scope = 'what?'
# p.founding = datetime.datetime.today()
# p.capital = 100000000000
# p.licence = '0101010101010'
# p.licenceCopy = 'mei you'
# p.tax = 'mei you'
# p.taxCopy = 'ye mei you'
# p.orgCode = '250'
# p.orgCodeCopy = 'mei you'
# p.employees = 3
# p.address = r'beijing'
# p.homepage = r'www.bjhjyd.gov.cn'
# p.tel = '62620202'
# p.fax = '66668888'
# p.post = u'北京市630信箱'
# p.summary = 'blahblahblah....'