import db_get as db_get
import os	
import background
## creating list of ip adressem, from a given list
def ipRange(start_ip, end_ip):
	try:
		start = list(map(int, start_ip.split(".")))
	except: 
		background.report_status('IP List', 'Wrong Ip List: first part', 1)
		background.configuration_status[0]['status']=2
		return 0
	else:
		try:
			end = list(map(int, end_ip.split(".")))
		except:
			background.report_status('IP List', 'Wrong Ip List: second part', 1)
			background.configuration_status[0]['status']=2
			return 0
		else:
			temp = start
			ip_range = []
			ip_range.append(start_ip)
			while temp != end:
				start[3] += 1
				for i in (3, 2, 1):
					if temp[i] == 255:
						temp[i] = 0
						temp[i-1] += 1
				ip_range.append(".".join(map(str, temp)))    
			return ip_range
	
	
	
	
def ipRange6(start_ip, end_ip):
	start = list(map(str, start_ip.split(":")))
	#print start
	end = list(map(str, end_ip.split(":")))
	#print end
	
	length=len(start)
	length=length-1
	
	x_start=int(start[length], 16)
	x_end=int(end[length], 16)
	x_value=x_start
	ip_range = []
	ip_range.append(start_ip)

	for x in range(x_start, x_end):
		x_value += 1
		x=format(hex(x_value))
		x=x[2:]
		start[length]=x
		
		#temp2[length]=str(hex(temp2[length]))
		ip_range.append(":".join(map(str, start)))  
		
	return ip_range
	

##prepare YML file,readable by Ansible	
def preparePROVmain(TEST_configuration):
	  #get All Information about specified test configuration
	id=TEST_configuration[0]['prov_configuration_id']   ## get id of PROV info
	name=TEST_configuration[0]['name']  ## get test name
	dir="Ansible/tests/"+TEST_configuration[0]['name']  ## get config dir
	###Getting rest of information, needed to successfuly create prov and cm data
	PROV_cm=db_get.PROV_cm(id)
	PROV_configuration=db_get.PROV_configuration(id)
	PROV_ipv4=db_get.PROV_ipv4(id)
	PROV_ipv6=db_get.PROV_ipv6(id)
	CM_List=db_get.CM_List()  
	dir="Ansible/tests/"+name
	cable_modems_ip=[]
	single_ip={}
	payload= []
	content = {}
	if PROV_configuration[0]['ip_version']=='IPv4':
		ip_version=0
	if PROV_configuration[0]['ip_version']=='IPv6':
		ip_version=1
	if PROV_configuration[0]['ip_version']=='IPv4 and IPv6':
		ip_version=2
	for rows in PROV_cm:
		CM=rows['cable_modem']
		cmList=CM.split('-')
		
		####IPv4 or both
		if ip_version==0 or ip_version==2:
		
			IPv4=rows['ipv4']
			ipv4List = IPv4.split('-')
			ip_range = ipRange(ipv4List[0], ipv4List[1])
			if background.configuration_status[0]['status']==2:
				return 0
			routersv4=rows['routersv4']
		#####IPv6 or borh
		if ip_version==1 or ip_version==2:
		
			IPv6=rows['ipv6']
			ipv6List = IPv6.split('-')
			ip_range6 = ipRange6(ipv6List[0], ipv6List[1])
			routersv6=rows['routersv6']
			
		config_file_nr=rows['cm_configuration_id']
		CM_configuration=db_get.CM_configuration(config_file_nr)
		config_file=CM_configuration[0]['name']
		licznik=0
		if len(cmList)==1:
			cmList.append(cmList[0])
		for nr in range(int(cmList[0]), int(cmList[1])+1):
			for modems in CM_List:
				if modems['nr']==nr:
					content = {"mac": modems['mac'], "ipv4": ip_range[licznik], "routersv4": routersv4, "config_file": config_file}
					if ip_version==0 or ip_version==2:
						ipv4={"ipv4": ip_range[licznik], "routersv4": routersv4}
						content.update(ipv4)
					if ip_version==1 or ip_version==2:
						ipv6={"ipv6": ip_range6[licznik], "routersv6": routersv6}
						content.update(ipv6)
					single_ip= {"ip": ip_range[licznik]}
					cable_modems_ip.append(single_ip)
					payload.append(content)
					content= {}
					single_ip={}
					licznik=licznik+1
	default_cm=PROV_configuration[0]['default_cm_configuration_id']	
	dhcp_interface=PROV_configuration[0]['dhcp_interface']
	dhcp_ip=PROV_configuration[0]['dhcp_ip']
	MainYmlFile=''	
	MainYmlFile+="config_file: '"+name+"'"
	MainYmlFile+="\ninterface: '"+dhcp_interface+"'"
	MainYmlFile+="\nip: '"+dhcp_ip+"'"
	MainYmlFile+="\nip_version: '"+str(ip_version)+"'"
	
	if ip_version==0 or ip_version==2:
		time_serverv4=PROV_ipv4[0]['time']
		tftp_serverv4=PROV_ipv4[0]['tftp']
		routersv4=PROV_ipv4[0]['routers']
		poolv4=PROV_ipv4[0]['pool_range']
		subnetv4=PROV_ipv4[0]['subnet']
		MainYmlFile+="\ntime_server: '"+time_serverv4+"'"
		MainYmlFile+="\ntftp_server: '"+tftp_serverv4+"'"
		MainYmlFile+="\nrouters: '"+routersv4+"'"
		MainYmlFile+="\npool: '"+poolv4+"'"
		MainYmlFile+="\nsubnet: '"+subnetv4+"'"
	if ip_version==1 or ip_version==2:
		time_serverv6=PROV_ipv6[0]['time']
		tftp_serverv6=PROV_ipv6[0]['tftp']
		routersv6=PROV_ipv6[0]['routers']
		poolv6=PROV_ipv6[0]['pool_range']
		subnetv6=PROV_ipv6[0]['subnet']
		MainYmlFile+="\ntime_server6: '"+time_serverv6+"'"
		MainYmlFile+="\ntftp_server6: '"+tftp_serverv6+"'"
		MainYmlFile+="\nrouters6: '"+routersv6+"'"
		MainYmlFile+="\npool6: '"+poolv6+"'"
		MainYmlFile+="\nsubnet6: '"+subnetv6+"'"
	
	
	if default_cm>0:
		CM_configuration=db_get.CM_configuration(default_cm)
		MainYmlFile+="\ndefault_config_file: '"+CM_configuration[0]['name']+"'"

	MainYmlFile+="\nconfig_files:"
	for modems in payload:
		MainYmlFile+="\n  - {mac: '"+modems['mac']
		if ip_version==0 or ip_version==2:
			MainYmlFile+="', ip: '"+modems['ipv4']
			MainYmlFile+="', routers: '"+modems['routersv4']
		if ip_version==1 or ip_version==2:
			MainYmlFile+="', ipv6: '"+modems['ipv6']
			MainYmlFile+="', routersv6: '"+modems['routersv6']
		MainYmlFile+="', config_file: '"+modems['config_file']+"'}"
	try:
		file_yml = open(dir+"/CMmain.yml", "w")
	except:
		background.report_status('Creating Cable Modem data', 'Error', 1)
		background.configuration_status['status']=2
		return 0
	else:
		file_yml.write(MainYmlFile)
		file_yml.close()
		return cable_modems_ip
