import re
import glob
comp=[]
mult=[]

def model(md):
	global comp
	global mult
	if md == 'OWS 47456':
		comp = ['f1','f2','f3','c1','c4','c6','c13','c8','c9','c18','c19','r1','u1%cr7_1','u1%cr7_2','u1%cr7_8','u1%cr7_9','u1%cr7_14']
		mult = [1,1,1,10e5,10e8,10e8,10e8,010e8,10e8,10e8,10e8,1,10e2,10e2,10e2,10e2,10e2]
	
	if md == 'Hex 39770':
		comp = ['r1','r4','c1','c4','c6','c8','c14','u1%cr_1_5','u1%cr_3_5','u1%cr_4_5','u1%cr_6_5','u1%cr_7_5','u1%cr_8_5']
		mult = [1,10e-4,10e8,10e8,10e8,010e8,10e8,10e2,10e2,10e2,10e2,10e2,10e2]
	
	if md == 'HCM 48038':
		comp = ['c1','c8','c9','c14','c18','c19','c20','c21','c24','c25','r1','r4','r7','r8','u1%cr2_1','u1%cr2_3','u1%cr2_4','u1%cr2_5','u1%cr2_6','u1%cr2_7','u1%cr2_8']
		mult = [9,9,9,9,9,9,9,6,9,9,0,-3,-3,-3,3,3,3,3,3,3,3]
	
	if md == 'CPOS':
		comp = ['r1','c1','c3','c4','c6','c8','c9','u1%cr_1_5','u1%cr_3_5','u1%cr_4_5','u1%cr_6_5','u1%cr_7_5','u1%cr_8_5']
		mult = [0,9,12,9,9,9,9,3,3,3,3,3,3]
	
	if md == '47303-4':
		comp = ['c1','c2','c3','c4','c5','c6','u1_diode%cr1_2','u1_diode%cr1_3','u1_diode%cr1_4','u1_diode%cr1_5','u1_diode%cr1_6','u1_diode%cr1_7','u1_diode%cr1_8','u1_diode%cr1_9','current_draw','voltage_tp2']
		mult = [9,9,9,12,6,12,0,0,0,0,0,0,0,0,3,0]
	
	if md == 'PS100':
		comp = ['c1','c4b','c5','c6','c18','c19','c20a','c20b','c27','c28','u1%cr1','u1%cr2','u1%cr3','u1%cr4','u1%cr5','u1%cr6','u1%cr7','u1%cr8','u1%cr9','u1%cr10','current_draw','voltage_tp1','voltage_tp2']
		mult = [9,12,9,12,9,9,9,9,9,9,0,0,0,0,0,0,0,0,0,0,2,0,0]

	if md == '48821':
		comp = ['r4','c1','c8','c4','c6','c14','u1_diode%cr2_1','u1_diode%cr2_3','u1_diode%cr2_4','u1_diode%cr2_6','u1_diode%cr2_1','u1_diode%cr2_1']
		mult = [-3,9,9,9,9,9,3,3,3,3,3,3]

	if md == '47998':
		comp = ['c1','c2','c3']
		mult = [9,9,9]

	if md == '48004':
		comp = ['c7','c8','c9']
		mult = [9,9,9]

	if md == '47256':
		comp = ['c7_new','c8_new','c9_new']
		mult = [9,9,9]

	if md == 'temp':
		comp = ['c2']
		mult = [9]

def meas_val(filename):
    f = open(filename).read()
    res = []
    for i, name in enumerate(comp):
    		if name == 'current_draw':
    			# patt = '@A-MEA\|\d\|(.*)\|I_R_shunt\{@LIM2'
    			patt = '@A-MEA\|\d\|(.*)\|Current_measure\{@LIM2'
    		elif name == 'voltage_tp1':
    			#patt = '@A-MEA\|\d\|(.*)\|V_DIG_TP2\{@LIM2'
    			patt = '@A-MEA\|\d\|(.*)\|Volt_P1\{@LIM2'
    		elif name == 'voltage_tp2':
    			#patt = '@A-MEA\|\d\|(.*)\|V_DIG_TP2\{@LIM2'
    			patt = '@A-MEA\|\d\|(.*)\|Volt_P2\{@LIM2'    			
    		else:
    			patt = '@BLOCK\|\d{1,2}%%%s\|.*\n.*\|(.*)\{@LIM'%(name)
    		v = re.findall(patt, f, re.MULTILINE)
    		#print v
    		if v != []:
    			res.append(float(v[0])*10**mult[i]+2)
    		else:
    			res.append(" ")
    return ', '.join([str(i) for i in res]) + '\n'


def log_data(path):
    res = []
    op = open('result.csv','w')
    op.writelines(['Parameter,'+','.join(comp)+'\n'+'Unit,'+','.join([str(i) for i in mult])+'\n'])
    files = glob.glob1(path,'*')
    for file in files:
        res.append(file +',' +meas_val(path+file))
    op.writelines(res)
    op.close()

model('47998')
log_data('./')
#print ','.join(comp)
# print meas_val('./golden/t1/Remove_C13_6-100517151937ICT_21')

# print meas_val('c:\\47456_Log\\PASS#02_17-100517152617ICT_21')
