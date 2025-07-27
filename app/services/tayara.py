import requests
from app.models.cleanText import clean

class Tayara:
    def __init__(self,query,page,category):
        self.query= query
        self.category= category
        self.base_url = f"https://www.tayara.tn/_next/data/dilyNx2OF-AueFH__c0OX/en/ads.json?page={page}&category={category}&q={query}"
    
    def fetch_json(self,page):
        url = self.base_url.format(page=page,category=self.category,query=self.query)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else :
                response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] FAILED TO FETCH PAGE {page}:{e}")
    
    def get_description(self, max_page=5):
        result = []
        for page in range (1,max_page +1):
            data = self.fetch_json(page)
            if data :
                ads = data.get("pageProps", {}).get("searchedListingsAction", {}).get("newHits", [])
                result = [{
                    "id": ad.get("id"),
                    "title": ad.get("title"),
                    "description": clean(ad.get("description")).clean_text(),
                    "images": ad.get("images", []),
                    "price": ad.get("price"),
                    "publisher_name": ad.get("metadata", {}).get("publisher", {}).get("name"),
                    "governorate": ad.get("location", {}).get("governorate"),
                    "delegation": ad.get("location", {}).get("delegation")
                } for ad in ads]
        return result
    
    def search (self,page=1):
        result = []
        data = self.fetch_json(page)
        if data:
            ads = data.get("pageProps", {}).get("searchedListingsAction", {}).get("newHits", [])
            result = [{
                "title":ad.get("title"),
                "description": ad.get("description"),
                "images": ad.get("images", []),
                "price": ad.get("price"),
                "publisher_name": ad.get("metadata", {}).get("publisher", {}).get("name"),
                "governorate": ad.get("location", {}).get("governorate"),
                "delegation": ad.get("location", {}).get("delegation")

            }for ad in ads]
        return result
    