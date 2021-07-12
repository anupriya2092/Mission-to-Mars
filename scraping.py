#import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {"news_title" : news_title,
            "news_paragraph": news_paragraph,
            "featured_image" : featured_image(browser),
            "facts" : mars_facts(),
            "hemispheres" : hemisphere_images(browser),
            "last_modified" : dt.datetime.now()}
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = "https://redplanetscience.com"
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("div.list_text",wait_time = 1)

    html = browser.html
    news_soup = soup(html,"html.parser")
    # Add try/except for error handling
    try:
        #slide_elem = news_soup.find("div", class_="list_text")
        slide_elem = news_soup.select_one("div.list_text")

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        #find the summary for the title
        news_p = slide_elem.find("div",class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Featured Images
def featured_image(browser):
    #visit url to get images
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button usinf browser
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try :
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"

    return img_url

# ## Mars Facts
def mars_facts():
    try:
        #collect facts about Mars from tabular format
        df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe

    df.columns = ['Description', 'Mars', 'Earth']
    df = df.drop([0])
    df.set_index('Description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes='table table-striped table-hover').replace("<thead>", "<thead class='bg-info'>").replace("<tbody>", "<tbody class='bg-success'>")

## Hemisphere images
def hemisphere_images(browser):
    #  Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    html = browser.html
    hemi_soup = soup(html, 'html.parser')

    #Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #code to retrieve the image urls and titles for each hemisphere.
    hemisphere_links = hemi_soup.find_all('div', class_='description')
    try:

        for link in hemisphere_links:
            h3 = link.find("h3").get_text()

            browser.links.find_by_partial_text(h3).click()
            image = {}
            
            sample = browser.find_by_text("Sample")
            url = sample["href"]
            
            title = browser.find_by_css('h2[class="title"]')
            
            image["img_url"] = url
            image["title"] = title.value
            hemisphere_image_urls.append(image)

            browser.back()
            
    except AttributeError:
        return None        
    
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
