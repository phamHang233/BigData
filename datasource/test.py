import argparse
import json
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

response = requests.get("https://www.careerlink.vn/tim-viec-lam/nhan-vien-ho-tro-ky-thuat-dtdd-laptop-chau-thanh-an-giang/2737347?source=site")
soup = BeautifulSoup(response.content, "html.parser")
summarize = soup.find('p', class_="org-name mb-2")
print(summarize.get_text())

# In mảng nội dung văn bản


