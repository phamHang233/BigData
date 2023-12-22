import argparse
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

response = requests.get("https://www.careerlink.vn/tim-viec-lam/nhan-vien-ho-tro-ky-thuat-dtdd-laptop-chau-thanh-an-giang/2737347?source=site")
soup = BeautifulSoup(response.content, "html.parser")
summarize = soup.find('div', class_="row job-summary d-flex")
labels = summarize.find_all('div', class_='my-0 summary-label')
for indx, label in enumerate(labels):
    if 'Loại công việc' in label.get_text():
        loai_con_viec= label.find_next_sibling('div').get_text()
    elif 'Cấp bậc' in label.get_text():
        cap_bac = label.find_next_sibling('div').get_text()
    elif 'Học vấn' in label.get_text():
        hoc_van = label.find_next_sibling("div").get_text()
    elif 'Giới tính' in label.get_text():
        gioi_tinh = label.find_next_sibling('div').get_text()
    elif 'Tuổi' in label.get_text():
        tuoi = label.find_next_sibling('div').get_text()


# In mảng nội dung văn bản


