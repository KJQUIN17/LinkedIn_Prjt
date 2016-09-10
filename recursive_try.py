from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

start_time = time.time()  # Start time

# *******make sure chrome driver is in the same folder********

chrome_options = webdriver.ChromeOptions()  # makes the session into incognito mode
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome()  # we are not using incognito, use other line instead for that
# driver = webdriver.Chrome(chrome_options=chrome_options)

letter = 'A'  # *****************LETTER VARIABLE IS HERE************************
              ###when using 'U" change the upper end in base case to 95 instead of 50

write_file = open('LinkedIn.csv', "w", encoding='utf-8')  # opens write file

url = 'https://www.linkedin.com/'
driver.get(url)

directory_box = driver.find_element_by_class_name('directory')  # this targets the letters in the alphabet

directory_box.find_element_by_partial_link_text(letter).click()  # click on the letter we want

info_box = driver.find_element_by_class_name('columns')  # this targets into the block of links we want

upper_end = (len(driver.find_elements_by_class_name('content')))  # length for how mny iterations the loop will complete

names = info_box.find_elements_by_partial_link_text(letter)  # gets all the links in info_box with the letters specified

name_urls = [link.get_attribute('href') for link in names]  # stores links in array


def multi_profile():  # function to check for multiple profiles under one name
    try:
        driver.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div[1]/h1')
        return True
    except NoSuchElementException:
        return False


def clear_history():  # function to check if history needs to be cleaned
    try:
        driver.find_element_by_id('join-password')
        return True
    except NoSuchElementException:
        return False


def scrape_directory(upper_end1, name_urls1, letter1):  # -- MAIN FUNCTION
    if upper_end1 < 50:  # --BASE CASE (This is not good base case and it will be changed)

        print("Number of names to parse:", upper_end1)

        for url in name_urls1:  # loop to parse through links

                driver.get(url)  # gets url
                try:

                    if multi_profile():  # calls function to see if there is more than one person with same name
                        print('profile check is true', driver.current_url)
                        multi_names = driver.find_elements_by_class_name('profile-img')
                        multi_name_urls = [link.get_attribute('href') for link in multi_names]
                        for url in multi_name_urls:
                            driver.get(url)

                    if clear_history():  # calls function to clear browser history when LinkedIn doesnt let me continue
                        print('clearing History')
                        driver.get('chrome://settings/clearBrowserData')
                        body = driver.find_element_by_tag_name('body')
                        body.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB,
                                       Keys.TAB, Keys.TAB, Keys.ENTER)

                    experience = driver.find_element_by_id('experience')  # find the following elements and saves them
                    education = driver.find_element_by_id('education')
                    top_info = driver.find_element_by_id('name')
                    location = driver.find_element_by_class_name('locality')

                    top_info_text, experience_text, education_text, location_text = top_info.text, experience \
                        .text, education.text, location.text  # converts the data in the elements to text

                    profile_url = driver.current_url  # url of the page we are currently on

                    data_list = [top_info_text.replace(',', ''), profile_url, location_text.replace(',', ''),
                                 experience_text.replace(',', ''), education_text.replace(',', '')]

                    print(data_list)
                    write_file.write(str(data_list))
                    write_file.write('\n')

                except NoSuchElementException:
                    pass

    else:  # -- RECURSIVE CASE

        print("Number of sub-directories to parse:", upper_end)

        for url in name_urls1:

            driver.get(url)  # same as what was outside of the function

            upper_end1 = (len(driver.find_elements_by_class_name('content')))

            info_box1 = driver.find_element_by_class_name('columns')

            names1 = info_box1.find_elements_by_partial_link_text(letter)

            name_urls1 = [link.get_attribute('href') for link in names1]

            scrape_directory(upper_end1, name_urls1, letter1)  # recursive call

scrape_directory(upper_end, name_urls, letter)  # main function call

write_file.close()  # close file
print("--- %s seconds ---" % (time.time() - start_time))  # prints total time it took to complete the code
