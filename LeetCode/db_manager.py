#! /usr/bin/env python
#coding=utf-8


import sys
import psycopg2
import traceback
import datetime,time
import thread
import threading


reload(sys)   
sys.setdefaultencoding('utf8')
mutex = threading.Lock()

class tuple(object):
    	def __init__(self):
            self.id=""
            self.name=""

class Rule(object):
    
    def __init__(self):
        self.full_content = 'content'
        self.content = '''content:"<IMG";nocase:;content:"SRC";distance:0;nocase:;isdataat:244,relative;pcre:"/src\s*\x3D(3D)?\s*['"][^'"]{244}/i";'''
        self.deprecated = 0
        self.flowbits = ''
        self.protocol = ''
        self.from_ports = ''
        self.to_ports = '80'
        self.metadata = ''
        self.sid = -1
        self.gid = -1
        self.revision = -1
        self.is_client_to_server = -1

class Reference(object):
    def __init__(self,type,name):
        self.type = type
        self.name = name
        
class OrderBy(object):
    def __init__(self,name,type):
        self.type = type
        self.name = name


class Vulnerability(object):
    
    SCHEMA = 'production'
    
    def __init__(self):
            
        self.remarks = '测试100'
        self.owner_name = 'user'
        self.has_rules = 1
        self.exploit_path = ''
        self.sample_path = ''
        self.ori_update_time = '1970-01-01'
        self.ori_repair_time = '1970-01-01'
        self.ori_publish_time = '1970-01-01'
        self.ori_description = ''
        self.severity = 'critical'
        self.ori_name = 'this is a test2'
        self.credit = 'bill gates'
        self.references = []
        self.rules = []
        self.category = 'DOS'
        
        rule = Rule()
        self.rules.append(rule)
        
        reference_1 = Reference('test','ref1')
        reference_2 = Reference('test','ref2')
        self.references.append(reference_1)
        self.references.append(reference_2)
        
    


class Database(object):


    def __init__(self,db_name,user_name):
        try:
            
            
            self.con = psycopg2.connect(database=db_name, user=user_name) 
            self.cur = self.con.cursor()
            
            '''
            self.cur.execute("set client_encoding = 'gbk'")
            self.con.commit()
            '''

            
            # for test use
            self.relations = {'vulnerabilities':{'source':'origin_id','status':'status_id','category':'ori_class_id','credit':'credit_id','users':'owner_id','result':'result_id'},'category':{'source':'source_id'},'users':{'role':'role_id'},'reference_to':{'references':'reference_id','vulnerabilities':'vulnerability_id'},'is_vulnerable':{'vulnerabilities':'vulnerability_id','software':'software_id'},'snort_rules':{'vulnerabilities':'vulnerability_id'},'is_same_vulnerability':{'vulnerabilities':'my_id'},'is_former_vulnerability':{'vulnerabilities':'my_id'}}
            
            
        except psycopg2.DatabaseError, e:
            print traceback.print_exc()
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
            sys.exit(1)
            
            
    def set_db_relations(self,dict):
        self.relations = dict;
            
            
    def __del__(self):
        if self.con:
            self.con.close()
        
        
        
    
    
    # four base operations
    
    def exeute_raw(self,query):
        try:
                            
            # print query
                            
            self.cur.execute(query) 
            self.con.commit()
            
            return True
                    
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
            
            return False
        
        
    
    def select_raw(self,col_names,query):
        data = []
                                
        try:
                    
            # print query
                    
            self.cur.execute(query) 
            rows = self.cur.fetchall()
            
            
            
            for row in rows:
                if len(col_names) == 1:
                    data.append(row[0])
                else:
                    dict = {}
                    for i in range(len(col_names)):
                        if isinstance(row[i],datetime.date):
                            dict[col_names[i]] = row[i].isoformat()
                        else:
                            dict[col_names[i]] = row[i]

                    data.append(dict)
            
            
            self.con.commit()
            
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
                    
                    
        
        
        print str(len(data)) + " is selected in select_raw"
        return data
        
		
    def select(self,table_name,schema,col_names,conditions={},order_bys=[]):                                                     
                
        data = []
                        
        try:
            
            col_name = ''
            
            if col_names != None:
                for col in col_names:
                    col_name += col + ','
            
            condition = ''
            if condition != None:
                for key,value in conditions.items():
                    condition += key + ' ' + value[0] + ' \'' + str(value[1]) + '\' and '
            
            order_by = ''
            for col in order_bys:
                order_by += col.name + ' ' + col.type + ', '
            
            
            if table_name != None:
                if schema == None or len(schema) == 0:
                    query = 'select ' + col_name[:-1] + ' from ' + table_name
                else:
                    query = 'select ' + col_name[:-1] + ' from ' + schema + '.' + table_name
                    
                if len(condition) > 0:
                    query += ' where ' + condition[:-4]
                if len(order_by) > 0:
                    query += ' order by ' + order_by[:-2]
                    
                #print query,'in select'    
                
                self.cur.execute(query) 
                rows = self.cur.fetchall()
            
                for row in rows:
                    if len(col_names) == 1:
                        data.append(row[0])
                    else:
                        dict = {}
                        for i in range(len(col_names)):
                            if isinstance(row[i],datetime.date):
                                dict[col_names[i]] = row[i].isoformat()
                            else:
                                dict[col_names[i]] = row[i]
                        
                        data.append(dict)
                        
                self.con.commit()
        except psycopg2.DatabaseError, e:
            print traceback.print_exc()
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
                    
                    
        
        
        # print str(len(data)) + " in select"
        return data

    
    def delete(self,table_name,conditions,schema = ''):
        # DELETE FROM 表名称 WHERE 列名称 = 值
        try:
                            

            condition = ''
            query = 'delete from '
            

                
            for key,value in conditions.items():
                condition += str(key) + value[0] + '\'' + str(value[1]) + '\' and '
            
            
            
            if len(schema) > 0:
                query += schema + '.'
                       
            
            query += table_name
            
            if len(condition) > 0:
                query += ' where ' + condition[:-4]
            
            # print query + "in delete"
                            
            self.cur.execute(query) 
            self.con.commit()
            
            return True
            
        except psycopg2.DatabaseError, e:
            print traceback.print_exc()
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
            
            return False
        

    def update(self,table_name,dict,conditions,schema = ''):
        # UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'

        try:
                    
            sets = ''
            condition = ''
            query = 'update ' 
            
            for key,value in dict.items():
                sets += str(key) + '= \'' + str(value) + '\' , '
                
            for key,value in conditions.items():
                if len(schema) > 0:
                    condition += schema + '.'
                condition += str(key) + value[0] + '\'' + str(value[1]) + '\' and '
            
            
            
            if len(schema) > 0:
                query += schema + '.'
                       
            
            query += table_name + ' set ' + sets[:-2]
            
            if len(condition) > 0:
                query += ' where ' + condition[:-4]
            
            print query + " in update"
                            
            self.cur.execute(query) 
            self.con.commit()
            
            return True
            
        except psycopg2.DatabaseError, e:
            print traceback.print_exc()
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
            
            return False
        

    def insert(self,table_name,dict,schema = ''):
        
        try:
            
            keys = ''
            values = ''
            
            for key,value in dict.items():
                # print key,value
                
                keys += key + ','
                values += '\'' + str(value) + '\','
            
            query = 'insert into ' 
            
            if len(schema) > 0:
                query += schema + '.'
            query += table_name + ' (' + keys[:-1] + ') values (' + values[:-1] + ')'
            
           # print query + " in insert"
                            
            self.cur.execute(query) 
            self.con.commit()
            
            return True
            
        except psycopg2.DatabaseError, e:
            print traceback.print_exc()
            print 'Error %s' % e    
            print sys.exc_info()[0],sys.exc_info()[1] 
            
            return False
        
    
    
    
    # functions for login
    def get_role(self,user,passwd):
        
        user_info = (' = ',user)
        passwd_info = (' = ',passwd)
        
        all_tables = ['users','role']
        all_fields = ['role.name']
        
        return self.select_complex(all_fields,all_tables,{'users.name':user_info,'users.password':passwd_info},Vulnerability.SCHEMA)
        

    
    
    # functions for browsing
    def get_serverinfoip(self):
	return self.select('serverinfo',Vulnerability.SCHEMA,('ip','function','admin','passwd'))
    def get_vminfo(self):
	return self.select('vminfo', Vulnerability.SCHEMA,('ip','username','soft','admin','passwd','iso'))


    def get_users(self):
        return self.select('users',Vulnerability.SCHEMA,('name',))
    
    
    def get_source(self):
         return self.select('source',Vulnerability.SCHEMA,('name',))
    
    
    def get_category(self):
        return self.select('category',Vulnerability.SCHEMA,('category',))
    
    def get_package(self):
	return self.select('exploitpackage', Vulnerability.SCHEMA,('sid','status','checkname','exploitname'))

    def get_rules(self):
	return self.select('rule', Vulnerability.SCHEMA,('name','status','testinfo','exinfo','rules','cve','sid'))


    def get_netentsec_category(self):
        all_tables = ['category','source']
        all_fields = ['category.category']
        
        
        order = OrderBy('category.category','asc')
        orders = []
        orders.append(order)
        
                
        return self.select_complex(all_fields,all_tables,{'source.name':(' = ','netentsec_snort')},Vulnerability.SCHEMA,orders)
                
        
    
    
    def get_status(self):
        return self.select('status',Vulnerability.SCHEMA,('name',))
    
    
    def get_credit(self):
        return self.select('credit',Vulnerability.SCHEMA,('name',))
    
    
    def get_result(self):
        return self.select('result',Vulnerability.SCHEMA,('name',))
    
    
    def get_severity(self):
        query = 'select distinct ori_severity from ' + Vulnerability.SCHEMA + '.vulnerabilities'
        return self.select_raw(['ori_severity'],query)
		
		
    
    def select_complex(self,fields,tables,conditions = {},schema = '',order_bys = [],is_distinct = False):
        query = 'select '
        
        if is_distinct:
            query += ' distinct '
                
        for i in range(len(fields)):
            
            
            if len(schema) == 0:
                query += fields[i]
            else:
                query += schema + '.' + fields[i]
            
            if i != len(fields) - 1:      
                query +=  ','
        
        query += ' from '
        
        for i in range(len(tables)):
            
            if len(schema) == 0:
                query += tables[i]
            else:
                query += schema + '.' + tables[i]
            
            if i != len(tables) - 1:                  
                query += ','
        
        condition = ''
        
        for table in tables:
            if table in self.relations:
                dict = self.relations.get(table)
                for key,value in dict.items():
                    
                    if key in tables:
                        
                        if len(schema) != 0:
                            condition += schema + '.' 
                        condition += table + '.' + value + ' = '
                    
                        if len(schema) != 0:
                            condition += schema + '.' 
                    
                        condition += key + '.id and '
        
        
        for key,value in conditions.items():
            
            if len(schema) > 0:
                condition += schema + '.'
