import requests
import bs4
import pandas as pd
from datetime import datetime


def get_jobs(soup):
    jobs = []
    elements = soup.find_all(name='a', attrs={'data-tn-element': 'jobTitle'})
    for element in elements:
            jobs.append(element['title'])
    return(jobs)


def get_companies(soup):
    companies = []
    spans = soup.find_all(name='span', attrs={'class': 'company'})
    for span in spans:
        companies.append(span.text)
    return(companies)


def get_locations(soup):
    locations = []
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)
    return(locations)


def get_summaries(soup):
    summaries = []
    spans = soup.findAll('span', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text)
    return(summaries)


def get_ages(soup):
    ages = []
    divs = soup.find_all(name='div', attrs={'class': 'result-link-bar'})
    for div in divs:
        span = div.find(name='span', attrs={'class': 'date'})
        if span is not None:
            ages.append(span.text)
        else:
            ages.append("No age found")
    return(ages)


def get_links(soup):
    links = []
    elements = soup.find_all(name='a', attrs={'data-tn-element': 'jobTitle'})
    for element in elements:
            links.append('www.indeed.com' + str(element['href']))
    return(links)


def does_a_nextpage_exist(soup):
    spans = soup.find_all(name='span', attrs={'class': 'np'})
    for span in spans:
        if 'Next' in span.text:
            nextpage_exists = True
        else:
            nextpage_exists = False
    return(nextpage_exists)


def get_nextpage_url(soup):
    div = soup.find(name='div', attrs={'class': 'pagination'})
    elements = div.find_all(name='a')
    nextpage_url = 'https://www.indeed.com/' + str(list(elements)[-1]['href'])
    return(nextpage_url)


def get_all_parameters_for_all_listings(url):
    response = requests.get(url)
    print(response.status_code)

    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    all_jobs = []
    all_companies = []
    all_locations = []
    all_summaries = []
    all_ages = []
    all_links = []

    page_counter = 1

    while True:
        currentpage_jobs = get_jobs(soup)
        all_jobs.extend(currentpage_jobs)

        currentpage_companies = get_companies(soup)
        all_companies.extend(currentpage_companies)

        currentpage_locations = get_locations(soup)
        all_locations.extend(currentpage_locations)

        currentpage_summaries = get_summaries(soup)
        all_summaries.extend(currentpage_summaries)

        currentpage_ages = get_ages(soup)
        all_ages.extend(currentpage_ages)

        currentpage_links = get_links(soup)
        all_links.extend(currentpage_links)

        # Check to see if this is the last page; if not, move to the next page
        nextpage_exists = does_a_nextpage_exist(soup)
        print(nextpage_exists)
        if nextpage_exists is True:
            page_counter += 1
            print(page_counter)

            nextpage_url = get_nextpage_url(soup)
            print(nextpage_url)

            response = requests.get(nextpage_url)
            print(response.status_code)

            html = response.text
            soup = bs4.BeautifulSoup(html, 'html.parser')

        else:
            break

    print('Print current # of jobs: ' + str(len(all_jobs)))
    print('Print current # of companies: ' + str(len(all_companies)))
    print('Print current # of locations: ' + str(len(all_locations)))
    print('Print current # of summaries: ' + str(len(all_summaries)))
    print('Print current # of ages: ' + str(len(all_ages)))
    print('Print current # of links: ' + str(len(all_links)))

    df_all_parameters = pd.DataFrame(
        {'Job_Title': all_jobs,
         'Company_Name': all_companies,
         'Location': all_locations,
         'Job_Summary': all_summaries,
         'Posting_Age': all_ages,
         'Link': all_links})

    return(df_all_parameters)


search_keyword = 'firefighter'
search_location = 'Bay Area, CA'
search_query = 'jobs?q=' + search_keyword + '&l=' + search_location
search_url = 'https://www.indeed.com/' + search_query
print(search_url)

df_all_parameters = get_all_parameters_for_all_listings(search_url)
current_date = datetime.now()

df_all_parameters.to_csv(
    current_date.strftime('%Y-%m-%d') + '_' + search_keyword.upper() + '.csv'
    )
