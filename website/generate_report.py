import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import db_get as db_get

def create(TEST_configuration, TEST_history):
	ccap_configuration_id=TEST_configuration[0]['ccap_configuration_id']
	prov_configuration_id=TEST_configuration[0]['prov_configuration_id']
	CCAP_configuration_new=db_get.CCAP_configuration_new(ccap_configuration_id)
	PROV_configuration=db_get.PROV_configuration(prov_configuration_id)
	name=TEST_configuration[0]['name']
	url="download/reports/"+name+"_report.pdf"
	doc = SimpleDocTemplate(url,pagesize=letter,
							rightMargin=72,leftMargin=72,
							topMargin=72,bottomMargin=18)
	Story=[]
	logo = "static/img/vt_logo.png"
	Data=[
	{"name": "Test scenario:", "data": TEST_configuration[0]['name']},
	{"name": "Test started:", "data": TEST_history[0]['data_start']},
	{"name": "Test planned_end:", "data": TEST_history[0]['data_planned_end']},
	{"name": "Test ended", "data": TEST_history[0]['data_end']},
	{"name": "Test interval:", "data": TEST_history[0]['interval']},
	{"name": "CCAP configuration name:", "data": CCAP_configuration_new[0]['name']},
	{"name": "Provisioning configuration name:", "data": PROV_configuration[0]['name']}
	]


	 
	formatted_time = time.ctime()
	im = Image(logo, 5*inch, 2*inch)
	Story.append(im)
	Story.append(Spacer(1, 12))
	Story.append(Spacer(1, 12))
	styles=getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
	ptext = '<font size=12>Report generated: %s</font>' % formatted_time
	Story.append(Paragraph(ptext, styles["Normal"]))
	Story.append(Spacer(1, 12))
	for row in Data:
		ptext = "<font size=12>"+row['name']+" "+row['data']+" </font>" 
		Story.append(Paragraph(ptext, styles["Normal"]))
		Story.append(Spacer(1, 12)) 
	doc.build(Story)
	return name+"_report.pdf"