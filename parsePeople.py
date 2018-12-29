import xml.dom.minidom
import urllib.request
import threadingFile
import queue
import glob


class PeopleParser(object):

    def __init__(self, url, flag='url'):
        self.list = []
        self.fileList = []
        self.errorPeople = []
        self.countPeople = 0
        self.flag = flag
        self.rem_value = 0
        xml = self.getXml(url)
        self.handleXml(xml)

    def getCountAfterPoint(self, number):
        s = str(number)
        if '.' in s:
            return abs(s.find('.') - len(s)) - 1
        else:
            return 0

    def getXml(self, url):
        try:
            print(url, sep=' \n ')  # имя xml файла
            f = urllib.request.urlopen(url)
        except:
            f = url

        doc = xml.dom.minidom.parse(f)
        node = doc.documentElement
        return node

    def findFileXml(self):
        for filename in glob.glob('*.xml'):
            self.fileList.append(filename)

    def handleXml(self, xml):
        # rem = xml.getElementsByTagName('list')
        appointments = xml.getElementsByTagName("СведенияОполучателе")
        self.handleAppts(appointments)

    def getElement(self, element):
        return self.getText(element.childNodes)

    def handleAppts(self, appts):
        for appt in appts:
            self.handleAppt(appt)

    # функция считает количество тегов "СуммаКвыплате" для сравнение с числом в теге "Количество" (выплат) до 10
    def countTagMoney(self, appt):
        for tag in range(1, 11):
            try:
                self.getElement(appt.getElementsByTagName("СуммаКвыплате")[int(tag)])
            except Exception:
                return int(tag)

    def addListInfoPeople(self,last_name,first_name,middle_name,numberToList,insuranceNumber,accountNumber,countTransfer,typeTransfer,summTransfer,SummingMoneyTransfer):
        construct = []
        construct.append(last_name)
        construct.append(first_name)
        construct.append(middle_name)
        construct.append(numberToList)
        construct.append(insuranceNumber)
        construct.append(int(accountNumber))
        construct.append(int(countTransfer))
        construct.append(typeTransfer)
        construct.append(float(summTransfer))
        construct.append(float(SummingMoneyTransfer))
        return construct

    def handleAppt(self, appt):
        numberToList = self.getElement(appt.getElementsByTagName("НомерВмассиве")[0])
        last_name = self.getElement(appt.getElementsByTagName("Фамилия")[0])
        first_name = self.getElement(appt.getElementsByTagName("Имя")[0])
        middle_name = self.getElement(appt.getElementsByTagName("Отчество")[0])
        insuranceNumber = self.getElement(appt.getElementsByTagName("СтраховойНомер")[0])
        accountNumber = self.getElement(appt.getElementsByTagName("НомерСчета")[0])
        countTransfer = self.getElement(appt.getElementsByTagName("Количество")[0])
        typeTransfer = self.getElement(appt.getElementsByTagName("ПризнакВыплаты")[0])
        moneyTransfer = self.getElement(appt.getElementsByTagName("СуммаКвыплате")[0])
        summTransfer = self.getElement(appt.getElementsByTagName("СуммаКдоставке")[0])

        if self.countTagMoney(appt) >= 1:
            SummingMoneyTransfer = 0 # переменная итогового сложения всех выплат
            SummingMoneyPASTTransfer = 0 # переменная итогового сложения всех ПРОШЕДШИХ выплат
            for ForcountTransfer in range(0,int(self.countTagMoney(appt))):
                SummingMoneyTransfer += float(self.getElement(appt.getElementsByTagName("СуммаКвыплате")[int(ForcountTransfer) ]))

                if self.getElement(appt.getElementsByTagName("ПризнакВыплаты")[int(ForcountTransfer) ]) == 'ПРОШЕДШАЯ':
                    SummingMoneyPASTTransfer += float(self.getElement(appt.getElementsByTagName("СуммаКвыплате")[int(ForcountTransfer) ]))
                else:
                    continue

            # Округляем итоговую сумму всех выплат
            SummingMoneyTransfer = round(float(SummingMoneyTransfer), self.getCountAfterPoint(summTransfer))
            SummingMoneyPASTTransfer = round(float(SummingMoneyPASTTransfer), self.getCountAfterPoint(summTransfer))
            ifTrue = 0
            if float(SummingMoneyPASTTransfer) > 20000:
                ifTrue += 1
            if float(SummingMoneyTransfer) != float(summTransfer):
                print(self.addListInfoPeople(last_name, first_name, middle_name, numberToList, insuranceNumber,
                             accountNumber, countTransfer, typeTransfer, summTransfer,SummingMoneyTransfer))
                print('Cумма выплат НЕ совпадает с итоговой!')
                print(SummingMoneyTransfer)
                print(summTransfer)
                print('//////////////////////////////////////')
                if ifTrue == 1:
                    print('Сумма прошедших выплат БОЛЬШЕ 20.000 рублей')
                    print(str(SummingMoneyPASTTransfer) + " > " + str(SummingMoneyTransfer))
                    print('//////////////////////////////////////')


        else:
            print('Ошибка!')

    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc



# if __name__ == "__main__":


# print(appt.list)
#     fileList = [
#         'PFR-700-Y-2018-ORG-091-001-004521-DIS-002-DCK-14837-001-DOC-SPIS-FSB-0001.xml',
#         'PFR-700-Y-2018-ORG-091-001-004521-DIS-003-DCK-14621-001-DOC-SPIS-FSB-0001.xml']
# for filename in glob.glob('*.xml'):
#     fileList.append(filename)
#     print(PeopleParser.fileList)
    # for file in fileList:
    #     appt = PeopleParser(file)
    #  PeopleParser("xml/people.xml")