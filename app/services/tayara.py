import os
import uuid
import requests
from app.models.cleanText import clean
import pandas as pd

class Tayara:
    def __init__(self,query,page,category):
        self.query= query
        self.category= category
        self.page= page
    
    def fetch_json(self,page):
        url = (
            f"https://www.tayara.tn/_next/data/dilyNx2OF-AueFH__c0OX/en/ads.json"
            f"?page={self.page}&category={self.category}&q={self.query}"
        )

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else :
                response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] FAILED TO FETCH PAGE {page}:{e}")
    
    def get_description(self, max_page):
        result = []
        for page in range (1,max_page +1):
            data = self.fetch_json(page)
            if data :
                ads = data.get("pageProps", {}).get("searchedListingsAction", {}).get("newHits", [])
                result.extend ( [{
                    "id": ad.get("id"),
                    "title": ad.get("title"),
                    "description": clean(ad.get("description")).clean_text(),
                    "images": ad.get("images", []),
                    "price": ad.get("price"),
                    "publisher_name": ad.get("metadata", {}).get("publisher", {}).get("name"),
                    "governorate": ad.get("location", {}).get("governorate"),
                    "delegation": ad.get("location", {}).get("delegation")
                } for ad in ads])
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
    
    def export_to_excel(result: list[dict])-> str:
        export_data= []
        for res in result:
            export_data.append({
                "Title": res["title"],
                "Description": res["description"],
                "Price": res["price"],
                "Publisher": res["publisher_name"],
                "Governorate": res["governorate"],
                "Delegation": res["delegation"],
                "Images": "\n".join(res["images"])

            })
        df = pd.DataFrame(export_data)
        os.makedirs("exports", exist_ok=True)
        file_name=f"export_tayara_{uuid.uuid4().hex[:8]}.xlsx"
        file_path=os.path.join("exports",file_name)
        df.to_excel(file_path,index=False)
        return file_path 
