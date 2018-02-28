import csv
import math
import sqlparse
import more_itertools
#met=raw_input('Enter the metadata file: ')
metadata = open('./files/metadata.txt')
db_list=[]
temp=[]
table_list=dict()
tables=[None]*10
csvfile=[None]*10
tl=[]
join_table=list()
join_index=dict()
t_index=0
b='<begin_table>'
e='<end_table>'
t='table'
for line in metadata:
	line=line.strip()
	if b in line:
		continue
	if e in line:
		continue
	if t in line:
		tl.append(line)
	db_list.append(line)
tl.append('none')

table_list[tl[0]]=[]
ind=0
for index, item in enumerate(db_list):
	if item==tl[ind]:
		k=ind
		ind=ind+1
		temp=[]
		continue
	if item!=tl[ind]:
		temp.append(item)
	table_list[tl[k]]=temp
table_list[tl[k]]=temp

csvfile[0]=open('./files/table1.csv','rb')
tables[t_index]=csv.reader(csvfile[0])
t_index=t_index+1
csvfile[1]=open('./files/table2.csv','rb')
tables[t_index]=csv.reader(csvfile[1])
t_index=t_index+1

for itr in range(t_index):
	csvfile[itr].seek(0)
query=raw_input('sql_query> ')
query_parsed=sqlparse.parse(query)
query_parsed=query_parsed[0]
query_token=query_parsed.tokens

if str(query_token[0]) != "select":
	print str(query_token[0])
	print "I cant recoginze what you want. you are not selecting anything :/"
	exit()


if len(query_token)<7:
	print "Error: Something is missing. Please type the whole command :/"
	exit()
Table=str(query_token[6])
flag=0
i=0
for tab in tl:
	if Table==tab:
		flag=1
		break
	i=i+1
if flag==0:
	print "Error: Couldnt find the table, sorry :("
	exit()

#for itr_i in range(len(query_token)):
#	print itr_i,str(query_token[itr_i])
columns=list()

for itr in range(t_index):
	csvfile[itr].seek(0)
k=0
ind_arr=list()
for p in tables[0]:
	for q in tables[1]:
		col_t=[0]*10
		tmp_t=[]
		for ind_p in p:
			tmp_t.append(ind_p)
			col_t[1]=col_t[1]+1
		for ind_q in q:
			col_t[2]=col_t[2]+1
			tmp_t.append(ind_q)
		join_table.append(tmp_t)		
	csvfile[1].seek(0)
for itr in range(t_index):
	csvfile[itr].seek(0)
#print join_table
#print
n_table=[]
#print col_t1, col_t2
# select * from table
if str(query_token[2]) == '*':
	print "<",
	for a in table_list:
		if a==Table:
			flag=1
			print "%s.%s" % (a,table_list[a][0]),
			for col in enumerate(table_list[a][1:]):
				print ", %s.%s" %(a,col[1]),
	print ">"
	print
	for x in tables[i]:
		print x
	for itr in range(t_index):
		csvfile[itr].seek(0)
#distinct columns
elif 'distinct' in str(query_token[2]):
	ind_d=list()
	col_dis=str(query_token[2])
	col_d=table_list[Table]
	for i_d, cols in enumerate(col_d):
		if cols in col_dis:
			ind_d.append(i_d)
			break
		else: 
			print "Error: cant find column :O" 
			exit()
	print "<",
	print "%s.%s" % (Table,table_list[Table][ind_d[0]]),
	if len(ind_d)>1:
		for col in enumerate(table_list[Table][ind_d[1]:]):
			print ", %s.%s" %(Table,col[1]),
	print ">"
	#not going into the tables[i] loop for the second time
	for l in ind_d:
		tmp=list()
		for x in tables[i]:
			tmp.append(x[l]);
		lst=list(more_itertools.unique_everseen(tmp))
		print lst
		for itr in range(t_index):
			csvfile[itr].seek(0)


#aggregate functions
elif 'sum' in str(query_token[2]):
	sum_x=0
	sum_str=str(query_token[2])
	col_s=table_list[Table]
	for i_s,cols in enumerate(col_s):
		if cols in sum_str:
			ind_s=i_s
			break
	for x in tables[i]:
		sum_x=sum_x+int(x[ind_s])
	for itr in range(t_index):
		csvfile[itr].seek(0)
	print sum_x

elif 'max' in str(query_token[2]):
	max_x=0
	max_str=str(query_token[2])
	col_s=table_list[Table]
	for i_s,cols in enumerate(col_s):
		if cols in max_str:
			ind_s=i_s
			break
		else:
			print "Error: cant find columns :O" 
			exit()
	for x in tables[i]:
		if max_x<=int(x[ind_s]):
			max_x=int(x[ind_s])
	for itr in range(t_index):
		csvfile[itr].seek(0)
	print max_x

elif 'min' in str(query_token[2]):
	min_x=100000
	min_str=str(query_token[2])
	col_s=table_list[Table]
	for i_s,cols in enumerate(col_s):
		if cols in min_str:
			ind_s=i_s
			break
		else: 
			print "Error: cant find columns :O" 
			exit()
	for x in tables[i]:
		if min_x>=int(x[ind_s]):
			min_x=int(x[ind_s])
	for itr in range(t_index):
		csvfile[itr].seek(0)
	print min_x

elif 'avg' in str(query_token[2]):
	sum_x=0
	cnt=0
	sum_str=str(query_token[2])
	col_s=table_list[Table]
	for i_s,cols in enumerate(col_s):
		if cols in sum_str:
			ind_s=i_s
			break
	for x in tables[i]:
		sum_x=sum_x+int(x[ind_s])
		cnt=cnt+1
	for itr in range(t_index):
		csvfile[itr].seek(0)
	print float(sum_x)/float(cnt)

#select col1,col2 from table
elif str(query_token[2]) in table_list[Table]:
	for l in query_token[2]:
		columns.append(str(l))
	for index,b in enumerate(table_list[Table]):
		for c in columns:
			if b==c:
				ind_arr.append(index)
	print "<",
	print "%s.%s" % (Table,table_list[Table][ind_arr[0]]),
	if len(ind_arr)>1:
		for col in enumerate(table_list[Table][ind_arr[1]:]):
			print ", %s.%s" %(Table,col[1]),

	print ">"
	print 
	for x in tables[i]:
		for j in ind_arr:
			print x[j],
		print
	for itr in range(t_index):
		csvfile[itr].seek(0)

elif 'where' in str(query_token[8]):
	ind_list=[]
	col_ind=[]
	for itr_j in range(len(tl)):
		if tl[itr_j] in Table:
			n_table.append(tl[itr_j])
			#print tl[itr_j]
	cols_mul=str(query_token[2])
	cols_mul_l=cols_mul.split(',')
	print "Error: Code not complete yet, dont use this function, but here is the whole table for you to work with till then :)"
	print
	for join_index in join_table:
		print join_index
		print
	#if 'and' in str(query_token[8]):
		#print 'and'

else: print "Cant read the command properly, Please check the syntax :)"