#            if key == 'ori_name':    
#		condition += 'upper(' key + ') ' + value[0] + ' \'' + str(value[1]) + '\' and '   
#            else:
		condition += key + ' ' + value[0] + ' \'' + str(value[1]) + '\' and '
            
            
        order_by = ''
        for col in order_bys:
            if len(schema) == 0:
                order_by += col.name + ' ' + col.type + ', '
            else:
                order_by += schema + '.' + col.name + ' ' + col.type + ', '

                        
            
            
                    
        if len(condition) > 0:
            query += ' where ' + condition[:-4]         
        
        if len(order_by) > 0:
            query += ' order by ' + order_by[:-2]
        
        
        print query + " in select complex"
        
        return self.select_raw(fields,query)
	
        
        
    def assign_vulnerabilities(self,user_name,ids):
        
        if user_name != None and len(ids) > 0:
            owner_id = self.select('users',Vulnerability.SCHEMA,('id',),{'name':(' =  ',user_name)})
            
            if len(owner_id) == 1:
                
                # UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
                
                query = 'update ' + Vulnerability.SCHEMA + '.vulnerabilities set owner_id = \'' + str(owner_id[0]) + '\' where id in ( '
                
                for id in ids:
                    query += str(id) + ','
                    
                query = query[:-1] + ')'
            
                # print query
                
                for id in ids:
                    table_name = 'vulnerabilities'
                    dict = {'status_id':2}
                    conditions = {'vulnerabilities.id':('=',id)}
                    updated = self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
                
                return self.exeute_raw(query)
            
        
        return False
                
                
    def specify_same_vulnerabilities(self,my_id,ids):
        
        if len(ids) > 0 and int(my_id) > 0:
            for id in ids:
                table_name = 'is_same_vulnerability'
                dict = {'my_id':int(my_id),'equivalent_id':int(id)}
                inserted = self.insert(table_name,dict,Vulnerability.SCHEMA)
                


  
    
    def get_vulnerability_list(self,dict={},order_by=[]):
        
        # original implementation
        
        '''
        all_tables = ['users','source','category','status','credit','result','vulnerabilities','snort_rules']
        all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ch_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ch_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.remarks']
        return self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)
        '''
        if  'references.name' in dict.keys():

            all_tables = ['users','source','category','status','credit','result','vulnerabilities','snort_rules','references','reference_to']
            all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ch_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ch_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path'
