import os
import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select as OriginalSelect

# by KCB: Computing repr of chrome_options (Options) ==> timeout increase
os.environ['PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT'] = '10'  # Set the timeout value to 5 seconds (or any desired value)

def loadJson(json_path):    
    global json_data
    
    print(json_path)

    with open(json_path) as file:
        json_data = json.load(file)
    
    return len(json_data["data"])

def getDataFromJson(idx):

    global firstName, lastName, password, skills, rate, dateOfBirth, country, streetAddress, city, zipCode, phoneNumber, lang_level, service, profile_idx

    firstName = json_data["data"][idx]['firstName']
    lastName = json_data["data"][idx]['lastName']
    password = json_data["data"][idx]['password']
    skills = json_data["data"][idx]['skills']
    rate = json_data["data"][idx]['rate']
    dateOfBirth = json_data["data"][idx]['birth']
    country = json_data["data"][idx]['country']
    streetAddress = json_data["data"][idx]['street']
    city = json_data["data"][idx]['city']
    zipCode = json_data["data"][idx]['zipcode']
    phoneNumber = json_data["data"][idx]['phoneNumber']
    lang_level= json_data["data"][idx]['langLevel']
    service= json_data["data"][idx]['service']
    
    profile_idx= idx
    print('>>>>', idx, firstName, lastName)
# Install multiple extensions on a profile
def install_extensions_on_profile( profile_directory, extension_paths ) :
    chrome_options = Options()
    
    chrome_options.add_experimental_option("detach", True)
    
    chrome_options.add_argument("--user-data-dir=" + profile_directory)
    
    unpacked_extension_paths = []
    for extension_path in extension_paths:
        if extension_path.endswith(".crx"):
            crx_extension_path = os.path.abspath(extension_path)
            print(crx_extension_path)
            chrome_options.add_extension(extension_path)
        else:
            unpacked_extension_path = os.path.abspath(extension_path)
            print(unpacked_extension_path)
            unpacked_extension_paths.append(unpacked_extension_path)

    # Join the unpacked extension paths with commas
    unpacked_extensions_argument = ",".join(unpacked_extension_paths)
    chrome_options.add_argument("--load-extension=" + unpacked_extensions_argument)
    chrome_options.add_argument("--start-maximized")
    return webdriver.Chrome(options=chrome_options)

def find_element_available(driver, element_criteria):
    flag = 1
    print('>>>>>', 'Finding ', element_criteria )
    time.sleep(3)
    while(flag):
        try:
            element = driver.find_element(By.XPATH, element_criteria)
            print('>>>>>', 'Found ', element_criteria )
            driver.execute_script('arguments[0].click()', element)
            flag = 0
        except Exception as e:
            print('>>>>>', 'Cannot find ', element_criteria )            
            print( e.msg )
            flag = 1
            time.sleep(1)

def pass_cloud_fare(driver) :
    flag = 1
    element_criteria = 'iframe'
    print('>>>>>', 'Finding ', element_criteria )
    time.sleep(1)
    while(flag):
        try:
            # iframe_element = driver.find_element(By.XPATH, element_criteria)
            iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe")))
            print("iframe", iframe)

            print('>>>>>', 'Found ', element_criteria )
            flag = 0
        except Exception as e:
            print('>>>>>', 'Cannot find ', element_criteria )            
            print( e.msg )
            flag = 1
            time.sleep(1)
    
    # tmp = driver
    # tmp.switch_to.frame(iframe_element)
    # element_in_iframe = tmp.find_element( By.XPATH, '//*[@id="ctp-checkbox-container"]' )

def perform_Tab_on_element(driver, element, repeat):
    for _ in range(repeat):  # Perform repeat Tab key presses
        element.send_keys(Keys.TAB)
        element = driver.switch_to.active_element
    return element   


def step1_joinClientOrLancer(driver):
    flag = 1
    i = 0
    while (flag) :
        try:
            # Find Radio
            parent = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.container div.row")))
            second_element = parent.find_element(By.CSS_SELECTOR, "div[data-qa='work']")
            second_element.click()
            print(">>>>>1","Found the freelancer radio")

            # Click Apply            
            apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.container button.up-btn.up-btn-primary.width-md.up-btn-block")))            
            apply_button.click()
            print(">>>>>1","Clicked Apply")

            flag = 0

        except Exception as e:
            print(">>>>>", 'Step 1 *** Failed')
            time.sleep(1)
            i +=1
            if i> 5:
                driver.refresh()
                print(">>>>>", 'Step 1 *** Upwork refreshed')
                time.sleep(10)
                i = 0

