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
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):
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

            try:
                driver.find_element_by_xpath("//*[@id='what']").clear()
                search_input1 = driver.find_element_by_xpath("//*[@id='what']")
            except:
                index = response.meta['index']
                yield SeleniumRequest(
                    url="https://www.hotfrog.com/",
                    wait_time=1000,

                    callback=self.parse,
                    errback=self.errback_hotfrog,
                    meta={'index': index},
                    dont_filter=True
                )
            search_input1.send_keys(find[index])
            self.find_search=find[index]
            self.near_search = near[index]
            driver.find_element_by_xpath("//*[@id='where']").clear()
            search_input2 = driver.find_element_by_xpath("//*[@id='where']")
            search_input2.send_keys(near[index])
            print("\n"*2)
            print(find[index],near[index])
            print("\n" * 2)
            search_button = driver.find_element_by_xpath("//header/div[2]/div/div[2]/form/div/button")
            search_button.click()
            web_name = []
            web_link = []
            web_phone = []
            web_business = []
            web_description = []
            web_directon = []
            i=1
            main_url = driver.current_url

            index += 1

            duplicate_list=[]

            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.parse_page,
                errback=self.errback_parse_page,
                meta={'index': index,'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,'web_business': web_business,'i':i,'main_url':main_url,'numpages':int(numpages[0]),'duplicate_list':duplicate_list,'web_description':web_description,'web_directon':web_directon},
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
        duplicate_list = response.meta['duplicate_list']
        web_description = response.meta['web_description']
        web_directon = response.meta['web_directon']
        print()
        print('number of pages',numpages)
        print('i', i)
        print(driver.current_url)
        print("\n"*2)


        try:
            html = driver.page_source
            response_obj = Selector(text=html)
            next_page = response_obj.xpath('//div[1]/div[2]/div[58]/nav/ul/li/a[contains(text(),"Next")]/@href').get()

            driver.switch_to.frame(driver.find_element_by_id('master-1'))

            html = driver.page_source
            response_obj = Selector(text=html)
            print("\n"*2)
            print('inside',response.url)
            print("\n"*2)
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
                business_info = detail.xpath('.//div[2]/a//text()').extract()
                business_description = detail.xpath('.//div[2]/div/span//text()').extract()
                direction = detail.xpath('.//div[2]/span//text()').extract()
                if(website_name not in duplicate_list):
                    duplicate_list.append(website_name)
                    print("\n"*2)
                    print(business_info)
                    print(business_description)
                    print(direction)

                    final_business_info=''
                    for data in business_info:
                        final_business_info += data

                    final_business_description = ''
                    for data in business_description:
                        final_business_description += data

                    final_direction = ''
                    for data in direction:
                        final_direction += data

                    if (website_name != None):
                        web_name.append(website_name)
                    else:
                        web_name.append("-")

                    if (website_link != None):
                        web_link.append(website_link)
                    else:
                        web_link.append("-")

                    if (phone != None):
                        web_phone.append(phone)
                    else:
                        web_phone.append("-")

                    if (final_business_info != ''):
                        web_business.append(final_business_info)
                    else:
                        web_business.append("-")

                    if (final_business_description != ''):
                        web_description.append(final_business_description)
                    else:
                        web_description.append("-")

                    if (final_direction != ''):
                        web_directon.append(final_direction)
                    else:
                        web_directon.append("-")


            print("\n"*2)
            print(i,next_page)
            print("\n"*2)
            # next_page=f"https://www.hotfrog.com{direction}"
            print()
            print(type(i))
            print(type(numpages))
            print()

            if (next_page and i < numpages):
                print()
                print('next page')
                next_page = f"https://www.hotfrog.com{next_page}"
                print("\n"*2)
                i = i + 1
                yield SeleniumRequest(
                    url=next_page,
                    wait_time=1000,
                    screenshot=True,
                    callback=self.parse_page,
                    errback=self.errback_parse_page,
                    meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                          'web_business': web_business,'i':i,'main_url':main_url,'index': index,'numpages':numpages,'duplicate_list':duplicate_list,'web_description':web_description,'web_directon':web_directon},
                    dont_filter=True
                )
            else:
                print("\n"*2)
                print('Ready for email',i)
                print("\n"*2)
                yield SeleniumRequest(
                    url=driver.current_url,
                    wait_time=1000,
                    screenshot=True,
                    callback=self.parse_email,
                    meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                          'web_business': web_business, 'index': index,'web_description':web_description,'web_directon':web_directon},
                    dont_filter=True
                )
        except:
            print("\n"*2)
            print('No more page')
            print("\n"*2)

            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.parse_email,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business,'index': index,'web_description':web_description,'web_directon':web_directon},
                dont_filter=True
            )




    def parse_email(self,response):
        Hotfrogdetails_Item = HotfrogdetailsItem()
        web_name = response.meta['web_name']
        web_link = response.meta['web_link']
        web_phone = response.meta['web_phone']
        web_business = response.meta['web_business']
        index = response.meta['index']
        web_description = response.meta['web_description']
        web_directon = response.meta['web_directon']
        # site_url = response.meta['site_url']

        if(response.url=='https://www.google.com/'):
            site_url = response.meta['site_url']
            finalemail = response.meta['finalemail']
            Hotfrogdetails_Item['website_name'] = web_name[0]
            Hotfrogdetails_Item['website_link'] = site_url
            Hotfrogdetails_Item['phone'] = web_phone[0]
            Hotfrogdetails_Item['business_info'] = web_business[0]
            Hotfrogdetails_Item['business_description'] = web_description[0]
            Hotfrogdetails_Item['direction'] = web_directon[0]
            Hotfrogdetails_Item['find'] = self.find_search
            Hotfrogdetails_Item['near'] = self.near_search
            Hotfrogdetails_Item['email'] = "-"
            Hotfrogdetails_Item['website'] = self.website

            print("\n"*2)
            print(len(finalemail))
            print(type(finalemail))
            print("\n" * 2)
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
            web_description.pop(0)
            web_directon.pop(0)
            if (len(web_link) > 0):
                if (web_link[0] != '-'):
                    site_url = web_link[0]
                    web_link.pop(0)
                    yield SeleniumRequest(
                        url=site_url,
                        wait_time=1000,
                        screenshot=True,
                        callback=self.emailtrack,
                        errback=self.errback_emailtrack,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business, 'site_url': site_url,'index': index,'web_description':web_description,'web_directon':web_directon},
                        dont_filter=True
                    )
                else:
                    yield SeleniumRequest(
                        url='https://www.google.com/',
                        wait_time=1000,
                        screenshot=True,
                        callback=self.parse_email,
                        errback=self.errback_google,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business, 'site_url': '-','index': index,'web_description':web_description,'web_directon':web_directon},
                        dont_filter=True
                    )
            else:
                yield SeleniumRequest(
                    url='https://www.hotfrog.com/',
                    wait_time=1000,
                    screenshot=True,
                    callback=self.parse,
                    errback=self.errback_hotfrog,
                    meta={'index': index},
                    dont_filter=True
                )
        else:
            if(len(web_link) > 0):
                if(web_link[0]!='-'):
                    site_url=web_link[0]
                    web_link.pop(0)
                    yield SeleniumRequest(
                        url=site_url,
                        wait_time=1000,
                        screenshot=True,
                        callback=self.emailtrack,
                        errback=self.errback_emailtrack,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'site_url':site_url,'index': index,'web_description':web_description,'web_directon':web_directon},
                        dont_filter=True
                    )
                else:
                    yield SeleniumRequest(
                        url='https://www.google.com/',
                        wait_time=1000,
                        screenshot=True,
                        callback=self.parse_email,
                        errback=self.errback_google,
                        meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                              'web_business': web_business,'site_url':'-','index': index,'web_description':web_description,'web_directon':web_directon},
                        dont_filter=True
                    )
            else:
                yield SeleniumRequest(
                    url='https://www.hotfrog.com/',
                    wait_time=1000,
                    screenshot=True,
                    callback=self.parse,
                    errback=self.errback_hotfrog,
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
        web_description = response.meta['web_description']
        web_directon = response.meta['web_directon']
        # duplicateurl = response.meta['duplicateurl']
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        Finallinks = [str(link.url) for link in links]
        links = []
        for link in Finallinks:
            if (
                    'Contact' in link or 'contact' in link or 'About' in link or 'about' in link  or 'CONTACT' in link or 'ABOUT' in link):
                links.append(link)

        links.append(str(response.url))

        if (len(links) > 0):
            l = links[0]
            links.pop(0)
            uniqueemail = set()

            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'uniqueemail': uniqueemail,'links': links,'index': index,'web_description':web_description,'web_directon':web_directon},
                dont_filter=True
            )
        else:
            finalemail=[]
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_email,
                errback=self.errback_google,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'finalemail': finalemail,'index': index,'web_description':web_description,'web_directon':web_directon},
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
        web_description = response.meta['web_description']
        web_directon = response.meta['web_directon']

        uniqueemail = response.meta['uniqueemail']

        flag = 0
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']
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
                        print("\n"*2)
                        print(uniqueemail)
                        print("\n"*2)
            else:
                pass

        if (len(links) > 0 and len(uniqueemail) < 5):
            print("\n"*2)
            print('hi', len(links))
            print("\n"*2)
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'uniqueemail': uniqueemail,'links': links,'index': index,'web_description':web_description,'web_directon':web_directon}

            )
        else:
            print("\n" * 2)
            print('hello')
            print("\n"*2)
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email or '.org' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print("\n"*2)
            print('final', finalemail)
            print("\n"*2)
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_email,
                errback=self.errback_google,
                dont_filter=True,
                meta={'web_name': web_name, 'web_link': web_link, 'web_phone': web_phone,
                      'web_business': web_business, 'site_url': site_url,'links': links,'finalemail': finalemail,'index': index,'web_description':web_description,'web_directon':web_directon}

            )



    def errback_finalemail(self,failure):
        meta=failure.request.meta
        links=meta['links']
        uniqueemail = meta['uniqueemail']
        if(len(links)>0):
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta=meta
            )
        else:
            print("\n"*2)
            print('hello I am in errback_finalemail')
            print("\n"*2)
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email or '.org' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print("\n"*2)
            print('final in errback_finalemail', finalemail)
            print("\n"*2)
            meta['finalemail']=finalemail
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_email,
                errback=self.errback_google,
                dont_filter=True,
                meta=meta
            )


    def errback_emailtrack(self,failure):
        meta = failure.request.meta
        finalemail = []
        meta['finalemail']=finalemail
        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse_email,
            errback=self.errback_google,
            meta=meta,
            dont_filter=True
        )


    def errback_parse_page(self,failure):
        meta=failure.request.meta
        yield SeleniumRequest(
            url='https://www.hotfrog.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse_email,
            meta=meta,
            dont_filter=True
        )

    def errback_hotfrog(self,failure):
        meta=failure.request.meta
        yield SeleniumRequest(
            url='https://www.hotfrog.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            errback=self.errback_hotfrog,
            meta=meta,
            dont_filter=True
        )


    def errback_google(self,failure):
        meta = failure.request.meta
        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse_email,
            errback=self.errback_google,
            meta=meta,
            dont_filter=True
        )