,'vulnerabilities.remarks']
            list = self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)

            existed = []
            new_list = []

            print 'original size',len(list)

            for row in list:
                if row['vulnerabilities.id'] in existed:
                    pass
                else:
                    existed.append(row['vulnerabilities.id'])
                    new_list.append(row)

            print len(list),len(new_list)
            return new_list    
            
        elif 'snort_rules.is_client_to_server' in dict.keys() or 'snort_rules.deprecated' in dict.keys() or 'snort_rules.sid' in dict.keys() or 'snort_rules.nsid' in dict.keys() or 'snort_rules.is_deleted' in dict.keys() or 'snort_rules.full_content' in dict.keys():
            
            all_tables = ['users','source','category','status','credit','result','vulnerabilities','snort_rules']
            all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.remarks']
            list = self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)
            
            existed = []
            new_list = []
            
            print 'original size',len(list)
            
            for row in list:
                if row['vulnerabilities.id'] in existed:
                    pass
                else:
                    existed.append(row['vulnerabilities.id'])
                    new_list.append(row)
            
            print len(list),len(new_list)
            return new_list
                
            
        else:
            all_tables = ['users','source','category','status','credit','result','vulnerabilities']
            all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ch_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ch_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.remarks']
            list = self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)
            
            print 'original size',len(list)
            
            return list
        
    
        '''
        if 'snort_rules.is_client_to_server' in dict.keys():
            # first select all vulnerabilities' ids which meet the requirements
            table_name = 'snort_rules'
            conditions = {}
            
            value = dict.get('snort_rules.is_client_to_server')
            
            conditions['is_client_to_server'] = (value[0],int(value[1]))
                    
            ids = self.select(table_name,Vulnerability.SCHEMA,('vulnerability_id',),conditions)
            ids = list(set(ids))
            
            # delete the unnecessary key
            dict.pop('snort_rules.is_client_to_server')
            
            all_tables = ['users','source','category','status','credit','result','vulnerabilities']
            all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.remarks']
            
            all_list = []
            
            for id in ids:
                dict['vulnerabilities.id'] = (' = ',int(id))
                
                a_list = self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)
                
                for element in a_list:
                    all_list.append(element)
                    
            
            # print all_list
            return all_list
        
        else:
            
            all_tables = ['users','source','category','status','credit','result','vulnerabilities']
            all_fields = ['vulnerabilities.id','users.name','source.name','category.category','status.name','credit.name','result.name','vulnerabilities.ori_name','vulnerabilities.ori_publish_time','vulnerabilities.ori_repair_time','vulnerabilities.ori_update_time','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.has_rules','vulnerabilities.ori_id','vulnerabilities.ori_severity','vulnerabilities.ori_description','vulnerabilities.ori_id','vulnerabilities.sample_path','vulnerabilities.exploit_path','vulnerabilities.remarks']
            return self.select_complex(all_fields,all_tables,dict,Vulnerability.SCHEMA,order_by)
        '''
            
        
    
    
   
    # functions for production
    def get_reference(self,id):
        
        all_tables = ['references','reference_to','vulnerabilities']
        all_fields = ['references.type','references.name']
        return self.select_complex(all_fields,all_tables,{'vulnerabilities.id':('=',id)},Vulnerability.SCHEMA,[],True)
        
        
    
    
    def get_rule(self,id):
	
	order_by = []
	tmp = tuple()
	tmp.name = "snort_rules.sid"
	tmp.type = "asc"        
	order_by.append(tmp)

        all_tables = ['snort_rules','vulnerabilities']
        all_fields = ['snort_rules.id','snort_rules.full_content','snort_rules.content','snort_rules.sid','snort_rules.gid','snort_rules.revision','snort_rules.protocol','snort_rules.flowbits','snort_rules.deprecated','snort_rules.from_ports','snort_rules.to_ports','snort_rules.metadata','snort_rules.is_client_to_server','snort_rules.nsid','snort_rules.sig_protocol','snort_rules.host_type','snort_rules.direction','snort_rules.default_action','snort_rules.os','snort_rules.is_valid','snort_rules.engine_type','snort_rules.xai_type']
        return self.select_complex(all_fields,all_tables,{'vulnerabilities.id':('=',id),'snort_rules.is_maxversion':('=',1)},Vulnerability.SCHEMA,order_by)
        
    
    def get_vulnerable(self,id):
        all_tables = ['is_vulnerable','software','vulnerabilities']
        all_fields = ['software.manufacturer','software.product_name','software.product_version']
        return self.select_complex(all_fields,all_tables,{'vulnerabilities.id':('=',id)},Vulnerability.SCHEMA)
        
    
    
    def get_correlated_vulnerabilities(self,id):
        all_tables = ['references','reference_to','vulnerabilities']
        all_fields = ['references.type','references.name']
        refs = self.select_complex(all_fields,all_tables,{'vulnerabilities.id':('=',id)},Vulnerability.SCHEMA)
        
        
        all_fields = ['vulnerabilities.id']
        
        ids = []
        for dic in refs:
            conditions = {}
            conditions['vulnerabilities.id'] = ('!=',id)
            for key,value in dic.items():
                conditions[key] = ('=',str(value))
                
            res = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
            
            for each in res:
                ids.append(each)
                
        return list(sorted(set(ids)))
            
    def get_accepted_vulnerability(self,id):
	cond = {}	

	all_tables = ['vulnerabilities','source']
	all_fields = ['source.name','vulnerabilities.ori_id']
	result = self.select_complex(all_fields,all_tables,{'vulnerabilities.id':('=',id)},Vulnerability.SCHEMA)
	if result[0]['source.name'] == 'netentsec_snort':
		cond['vulnerabilities.id'] = ('=',result[0]['vulnerabilities.ori_id'])
		
	else:
		cond['vulnerabilities.ori_id'] = ('=',id)
			


	all_tables = ['vulnerabilities']
	all_fields = ['vulnerabilities.id']	

	ids = self.select_complex(all_fields,all_tables,cond,Vulnerability.SCHEMA)
    	netentsec_id = []
	if len(ids) > 0: 
		for id in ids:
			netentsec_id.append(id)
		return netentsec_id[0]
	else:
		return 0

    def insert_or_update(self,table_name,dict,identifier):
        '''the function is used to insert or update table, return the ids of the new inserted or updated lines'''
        
        # print dict
        
        conditions = {}
        
        for key,value in identifier.items():
            
            conditions[key] = (' = ',value)
            
        id = self.select(table_name,Vulnerability.SCHEMA,('id',),conditions)
        
        
        if len(id) == 0:
            inserted = self.insert(table_name,dict,Vulnerability.SCHEMA)
            if inserted:
                conditions = {}
                for key,value in dict.items():
                    conditions[key] = (' = ',value)
                    
                new_id = self.select(table_name,Vulnerability.SCHEMA,('id',),conditions)
                if len(new_id) == 1:
                    return new_id[0]
        else:
            
            if len(id) == 1:
                conditions = {table_name+'.id':('=',id[0])}
                updated = self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
                if updated:
                    return id[0]
            
        return False

    def add_new_XAI_rule(self,id,vul_obj,is_update = False):
	time_update = time.strftime('%Y-%m-%d')
	vul_id = 0
	vul_nsid = 0
	
	all_tables = ['vulnerabilities','source']
	all_fields = ['vulnerabilities.id'] 
	conditions = {}
	conditions['vulnerabilities.ori_name'] = ('=',str(eval(repr(vul_obj.ori_name))).encode('string-escape'))
	conditions['source.name'] = ('=','netentsec_XAI')
	vul_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)   
        if len(vul_id) == 0:
		dict = {}
		dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
		dict['has_rules'] = vul_obj.has_rules
		dict['exploit_path'] = vul_obj.exploit_path
		dict['sample_path'] = vul_obj.sample_path
		dict['ori_update_time'] = time_update
		dict['ori_repair_time'] = vul_obj.ori_repair_time
		dict['ori_publish_time'] = vul_obj.ori_publish_time
		dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
		dict['ch_description'] = str(eval(repr(vul_obj.ch_description))).encode('string-escape')
		dict['ori_severity'] = vul_obj.severity
		dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')
		dict['ori_id'] = 0
			
		# update origin_id
		origin_id = self.select('source',Vulnerability.SCHEMA,('id',),{'name':(' =  ','netentsec_XAI')})
		if len(origin_id) == 1:
			dict['origin_id'] = int(origin_id[0])
					
		# update ori_class_id
		all_tables = ['source','category']
		all_fields = ['category.id']
		conditions = {'source.name':('=','netentsec_XAI'),'category.category':('=',vul_obj.category)}
		class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
		#print 'category_id',class_id
		if len(class_id) == 0:
			dict1 = {}
			dict1['source_id'] = int(origin_id[0])
			dict1['category'] = vul_obj.category
			id_tmp = self.insert_or_update('category',dict1,dict1)
			dict['ori_class_id'] = id_tmp
		elif len(class_id) == 1:
			dict['ori_class_id'] = int(class_id[0])

		# update netentsec_sid
		mutex.acquire()
		time.sleep(10)
		fields = ['snort_rules.nsid']
		query = 'select max(nsid) from '+ Vulnerability.SCHEMA +'.snort_rules'
		max_nsid = self.select_raw(fields,query)
		fields = ['vulnerabilities.netentsec_sid']
		query = 'select max(netentsec_sid) from '+ Vulnerability.SCHEMA +'.vulnerabilities'
		max_netentsec_sid = self.select_raw(fields,query)
	#	print 'max_nsid',max_nsid,'max_nsid[0]',max_nsid[0],'max_netentsec_sid',max_netentsec_sid,'max_netentsec_sid[0]',max_netentsec_sid[0]
	#	print max_nsid,max_netentsec_sid,'@@@@@@@@@@@@@@@@@@@@@'
		if max_nsid[0] >= max_netentsec_sid[0]:
			vul_nsid = max_nsid[0] + 1
		else:
			vul_nsid = max_netentsec_sid[0] + 1
		while (vul_nsid == 10000001 or vul_nsid == 10000002 or vul_nsid == 10000003 or vul_nsid == 10000004):
			vul_nsid += 1
		dict['netentsec_sid'] = vul_nsid
				
        	inserted = self.insert('vulnerabilities',dict,Vulnerability.SCHEMA) ### INSERT INTO NEW 
		mutex.release()
	
		# update credit_id
 #           	dict = {}
  #          	dict['name'] = vul_obj.credit
   #         	credit_id = self.insert_or_update('credit',dict,dict)
            
          #  	if credit_id > 0:
           #     	conditions = {'vulnerabilities.id':('=',vul_id[0])}
            #    	updated = self.update('vulnerabilities',{'credit_id':credit_id},conditions,Vulnerability.SCHEMA)
		
		print '=' * 5 + ': ' + 'vulnerability is inserted' 
		new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_name':(' =  ',str(eval(repr(vul_obj.ori_name))).encode('string-escape'))})
	#	print new_vul_id
		vul_id = int(new_vul_id[0])
	else:
		vul_id = vul_id[0]
		
		n_sid =  self.select('vulnerabilities',Vulnerability.SCHEMA,('netentsec_sid',),{'ori_name':(' =  ',str(eval(repr(vul_obj.ori_name))).encode('string-escape'))})
		vul_nsid = int(n_sid[0])
			
		
	# update reference table
	ref_ids = []
        refs = vul_obj.references
        for ref in refs:
		dict = {}
            	dict['type'] = ref.type
            	dict['name'] = ref.name
        # insert into references
		id_tmp = self.insert_or_update('references',dict,dict)
            	ref_ids.append(id_tmp)
        print '=' * 5 + ': ' + 'references are inserted'
                
            
        # update credit_id
        dict = {}
        dict['name'] = vul_obj.credit
        credit_id = self.insert_or_update('credit',dict,dict)
        if credit_id > 0:
        	conditions = {'vulnerabilities.id':('=',vul_id)}
            	updated = self.update('vulnerabilities',{'credit_id':credit_id},conditions,Vulnerability.SCHEMA)
            
        print '=' * 5 + ': ' + 'vulnerability is updated' 
            
        # udpate status and result
        conditions = {'vulnerabilities.id':('=',vul_id)}
        updated = self.update('vulnerabilities',{'status_id':3},conditions,Vulnerability.SCHEMA)
        updated = self.update('vulnerabilities',{'result_id':4},conditions,Vulnerability.SCHEMA)
            
        # update owner
        owner_id = self.select('users',Vulnerability.SCHEMA,('id',),{'name':(' =  ',vul_obj.owner_name)})
        if len(owner_id) == 1:
            	conditions = {'vulnerabilities.id':('=',vul_id)}
        updated = self.update('vulnerabilities',{'owner_id':int(owner_id[0])},conditions,Vulnerability.SCHEMA)
 
	# processing rules
        conditions = {'vulnerability_id':('=',vul_id)}
        rule_ids = []
        rules = vul_obj.rules
        for rule in rules:
        	dict = {}
            	dict['content'] = str(eval(repr(rule.content))).encode('string-escape')
            	dict['protocol'] = rule.protocol
            	dict['metadata'] = rule.metadata
            	dict['sid'] = rule.sid
            	dict['gid'] = rule.gid
            	dict['revision'] = rule.revision
            	dict['deprecated'] = rule.deprecated
            	dict['flowbits'] = rule.flowbits
            	dict['from_ports'] = rule.from_ports
            	dict['to_ports'] = rule.to_ports
            	dict['is_client_to_server'] = rule.is_client_to_server
                # dict['full_content'] = str(rule.full_content).encode('string-escape')
            	dict['full_content'] = str(eval(repr(rule.full_content))).encode('string-escape')
		dict['sig_protocol'] = str(eval(repr(rule.sig_protocol))).encode('string-escape')
		dict['direction'] = str(eval(repr(rule.direction))).encode('string-escape')
		dict['host_type'] = str(eval(repr(rule.host_type))).encode('string-escape')
		dict['default_action'] = str(eval(repr(rule.default_action))).encode('string-escape')
		dict['os'] = str(eval(repr(rule.os))).encode('string-escape')
		dict['is_valid'] = rule.is_valid
		dict['engine_type'] = str(eval(repr(rule.engine_type))).encode('string-escape')
                dict['xai_type'] = rule.xai_type
 
            	dict['vulnerability_id'] = vul_id
	 	
	    	dict['is_maxversion'] = 1 
            	dict['is_update_or_insert'] = time_update

		dict['nsid'] = vul_nsid
				
		identifer = {}	
		identifer['snort_rules.sid'] = rule.sid
		identifer['snort_rules.vulnerability_id'] = vul_id

              	id_tmp = self.insert_or_update('snort_rules',dict,identifer)
		
                #id_tmp = self.insert('snort_rules',dict,Vulnerability.SCHEMA)
		rule_ids.append(id_tmp)
            
        print '=' * 5 + ': ' + 'rules are updated'
            
        # update reference_to table
        for ref_id in ref_ids:
        	dict = {}
                dict['reference_id'] = ref_id
                dict['vulnerability_id'] = vul_id
            # insert into reference_to
                ref_to_id = self.insert_or_update('reference_to',dict,dict)
                
        print '=' * 5 + ': ' + 'reference_to are inserted'
            
            # change the status of the vulnerability
            # self.complete_new_vulnerability(id)
                    
        print '=' * 5 + ': ' + 'all succeed'
            
        return vul_id
	
    def add_new_vulnerability(self,id,vul_obj,is_update = False):
	time_update = time.strftime('%Y-%m-%d')	
	vul_id = 0
	
	all_tables = ['vulnerabilities','source']
	all_fields = ['vulnerabilities.id'] 
	conditions = {}
	conditions['vulnerabilities.ori_name'] = ('=',str(eval(repr(vul_obj.ori_name))).encode('string-escape'))
	conditions['source.name'] = ('=','netentsec_snort')
	vul_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)   
        if len(vul_id) == 0:
		dict = {}
		dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
		dict['has_rules'] = vul_obj.has_rules
		dict['exploit_path'] = vul_obj.exploit_path
		dict['sample_path'] = vul_obj.sample_path
		dict['ori_update_time'] = time_update
		dict['ori_repair_time'] = vul_obj.ori_repair_time
		dict['ori_publish_time'] = vul_obj.ori_publish_time
		dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
		dict['ch_description'] = str(eval(repr(vul_obj.ch_description))).encode('string-escape')
		dict['ori_severity'] = vul_obj.severity
		dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')
		dict['ori_id'] = 0
			
		# update origin_id
		origin_id = self.select('source',Vulnerability.SCHEMA,('id',),{'name':(' =  ','netentsec_snort')})
		if len(origin_id) == 1:
			dict['origin_id'] = int(origin_id[0])
					
		# update ori_class_id
		all_tables = ['source','category']
		all_fields = ['category.id']
		conditions = {'source.name':('=','netentsec_snort'),'category.category':('=',vul_obj.category)}
		class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
		#print 'category_id',class_id
		if len(class_id) == 1:
			dict['ori_class_id'] = int(class_id[0])
				
          	inserted = self.insert('vulnerabilities',dict,Vulnerability.SCHEMA)
		print '=' * 5 + ': ' + 'vulnerability is inserted' 
		new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_name':(' =  ',str(eval(repr(vul_obj.ori_name))).encode('string-escape'))})
		print new_vul_id
		vul_id = int(new_vul_id[0])
	else:
		vul_id = vul_id[0]
			
		
	# update reference table
	ref_ids = []
        refs = vul_obj.references
        for ref in refs:
		dict = {}
            	dict['type'] = ref.type
            	dict['name'] = ref.name
        # insert into references
		id_tmp = self.insert_or_update('references',dict,dict)
            	ref_ids.append(id_tmp)
        print '=' * 5 + ': ' + 'references are inserted'
                
            
        # update credit_id
        dict = {}
        dict['name'] = vul_obj.credit
        credit_id = self.insert_or_update('credit',dict,dict)
        if credit_id > 0:
        	conditions = {'vulnerabilities.id':('=',vul_id)}
            	updated = self.update('vulnerabilities',{'credit_id':credit_id},conditions,Vulnerability.SCHEMA)
            
        print '=' * 5 + ': ' + 'vulnerability is updated' 
            
        # udpate status and result
        conditions = {'vulnerabilities.id':('=',vul_id)}
        updated = self.update('vulnerabilities',{'status_id':3},conditions,Vulnerability.SCHEMA)
        updated = self.update('vulnerabilities',{'result_id':4},conditions,Vulnerability.SCHEMA)
            
        # update owner
        owner_id = self.select('users',Vulnerability.SCHEMA,('id',),{'name':(' =  ',vul_obj.owner_name)})
        if len(owner_id) == 1:
            	conditions = {'vulnerabilities.id':('=',vul_id)}
        updated = self.update('vulnerabilities',{'owner_id':int(owner_id[0])},conditions,Vulnerability.SCHEMA)
 
	# processing rules
        conditions = {'vulnerability_id':('=',vul_id)}
        rule_ids = []
        rules = vul_obj.rules
        for rule in rules:
        	dict = {}
            	dict['content'] = str(eval(repr(rule.content))).encode('string-escape')
            	dict['protocol'] = rule.protocol
            	dict['metadata'] = rule.metadata
            	dict['sid'] = rule.sid
            	dict['gid'] = rule.gid
            	dict['revision'] = rule.revision
            	dict['deprecated'] = rule.deprecated
            	dict['flowbits'] = rule.flowbits
            	dict['from_ports'] = rule.from_ports
            	dict['to_ports'] = rule.to_ports
            	dict['is_client_to_server'] = rule.is_client_to_server
                # dict['full_content'] = str(rule.full_content).encode('string-escape')
            	dict['full_content'] = str(eval(repr(rule.full_content))).encode('string-escape')
                
            	dict['vulnerability_id'] = vul_id
	 	
	    	dict['is_maxversion'] = 1 
            	dict['is_update_or_insert'] = time_update

				
            	tables = ['source','vulnerabilities','snort_rules']
	    	fields = ['snort_rules.nsid']
	    	cond = {'snort_rules.sid':('=',rule.sid),'snort_rules.vulnerability_id':('=',vul_id)}
		result = self.select_complex(fields,tables,cond,Vulnerability.SCHEMA)
		print result,'nsid***'*10,len(result)
		mutex.acquire()
		if len(result) == 0 or result[0] == 0:
			query = 'select max(nsid) from '+ Vulnerability.SCHEMA +'.snort_rules'
			max_nsid = self.select_raw(fields,query)
	#		print 'max_nsid',max_nsid,'max_nsid[0]',max_nsid[0]
			pre_nsid = max_nsid[0] + 1
			while (pre_nsid == 10000001 or pre_nsid == 10000002 or pre_nsid == 10000003 or pre_nsid == 10000004):
				pre_nsid += 1
			dict['nsid'] = pre_nsid
		else:
			pass
		identifer = {}	
		identifer['snort_rules.sid'] = rule.sid
		identifer['snort_rules.vulnerability_id'] = vul_id

              	id_tmp = self.insert_or_update('snort_rules',dict,identifer)
		mutex.release()
                #id_tmp = self.insert('snort_rules',dict,Vulnerability.SCHEMA)
		rule_ids.append(id_tmp)
            
        print '=' * 5 + ': ' + 'rules are updated'
            
        # update reference_to table
        for ref_id in ref_ids:
        	dict = {}
                dict['reference_id'] = ref_id
                dict['vulnerability_id'] = vul_id
            # insert into reference_to
                ref_to_id = self.insert_or_update('reference_to',dict,dict)
                
        print '=' * 5 + ': ' + 'reference_to are inserted'
            
            # change the status of the vulnerability
            # self.complete_new_vulnerability(id)
                    
        print '=' * 5 + ': ' + 'all succeed'
	
	return vul_id

    def confirm_new_vulnerability(self,id,vul_obj,is_update = False):
	    time_update = time.strftime('%Y-%m-%d')	
	    is_exist = False
	    vul_id = 0

	    try:
           	print '=' * 5 + ': ' + 'begin check if the vulnerability is existed' 
		
            #judge where the vulnerability come from netentsec_snort or other source
		
	        all_tables = ['source','vulnerabilities']
	        all_fields = ['source.name']
	        conditions = {}
	        conditions['vulnerabilities.id'] = ('=',id) 
	        vul_source = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
	#        print vul_source[0],'*#'*20
	        if vul_source[0] == 'netentsec_snort' :
		    dict = {}
        	    dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
           	    dict['has_rules'] = vul_obj.has_rules
          	    dict['exploit_path'] = vul_obj.exploit_path
            	    dict['sample_path'] = vul_obj.sample_path
           	    dict['ori_update_time'] = time_update
         	    dict['ori_repair_time'] = vul_obj.ori_repair_time
            	    dict['ori_publish_time'] = vul_obj.ori_publish_time
            	    dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
		    dict['ch_description'] = str(eval(repr(vul_obj.ch_description))).encode('string-escape')
            	    dict['ori_severity'] = vul_obj.severity
            	    dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		    dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')		    
	
		    cond={'vulnerabilities.id': ('=',id)}
            	    updated = self.update('vulnerabilities',dict,cond,Vulnerability.SCHEMA)
	    	    print '=' * 5 + ': ' + 'vulnerabilities are updated'
			
			        # update ori_class_id
			
		    all_tables = ['source','category']
                    all_fields = ['category.id']
					
		    conditions = {'source.name':('=','netentsec_snort'),'category.category':('=',vul_obj.category)}
            	    class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
         #   	    print 'category_id',class_id
					
            	    if len(class_id) == 1:
                    	conditions = {'vulnerabilities.id':('=',id)}
                    	updated = self.update('vulnerabilities',{'ori_class_id':int(class_id[0])},conditions,Vulnerability.SCHEMA)
                	print '=' * 5 + ': ' + 'class are inserted'
				
		    vul_id = id

	        else:
				
		        all_tables = ['source','vulnerabilities']
		        all_fields = ['vulnerabilities.id']
		        conditions = {'source.name':('=','netentsec_snort')}
			
		       # vul_name = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		       # if not vul_name == None and len(vul_name) > 0:
			conditions['vulnerabilities.ori_id'] = ('=',id)      
				# judge if the vulnerability has been existed by the name of it
			result = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
			
	#		print result,'ori_id'*20
            		if len(result) > 0: # is existed already
                		is_exist = True
                		print '=' * 5 + ': ' + 'the vulnerability is existed' 
            		else:
                		print '=' * 5 + ': ' + 'the vulnerability isn\'t existed'

		        if not is_update:
			        return is_exist
                
		        if is_exist == False:
			        dict = {}
			        dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
			        dict['has_rules'] = vul_obj.has_rules
			        dict['exploit_path'] = vul_obj.exploit_path
			        dict['sample_path'] = vul_obj.sample_path
			        dict['ori_update_time'] = time_update
			        dict['ori_repair_time'] = vul_obj.ori_repair_time
			        dict['ori_publish_time'] = vul_obj.ori_publish_time
			        dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
			        dict['ch_description']=str(eval(repr(vul_obj.ch_description))).encode('string-escape')
				dict['ori_severity'] = vul_obj.severity
			        dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
				dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')
			        dict['ori_id'] = int(id)

			        # update origin_id
			        origin_id = self.select('source',Vulnerability.SCHEMA,('id',),{'name':(' =  ','netentsec_snort')})
			        if len(origin_id) == 1:
				        dict['origin_id'] = int(origin_id[0])
					
			
				        # update ori_class_id
				
			        all_tables = ['source','category']
			        all_fields = ['category.id']
			        conditions = {'source.name':('=','netentsec_snort'),'category.category':('=',vul_obj.category)}
			        class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
	#	    	    	print 'category_id',class_id
			        if len(class_id) == 1:
				        dict['ori_class_id'] = int(class_id[0])
				
                		inserted = self.insert('vulnerabilities',dict,Vulnerability.SCHEMA)
			        print '=' * 5 + ': ' + 'vulnerability is inserted' 
				
			        new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_id':(' =  ',int(id))})
			        vul_id = int(new_vul_id[0])
				
		        else :   # is_exist == True
            
			        dict = {}
			        dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
			        dict['has_rules'] = vul_obj.has_rules
			        dict['exploit_path'] = vul_obj.exploit_path
			        dict['sample_path'] = vul_obj.sample_path
			        dict['ori_update_time'] = time_update
			        dict['ori_repair_time'] = vul_obj.ori_repair_time
			        dict['ori_publish_time'] = vul_obj.ori_publish_time
			        #dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
			        #dict['ori_severity'] = vul_obj.severity
			        #dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
				
			        cond={'vulnerabilities.ori_id': ('=',id)}
			        updated = self.update('vulnerabilities',dict,cond,Vulnerability.SCHEMA)
			        print '=' * 5 + ': ' + 'vulnerabilities are updated'
				
			        new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_id':(' =  ',int(id))})
			        vul_id = int(new_vul_id[0])
            
		# update reference table
            	ref_ids = []
            	refs = vul_obj.references
            	for ref in refs:
                	dict = {}
                	dict['type'] = ref.type
                	dict['name'] = ref.name
                # insert into references
                	id_tmp = self.insert_or_update('references',dict,dict)
                	ref_ids.append(id_tmp)
            	print '=' * 5 + ': ' + 'references are inserted'
                
            
            # update credit_id
            	dict = {}
            	dict['name'] = vul_obj.credit
            	credit_id = self.insert_or_update('credit',dict,dict)
            
            	if credit_id > 0:
                	conditions = {'vulnerabilities.id':('=',vul_id)}
                	updated = self.update('vulnerabilities',{'credit_id':credit_id},conditions,Vulnerability.SCHEMA)
            
            
            	print '=' * 5 + ': ' + 'vulnerability is updated' 
            
            
            # udpate status and result
            	conditions = {'vulnerabilities.id':('=',vul_id)}
            	updated = self.update('vulnerabilities',{'status_id':3},conditions,Vulnerability.SCHEMA)
            	updated = self.update('vulnerabilities',{'result_id':4},conditions,Vulnerability.SCHEMA)
            
            
            # update owner
            	owner_id = self.select('users',Vulnerability.SCHEMA,('id',),{'name':(' =  ',vul_obj.owner_name)})
                        
            	if len(owner_id) == 1:
                	conditions = {'vulnerabilities.id':('=',vul_id)}
                	updated = self.update('vulnerabilities',{'owner_id':int(owner_id[0])},conditions,Vulnerability.SCHEMA)
            

            # processing rules

           	conditions = {'vulnerability_id':('=',vul_id)}
            