def step2_createNewAccountPage( driver, email ):
    flag = 1
    while (flag) :
        try:
            element = driver.find_element(By.ID, 'first-name-input')
            element.clear()
            element.send_keys(firstName)
            
            element = driver.find_element(By.ID, 'last-name-input')
            element.clear()
            element.send_keys(lastName)
            
            element = driver.find_element(By.ID, 'redesigned-input-email')
            element.clear()
            element.send_keys(email)
            
            element = driver.find_element(By.ID, 'password-input')
            element.clear()
            element.send_keys(password)

            check_agree = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="checkbox-terms"][aria-required="true"][aria-describedby="checkbox-terms-validation-messages"][type="checkbox"]')))
            check_agree.send_keys(Keys.SPACE)
            time.sleep(1)
            
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="button-submit-form"][type="button"]')))
            nextButton.send_keys(Keys.SPACE)
        
            print(">>>>>2", "Clicked Create")

            flag = 0

        except Exception as e:
            print(">>>>>", 'Step 2 *** Failed')
            time.sleep(3)

def closeTab(driver, url):
    window_handles = driver.window_handles
    for handle in window_handles:
        driver.switch_to.window(handle)
        if url in driver.current_url:
            print('>>>>>2', 'Close ', url)
            driver.close()


def step2_switchTabAndVerify(driver):
    # driver.switch_to.window(driver.window_handles[2])
    # driver.close()
    
    closeTab(driver, "adblock")
    
    # driver.switch_to.window(driver.window_handles[1])
    # driver.close()
    print('>>>>>2', 'Close Other Tabs')

    driver.switch_to.window(driver.window_handles[0])
    print('>>>>>2', 'Page switched')
    time.sleep(3)
    # driver.refresh()
    print('>>>>>2', 'refresh end')

    # driver.get('https://www.minuteinbox.com/window/id/2')
    flag = 1
    i = 0
    while (flag) :
        try :
            # iframe = WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe")))
            print('>>>>>2', 'Finding new email')

            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-href="2"].hidden-xs.hidden-sm.klikaciRadek.newMail')))
            # element = element.find_element( By.CSS_SELECTOR, "tr[data-href='2']" )
            element.click()

            driver.switch_to.frame("iframeMail")
            parent = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button-holder")))
            verifyBtn = parent.find_element(By.CSS_SELECTOR, 'a')
            verifyBtn.click()
            time.sleep(2)
            flag = 0
            print(">>>>>2","Clicked Verify")
        except Exception as e:
            print(">>>>>", 'Step Email Verify Failed')
            time.sleep(1)
            i += 1
            if i> 5:
                driver.refresh()
                print(">>>>>", 'Step 2 *** MinuteInBox refreshed')
                time.sleep(10)
                i = 0

def closeOtherTabs(driver):
    time.sleep(1)
    window_handles = driver.window_handles
    for handle in window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)
            driver.close()
    print('>>>>>', 'Closed Other tabs' )

def switch_window(driver, index) :
    time.sleep(1)
    flag = 1
    while(flag):
        try:
            driver.switch_to.window(driver.window_handles[index])
            flag = 0
        except:
            time.sleep(1)
    time.sleep(1)

def step3_closeCookieModal(driver):
    flag = 1
    i = 0
    while (flag):
        try:
        # Accept close_button.click()   
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ot-sdk-container button.onetrust-close-btn-handler.banner-close-button.ot-close-icon"))).click()
            print("Close Cookie Modal Success")
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>3', 'Close Cookie Modal Failed')
            i += 1
            if i> 5: break
            time.sleep(1)

def step3_clickGetStartedBtn(driver):
    flag = 1
    i = 0
    while (flag):
        try:
            getStartedButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-qa="get-started-btn"][type="button"]')))
            getStartedButton.click()
            print('>>>>>3', 'Click Get Started Button Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>3', 'Click Get Started Button Failed')
            time.sleep(1)
            i +=1
            if i> 5:
                driver.refresh()
                print(">>>>>", 'Click Get Started Button refreshed')
                time.sleep(10)
                i = 0


def step3_clickExpertbox(driver):
    flag = 1
    while(flag):    
        try:
            expertRadio = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="radio"][value="FREELANCED_BEFORE"]')))
            expertRadio.click()
            time.sleep(1)
         # next button click event
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()  
            time.sleep(2)
            print('>>>>>3', 'Click I am a expert Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>3', 'Click I am a expert Failed')
            time.sleep(1)

