from bs4 import BeautifulSoup
import re
from db import result_database
import sqlite3
from excel import Excel
import time
import logging
import os
logging.basicConfig(level=logging.INFO)

                    
class LTE_xml():                    
    def read(self, filename):
        self.infile = open(filename,"r",encoding="utf8")
        return self.infile.read()
    def get_Measured(self, contents):
        self.result_list = []
        self.soup = BeautifulSoup(contents,'xml') 
        for self.tag in self.soup.find_all('Name',text ='LTE3GPPTest_V12_4'):
            self.tag1 = self.tag.next_sibling.next_sibling
            if self.tag1 == None:
                continue
            self.tag2 = self.tag1.find_all('TestItemList')
            for m in self.tag2:
                self.tag3 = m.find_all('ListContext')
                for tag3_item in self.tag3:
                    logging.debug('tag3_item = {0}'.format(tag3_item))
                    testitem = tag3_item.string.split('@')[0]   #获得测试项目与频段
                    band = tag3_item.string.split('@')[1]
    #                logging.info(testitem, band)
                self.tag4 = m.find_all('TestItem')
                for n in self.tag4:
                    channel = re.search(r'(\d+)',n.Condition.string).group()
                    condition = re.search(r'BW.+',n.Condition.string).group()
                    description = n.Description.string
                    if testitem == '6.5.2.4 EVM Equalizer Spectrum Flatness' or testitem == '6.6.1 Occupied Bandwidth ':
                        value = n.Verdict.string
                    else:
                        value = n.MeasValue.string
                    self.result_list.append((band, channel, testitem, description, condition, value))
        return self.result_list        
    def print_(self):
        print(self.result_list)    
        
def main():  
    global band, channel, lte_test_items, lte_items_local, aclr_local, aclr_description, aclr_condition, frq_err_condition
    band ={'lte':(
                    # '1',
                    '3', 
                    '7', 
                    # '8',
                    '20', 
                    # '38', 
                    )}
    channel = {
                '1':('18050', '18300', '18550'),
                '3':('19250', '19575', '19900'), 
                '20':('24200', '24300', '24400'), 
                '7':('20800', '21100', '21400'), 
                '8':('21500', '21625', '21750'),                 
                '38':('37800', '38000', '38200'), 
                '40':('38700', '39150', '39600')
                }
    lte_test_items = {
#                        '6.2.2 Maximum Output Power ': 'BW: 10 MHz ; UL_MOD_RB: QPSK, 12 (RB_Pos:LOW)', 
                        '6.2.3 Maximum Power Reduction ':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:LOW)',  
                        '6.3.2 Minimum Output Power ':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)',  
