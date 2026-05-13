def fetch_amazon_images_strict(query, channel_type):
    clean_query = re.sub(r'[^a-zA-Z0-9 ]', '', str(query)).strip()
    print(f"🛒 Amazon se '{clean_query}' ki photos nikal rahi hain...")
    if not RAPIDAPI_KEY: raise Exception("⚠️ RAPIDAPI_KEY Missing in Secrets!")
    url, headers = "https://real-time-amazon-data.p.rapidapi.com/search", {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"}
    try:
        response = requests.get(url, headers=headers, params={"query": clean_query, "page": "1", "country": "IN", "sort_by": "RELEVANCE"}, timeout=40)
        
        # 🟢 यह लाइन आपको असली एरर कोड बताएगी (जैसे 401 या 429)
        if response.status_code != 200:
            print(f"❌ API Status Code: {response.status_code} | Message: {response.text}")
            raise Exception(f"Server rejected Key (Error {response.status_code})")

        image_files = []
        for i, prod in enumerate(response.json().get("data", {}).get("products", [])):
            if len(image_files) >= 6: break
            photo_url = prod.get("product_photo")
            if photo_url:
                img_res = requests.get(photo_url, timeout=15)
                if img_res.status_code == 200:
                    fname = f"amazon_img_{channel_type}_{i}.jpg"
                    with open(fname, "wb") as f: f.write(img_res.content)
                    image_files.append(fname)
        return image_files
    except Exception as e: raise Exception(f"Amazon Fail: {e}")