#            self.delete('snort_rules',conditions,Vulnerability.SCHEMA)
#                mutex = threading.Lock()
            	rule_ids = []
            	rules = vul_obj.rules
            	for rule in rules:
                	dict = {}
                	dict['content'] = str(eval(repr(rule.content))).encode('string-escape')
                	dict['protocol'] = rule.protocol
                	dict['metadata'] = rule.metadata
                	dict['sid'] = rule.sid
                	dict['gid'] = rule.gid
                	dict['revision'] = rule.revision
                	dict['deprecated'] = rule.deprecated
                	dict['flowbits'] = rule.flowbits
                	dict['from_ports'] = rule.from_ports
                	dict['to_ports'] = rule.to_ports
                	dict['is_client_to_server'] = rule.is_client_to_server
                # dict['full_content'] = str(rule.full_content).encode('string-escape')
                	dict['full_content'] = str(eval(repr(rule.full_content))).encode('string-escape')
                
                	dict['vulnerability_id'] = vul_id
	 	
		        dict['is_maxversion'] = 1 
                	dict['is_update_or_insert'] = time_update
	#	        print '*' * 50
	#	        print "CCC",repr(rule.full_content)

        #        	print dict['full_content']
				
                # insert into rules
				
               		tables = ['source','vulnerabilities','snort_rules']
		        fields = ['snort_rules.nsid']
		        cond = {'snort_rules.sid':('=',rule.sid),'snort_rules.vulnerability_id':('=',vul_id)}
		        result = self.select_complex(fields,tables,cond,Vulnerability.SCHEMA)
	#		print result,'nsid***'*10
			mutex.acquire()
		        if len(result) == 0 or result[0] == 0:
	#			mutex.acquire()
			        query = 'select max(nsid) from '+ Vulnerability.SCHEMA +'.snort_rules'
			        max_nsid = self.select_raw(fields,query)
	#		        print 'max_nsid',max_nsid,'max_nsid[0]',max_nsid[0]
			        pre_nsid = max_nsid[0] + 1
			        while (pre_nsid == 10000001 or pre_nsid == 10000002 or pre_nsid == 10000003 or pre_nsid == 10000004):
				    pre_nsid += 1
			        dict['nsid'] = pre_nsid
		        else:
			        pass
		        identifer = {}	
		        identifer['snort_rules.sid'] = rule.sid
		        identifer['snort_rules.vulnerability_id'] = vul_id

                	id_tmp = self.insert_or_update('snort_rules',dict,identifer)
			mutex.release()
                #id_tmp = self.insert('snort_rules',dict,Vulnerability.SCHEMA)
		        rule_ids.append(id_tmp)
            
                print '=' * 5 + ': ' + 'rules are inserted'
            
            # update reference_to table
            	for ref_id in ref_ids:
                	dict = {}
                	dict['reference_id'] = ref_id
                	dict['vulnerability_id'] = vul_id
                                
                                
                # insert into reference_to
                	ref_to_id = self.insert_or_update('reference_to',dict,dict)
                
            	print '=' * 5 + ': ' + 'reference_to are inserted'
            
            # change the status of the vulnerability
            # self.complete_new_vulnerability(id)
                    
            	print '=' * 5 + ': ' + 'status are updated,all succeed'
                    
            	return {'succeed':True}
            except:
            	print traceback.print_exc()
            	print sys.exc_info() 
            	return {'succeed':False}
            
            
    
    def complete_new_vulnerability(self,id):
        
        
        all_tables = ['source','vulnerabilities']
        all_fields = ['source.name']
        
        # append the selective condition
        conditions = {'vulnerabilities.id':('=',id)}
            
        result = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
        
        if len(result) > 0:
            table_name = 'vulnerabilities'
            dict = {'status_id':3,'result_id':4}
            conditions = {'vulnerabilities.id':('=',id)}
            return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
            
        else:
            table_name = 'vulnerabilities'
            dict = {'status_id':5,'result_id':4}
            conditions = {'vulnerabilities.id':('=',id)}
            return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
    

    def confirm_new_XAI_vulnerability(self,id,vul_obj,is_update = False):

	    time_update = time.strftime('%Y-%m-%d')	
	    is_exist = False
	    vul_id = 0
	    vul_nsid = 0
	    try:
           	print '=' * 5 + ': ' + 'begin check if the vulnerability is existed' 
		
            #judge where the vulnerability come from netentsec_snort or other source
		
	        all_tables = ['source','vulnerabilities']
	        all_fields = ['source.name','source.id']
	        conditions = {}
	        conditions['vulnerabilities.id'] = ('=',id) 
	        vul_source = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
	        print vul_source,'*#'*20
	        if vul_source[0]['source.name'] == 'netentsec_XAI':
		    dict = {}
        	    dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
           	    dict['has_rules'] = vul_obj.has_rules
          	    dict['exploit_path'] = vul_obj.exploit_path
            	    dict['sample_path'] = vul_obj.sample_path
           	    dict['ori_update_time'] = time_update
         	    dict['ori_repair_time'] = vul_obj.ori_repair_time
            	    dict['ori_publish_time'] = vul_obj.ori_publish_time
            	    dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
		    dict['ch_description'] = str(eval(repr(vul_obj.ch_description))).encode('string-escape')
            	    dict['ori_severity'] = vul_obj.severity
            	    dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		    dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')
				
		    cond={'vulnerabilities.id': ('=',id)}
            	    updated = self.update('vulnerabilities',dict,cond,Vulnerability.SCHEMA)
	    	    print '=' * 5 + ': ' + 'vulnerabilities are updated'
			
			        # update ori_class_id
			
		    all_tables = ['source','category']
                    all_fields = ['category.id']
					
		    conditions = {'source.name':('=','netentsec_XAI'),'category.category':('=',vul_obj.category)}
            	    class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
         #   	    print 'category_id',class_id
		    if len(class_id) == 0:
			dict1 = {}                                                                            
                        dict1['source_id'] = int(vul_source[0]['source.id'])                                                
                        dict1['category'] = vul_obj.category                                                  
                        id_tmp = self.insert_or_update('category',dict1,dict1)
			conditions = {'vulnerabilities.id':('=',id)}
                    	updated = self.update('vulnerabilities',{'ori_class_id':int(id_tmp)},conditions,Vulnerability.SCHEMA)						
            	    elif len(class_id) == 1:
                    	conditions = {'vulnerabilities.id':('=',id)}
                    	updated = self.update('vulnerabilities',{'ori_class_id':int(class_id[0])},conditions,Vulnerability.SCHEMA)
                	print '=' * 5 + ': ' + 'class are inserted'

		    fields = ['vulnerabilities.netentsec_sid']
                    query = 'select netentsec_sid from '+ Vulnerability.SCHEMA +'.vulnerabilities where id = %d' % int(id)
                    netentsec_sid = self.select_raw(fields,query)			
		    vul_nsid =netentsec_sid[0] 	
		    vul_id = id

	        else:
				
		        all_tables = ['source','vulnerabilities']
		        all_fields = ['vulnerabilities.id']
		        conditions = {'source.name':('=','netentsec_XAI')}
			
		       # vul_name = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
		       # if not vul_name == None and len(vul_name) > 0:
			conditions['vulnerabilities.ori_id'] = ('=',id)      
				# judge if the vulnerability has been existed by the name of it
			result = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
			
	#		print result,'ori_id'*20
            		if len(result) > 0: # is existed already
                		is_exist = True
                		print '=' * 5 + ': ' + 'the vulnerability is existed' 
            		else:
                		print '=' * 5 + ': ' + 'the vulnerability isn\'t existed'

		        if not is_update:
			        return is_exist
                
		        if is_exist == False:
			        dict = {}
			        dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
			        dict['has_rules'] = vul_obj.has_rules
			        dict['exploit_path'] = vul_obj.exploit_path
			        dict['sample_path'] = vul_obj.sample_path
			        dict['ori_update_time'] = time_update
			        dict['ori_repair_time'] = vul_obj.ori_repair_time
			        dict['ori_publish_time'] = vul_obj.ori_publish_time
			        dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
				dict['ch_description']=str(eval(repr(vul_obj.ch_description))).encode('string-escape')
			        dict['ori_severity'] = vul_obj.severity
			        dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
				dict['ch_name'] = str(eval(repr(vul_obj.ch_name))).encode('string-escape')
			        dict['ori_id'] = int(id)

			        # update origin_id
			        origin_id = self.select('source',Vulnerability.SCHEMA,('id',),{'name':(' =  ','netentsec_XAI')})
			        if len(origin_id) == 1:
				        dict['origin_id'] = int(origin_id[0])
					
			
				        # update ori_class_id
				
			        all_tables = ['source','category']
			        all_fields = ['category.id']
			        conditions = {'source.name':('=','netentsec_XAI'),'category.category':('=',vul_obj.category)}
			        class_id = self.select_complex(all_fields,all_tables,conditions,Vulnerability.SCHEMA)
	#	    	    	print 'category_id',class_id
				if len(class_id) == 0:
					dict1 = {}                                                                            
                        		dict1['source_id'] = int(vul_source[0]['source.id'])
         				dict1['category'] = vul_obj.category                                                  
                        		id_tmp = self.insert_or_update('category',dict1,dict1)
					dict['ori_class_id'] = int(id_tmp)
			        elif len(class_id) == 1:
				        dict['ori_class_id'] = int(class_id[0])
						
				#  update netentsec_sid

				mutex.acquire()
				fields = ['snort_rules.nsid']
				query = 'select max(nsid) from '+ Vulnerability.SCHEMA +'.snort_rules'
				max_nsid = self.select_raw(fields,query)
				fields = ['vulnerabilities.netentsec_sid']
				query = 'select max(netentsec_sid) from '+ Vulnerability.SCHEMA +'.vulnerabilities'
				max_netentsec_sid = self.select_raw(fields,query)
				if max_nsid[0] >= max_netentsec_sid[0]:
					vul_nsid = max_nsid[0] + 1
				else:
					vul_nsid = max_netentsec_sid[0] + 1
				while (vul_nsid == 10000001 or vul_nsid == 10000002 or vul_nsid == 10000003 or vul_nsid == 10000004):
					vul_nsid += 1
				dict['netentsec_sid'] = vul_nsid	
				
                		inserted = self.insert('vulnerabilities',dict,Vulnerability.SCHEMA)
			        print '=' * 5 + ': ' + 'vulnerability is inserted' 
				mutex.release()

			        new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_id':(' =  ',int(id))})
			        vul_id = int(new_vul_id[0])
				
		        else :   # is_exist == True
            
			        dict = {}
			        dict['remarks'] = str(eval(repr(vul_obj.remarks))).encode('string-escape')
			        dict['has_rules'] = vul_obj.has_rules
			        dict['exploit_path'] = vul_obj.exploit_path
			        dict['sample_path'] = vul_obj.sample_path
			        dict['ori_update_time'] = time_update
			        dict['ori_repair_time'] = vul_obj.ori_repair_time
			        dict['ori_publish_time'] = vul_obj.ori_publish_time
			        #dict['ori_description'] = str(eval(repr(vul_obj.ori_description))).encode('string-escape')
			        #dict['ori_severity'] = vul_obj.severity
			        #dict['ori_name'] = str(eval(repr(vul_obj.ori_name))).encode('string-escape')
				
			        cond={'vulnerabilities.ori_id': ('=',id)}
			        updated = self.update('vulnerabilities',dict,cond,Vulnerability.SCHEMA)
			        print '=' * 5 + ': ' + 'vulnerabilities are updated'
				
			        new_vul_id =  self.select('vulnerabilities',Vulnerability.SCHEMA,('id',),{'ori_id':(' =  ',int(id))})
				fields = ['vulnerabilities.netentsec_sid']                                                
                    		query = 'select netentsec_sid from '+ Vulnerability.SCHEMA +'.vulnerabilities where id = %d'% int(id)
                    		netentsec_sid = self.select_raw(fields,query)                                             
                    		vul_nsid =netentsec_sid[0]

			        vul_id = int(new_vul_id[0])
            
		# update reference table
            	ref_ids = []
            	refs = vul_obj.references
            	for ref in refs:
                	dict = {}
                	dict['type'] = ref.type
                	dict['name'] = ref.name
                # insert into references
                	id_tmp = self.insert_or_update('references',dict,dict)
                	ref_ids.append(id_tmp)
            	print '=' * 5 + ': ' + 'references are inserted'
                
            
            # update credit_id
            	dict = {}
            	dict['name'] = vul_obj.credit
            	credit_id = self.insert_or_update('credit',dict,dict)
            
            	if credit_id > 0:
                	conditions = {'vulnerabilities.id':('=',vul_id)}
                	updated = self.update('vulnerabilities',{'credit_id':credit_id},conditions,Vulnerability.SCHEMA)
            
            
            	print '=' * 5 + ': ' + 'vulnerability is updated' 
            
            
            # udpate status and result
            	conditions = {'vulnerabilities.id':('=',vul_id)}
            	updated = self.update('vulnerabilities',{'status_id':3},conditions,Vulnerability.SCHEMA)
            	updated = self.update('vulnerabilities',{'result_id':4},conditions,Vulnerability.SCHEMA)
            
            
            # update owner
            	owner_id = self.select('users',Vulnerability.SCHEMA,('id',),{'name':(' =  ',vul_obj.owner_name)})
                        
            	if len(owner_id) == 1:
                	conditions = {'vulnerabilities.id':('=',vul_id)}
                	updated = self.update('vulnerabilities',{'owner_id':int(owner_id[0])},conditions,Vulnerability.SCHEMA)
            

            # processing rules

           	conditions = {'vulnerability_id':('=',vul_id)}
            
