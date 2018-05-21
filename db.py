import sqlite3
import logging

class result_database():
    def __init__(self, tbname):
        self.dbname = 'test.db'
        self.tbname = tbname
        
    def check_exist(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        sql="SELECT count(*) FROM sqlite_master WHERE type='table' AND name='"+self.tbname+"'"
        cursor.execute(sql)
        b=cursor.fetchall()
        if b[0][0] == 1: 
#            pass
            logging.info('table <{0}> exists'.format(self.tbname))
            return True
        else:
            logging.info('table <{0}> do not exists'.format(self.tbname))
            return False
            
#            cursor.execute('drop table {0}'.format(self.tbname))
##            cursor.execute('create table {0} (ref_designer primary key)'.format(self.tbname)) 
#        else:
#            logging.info('{0} do not exists, create new one'.format(self.tbname))
#        cursor.execute('''create table {0} (
#                                            band char,
#                                            channel char, 
#                                            testitem char, 
#                                            condition char, 
#                                            value char 
#                                            )'''.format(self.tbname)) 
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()  
    def print_header(self):        
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info ({0})".format(self.tbname)) 
        b=cursor.fetchall()
#        cursor.close()
#        # 提交事务:
#        conn.commit()
#        # 关闭Connection:
#        conn.close()  
        print('the table \'{0}\' header is:{1}'.format(self.tbname, b))
    def print_tables(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute('select name from sqlite_master where type = "table" order by name')
        b=cursor.fetchall()
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()  
        print('The table is:{0}'.format(b))
    def print_all(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute('select * from {0}'.format(self.tbname))
        b=cursor.fetchall()
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()  
        print('{0}'.format(b))    
    def drop_table(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        sql="SELECT count(*) FROM sqlite_master WHERE type='table' AND name='"+self.tbname+"'"
        cursor.execute(sql)
        b=cursor.fetchall()
        if b[0][0] == 1: 
            logging.info('table \'{0}\' exists,drop...'.format(self.tbname))
            cursor.execute('drop table {0}'.format(self.tbname))
            logging.info('drop table \'{0}\' succeful'.format(self.tbname))
        else:
            logging.info('table {0} do not exists'.format(self.tbname))
    def writetotable(self, list):   
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        try:
            cursor.execute("insert into {0} values {1}".format(self.tbname, list))
        except sqlite3.IntegrityError as e:
            print(e)
        cursor.close()
        conn.commit()
        conn.close()  

    def read_part(self, target_, col, data_):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
#        logging.info(target_, tbname, col, data_)
        cursor.execute("select {0} from {1} where {2} is '{3}'".format(target_, self.tbname, col, data_))
        b=cursor.fetchall()
#        cursor.close()
#        # 提交事务:
#        conn.commit()
#        # 关闭Connection:
#        conn.close() 
        if b == []:
            pass
#           logging.info('{0} 未在本地找到'.format(data_))
            return ''
        else:
            pass
#            logging.info('{0}'.format(b)) 
        return b[0][0]
    def del_part(self, col, data_):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute("delete from {0} where {1} is '{2}'".format(self.tbname, col, data_))
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close()  
    def create_table(self, tuple_):    
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        cursor.execute('create table {0} {1}'.format(self.tbname, tuple_))
        cursor.close()
        # 提交事务:
        conn.commit()
        # 关闭Connection:
        conn.close() 
    def writetotable_list3D(self, list3D):    
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        n = 0
        for a in list3D:
            try:
                n = n + 1
#                logging.info(a)
                cursor.execute("insert into {0} values {1}".format(self.tbname, a))
#                logging.info(n)
            except sqlite3.IntegrityError as e:
                logging.info(e)
        cursor.close()
        conn.commit()
        conn.close() 
if __name__ == '__main__':
    
    result = result_database('result')
    result.check_exist()
#    result.create_table('result', ('band char','channel char','testitem char','condition char','value char'))
#    result.print_tables()
    result.print_header()
#    result.print_all()
#    result.drop_table('result')
#    list_ = (' Band3', '19250', '6.2.2 Maximum Output Power ', 'BW: 10 MHz ; UL_MOD_RB: QPSK, 1 (RB_Pos:HIGH)', '23.45')
#    result.writetotable('result', list_)
    # datalist0 = main.opendata0('data0.csv')
#    print(result.read_part('temp','description','Part_Number', 'AMY0001466CX'))
#    result.del_part('Part_Number', 'AMY0001466CX')
#    result.drop_table('result')
#    result.create_table('temp', ('Part_Number primary key', 'desc char', 'name char', 'decal char', 'value char', 'ref char'))
#    result.writetotable('temp', ('','','ACA56HHA02CX','电感,Inductor,5.6 nH,±3 %,DCR=0.88 ohm,250 mA,0201,Film,0.63×0.33×0.33 mm,LQP03TG5N6H02D,MURATA', '电感', '0201', '5.6nh', 'L4261,L4442'))