#                        '6.5.1 Frequency Error ':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)', 
                        '6.5.2.1 Error Vector Magnitude (EVM) for PUSCH ':'BW: 10 MHz , ULPower: 23 dBm; UL_MOD_RB: QPSK, 12 (RB_Pos:LOW)' , 
                        '6.5.2.4 EVM Equalizer Spectrum Flatness':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)' , 
                        '6.6.1 Occupied Bandwidth ':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)'  
                        }
                        
    lte_items_local = {
                        '6.2.2 Maximum Output Power ': (12, 6),  
                        '6.2.3 Maximum Power Reduction ':(13, 6),  
                        '6.3.2 Minimum Output Power ':(14, 6),  
                        '6.5.1 Frequency Error ':(15, 6), 
                        '6.5.2.1 Error Vector Magnitude (EVM) for PUSCH ':(16, 6) , 
                        '6.5.2.4 EVM Equalizer Spectrum Flatness':(17, 6) , 
                        '6.6.1 Occupied Bandwidth ':(18, 6) 

                        }  
    aclr_local = {
                    'BW: 10 MHz ; UL_MOD_RB: QPSK, 12 (RB_Pos:LOW)':(19, 6), 
                    'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:LOW)':(22, 6)
                    }
    aclr_description =  {
                        '1':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '3':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '5':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '7':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '8':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '20':('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-7.5MHz):', 'UTRA ACLR1 (+7.5MHz):', 'UTRA ACLR2 (-12.5MHz):', 'UTRA ACLR2 (+12.5MHz):'), 
                        '38': ('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-5.8MHz):', 'UTRA ACLR1 (+5.8MHz):', 'UTRA ACLR2 (-7.4MHz):', 'UTRA ACLR2 (+7.4MHz):'), 
                        '40': ('E-UTRA ACLR (-10MHz):', 'E-UTRA ACLR (+10MHz):', 'UTRA ACLR1 (-5.8MHz):', 'UTRA ACLR1 (+5.8MHz):', 'UTRA ACLR2 (-7.4MHz):', 'UTRA ACLR2 (+7.4MHz):')
                        }
                        
    aclr_condition = [
                'BW: 10 MHz ; UL_MOD_RB: QPSK, 12 (RB_Pos:LOW)', 
                'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:LOW)'
                ] 
    frq_err_condition = {
                        '1':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)', 
                        '3':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)',  
                        '5':'BW: 10 MHz ; UL_MOD_RB: QPSK, 25 (RB_Pos:HIGH)', 
                        '7':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)', 
                        '8':'BW: 10 MHz ; UL_MOD_RB: QPSK, 25 (RB_Pos:HIGH)', 
                        '20':'BW: 10 MHz ; UL_MOD_RB: QPSK, 20 (RB_Pos:HIGH)', 
                        '38':'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)', 
                        '40': 'BW: 10 MHz ; UL_MOD_RB: QPSK, 50 (RB_Pos:HIGH)',   
                        }            
    input('请确定band配置正确，Enter to continue\n{0}'.format(band))
    LTE = LTE_xml()
    path = "./xml_file"
    files= os.listdir(path)
    file = "./xml_file/"+files[0]    
    contents = LTE.read(file)
    result_list = LTE.get_Measured(contents)
    logging.info('{0} get data from xml file done'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
    result = result_database('result')
    if result.check_exist():
        result.drop_table()
    result.create_table('(band char,channel char,testitem char, description char, condition char,value char)')
    result.writetotable_list3D(result_list)  
    logging.info('{0} write data to database done'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
    list_a = []
    for key in lte_test_items:    #根据lte_test_items查找出对应的value
        for band_lte in band['lte']:
            n = 0
            for chan in channel[band_lte]:
                conn = sqlite3.connect('test.db')
                cursor = conn.cursor()                       
                cursor.execute('''
                                    select value from result 
                                    where 
                                    band is '{0}' 
                                    and 
                                    channel is '{1}' 
                                    and 
                                    testitem is '{2}' 
                                    and 
                                    condition is '{3}'
                                    '''
                                    .format(' Band'+band_lte, chan, key, lte_test_items[key]))
                r=cursor.fetchall()
#                logging.info(' Band{0},{1},{2},{3},{4}'.format(band_lte, chan, key, lte_test_items[key], r))
                list_a.append(['LTEB'+band_lte, lte_items_local[key][0], lte_items_local[key][1]+n, max(r)[0] ])
                n = n + 1
    aclr = aclr_get()
    frq_err = freq_err_get()
    maxpwr = maxpwr_get()
    list_a = list_a + aclr + frq_err + maxpwr
    for index, item in enumerate(list_a):  #将value转换为数值类型
        try:
            list_a[index][3] = eval(item[3])
        except NameError:
            continue
    logging.info('{0} format data done'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))            
    logging.debug('list_a = {0}'.format(list_a))  
    path = "./excel_model"
    files= os.listdir(path)
    file = "./excel_model/"+files[0]
    excel = Excel(file)
    logging.info('{0} writing data to excel file: \'a_changed.xlsx\' '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))        
    NOK = 1
    while NOK:
        try:
            excel.writeto(list_a)
            NOK = 0
        except PermissionError:
            logging.error('请关闭excel文件后,Enter重试')
            input()
    logging.info('{0} analys successful'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ))
    input('Enter to Exit')

    
