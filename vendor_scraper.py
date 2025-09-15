import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
import pandas as pd
# Selenium imports commented out for basic version
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings('ignore')

class VendorScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.vendors = []
    
    def scrape_indiamart_vendors(self, material_type, location="Maharashtra"):
        """Scrape vendor information from IndiaMART (simulated for demo)"""
        print(f"Searching for {material_type} vendors in {location}...")
        
        # Simulated vendor data (in real implementation, this would scrape actual websites)
        simulated_vendors = {
            "Steel Reinforcement Bars": [
                {
                    "name": "Mumbai Steel Works Pvt Ltd",
                    "location": "Mumbai, Maharashtra",
                    "contact": "+91-22-2345-6789",
                    "email": "info@mumbaisteel.com",
                    "services": ["Steel Reinforcement Bars", "TMT Bars", "Structural Steel"],
                    "rating": 4.5,
                    "years_experience": 15,
                    "website": "www.mumbaisteel.com"
                },
                {
                    "name": "Pune Iron & Steel Co.",
                    "location": "Pune, Maharashtra", 
                    "contact": "+91-20-3456-7890",
                    "email": "sales@puneiron.com",
                    "services": ["Steel Bars", "Iron Products", "Metal Fabrication"],
                    "rating": 4.2,
                    "years_experience": 12,
                    "website": "www.puneiron.com"
                },
                {
                    "name": "Nashik Steel Industries",
                    "location": "Nashik, Maharashtra",
                    "contact": "+91-253-456-7891", 
                    "email": "contact@nashiksteel.com",
                    "services": ["TMT Bars", "Steel Reinforcement", "Construction Steel"],
                    "rating": 4.0,
                    "years_experience": 10,
                    "website": "www.nashiksteel.com"
                }
            ],
            "Concrete Mix": [
                {
                    "name": "Maharashtra Concrete Solutions",
                    "location": "Mumbai, Maharashtra",
                    "contact": "+91-22-4567-8901",
                    "email": "info@mahaconcrete.com",
                    "services": ["Ready Mix Concrete", "Precast Concrete", "Concrete Pumping"],
                    "rating": 4.6,
                    "years_experience": 20,
                    "website": "www.mahaconcrete.com"
                },
                {
                    "name": "Pune Ready Mix Ltd",
                    "location": "Pune, Maharashtra",
                    "contact": "+91-20-5678-9012", 
                    "email": "orders@punereadymix.com",
                    "services": ["Ready Mix Concrete", "Concrete Supply", "Quality Testing"],
                    "rating": 4.3,
                    "years_experience": 18,
                    "website": "www.punereadymix.com"
                }
            ],
            "Electrical Cables": [
                {
                    "name": "Maharashtra Cables & Wires",
                    "location": "Aurangabad, Maharashtra",
                    "contact": "+91-240-234-5678",
                    "email": "sales@mahacables.com", 
                    "services": ["Power Cables", "Control Cables", "Fiber Optic Cables"],
                    "rating": 4.4,
                    "years_experience": 14,
                    "website": "www.mahacables.com"
                },
                {
                    "name": "Western India Electricals",
                    "location": "Mumbai, Maharashtra",
                    "contact": "+91-22-6789-0123",
                    "email": "info@wielectricals.com",
                    "services": ["Electrical Cables", "Switchgear", "Electrical Components"],
                    "rating": 4.1,
                    "years_experience": 16,
                    "website": "www.wielectricals.com"
                }
            ],
            "HVAC Equipment": [
                {
                    "name": "Cool Air Systems Maharashtra",
                    "location": "Pune, Maharashtra", 
                    "contact": "+91-20-7890-1234",
                    "email": "info@coolair.com",
                    "services": ["HVAC Systems", "Air Conditioning", "Ventilation Equipment"],
                    "rating": 4.5,
                    "years_experience": 22,
                    "website": "www.coolair.com"
                },
                {
                    "name": "Mumbai Climate Control",
                    "location": "Mumbai, Maharashtra",
                    "contact": "+91-22-8901-2345",
                    "email": "sales@mumbaiclimate.com", 
                    "services": ["HVAC Installation", "Climate Control", "Maintenance Services"],
                    "rating": 4.2,
                    "years_experience": 19,
                    "website": "www.mumbaiclimate.com"
                }
            ]
        }
        
        # Return vendors for the specified material type
        return simulated_vendors.get(material_type, [])
    
    def scrape_justdial_vendors(self, material_type, location="Maharashtra"):
        """Scrape vendor information from JustDial (simulated for demo)"""
        print(f"Searching JustDial for {material_type} vendors in {location}...")
        
        # Additional simulated vendors from JustDial
        justdial_vendors = {
            "Steel Reinforcement Bars": [
                {
                    "name": "Shree Steel Trading Co.",
                    "location": "Thane, Maharashtra",
                    "contact": "+91-22-9012-3456", 
                    "email": "shreesteel@gmail.com",
                    "services": ["Steel Bars", "TMT Bars", "Steel Trading"],
                    "rating": 3.8,
                    "years_experience": 8,
                    "website": "www.shreesteel.in"
                }
            ],
            "Concrete Mix": [
                {
                    "name": "Reliable Concrete Works",
                    "location": "Nagpur, Maharashtra",
                    "contact": "+91-712-345-6789",
                    "email": "reliable@concrete.com", 
                    "services": ["Concrete Supply", "RMC", "Concrete Testing"],
                    "rating": 4.0,
                    "years_experience": 12,
                    "website": "www.reliableconcrete.com"
                }
            ]
        }
        
        return justdial_vendors.get(material_type, [])
    
    def get_comprehensive_vendor_list(self, material_type, location="Maharashtra"):
        """Get vendors from multiple sources"""
        all_vendors = []
        
        # Get vendors from different sources
        indiamart_vendors = self.scrape_indiamart_vendors(material_type, location)
        justdial_vendors = self.scrape_justdial_vendors(material_type, location)
        
        all_vendors.extend(indiamart_vendors)
        all_vendors.extend(justdial_vendors)
        
        # Sort by rating (descending)
        all_vendors.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        return all_vendors
    
    def save_vendors_to_json(self, vendors, filename):
        """Save vendor data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(vendors, f, indent=2, ensure_ascii=False)
        print(f"Vendor data saved to {filename}")
    
    def save_vendors_to_csv(self, vendors, filename):
        """Save vendor data to CSV file"""
        df = pd.DataFrame(vendors)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Vendor data saved to {filename}")
    
    def display_vendor_info(self, vendors):
        """Display vendor information in a formatted way"""
        if not vendors:
            print("No vendors found.")
            return
        
        print(f"\nFound {len(vendors)} vendors:")
        print("=" * 80)
        
        for i, vendor in enumerate(vendors, 1):
            print(f"{i}. {vendor['name']}")
            print(f"   Location: {vendor['location']}")
            print(f"   Contact: {vendor['contact']}")
            print(f"   Email: {vendor['email']}")
            print(f"   Rating: ⭐ {vendor['rating']}/5.0")
            print(f"   Experience: {vendor['years_experience']} years")
            print(f"   Services: {', '.join(vendor['services'])}")
            print(f"   Website: {vendor['website']}")
            print("-" * 80)

def main():
    scraper = VendorScraper()
    
    # Material types to search for
    materials = [
        "Steel Reinforcement Bars",
        "Concrete Mix", 
        "Electrical Cables",
        "HVAC Equipment"
    ]
    
    all_vendor_data = {}
    
    for material in materials:
        print(f"\n🔍 Searching for {material} vendors...")
        vendors = scraper.get_comprehensive_vendor_list(material, "Maharashtra")
        all_vendor_data[material] = vendors
        
        scraper.display_vendor_info(vendors)
        
        # Save individual material vendor data
        filename_json = f"vendors_{material.replace(' ', '_').lower()}.json"
        filename_csv = f"vendors_{material.replace(' ', '_').lower()}.csv"
        
        scraper.save_vendors_to_json(vendors, filename_json)
        scraper.save_vendors_to_csv(vendors, filename_csv)
        
        time.sleep(1)  # Be respectful to websites
    
    # Save comprehensive vendor database
    scraper.save_vendors_to_json(all_vendor_data, "comprehensive_vendor_database.json")
    
    # Create a summary CSV with all vendors
    all_vendors_flat = []
    for material, vendors in all_vendor_data.items():
        for vendor in vendors:
            vendor_copy = vendor.copy()
            vendor_copy['material_type'] = material
            all_vendors_flat.append(vendor_copy)
    
    scraper.save_vendors_to_csv(all_vendors_flat, "all_vendors_summary.csv")
    
    print(f"\n✅ Vendor scraping completed!")
    print(f"📊 Total vendors found: {len(all_vendors_flat)}")
    print(f"📁 Files generated:")
    print(f"   - comprehensive_vendor_database.json")
    print(f"   - all_vendors_summary.csv") 
    print(f"   - Individual material vendor files")

if __name__ == "__main__":
    main()