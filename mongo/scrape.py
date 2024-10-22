import googlemaps
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Date of Creation: 14th October 2024
# Author: Victor Baron
# Salutation: Instagram followers and posts added for Khanna Ji!

API_KEY = 'AIzaSyAwLB3TGsHTItz3iZQAfg1OhsM4L2dKzrk'  # Insert your API key here

gmaps = googlemaps.Client(key=API_KEY)

# Helper function to check if a place is new (opened within the last 2 years)
def is_place_new(reviews):
    if reviews:
        # Sort reviews by time and get the earliest one
        earliest_review_time = min(review['time'] for review in reviews)
        earliest_review_date = datetime.utcfromtimestamp(earliest_review_time)
        # Check if it's within the last 2 years
        two_years_ago = datetime.utcnow() - timedelta(days=365 * 2)
        if earliest_review_date > two_years_ago:
            return '✓'  # New
        else:
            return '✗'  # Old
    return '✗'  # No reviews, assume old

def get_instagram_data(instagram_url):
    try:
        response = requests.get(instagram_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the meta tag with property='og:description'
        meta_tag = soup.find('meta', property='og:description')
        
        if meta_tag and 'content' in meta_tag.attrs:
            # Extract content from meta tag
            content = meta_tag['content']
            parts = content.split('-')
            if len(parts) >= 2:
                # Extract followers and posts count from the description
                followers = parts[0].strip().split(' ')[0].replace(',', '')
                posts = parts[1].strip().split(' ')[0].replace(',', '')
                return followers, posts
        return 'N/A', 'N/A'
    
    except (requests.RequestException, AttributeError):
        return 'N/A', 'N/A'  # Return N/A if unable to scrape


def get_places(location, place_type, category_name):
    # Search for places like resorts, lounges, or cafes
    places_result = gmaps.places_nearby(location=location, radius=5000, type=place_type)
    
    places_info = []
    
    for place in places_result['results']:
        place_name = place['name']
        place_address = place.get('vicinity', 'Address not found')
        place_id = place['place_id']
        
        # Get detailed info using Place ID
        details = gmaps.place(place_id=place_id, fields=['website', 'formatted_phone_number', 'opening_hours', 'formatted_address', 'url', 'reviews', 'user_ratings_total'])
        
        website_url = details['result'].get('website', 'No website found')
        phone_number = details['result'].get('formatted_phone_number', 'No phone number found')
        opening_hours = details['result'].get('opening_hours', {}).get('weekday_text', 'No opening hours found')
        full_address = details['result'].get('formatted_address', place_address)
        reviews = details['result'].get('reviews', [])
        number_of_reviews = details['result'].get('user_ratings_total', 'No reviews')
        
        # Try to find Instagram from the website
        instagram_id = scrape_instagram_from_website(website_url) if website_url != 'No website found' else 'No website'
        
        # Check if the place is new (opened within the last 2 years)
        new_status = is_place_new(reviews)
        
        # Scrape Instagram followers and posts count
        followers_count, posts_count = get_instagram_data(instagram_id) if instagram_id != 'No website' else ('N/A', 'N/A')
        
        places_info.append({
            'Name': place_name,
            'Category': category_name,
            'Address': full_address,
            'Phone Number': phone_number,
            'Opening Hours': opening_hours,
            'Website': website_url,
            'Instagram': instagram_id,
            'No. of Google Reviews': number_of_reviews,
            'New': new_status,
            'Instagram Followers': followers_count,
            'Instagram Posts': posts_count
        })
    
    return places_info

def scrape_instagram_from_website(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find Instagram links
        instagram_link = soup.find('a', href=lambda href: href and 'instagram.com' in href)
        if instagram_link:
            return instagram_link['href']
        else:
            return 'Instagram not found'
    except requests.RequestException:
        return 'Failed to scrape website'

def save_to_excel(places_info, area_name):
    df = pd.DataFrame(places_info)
    filename = f"{area_name}_places_info.xlsx"
    df.to_excel(filename, index=False)
    print(f"Data has been saved to {filename} successfully!")

if __name__ == "__main__":
    area_name = input("Enter the area name (e.g., Modinagar, UP): ")
    # Geocode to get latitude and longitude
    geocode_result = gmaps.geocode(area_name)
    
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        
        # Search for resorts, lounges, and cafes
        print(f"\nFetching results for {area_name}...\n")
        categories = {
            'resort': 'Resort',
            'cafe': 'Cafe',
            'night_club': 'Lounge'  # For lounges, night_club is used
        }
        
        all_places_info = []
        
        for category_key, category_name in categories.items():
            print(f"\nPlaces in category: {category_name}:\n")
            places = get_places(location, category_key, category_name)
            all_places_info.extend(places)
            
            for place in places:
                print(f"Name: {place['Name']}")
                print(f"Category: {place['Category']}")
                print(f"Address: {place['Address']}")
                print(f"Phone Number: {place['Phone Number']}")
                print(f"Opening Hours: {place['Opening Hours']}")
                print(f"Website: {place['Website']}")
                print(f"Instagram: {place['Instagram']}")
                print(f"No. of Google Reviews: {place['No. of Google Reviews']}")
                print(f"New: {place['New']}")
                print(f"Instagram Followers: {place['Instagram Followers']}")
                print(f"Instagram Posts: {place['Instagram Posts']}\n")
        
        # Save to Excel
        save_to_excel(all_places_info, area_name)
        
    else:
        print("Location not found!")
