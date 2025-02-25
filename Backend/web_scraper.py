from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re

def scrape(url):  # URL -> List of scraped data
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening browser

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)  # Change to your target site

    time.sleep(3)  # Allow JavaScript to load content

    image_text_data = []
    
    # Find all standard images
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        try:
            img_url = img.get_attribute("src")
            alt_text = img.get_attribute("alt") or ""  # Extract alt text

            # Get text from the closest paragraph (<p>), div, or span before & after the image
            prev_text = ""
            next_text = ""

            try:
                prev_text = img.find_element(By.XPATH, "preceding::p[1] | preceding::div[1] | preceding::span[1]").text.strip()
            except:
                pass

            try:
                next_text = img.find_element(By.XPATH, "following::p[1] | following::div[1] | following::span[1]").text.strip()
            except:
                pass

            # Get text from multiple levels of parent elements
            parent_text = ""
            parent = img
            for _ in range(3):  # Check up to 3 levels up
                try:
                    parent = parent.find_element(By.XPATH, "..")
                    parent_text = parent.text.strip()
                    if parent_text:
                        break  # Stop if we find valid text
                except:
                    break

            # Combine all text sources
            surrounding_text = " ".join(filter(None, [alt_text, prev_text, parent_text, next_text]))
            image_text_data.append((img_url, surrounding_text))

        except Exception as e:
            print(f"Error processing image: {e}")
    
    # Find Revolution Slider images (which use divs with background images)
    rev_slider_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'rev_slider') or contains(@class, 'tp-bgimg')]")
    for div in rev_slider_divs:
        try:
            style = div.get_attribute("style")
            match = re.search(r'url\((.*?)\)', style)
            if match:
                img_url = match.group(1).strip('"')
                
                # Get text from surrounding elements
                parent_text = ""
                parent = div
                for _ in range(3):  # Check up to 3 levels up
                    try:
                        parent = parent.find_element(By.XPATH, "..")
                        parent_text = parent.text.strip()
                        if parent_text:
                            break  # Stop if we find valid text
                    except:
                        break
                
                image_text_data.append((img_url, parent_text))
        
        except Exception as e:
            print(f"Error processing Revolution Slider image: {e}")
    
    driver.quit()
    return image_text_data

if __name__ == "__main__":
    site_data = scrape("https://lied.ku.edu/?event=mnozil-brass-2025&event_date=2025-03-03%2019:30")
    for item in site_data:
        print(f"Image: {item[0]}\nText: {item[1]}\n{'-'*50}")