def step3_clickToEarn(driver):
    flag = 1
    while(flag):    
        try:
        #### https://www.upwork.com/nx/create-profile/goal          
        # slide 2: 
         # To earn my main income  
            earnRadio = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="radio"][value="MAIN_INCOME"]')))
            earnRadio.click()
            time.sleep(1)
         # next button click event
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()  
            time.sleep(2)
            print('>>>>>3', 'Click ToEarn Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>3', 'Click ToEarn Failed')
            time.sleep(1)

def step3_clickSelectWork(driver):
    flag = 1
    while(flag):    
        try:
        #### https://www.upwork.com/nx/create-profile/work-preference        
        # slide 3: 
         # select work ways
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"][aria-labelledby="button-box-29"]')))
            element.click()
            for _ in range(2):  # Perform 3 Tab key presses
                element.send_keys(Keys.TAB)
                element = driver.switch_to.active_element
                element.send_keys(Keys.SPACE)
            time.sleep(1)
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>3', 'Click Select Work ways Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>3', 'Click Select Work ways Failed')
            time.sleep(1)


def step3_getStarted(driver):
    print('>>>>>Step3', 'get started')
    
    switch_window(driver, 2)
    # closeOtherTabs(driver)
    step3_closeCookieModal(driver)
    time.sleep(2)
    
    step3_clickGetStartedBtn(driver)
    step3_clickExpertbox(driver)
    step3_clickToEarn(driver)
    step3_clickSelectWork(driver)
    
def step4_createProfile_slide_1(driver):
    time.sleep(3)
    print('>>>>>Step4', 'Create Profile and Skill select')
    uploadResume = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="resume-upload-btn-mobile"]')))
    uploadResume.click()
    i = 0
    file_path='resume.docx'
    file_path = os.path.abspath(file_path)
    print(file_path)

    while True:
        try:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"][accept=".pdf,.doc,.docx,.rtf"]')))
            element.send_keys(file_path)
            print('>>>>>', 'Step4-Upload resume', 'Success')
            time.sleep(13)
            
            continue_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="resume-upload-continue-btn"]')))
            continue_button.click()
            break
        except Exception as e:
            print('>>>>>', 'Step10-Upload resume', 'Failed')
            if i > 5: break
            time.sleep(1)


def step4_createProfile_slide_2(driver):        
    flag = 1
    time.sleep(3)
    while(flag):    
        try:    
        # slide 2
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_2', 'fill role Failed')
            time.sleep(1)
            
def step4_createProfile_slide_3_Add_experience(driver):        
    flag = 1
    time.sleep(3)
    while(flag):    
        try:             
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_3', 'Success, "Next your education"')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_3', 'Add_experience failed') 
            time.sleep(1)
                        
def step4_createProfile_slide_4_Add_education(driver):
    flag = 1
    time.sleep(3)
    while(flag):    
        try:     
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_4', '"Next your education" click Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_4', '"Next your education" click Failed')  
            time.sleep(1)

def step4_createProfile_slide_5(driver):        
    flag = 1
    time.sleep(3)
    while(flag):    
        try:                 
        # slide 5
         # Add language     
            lang_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa="english-level"] div[data-test="dropdown-toggle"]')))
            # country_input.click()
            time.sleep(0.5)
            click_in_toggle_list(driver, lang_input, lang_level)
            
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_5', '"Next add your skills" click Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_5', '"Next add your skills" click Failed')
            time.sleep(1)    

def click_in_toggle_list(driver, element, text, attribute="aria-expanded"):
    element.click()
    i = 0
    while True:
        if element.get_attribute(attribute) == 'true':
            # items = driver.find_elements_by_css_selector('li[role="option"]')
            items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[role="option"]')))
            for item in items:
                if text in item.get_attribute('innerHTML'):
                    item.click()
                    break
            break
        time.sleep(1)
        i += 1
        if i > 40:
            break

def step4_createProfile_slide_6(driver):     

    time.sleep(3)
    
    for skill in skills:
        while True:
            try:
                skill_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="skills-input"]')))
                skill_input.click()
                skill_input.send_keys(skill)
                time.sleep(1)
                click_in_toggle_list(driver, skill_input, skill)
                break
            except Exception as e:
                time.sleep(1)
                try:
                    skill_input.clear()
                except Exception as e:
                    print('>>>>>Step6', skill, "Failed to Clear")
                print('>>>>>Step6', skill, "Failed to Click", skill)
                
    nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
    nextButton.click()         
    print('>>>>>4_6', 'Skill insert Success')
    
