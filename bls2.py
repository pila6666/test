import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.chrome.options import Options
import csv
import requests
import threading


def random_number():
    st = "7"
    for i in range(8):
        st += str(random.randint(0, 9))
    return st


def notify():
    mail_content = '''Hello,\nThe registration to the bls is now open.'''
    sender_address = 'dzkimos04@gmail.com'
    sender_pass = 'g?XKTQY@7NTN@FjY'
    # receiver_address = 'abdelooledba@gmail.com'
    receiver_address = "floraledz@gmail.com"
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'BLS Registration'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def fill(client, index):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #, desired_capabilities=capabilities)
    driver.get('https://nigeria.blsspainvisa.com/book_appointment.php')
    driver.find_element_by_xpath("""//*[@id="centre"]/option[text()='Lagos']""").click()
    time.sleep(2)
    driver.find_element_by_xpath("""//*[@id="category"]/option[text()='Normal']""").click()
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="phone"]""").send_keys(client['Phone'])
    time.sleep(1)
    dr = webdriver.Chrome(ChromeDriverManager().install())
    dr.get('https://temp-mail.org/')
    time.sleep(4)
    email = dr.find_element_by_xpath('//*[@id="mail"]').get_attribute("value")
    global clients
    clients[index]['Email'] = email
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="email"]""").send_keys(email)
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="verification_code"]""").click()
    time.sleep(1)
    code = -1
    while True:
        if "Email verification" not in str(dr.page_source):
            dr.find_element_by_xpath("""//*[@id="click-to-refresh"]""").click()
            time.sleep(4)
            continue
        # el = dr.find_element_by_xpath("""//*[@id="tm-body"]/main/div[1]""")
        el = dr.find_element_by_xpath("""//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[
        4]/ul/li[2]/div[2]/span/a""")
        time.sleep(1)
        dr.execute_script("arguments[0].scrollIntoView();", el)
        el.click()
        time.sleep(2)
        code = str(dr.find_element_by_xpath("""//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[
        1]/div/div[2]/div[3]/table/tbody/tr[7]/td""").text)[-4:]
        dr.close()
        break
    driver.find_element_by_xpath("""//*[@id="otp"]""").send_keys(code)
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="em_tr"]/div[3]/input""").click()
    time.sleep(1)
    element = driver.find_element_by_xpath("""//*[@id="nigeriaFirst"]/section/div/div/div/div[3]/div[1]/button""")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()
    time.sleep(2)
    date = driver.find_element_by_xpath("""//*[@id="app_date"]""")
    driver.execute_script("arguments[0].value='" + client['Date'] + "';", date)
    date.click()
    time.sleep(0.5)
    driver.find_element_by_xpath("""//*[@id="app_date_tr"]/td[1]""").click()
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="app_time"]/option[text()='""" + client['Time'] + """']""").click()
    time.sleep(0.3)
    driver.find_element_by_xpath("""//*[@id="VisaTypeId"]/option[text()='""" + client['Type'] + """']""").click()
    time.sleep(0.3)
    driver.find_element_by_xpath("""//*[@id="first_name"]""").send_keys(client['First name'])
    time.sleep(0.1)
    driver.find_element_by_xpath("""//*[@id="last_name"]""").send_keys(client['Last name'])
    time.sleep(0.1)
    birthday = driver.find_element_by_xpath("""//*[@id="dateOfBirth"]""")
    driver.execute_script("arguments[0].value='" + client['Birthday'] + "';", birthday)
    time.sleep(0.1)
    # driver.find_element_by_xpath("""//*[@id="phone"]""").send_keys(client['Phone'])
    # time.sleep(0.1)
    driver.find_element_by_xpath("""//*[@id="nationalityId"]/option[@value="62"]""").click()
    time.sleep(0.1)
    driver.find_element_by_xpath("""//*[@id="passportType"]/option[@value="01"]""").click()
    time.sleep(0.1)
    driver.find_element_by_xpath("""//*[@id="passport_no"]""").send_keys(client['Passport number'])
    time.sleep(0.1)
    issue = driver.find_element_by_xpath("""//*[@id="pptIssueDate"]""")
    driver.execute_script("arguments[0].value='" + client['Passport issue date'] + "';", issue)
    time.sleep(0.1)
    exp = driver.find_element_by_xpath("""//*[@id="pptExpiryDate"]""")
    driver.execute_script("arguments[0].value='" + client['Passport expiry date'] + "';", exp)
    time.sleep(0.1)
    driver.find_element_by_xpath("""//*[@id="pptIssuePalace"]""").send_keys(client['Passport issue place'])
    return


a_csv_file = open("clients_to_book.csv", "r")
dict_reader = csv.DictReader(a_csv_file)
ordered_dict_from_csv = list(dict_reader)
print(ordered_dict_from_csv)
clients = ordered_dict_from_csv
print(clients)
ind = 0
while True:
    resp = requests.get('https://nigeria.blsspainvisa.com/book_appointment.php')
    if "Appointment dates are not available." not in resp.text:
        notify()
        break
    time.sleep(120)
    print("le site est fermer")
for i in clients:
    thread = threading.Thread(target=fill, args=(dict(i), ind,))
    thread.start()
while threading.active_count() > 1:
    time.sleep(4)
with open("clients_to_book.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=clients[0].keys())
    writer.writeheader()
    for data in ordered_dict_from_csv:
        writer.writerow(dict(data))
