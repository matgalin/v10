import db_get as db_get
###create config file for every specified Cable Modem
def createCMconfig(TEST_configuration):
	###Get Information about specified data, cable modem config file, etc
	id=TEST_configuration[0]['prov_configuration_id']
	name=TEST_configuration[0]['name']
	PROV_configuration=db_get.PROV_configuration(id)
	dir="Ansible/tests/"+name+"/configs"
	PROV_cm=db_get.PROV_cm(id)
	CM_part=db_get.CM_part()  
	for rows in PROV_cm:
		ConfigFileContentMid=''
		ConfigFileContent=''
		config_file=rows['cm_configuration_id']
		CM_configuration=db_get.CM_configuration(config_file)
		##iteration in all parts: looking for parts which are 
		for parts in CM_part:
			if str(parts['configuration_id'])==str(config_file):
				for line in parts['content'].splitlines():
					line=str(line).replace('\\r\\n', '\n').replace('\\"', '"')
					ConfigFileContentMid+=line
		GroupName=CM_configuration[0]['name']
		ConfigFileContentStart="Main {\n"
		ConfigFileContentStop="\n }"
		ConfigFileContent=ConfigFileContentStart+ConfigFileContentMid+ConfigFileContentStop
		file_conf = open(dir+"/"+str(GroupName)+".conf", "w")
		file_conf.write(ConfigFileContent)
		file_conf.close()
	default_cm=PROV_configuration[0]['default_cm_configuration_id']
	
	if default_cm > 0:
		ConfigFileContentMid=''
		ConfigFileContent=''
		CM_configuration=db_get.CM_configuration(default_cm)
		for parts in CM_part:
			if str(parts['configuration_id'])==str(default_cm):
				for line in parts['content'].splitlines():
					line=str(line).replace('\\r\\n', '\n').replace('\\"', '"')
					ConfigFileContentMid+=line
		GroupName=CM_configuration[0]['name']
		ConfigFileContentStart="Main {\n"
		ConfigFileContentStop="\n }"
		ConfigFileContent=ConfigFileContentStart+ConfigFileContentMid+ConfigFileContentStop
		file_conf = open(dir+"/"+str(GroupName)+".conf", "w")
		file_conf.write(ConfigFileContent)
		file_conf.close()
	

		