def step4_createProfile_slide_7(driver):        
    flag = 1
    time.sleep(3)    
    while(flag):    
        try:                 
        # slide 7
         # your profile
            driver.refresh()
            time.sleep(2)
            
            nextButton = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_7', 'Profile overview insert Success')

            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_7', 'Profile insert Failed')
            time.sleep(1)
            
# def service_add(driver, repeat):
#     for _ in range(repeat):  # Perform repeat Tab key presses
#         web_dev = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="category-add-btn"][aria-label="Web Development"]')))
#         web_dev.click()
#         time.sleep(1)
def step4_createProfile_slide_8(driver):        
    flag = 1
    time.sleep(3)
    while(flag):    
        try:                 
        # slide 8
         # Suggested Services 
            # element = driver.switch_to.active_element
            # element  = perform_Tab_on_element(driver, element, 2)
            # element.send_keys(Keys.SPACE)
            # element = driver.switch_to.active_element 
            # element  = perform_Tab_on_element(driver, element, 1)
            # element.send_keys(Keys.SPACE) 
            # element = driver.switch_to.active_element 
            # element  = perform_Tab_on_element(driver, element, 1)
            # element.send_keys(Keys.SPACE) 
            # element = driver.switch_to.active_element 
            # element  = perform_Tab_on_element(driver, element, 1)
            # element.send_keys(Keys.SPACE) 
            # element = driver.switch_to.active_element 
            # element  = perform_Tab_on_element(driver, element, 1)
            # element.send_keys(Keys.SPACE) 
            # element  = perform_Tab_on_element(driver, element, 1)
            # element.send_keys(Keys.SPACE)             
            
            
            
            element = driver.switch_to.active_element
            parent  = perform_Tab_on_element(driver, element, 1)
            element = parent.find_element(By.CSS_SELECTOR, 'span[class="air3-dropdown-toggle-label ellipsis"]')
            print("slide 8:", element.get_attribute("innerHTML"))
            # driver.execute_script("arguments[0].innerHTML = 'Blockchain, NFT & Cryptocurrency, Web Development, Web & Mobile Design, Mobile Development, Game Design & Development, Desktop Application Development';", element)
            
            driver.execute_script('arguments[0].innerHTML =' + "'" + service + "'", element)

            time.sleep(2)
            element = driver.switch_to.active_element
            parent = perform_Tab_on_element(driver, element, 1)
            print("slide 8: suggested service ==> ", element.get_attribute("innerHTML"))
            parent.send_keys(Keys.SPACE)
            
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_8', 'Suggested Services insert Success')

            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_8', 'Suggested Services insert Failed')
            time.sleep(1)

def step4_createProfile_slide_9(driver):        
    flag = 1
    time.sleep(3)

    while(flag):    
        try:                 
        # slide 9 
         # Hourly rate
            hourSalary = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-describedby="currency-hourly-12 hourly-rate-description"][data-test="currency-input"]')))
            hourSalary.send_keys(rate)
            
            nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
            nextButton.click()
            print('>>>>>4_9', 'Hourly rate insert Success')
            flag = 0
        except Exception as e:
            # print(e)  
            print('>>>>>4_9', 'Hourly rate insert Failed')
            time.sleep(1)

