from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
import sys, time

# input: python 104.py (intern) (# of jobs)
# (intern): 0 means search for all types of job, 1 means search for intern specifically
# (# of jobs): # of jobs you are looking for

driver = webdriver.Chrome()
driver.get("https://www.104.com.tw/jobs/main/")
wait = WebDriverWait(driver, 20)

inputgroup = driver.find_element_by_class_name("input-group")
searchWait = WebDriverWait(inputgroup, 20)

# Select job locations
searchWait.until(EC.element_to_be_clickable((By.NAME, "icity"))).click()
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "category-picker__second-floor")))
locationBorad = driver.find_element_by_class_name("second-floor-rect")
locationBorad.find_element(By.XPATH, "//span[@class='children'][text()='台北市']/..//input").click()
WebDriverWait(locationBorad, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='確定']"))
).click()

# Select job type
jobtype = ["資訊軟體系統類", "研發相關類"]
searchWait.until(EC.element_to_be_clickable((By.NAME, "ijob"))).click()
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "category-picker__level-one")))
jobcategory = driver.find_element_by_class_name("category-picker__level-one")
for i in range(len(jobtype)):
    jobcategory.find_element(
        By.XPATH, "//span[@class='children'][text()='%s']/../..//button" % jobtype[i]
    ).click()
    wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "category-picker__second-floor"))
    )
    jobchild = driver.find_element_by_class_name("category-picker__second-floor")
    if i == 0:
        jobchild.find_element(
            By.XPATH,
            "//span[@class='children'][text()='資訊軟體系統類']/..//span[@class='category-picker-checkbox-input']",
        ).click()
    elif i == 1:
        jobchild.find_element(
            By.XPATH, "//span[@class='children'][text()='工程研發類人員']/..//input"
        ).click()
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='category-picker__modal-footer']/button"))
).click()

# job title
searchWait.until(EC.visibility_of_element_located((By.TAG_NAME, "input"))).send_keys("軟體工程師")
# click search button
searchWait.until(EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

# search for intern or not
if sys.argv[1] == "1":
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-title='更多條件']"))).click()
    jobfilter = wait.until(EC.presence_of_element_located((By.ID, "js-sub-filter")))
    WebDriverWait(jobfilter, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='實習工作']"))
    ).click()

# Create workbook
wb = Workbook()
ws = wb.active
# TO DO - rename sheet to searching input of job title
titles = [
    "Job Title",
    "Company",
    "Location",
    "Experience",
    "Education",
    "Content",
    "Salary",
    "Employees",
    "Applying Condition",
    "Additional Info",
]
ws.append(titles)

jobCount = 0
jobsInPage = 20

while jobCount < int(sys.argv[2]):
    jobContainer = wait.until(EC.visibility_of_element_located((By.ID, "js-job-content")))
    jobCards = jobContainer.find_elements_by_tag_name("article")
    if len(jobCards) < jobsInPage:
        driver.execute_script("arguments[0].scrollIntoView();", jobCards[-1])
        jobCards = jobContainer.find_elements_by_tag_name("article")
    for job in jobCards:
        card = list(job.text.split("\n"))
        # info = ["N/A"] * len(titles)
        info = list(["N/A"] * len(titles))
        # assign Job Title, Company, Location, Experience, Education, Content
        info[0] = job.find_element_by_tag_name("a").text
        jobTitle = job.find_element_by_class_name("b-list-inline").text.split("\n")
        info[1] = jobTitle[0]
        info[2:6] = card[3:7] if len(jobTitle) > 1 else card[2:6]
        info[-2] = card[-1]  # assign Applying Condition
        # assign Salary, Employees, Additional Info
        additionInfo = job.find_elements_by_class_name("b-tag--default")
        for i in range(len(additionInfo)):
            if additionInfo[i].text.startswith("員工"):
                info[7] = additionInfo[i].text
            elif "公司" in additionInfo[i].text:
                info[-1] = additionInfo[i].text
            elif i == 0:
                info[6] = additionInfo[i].text
        ws.append(info)
        jobCount += 1
        if jobCount == int(sys.argv[2]) or jobCount % jobsInPage == 0:
            break
    if jobCount < int(sys.argv[2]):
        driver.find_element_by_class_name("js-next-page").click()
wb.save("104.xlsx")
driver.close()