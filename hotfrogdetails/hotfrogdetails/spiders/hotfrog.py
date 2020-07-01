import scrapy
import time
import os
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from ..items import HotfrogdetailsItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HotfrogSpider(scrapy.Spider):
    name = 'hotfrog'

    website = 'hotfrog'
    ind=0
    find_search=''
    near_search = ''
    # website_name = ''
    # website_link = ''
    # phone = ''
    # business_info = ''


    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://www.hotfrog.com/",
            wait_time=3,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):
        if(response.url!='https://www.google.com/'):
            driver = response.meta['driver']
            index = response.meta['index']

            firstinput = os.path.abspath(os.curdir) + "\option.txt"
            secondinput = os.path.abspath(os.curdir) + "\location.txt"
            thirdinput = os.path.abspath(os.curdir) + "\pages.txt"

            f = open(firstinput, "r")
            find = f.read().splitlines()

            f = open(secondinput, "r")
            near = f.read().splitlines()

            f = open(thirdinput, "r")
            numpages = f.read().splitlines()
            length = len(find)
            if(index<length):
                # ind = index


                driver.find_element_by_xpath("//*[@id='what']").clear()
                search_input1 = driver.find_element_by_xpath("//*[@id='what']")
                search_input1.send_keys(find[index])
                self.find_search=find[index]
                self.near_search = near[index]
                driver.find_element_by_xpath("//*[@id='where']").clear()
                search_input2 = driver.find_element_by_xpath("//*[@id='where']")
                search_input2.send_keys(near[index])
                print()
                print()
                print(find[index],near[index])
                print()
                print()
                search_button = driver.find_element_by_xpath("//header/div[2]/div/div[2]/form/div/button")
                search_button.click()
                web_name = []
                web_link = []
                web_phone = []
                web_business = []
                i=1
                main_url = driver.current_url

                index += 1

                yield SeleniumRequest(
                    url=driver.current_url,
                    wait_time=3,
                    screenshot=True,
                    callback=self.parse_page,
                    meta={'index': index,'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'i':i,'main_url':main_url,'numpages':numpages[0]},
                    dont_filter=True
                )


    def parse_page(self,response):
        # time.sleep(4)
        driver = response.meta['driver']
        web_name = response.meta['web_name']
        web_link = response.meta['web_link']
        web_phone = response.meta['web_phone']
        web_business = response.meta['web_business']
        index = response.meta['index']
        numpages = response.meta['numpages']
        i = response.meta['i']
        main_url = response.meta['main_url']
        # if(response.url!='https://www.google.com/'):
        #     print()
        #     print(driver.current_url)
        #     print()
        #     print()
        try:
            if(driver.find_element_by_id('master-1')):
                driver.switch_to.frame(driver.find_element_by_id('master-1'))

                html = driver.page_source
                response_obj = Selector(text=html)
                print()
                print()
                print(response.url)
                print()
                print()
                details = response_obj.xpath("//div[@class='gc_ si101 c_']")
                print()
                print(len(details))
                print('hello')
                print()
                # web_name = []
                # web_link = []
                # web_phone = []
                # web_business = []
                for detail in details:
                    website_name = detail.xpath('.//div/div/a[2]/text()').get()
                    website_link = detail.xpath('.//div/div/a[1]/@href').get()
                    phone = detail.xpath('.//div[1]/span[@class="mc_ si20 "]/text()').get()
                    business_info = detail.xpath('.//div[2]/a/text()').get()

                    if (website_name != None):
                        web_name.append(website_name)
                    else:
                        web_name.append("NA")

                    if (website_link != None):
                        web_link.append(website_link)
                    else:
                        web_link.append("NA")

                    if (phone != None):
                        web_phone.append(phone)
                    else:
                        web_phone.append("NA")

                    if (business_info != None):
                        web_business.append(business_info)
                    else:
                        web_business.append("NA")
                # if(i==1):
                #     i = i + 1
                #     main_url = response.url
                #     next_page = main_url + f'/{i}'
                #
                # else:
                i = i+1
                next_page = main_url + f'/{i}'
                # next_page=f"https://www.hotfrog.com{direction}"
                if(i>=numpages):
                    print()
                    print()
                    print('Page',i)
                    print()
                    print()
                    yield SeleniumRequest(
                        url=driver.current_url,
                        wait_time=3,
                        screenshot=True,
                        callback=self.parse_email,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business, 'index': index},
                        dont_filter=True
                    )
                else:
                    yield SeleniumRequest(
                        url=next_page,
                        wait_time=3,
                        screenshot=True,
                        callback=self.parse_page,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'i':i,'main_url':main_url,'index': index,'numpages':numpages},
                        dont_filter=True
                    )
        except:
            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=3,
                screenshot=True,
                callback=self.parse_email,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business,'index': index},
                dont_filter=True
            )

        # else:
        #     yield SeleniumRequest(
        #         url='https://www.google.com/',
        #         wait_time=3,
        #         screenshot=True,
        #         callback=self.parse,
        #         # meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
        #         #       'web_business': web_business},
        #         dont_filter=True
        #     )


        # else:





    def parse_email(self,response):
        Hotfrogdetails_Item = HotfrogdetailsItem()
        web_name = response.meta['web_name']
        web_link = response.meta['web_link']
        web_phone = response.meta['web_phone']
        web_business = response.meta['web_business']
        index = response.meta['index']
        # site_url = response.meta['site_url']

        if(response.url=='https://www.google.com/'):
            site_url = response.meta['site_url']
            finalemail = response.meta['finalemail']
            Hotfrogdetails_Item['website_name'] = web_name[0]
            Hotfrogdetails_Item['website_link'] = site_url
            Hotfrogdetails_Item['phone'] = web_phone[0]
            Hotfrogdetails_Item['business_info'] = web_business[0]
            Hotfrogdetails_Item['find'] = self.find_search
            Hotfrogdetails_Item['near'] = self.near_search
            Hotfrogdetails_Item['email'] = "NA"
            Hotfrogdetails_Item['website'] = self.website

            print()
            print()
            print(len(finalemail))
            print(type(finalemail))
            print()
            print()
            if (len(finalemail) == 0):
                yield Hotfrogdetails_Item
            else:
                if (len(finalemail) < 5):
                    length = len(finalemail)
                else:
                    length = 5
                for i in range(0, length):
                    Hotfrogdetails_Item['email'] = finalemail[i]
                    yield Hotfrogdetails_Item

            web_name.pop(0)
            web_phone.pop(0)
            web_business.pop(0)
            if (len(web_link) > 0):
                if (web_link[0] != 'NA'):
                    site_url = web_link[0]
                    web_link.pop(0)
                    yield SeleniumRequest(
                        url=site_url,
                        wait_time=3,
                        screenshot=True,
                        callback=self.emailtrack,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business, 'site_url': site_url,'index': index},
                        dont_filter=True
                    )
                else:
                    yield SeleniumRequest(
                        url='https://www.google.com/',
                        wait_time=3,
                        screenshot=True,
                        callback=self.parse_email,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business, 'site_url': 'NA','index': index},
                        dont_filter=True
                    )
            else:
                yield SeleniumRequest(
                    url='https://www.hotfrog.com/',
                    wait_time=3,
                    screenshot=True,
                    callback=self.parse,
                    meta={'index': index},
                    dont_filter=True
                )
        else:
            if(len(web_link) > 0):
                if(web_link[0]!='NA'):
                    site_url=web_link[0]
                    web_link.pop(0)
                    yield SeleniumRequest(
                        url=site_url,
                        wait_time=3,
                        screenshot=True,
                        callback=self.emailtrack,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'site_url':site_url,'index': index},
                        dont_filter=True
                    )
                else:
                    yield SeleniumRequest(
                        url='https://www.google.com/',
                        wait_time=3,
                        screenshot=True,
                        callback=self.parse_email,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'site_url':'NA','index': index},
                        dont_filter=True
                    )
            else:
                yield SeleniumRequest(
                    url='https://www.hotfrog.com/',
                    wait_time=3,
                    screenshot=True,
                    callback=self.parse,
                    meta={'index': index},
                    dont_filter=True
                )

    def emailtrack(self,response):
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)

        # page = response.meta['page']
        index = response.meta['index']
        web_name = response.meta['web_name']
        web_link = response.meta['web_link']
        web_phone = response.meta['web_phone']
        web_business = response.meta['web_business']
        site_url = response.meta['site_url']

        # duplicateurl = response.meta['duplicateurl']
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        Finallinks = [str(link.url) for link in links]
        links = []
        for link in Finallinks:
            if (
                    'Contact' in link or 'contact' in link or 'About' in link or 'about' in link or 'home' in link or 'Home' in link or 'HOME' in link or 'CONTACT' in link or 'ABOUT' in link):
                links.append(link)

        links.append(str(response.url))

        if (len(links) > 0):
            l = links[0]
            links.pop(0)
            uniqueemail = set()

            yield SeleniumRequest(
                url=l,
                wait_time=3,
                screenshot=True,
                callback=self.finalemail,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'uniqueemail': uniqueemail,'links': links,'index': index},
                dont_filter=True
            )
        else:
            finalemail=[]
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=3,
                screenshot=True,
                callback=self.parse_email,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'finalemail': finalemail,'index': index},
                dont_filter=True
            )


    def finalemail(self,response):
        links = response.meta['links']
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        index = response.meta['index']
        web_name = response.meta['web_name']
        web_link = response.meta['web_link']
        web_phone = response.meta['web_phone']
        web_business = response.meta['web_business']
        site_url = response.meta['site_url']


        uniqueemail = response.meta['uniqueemail']

        flag = 0
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki']
        for word in bad_words:
            if word in str(response.url):
                # return
                flag = 1
        if (flag != 1):
            html_text = str(response.text)
            mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)
            #
            mail_list = set(mail_list)
            if (len(mail_list) != 0):
                for i in mail_list:
                    mail_list = i
                    if (mail_list not in uniqueemail):
                        uniqueemail.add(mail_list)
                        print()
                        print()
                        print()
                        print(uniqueemail)
                        print()
                        print()
                        print()
            else:
                pass

        if (len(links) > 0 and len(uniqueemail) < 5):
            print()
            print()
            print()
            print('hi', len(links))
            print()
            print()
            print()
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                dont_filter=True,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'uniqueemail': uniqueemail,'links': links,'index': index}
            )
        else:
            print()
            print()
            print()
            print('hello')
            print()
            print()
            print()
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email or '.org' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print()
            print()
            print()
            print('final', finalemail)
            print()
            print()
            print()
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_email,
                dont_filter=True,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'links': links,'finalemail': finalemail,'index': index}

            )

















        # frame_url = response_obj.xpath('//iframe[@id="master-1"]/@src').get()
        # # frame_url=frame_url.split('#master')[0]
        # print()
        # print(frame_url)
        # print()
        # yield SeleniumRequest(
        #     url=frame_url,
        #     wait_time=3,
        #     screenshot=True,
        #     callback=self.scrape_detail,
        #     dont_filter=True
        # )

    # def scrape_detail(self,response):
    #     driver = response.meta['driver']
    #     html = driver.page_source
    #     response_obj = Selector(text=html)
    #     print()
    #     print(html)
    #     print()
    #     print()
    #     details = response_obj.xpath("//div[@class='gc_ si101 c_']")
    #     print()
    #     print(len(details))
    #     print('hi')
    #     print()
    #     for detail in details:
    #         self.website_name = detail.xpath('.//div/div/a[2]/text()').get()
    #         # self.website_link = detail.xpath('.//div[1]/div/a[2]/@href()').get()
    #         # self.phone = detail.xpath('.//div[1]/span/text()').get()
    #         # self.business_info = detail.xpath('.//div[2]/a/text()').get()
    #
    #         yield {
    #             'website_name': self.website_name
    #             # 'website_link': self.website_link,
    #             # 'phone': self.phone,
    #             # 'business_info': self.business_info
    #         }



























