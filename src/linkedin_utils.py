from time import sleep

from parsel import Selector
from tqdm import tqdm

import parameters


def login_user(args, driver):
    driver.get(parameters.URLS['login'])
    username = driver.find_element_by_id('username')
    username.send_keys(args.email)
    sleep(0.5)

    password = driver.find_element_by_id('password')
    password.send_keys(args.password)
    sleep(0.5)

    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    sleep(0.5)


def get_urls_of_group_members(group_ids, driver):
    profile_urls = list()
    group_ids = group_ids.split(',')

    for group_id in group_ids:
        driver.get(parameters.URLS['group'].format(group_id.strip()))
        sleep(3)

        group_profile_urls = driver.find_elements_by_class_name('ui-entity-action-row__link')
        profile_urls += [url.get_attribute('href') for url in group_profile_urls]
        sleep(0.5)
    return profile_urls


def scrape_profiles(driver, profile_urls):
    members = list()
    for profile_url in tqdm(profile_urls):
        member = dict()
        driver.get(profile_url)
        sleep(5)
        sel = Selector(text=driver.page_source)

        member['name'] = ' '.join(
            sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split())
        member['position'] = ' '.join(
            sel.xpath('//*[@class = "mt1 t-18 t-black t-normal"]/text()').extract_first().split())
        experience = sel.xpath('//*[@class = "pv-top-card--experience-list"]')
        company = experience.xpath('.//a[@data-control-name = "position_see_more"]//span/text()').extract_first()
        member['company'] = ''.join(company.split()) if company else None
        education = experience.xpath('.//a[@data-control-name = "education_see_more"]//span/text()').extract_first()
        member['education'] = ' '.join(education.split()) if education else None
        member['location'] = ' '.join(
            sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

        member['url'] = driver.current_url
        members.append(member)

    return members
