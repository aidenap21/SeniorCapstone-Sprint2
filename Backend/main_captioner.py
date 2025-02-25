from Backend.create_caption import create_caption
from Backend.web_scraper import scrape
from Backend.csv_to_pdf import create_pdf
import csv
import time

def caption_site(url, output_name='site'):
    site_data = scrape(url)

    if site_data is None:
        return

    with open(f"outputs/{output_name}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write a header row (optional)
        writer.writerow(["image_link", "generated_output"])
        
        for image, text in site_data:
            writer.writerow([
                image,
                create_caption(image, text, URL=True)
            ])

if __name__ == "__main__":
    start_time = time.time()
    
    output_name = "lied_center"
    site_url = "https://lied.ku.edu"
    caption_site(site_url, output_name=output_name)
    create_pdf("outputs/"+output_name)
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