#            self.delete('snort_rules',conditions,Vulnerability.SCHEMA)
#                mutex = threading.Lock()
            	rule_ids = []
            	rules = vul_obj.rules
            	for rule in rules:
                	dict = {}
                	dict['content'] = str(eval(repr(rule.content))).encode('string-escape')
                	dict['protocol'] = rule.protocol
                	dict['metadata'] = rule.metadata
                	dict['sid'] = rule.sid
                	dict['gid'] = rule.gid
                	dict['revision'] = rule.revision
                	dict['deprecated'] = rule.deprecated
                	dict['flowbits'] = rule.flowbits
                	dict['from_ports'] = rule.from_ports
                	dict['to_ports'] = rule.to_ports
                	dict['is_client_to_server'] = rule.is_client_to_server
                # dict['full_content'] = str(rule.full_content).encode('string-escape')
                	dict['full_content'] = str(eval(repr(rule.full_content))).encode('string-escape')
                	dict['sig_protocol'] = str(eval(repr(rule.sig_protocol))).encode('string-escape')
			dict['direction'] = str(eval(repr(rule.direction))).encode('string-escape')
			dict['host_type'] = str(eval(repr(rule.host_type))).encode('string-escape')
			dict['default_action'] = str(eval(repr(rule.default_action))).encode('string-escape')
			dict['os'] = str(eval(repr(rule.os))).encode('string-escape')
			dict['is_valid'] = rule.is_valid
			dict['engine_type'] = str(eval(repr(rule.engine_type))).encode('string-escape')
			dict['xai_type'] = rule.xai_type
                	dict['vulnerability_id'] = vul_id
	 	
		        dict['is_maxversion'] = 1 
                	dict['is_update_or_insert'] = time_update

			dict['nsid'] = vul_nsid
                # insert into rules
				
              
		        identifer = {}	
		        identifer['snort_rules.sid'] = rule.sid
		        identifer['snort_rules.vulnerability_id'] = vul_id

                	id_tmp = self.insert_or_update('snort_rules',dict,identifer)
			
                #id_tmp = self.insert('snort_rules',dict,Vulnerability.SCHEMA)
		        rule_ids.append(id_tmp)
            
                print '=' * 5 + ': ' + 'rules are inserted'
            
            # update reference_to table
            	for ref_id in ref_ids:
                	dict = {}
                	dict['reference_id'] = ref_id
                	dict['vulnerability_id'] = vul_id
                                
                                
                # insert into reference_to
                	ref_to_id = self.insert_or_update('reference_to',dict,dict)
                
            	print '=' * 5 + ': ' + 'reference_to are inserted'
            
            # change the status of the vulnerability
            # self.complete_new_vulnerability(id)
                    
            	print '=' * 5 + ': ' + 'status are updated,all succeed'
                    
            	return {'succeed':True}
            except:
            	print traceback.print_exc()
            	print sys.exc_info() 
            	return {'succeed':False}
	
 
    def reject_new_vulnerability(self,id):
        table_name = 'vulnerabilities'
        dict = {'status_id':3,'result_id':3}
        conditions = {'vulnerabilities.id':('=',id)}
        return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
        
    
    def postpone_new_vulnerability(self,id):
        table_name = 'vulnerabilities'
        dict = {'status_id':3,'result_id':2}
        conditions = {'vulnerabilities.id':('=',id)}
        return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
    
        
    
    
    # functions for check
    def accept(self,id):
        table_name = 'vulnerabilities'
        dict = {'status_id':4}
        conditions = {'vulnerabilities.id':('=',id)}

	col_names = ['ori_id']
	ori_id = self.select(table_name,Vulnerability.SCHEMA,col_names,conditions)
	if ori_id[0] > 0 :
		conditions_ori = {'vulnerabilities.id':('=',ori_id[0])}
		self.update(table_name,dict,conditions_ori,Vulnerability.SCHEMA)
	else:
		pass
        return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
        
    
    
    def decline(self,id):
        table_name = 'vulnerabilities'
        dict = {'status_id':2}
        conditions = {'vulnerabilities.id':('=',id)}

        col_names = ['ori_id']
        ori_id = self.select(table_name,Vulnerability.SCHEMA,col_names,conditions)
	dict_ori = {'status_id':4}
        if ori_id[0] > 0 :
                conditions_ori = {'vulnerabilities.id':('=',ori_id[0])}
                self.update(table_name,dict_ori,conditions_ori,Vulnerability.SCHEMA)
        else:
                pass
        return self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
        
    
    def insert_snort_category(self,file_name,source_name):
        
        file = open(file_name)
        lines = file.readlines()
        
        origin_id = self.select('source',Vulnerability.SCHEMA,('id',),{'name':(' =  ',str(source_name))})
        print "source_id",origin_id

        
        for line in lines:
            fields = line.strip().split(',')
            
            if len(fields) ==  3:
                name = fields[0]
                description = fields[1]
                severity = fields[2]
                
                
                '''
                dict = {}
                dict['category'] = name
                dict['source_id'] = origin_id[0]
                           
                table_name = 'category'         
                category_id = self.insert_or_update(table_name,dict,dict)
                
                
                # update other infomation
                dict = {}
                dict = {'description':description,'source_id':origin_id[0]}
                conditions = {'category.id':('=',category_id)}
                self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
                
                # update the vulnerabilities severity
                dict = {}
                dict = {'ori_severity':severity}
                table_name = 'vulnerabilities' 
                conditions = {'vulnerabilities.ori_class_id':('=',category_id)}
                self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
                
                # print name,description,severity
                '''
                
                
                
                # update the vulnerabilities severity
                dict = {}
                dict = {'ori_severity':severity}
                table_name = 'vulnerabilities' 
                conditions = {'vulnerabilities.ori_scenario':('=',name)}
                self.update(table_name,dict,conditions,Vulnerability.SCHEMA)
                
                
                
            else:
                print fields
        
        
            
            
    
    # used for debug
    def show(self,list):
        
        print len(list)
        
        if list != None and len(list) > 0:
            for row in list:
                print row
    