def aclr_get():
    list_a = []
    tempdic={}  
    for band_lte in band['lte']:
        n = 0
        for chan in channel[band_lte]:
            for condition in aclr_condition:
                for description in aclr_description[band_lte]:
                    conn = sqlite3.connect('test.db')
                    cursor = conn.cursor()                       
                    cursor.execute('''
                                        select value from result 
                                        where 
                                        band is '{0}' 
                                        and 
                                        channel is '{1}' 
                                        and 
                                        testitem is '{2}' 
                                        and 
                                        description is '{3}' 
                                        and
                                        condition is '{4}'
                                        '''
                                        .format(
                                        " Band"+band_lte, chan, '6.6.2.3 Adjacent Channel Leakage Power Ratio ', description, condition
                                        ))
                    r=cursor.fetchall()
                    tempdic[description] = r
#                    logging.info(band_lte, chan, description, condition, r)
                    
                E_UTRA_value = min(tempdic[aclr_description[band_lte][0]], tempdic[aclr_description[band_lte][1]])[0][0]
                
                UTRA1_value = min(tempdic[aclr_description[band_lte][2]], tempdic[aclr_description[band_lte][3]])[0][0]
                UTRA2_value = min(tempdic[aclr_description[band_lte][3]], tempdic[aclr_description[band_lte][4]])[0][0]
                list_a.append(['LTEB'+band_lte, aclr_local[condition][0], aclr_local[condition][1]+n, E_UTRA_value])
                list_a.append(['LTEB'+band_lte, aclr_local[condition][0]+1, aclr_local[condition][1]+n, UTRA1_value])
                list_a.append(['LTEB'+band_lte, aclr_local[condition][0]+2, aclr_local[condition][1]+n, UTRA2_value])
            n = n + 1
                
    return list_a
    
def freq_err_get():    
    list_a = []
    for band_lte in band['lte']:
        n = 0
#        logging.info(band_lte)
        condition = frq_err_condition[band_lte]
        for chan in channel[band_lte]:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()                       
            cursor.execute('''
                                select value from result 
                                where 
                                band is '{0}' 
                                and 
                                channel is '{1}' 
                                and 
                                testitem is '{2}' 
                                and 
                                condition is '{3}'
                                '''
                                .format(
                                ' Band'+band_lte, 
                                chan, 
                                '6.5.1 Frequency Error ', 
                                condition
                                ))
            r=cursor.fetchall()
#            logging.info(' Band'+band_lte, chan, '6.5.1 Frequency Error ', condition, r)
            list_a.append(['LTEB'+band_lte, lte_items_local['6.5.1 Frequency Error '][0], lte_items_local['6.5.1 Frequency Error '][1]+n, max(r)[0] ])
            n = n + 1
    return list_a

def maxpwr_get():    
    list_a = []
    for band_lte in band['lte']:
        n = 0
        for chan in channel[band_lte]:
            if chan == '18550' or chan == '38200' or chan == '39600':
                condition = 'BW: 10 MHz ; UL_MOD_RB: QPSK, 12 (RB_Pos:HIGH)'
            else:
                condition = 'BW: 10 MHz ; UL_MOD_RB: QPSK, 12 (RB_Pos:LOW)'
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()                       
            cursor.execute('''
                                select value from result 
                                where 
                                band is '{0}' 
                                and 
                                channel is '{1}' 
                                and 
                                testitem is '{2}' 
                                and 
                                condition is '{3}'
                                '''
                                .format(
                                ' Band'+band_lte, 
                                chan, 
                                '6.2.2 Maximum Output Power ', 
                                condition
                                ))
            r=cursor.fetchall()
#            logging.info(' Band'+band_lte, chan, '6.2.2 Maximum Output Power ', condition, r)
            list_a.append(['LTEB'+band_lte, lte_items_local['6.2.2 Maximum Output Power '][0], lte_items_local['6.2.2 Maximum Output Power '][1]+n, max(r)[0] ])
            n = n + 1
    return list_a    
if __name__ == '__main__':
    main()
