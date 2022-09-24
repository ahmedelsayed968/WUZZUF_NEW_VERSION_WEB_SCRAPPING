from lib2to3.pgen2 import driver
from pydoc import describe
from tkinter import Pack
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import warnings
import urllib.request
from time import sleep
import numpy as np
# from macpath import join
warnings.filterwarnings('ignore')
PATH = "C:\chromedriver.exe"

class WUZZUF:
    base_url ='https://wuzzuf.net/search/jobs/'
    url_web= 'https://wuzzuf.net'
    def __init__(self):
        self.needed_links =[]
        self.jobs_title =[]
        self.durations = []
        self.company_names = []
        self.locations = []
        self.data_posted =[]
        self.n_applicants = []
        self.n_views = []
        self.no_in_consideration = []
        self.no_not_selected = []
        self.jobs_link = []
        self.logoes = []
        self.driver = webdriver.Chrome(PATH)
        self.driver.get(WUZZUF.base_url)
        
        self.skills_and_tools = []
        self.salary = []
        self.experience_needed = []
        self.education_level = []
        self.job_categories = []
        self.career_level = []
        
        self.job_description =[]
        self.job_requirement = []
         
        
        pass
    def get_job_details(self,job_name:str,n_pages:int)->dict:
        """
        Description:
            inputs: job_name , number of needed pages to loaded from the website
            return: dictionary contain all needed info.
        """
        self.__load_all_needed_links(job_name,n_pages)
        # print(self.needed_links)
        self.__load_all_jobs_link()
        self.__load_all_logoes_on_current_page()
        # print(self.logoes)
        # print('-'*100)
        # print(self.jobs_link)
        self.__load_all_details_for_the_job()
        print(self.needed_links)
#         print(self.company_names)
        
        jobs_details = {'job_title':self.jobs_title,
                        'company_name':self.company_names,
                       'location':self.locations,
                       'duration':self.durations,
                       'date_posted':self.data_posted,
                       'Num_Applicants':self.n_applicants,
                       'Num_Views':self.n_views,
                       'Num_In_Consideration':self.no_in_consideration,
                       'Num_Not_Selected':self.no_not_selected,
                       'skills_and_tools':self.skills_and_tools,
                       'salary':self.salary,
                       'experience_needed':self.experience_needed,
                       'education_level':self.education_level,
                       'job_categories':self.job_categories,
                       'career_level':self.career_level,
                       'job_description':self.job_description,
                       'job_requirements':self.job_requirement,
                       'job_link':self.jobs_link,
                       'Logo':self.logoes}
        return jobs_details
        
    def __load_all_needed_links(self,job_name:str,n_pages:int)->None:
        for page_index in range(n_pages):
            current_page_link = WUZZUF.base_url +'?q='+ job_name.strip().replace(' ','%20')+'&start={}'.format(page_index)
            self.needed_links.append(current_page_link)

    def __load_all_jobs_link(self):
            
        for link in self.needed_links:
