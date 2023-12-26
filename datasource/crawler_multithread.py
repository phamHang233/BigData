import argparse
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def get_list_link(start, end):
    links = []
    for i in range(start, end + 1):
        links.append(f"https://www.careerlink.vn/vieclam/list?category_ids=130%2C19&page={i}")
    return links


def get_titles(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all('a', class_="job-link clickable-outside")
    return titles


def crawl_content(link):
    data = {}
    news = requests.get(f"https://www.careerlink.vn{link}")
    soup = BeautifulSoup(news.content, "html.parser")

    names_obj = soup.find('h1', class_="job-title mb-0")
    if names_obj is None:
        return None

    job_names = names_obj.text
    data['tên công việc'] = job_names

    company_name = soup.find('p', class_="org-name mb-2")
    data['tên công ty'] = company_name.get_text()

    # ... (các phần xử lý khác giữ nguyên)

    return data


def crawl_contents(filename, links_company):
    job_info = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(crawl_content, links_company))

    for result in results:
        if result is not None:
            job_info.append(result)

    with open(filename, 'w') as f:
        json.dump(job_info, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("Parsing Args")
    parser = argparse.ArgumentParser()
    parser.add_argument("start")
    parser.add_argument("end")
    args = parser.parse_args()

    print("Start crawling from", args.start, "to", args.end)
    links = get_list_link(int(args.start), int(args.end))
    print("get list link")

    with ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(get_titles, links))

    links_company = [link['href'] for title in titles for link in title]
    print("get all link of company")

    filename = f"result/recruit_{args.start}_{args.end}.json"
    crawl_contents(filename, links_company)
