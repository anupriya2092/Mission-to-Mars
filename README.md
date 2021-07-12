# Mission-to-Mars
Web Scraping from different Mars websites using tools like Splinter and Beautiful soup.

## Purpose and Overview of the project
1. The main purpose of the project is to build a web application that will scrape new data every time with the click of a button.

2. For this, we will use splinter to automate the web browser to visit different websites to extract data about the mission to mars. 

3. Also we have used the chrome developer tools to identify the HTML components attached to the data we want.

4. We have scraped the data from different websites using beautiful soup and its HTML parser. We looped through this parsed data to get the desired results.

5. Our python script contains data that we retrieved from different websites and then finally we added this data to our Mongo database which is a non SQL database. So every time
   we click the scrape button the database gets updated with the new and latest data.
   
6. WE have used flask to create a web application and used Pymongo to setup the connection between the python script and the mongo database. We used the rendered template from
   HTML to build and style our webpage.We have also incorporated bootstrap in our HTML code so our webpage is compatible with all devices and also used most of the bootstrap components
   that make our code easy to read and understand.
   
7. Our webpage displays all the facts about mars in the from of a table, most recent news article about mars and also the mars images.