def step10_upload_avatar(driver):
    
    time.sleep(3)
    uploadPhoto = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="open-loader"]')))
    uploadPhoto.click()

    i = 0
    file_path=f'./avatar/avatar{profile_idx+1}.png'
    file_path = os.path.abspath(file_path)
    print(file_path)

    while True:
        try:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"][accept="image/*"]')))
            element.send_keys(file_path)
            print('>>>>>', 'Step10-Upload Avatar', 'Success')
            time.sleep(2)
            break
        except Exception as e:
            print('>>>>>', 'Step10-Upload Avatar', 'Failed')
            if i > 5: break
            time.sleep(1)


    uploadPhoto = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="btn-save"]')))
    uploadPhoto.click()
    time.sleep(7)
        
def step4_createProfile_slide_10(driver):        
    flag = 1
    time.sleep(2)
    step10_upload_avatar(driver)
    # Country
    while True:
        try:
            country_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa="dropdown-country"] div[data-test="dropdown-toggle"]')))
            # country_input.click()
            # time.sleep(0.5)
            click_in_toggle_list(driver, country_input, country)
            print('>>>>>Step10', "Success to Click", country)
            break
        except Exception as e:
            print('>>>>>Step10', "Failed to Click", country)
            
    time.sleep(1)
    # # City
    # while True:
    #     try:
    #         city_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="city-label"]')))
    #         city_input.send_keys(city)
    #         time.sleep(3)
    #         click_in_toggle_list(driver, city_input, city)
    #         break
    #     except Exception as e:
    #         time.sleep(1)
    #         try:
    #             city_input.clear()
    #         except Exception as e:
    #             print('>>>>>Step10', "Failed to Clear", city)
    #         print('>>>>>Step10', "Failed to Click", city)
    while(flag):    
        try:             
        # slide 10
         # person information
            # element  = perform_Tab_on_element(driver, element, 2)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="date-of-birth-label"]')))
            element.clear()
            element.send_keys(dateOfBirth)
            time.sleep(1)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="street-label"]')))
            element.clear()
            element.send_keys(streetAddress)
            time.sleep(1)
            # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[role="combobox"][aria-labelledby="city-label"]')))
            element = driver.switch_to.active_element   
            element  = perform_Tab_on_element(driver, element, 2)
            element = driver.switch_to.active_element 
            element.clear()
            element.send_keys(city)
            # element = driver.switch_to.active_element   
            time.sleep(5)
            element  = perform_Tab_on_element(driver, element, 2)
            element.send_keys(Keys.SPACE)
            time.sleep(1)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-labelledby="postal-code-label"]')))
            element.clear()
            element.send_keys(zipCode)
            time.sleep(1)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="tel"]')))
            element.clear()
            element.send_keys(phoneNumber)
                                
            flag = 0
        except Exception as e:
            print("person information failed")
            time.sleep(1)
            
    nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="next-button"][data-ev-label="wizard_next"]')))
    nextButton.click()
    
    print("person information Success")
            
    time.sleep(3)
    nextButton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-qa="submit-profile-top-btn"][type="button"]')))
    nextButton.click()
    print("information submit Success")
    
    time.sleep(3)
    browseJobs = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="up-n-link air3-btn air3-btn-primary"]')))
    browseJobs.click()    
    flag = 0
    print("browse Job Success")
            
    time.sleep(3)
    closeTab(driver, "https://www.minuteinbox.com/window/id/2")
    closeTab(driver, "https://www.upwork.com/nx/signup/")
    # driver.switch_to.window(driver.window_handles[1])
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])
    # driver.close() 
    print("person account create Successfully!")


def openMinuteInBox(driver):
    time.sleep(1)
    print('>>>>>', 'Opening MinuteInBox' )
    driver.get('https://www.minuteinbox.com/')

    flag = 1
    i = 0
    while (flag) :
        try:
            spanbox= WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.animace")))
            email = spanbox.text

            print(">>>>>", 'Found Email Success', email)
            flag = 0
        except Exception as e:
            print(">>>>>", 'Finding Email Failed')
            time.sleep(1)
            i +=1
            if i> 5:
                driver.refresh()
                print(">>>>>", 'Step 1 *** Upwork refreshed')
                time.sleep(10)
                i = 0
        
    return email


def openUpwork(driver, email):

    time.sleep(3)
    print('>>>>>', 'Opening Upwork' )

    driver.switch_to.new_window('tab')
    driver.get('https://www.upwork.com/nx/signup/')

    step1_joinClientOrLancer(driver)
    step2_createNewAccountPage(driver, email)
    step2_switchTabAndVerify(driver)
    step3_getStarted(driver)
    step4_createProfile_slide_1(driver)   
    step4_createProfile_slide_2(driver)
    step4_createProfile_slide_3_Add_experience(driver)
    step4_createProfile_slide_4_Add_education(driver)
    step4_createProfile_slide_5(driver)
    step4_createProfile_slide_6(driver)
    step4_createProfile_slide_7(driver)
    step4_createProfile_slide_8(driver)
    step4_createProfile_slide_9(driver)
    step4_createProfile_slide_10(driver)

    
def openTempMail(driver):
    time.sleep(1)
    driver.get('https://temp-mail.org/en')
    print('>>>>>', 'Opened temp-mail' )

    window_handles = driver.window_handles
    for handle in window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)
            driver.close()
    print('>>>>>', 'Closed Other tabs' )

    driver.switch_to.window(driver.window_handles[0])    

    time.sleep(2)

    # Click CloudFlare 
    # pass_cloud_fare(driver)
    # find_element_available(driver, '//*[@id="ctp-checkbox-container"]')
    # driver.find_element(By.XPATH, '//*[@id="content"]').click()