if __name__ == '__main__':
    
    print sys.getdefaultencoding()
        
    db = Database('vulnerability','postgres')
    print sys.getdefaultencoding()
    
    cond = {}
    order_by = []
    cond['references.name'] = ('=','2013-0156')
    cond['snort_rules.sid'] = ('=','17425')
    data = []
#    print data
	
    '''
    order = OrderBy('id','asc')
    orders = []
    orders.append(order)
    db.show(db.select('vulnerabilities',Vulnerability.SCHEMA,('id','ori_name'),{'id':(' < ',100)},orders))
    '''
    
    # db.insert_snort_category('/home/jk_jia/classification.txt','snort')
    
    
    
    # db.show(db.select('status',Vulnerability.SCHEMA,('name',)))
    
    # db.show(db.get_role('admin','admin'))
    
    # db.show(db.get_severity())
    
    # db.show(db.get_users())
    
    # db.show(db.get_source())
    
    # db.show(db.get_netentsec_category())
    
    #db.show(db.get_status())
    
    #db.show(db.get_credit())
    
    #db.show(db.get_result())
    
    
    # db.show(db.get_vulnerability_list())
    
    # db.get_vulnerability_list({'snort_rules.is_client_to_server':('=',-1)})
    
    # db.get_vulnerability_list()
    
    # db.assign_vulnerabilities('user',[3,4,5])

####    db.show(db.get_reference(1))
    
    # db.show(db.get_rule(1))
   
    # db.show(db.get_vulnerable(1))
    
    # db.get_correlated_vulnerabilities(1)
    
    
    
    # vul = Vulnerability()
    # db.confirm_new_vulnerability(1,vul,True)
    
    # db.complete_new_vulnerability(1)
    
    # db.show(db.select_complex(fields,tables,{'source.name':('=','snort'),},Vulnerability.SCHEMA))
    
    # db.show(db.get_vulnerability_list({'source':('=','snort'),'category':('=','web-application-activity'),'status':('=','待处理'),'publish_time_before':('<','2012-01-01'),'publish_time_after':('>=','1970-01-01'),'has_sample':('=','f'),'has_rules':('=','t')}))
    
    

        
        
    
    
