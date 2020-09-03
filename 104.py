from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, time

driver = webdriver.Chrome()
driver.get("https://www.104.com.tw/jobs/main/")
wait = WebDriverWait(driver, 20)

inputgroup = driver.find_element_by_class_name("input-group")
searchWait = WebDriverWait(inputgroup, 20)

# Select job locations
searchWait.until(EC.element_to_be_clickable((By.NAME, "icity"))).click()
wait.until(
    EC.visibility_of_all_elements_located(
        (By.CLASS_NAME, "category-picker__second-floor")))
locationBorad = driver.find_element_by_class_name("second-floor-rect")
locationBorad.find_element(
    By.XPATH, "//span[@class='children'][text()='台北市']/..//input").click()
WebDriverWait(locationBorad, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='確定']"))).click()

# Select job type
searchWait.until(EC.element_to_be_clickable((By.NAME, "ijob"))).click()
wait.until(
    EC.visibility_of_all_elements_located(
        (By.CLASS_NAME, "category-picker__level-one")))
jobcategory = driver.find_element_by_class_name("category-picker__level-one")
jobcategory.find_element(
    By.XPATH,
    "//span[@class='children'][text()='資訊軟體系統類']/../..//button").click()
wait.until(
    EC.visibility_of_all_elements_located(
        (By.CLASS_NAME, "category-picker__second-floor")))
jobtype = driver.find_element_by_class_name("category-picker__second-floor")
jobtype.find_element(
    By.XPATH,
    "//span[@class='children'][text()='資訊軟體系統類']/..//span[@class='category-picker-checkbox-input']"
).click()
jobcategory.find_element(
    By.XPATH,
    "//span[@class='children'][text()='研發相關類']/../..//button").click()
wait.until(
    EC.visibility_of_all_elements_located(
        (By.CLASS_NAME, "category-picker__second-floor")))
jobtype = driver.find_element_by_class_name("category-picker__second-floor")
jobtype.find_element(
    By.XPATH, "//span[@class='children'][text()='工程研發類人員']/..//input").click()
wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,
         "//div[@class='category-picker__modal-footer']/button"))).click()
# job title
searchWait.until(EC.visibility_of_element_located(
    (By.TAG_NAME, "input"))).send_keys('軟體工程師')

searchWait.until(EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()
time.sleep(3)
driver.close()