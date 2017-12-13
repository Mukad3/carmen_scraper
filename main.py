import re
import bs4
import time
import requests
import smtplib


print 'Welcome to the scraper'


def evaluate_job(job_url):
	try:
		job_html = requests.request('GET', job_url, timeout = 100)
	except:
		print 'No data found, you idiot'
		return 0


	job_soup = bs4.BeautifulSoup(job_html.content, 'html.parser')
	soup_body = job_soup('body')[0]	


	chem_count = soup_body.text.count('Chemist') + soup_body.text.count('chemist') + soup_body.text.count('chemists') 
	teach_count = soup_body.text.count('Teaching') + soup_body.text.count('teaching')
	skill_count = chem_count + teach_count
	print 'Chem count: {0}, Teach count: {1}'.format(chem_count, teach_count)
	return skill_count
		
def extract_job_data_from_seek(base_url):
	response = requests.get(base_url)
	soup = bs4.BeautifulSoup(response.content, 'html.parser')
	tags = soup.find_all('article', {'data-automation' : "normalJob"})
	companies_list = [x.a.text for x in tags]
	dates = [x.find('span', {'aria-hidden' : "true"}).find(string=re.compile("ago")) for x in tags]
	locations = [x.strong.span.get_text() for x in tags]
	attrs_list = zip(companies_list, dates)
	new_list = dict(zip(attrs_list, locations)) 

	print new_list

	return new_list
	
	
extract_job_data_from_seek('https://www.seek.com.au/jobs-in-science-technology/chemistry-physics')

def send_gmail(from_addr = '****', to_addr = '****',
								location = 'Canberra, ACT'
               subject = 'New Jobs from Seek', text = None):
    
    message = 'Subject: {0}\n\nJobs in: {1}\n\n{2}'.format(subject, location, text)

    # login information
    username = '****'
    password = '****'
    
    # send the message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message)
    server.quit()
    print 'Email sent.'
