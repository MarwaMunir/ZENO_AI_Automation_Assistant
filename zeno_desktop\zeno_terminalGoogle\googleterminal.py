import os
import requests
import webbrowser
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Cache to store results temporarily
SEARCH_CACHE = {}

def search_google_links(query, num_results=5):
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "num": 10,
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("organic_results", [])
        links = [res.get("link") for res in results if "link" in res]

        def rank(url):
            if "github.com" in url:
                return 1
            elif "stackoverflow.com" in url:
                return 2
            return 3

        sorted_links = sorted(links, key=rank)[:3]
        SEARCH_CACHE["last_results"] = sorted_links
        return sorted_links
    except Exception as e:
        print("Error during search:", e)
        return []

def open_result_by_number(number: int):
    results = SEARCH_CACHE.get("last_results", [])
    idx = number - 1
    if 0 <= idx < len(results):
        webbrowser.open(results[idx])
        return results[idx]
    else:
        return None


def main():
    query = input("🔍 What would you like to search? ")
    results = search_google_links(query, num_results=5)

    if not results:
        print("❌ No results found or API error.")
        return

    print("\n📄 Top Results:")
    for idx, url in enumerate(results, 1):
        print(f"{idx}. {url}")

    try:
        choice = int(input("\n➡️ Enter the number of the result you want to open (0 to cancel): "))
        if choice == 0:
            print("❎ Cancelled.")
            return

        selected_url = open_result_by_number(choice)
        if selected_url:
            print(f"✅ Opened: {selected_url}")
        else:
            print("⚠️ Invalid number selected.")
    except ValueError:
        print("❌ Please enter a valid number.")

if __name__ == "__main__":
    main()
    


 
   