#             self.driver.get(link)
            sleep(1)
            html = requests.get(link,'lxml.parser')
            soup = BeautifulSoup(html.text)
            for link in soup.find_all('a',{'class':'css-o171kl','target':'_blank'}):
                absulate_link = WUZZUF.url_web+link['href']
                self.jobs_link.append(absulate_link)
    
    
    def __load_all_logoes_on_current_page(self):
        for link in self.needed_links:
            self.driver.get(link)
            images = self.driver.find_elements(By.CLASS_NAME,'css-17095x3')
            for image in images:
                self.logoes.append(image.get_attribute('src'))
            
    def __load_all_details_for_the_job(self):
        for link in self.jobs_link:
            print(link)
            self.driver.get(link)

            self.__get_job_title()
            print('title done')

            self.__get_duration()
            print('duration done')

            self.__get_company_name()
            print('company_name done')

            self.__get_location()
            print('location done')
            
            self.__get_date_posted()
            print('date_posted done')
            
            self.__get_num_applicants()
            print('applicants done')
            
            self.__get_num_views()
            print('views done')
            
            self.__get_num_in_consideration()
            print('considers done')
            
            self.__get__num_not_selected()
            print('not selected done')

            self.__get_skills_and_tools()
            self.__get_job_requirements()
            self.__get_job_description()
            self. __get_job_categories()
            self.__get_education_level()
            self.__get_career_level()
            self. __get_experience_needed()
            self. __get_salary()
            

                           
    def __get_job_title(self):
        try: 
            title = self.driver.find_element(By.CLASS_NAME,'css-f9uh36').text
            self.jobs_title.append(title)
            print('here')
        except:
            self.jobs_title.append('Not Found')
            
    def __get_duration(self):
        try:
            duration_search = self.driver.find_elements(By.CLASS_NAME,'css-ja0r8m')
            temp_list = []
            for item in duration_search:
                temp_list.append(item.text)
            self.durations.append(','.join(temp_list))            
        except:
            self.durations.append(np.nan)
            
    def __get_company_name(self):
        try:
            company_name = self.driver.find_element(By.CLASS_NAME,'css-p7pghv')
            self.company_names.append(company_name.text)
        except:
            company_name = self.driver.find_element(By.CLASS_NAME,'css-9iujih').text.split('\n-')[0]
            self.company_names.append(company_name)
            
    def __get_location(self):
        try:
            list_item = self.driver.find_elements(By.CLASS_NAME,'css-9geu3q')[0].text.split('\n')
            self.locations.append(' '.join(list_item[2:]))
        except:
            self.locations.append(np.nan)
                
        
    def __get_date_posted(self):
        try:
            date = self.driver.find_element(By.CLASS_NAME,'css-182mrdn').text.split()[1:]
            self.data_posted.append(' '.join(date))
        except:
            self.data_posted.append(np.nan)
     
    def __get_num_applicants(self):
        try:
            num = self.driver.find_element(By.CLASS_NAME,'css-u1gwks').text  
            self.n_applicants.append(num)
        except:
            self.n_applicants.append(0)
    
    def __get_num_views(self):
        try:
            views = self.driver.find_elements(By.CLASS_NAME,'css-bs44nc')[0].text
            self.n_views.append(views)
        except:
            self.n_views.append(np.nan)
    
    def __get_num_in_consideration(self):
        try:
            considers = self.driver.find_elements(By.CLASS_NAME,'css-bs44nc')[1].text
            self.no_in_consideration.append(considers)
        except:
            self.no_in_consideration.append(np.nan)
            
            
    def __get__num_not_selected(self):
        try:
            not_selected = self.driver.find_elements(By.CLASS_NAME,'css-bs44nc')[2].text  
            self.no_not_selected.append(not_selected)
        except:
            self.no_not_selected.append(np.nan)
            
    def __get_skills_and_tools(self):
        try:
            elements = self.driver.find_elements(By.CLASS_NAME,'css-158icaa')
            for skill in elements:
                self.skills_and_tools.append(skill.text)
        except:
            self.skills_and_tools.append(np.nan)
    
    def __get_salary(self):
        try:
            search = self.driver.find_elements(By.CLASS_NAME,'css-4xky9y')
            salary = search[3].text
            self.salary.append(salary)
        except:
            self.salary.append(np.nan)
    
    def __get_experience_needed(self):
        try:
            search = self.driver.find_elements(By.CLASS_NAME,'css-4xky9y')
            experience_needed = search[0].text
            self.experience_needed.append(experience_needed)
        except:
            self.experience_needed.append(np.nan)
            
    def __get_career_level(self):
        try:
            search = self.driver.find_elements(By.CLASS_NAME,'css-4xky9y')
            career_level = search[1].text
            self.career_level.append(career_level)
        except:
            self.career_level.append(np.nan)
    
    def __get_education_level(self):
        try:
            search = self.driver.find_elements(By.CLASS_NAME,'css-4xky9y')
            education_level = search[2].text
            self.education_level.append(education_level)
        except:
            self.education_level.append(np.nan)
    
    def __get_job_categories(self):
        try:
            categories = self.driver.find_elements(By.CLASS_NAME,'css-tmajg1')
            temp =  []
            for item in categories:
                temp.append(item.text)
            self.job_categories.append(','.join(temp))  
        except:
            self.job_categories.append(np.nan)      
                        
    def __get_job_description(self):
        try:
            description = self.driver.find_element(By.CLASS_NAME,'css-1uobp1k')
            description = description.text.split('\n')
            self.job_description.append(description)
        except:
             self.job_description.append(np.nan)
                
        
    def __get_job_requirements(self):
        try:
            requirements = self.driver.find_element(By.CLASS_NAME,'css-1t5f0fr')
            requirements = requirements.text.split('\n')
            self.job_requirement.append(requirements)
        except:
            self.job_requirement.append(np.nan)
                
            
                    
                            
                    
if __name__ == '__main__':
    pass
