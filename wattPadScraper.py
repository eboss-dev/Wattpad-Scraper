from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    
    # Opens the links.txt file.
    with open('links.txt', 'r', encoding='utf-8') as cd:
        
        # Run the readlines() method and store the list in storyLinks
        story_links = cd.readlines()
        
        # Loop through each story link in the list.
        for story_link in story_links:
            
            # Assign the empty variables
            text_paragraph = ""
            chapter_links = []
            
            # Open the story's main page
            page.goto(story_link)

            # Query all of the selectors that contain the href for the chapters
            story_parts = page.locator('[aria-label="story-parts"]')
            import time
            time.sleep(2)
            a_ref = story_parts.locator('a')
            print(a_ref.count())
            for i in range(a_ref.count()):
                elem = a_ref.nth(i)
                chapter_links.append(elem.get_attribute("href"))

            print(f"Chapter to retrieve: {chapter_links}")
            for chapter_link in chapter_links:
                print(f"Opening {chapter_link}")

                page.goto(chapter_link)
                
                # Query all paragraph selectors in the pre tag. This holds the story text
                paragraphs = page.query_selector_all('pre >> p')
                print("Paragraphs retrieved")
                # Loop through the selectors and add assign the text content onto the text_paragraph variable
                for paragraph in paragraphs:
                    
                    text_paragraph += paragraph.text_content()
                
                # Open the wattPadExport text file, then replace the + symbol that gets scraped, and write the scraped
                # text content from the story. Then write new lines to seperate the next story.
                import re
                story_link_number = re.sub(r'\D', '', story_link)
                with open(f'{story_link_number}.txt', 'w', encoding="utf-8", newline='\n') as cd:

                    text_paragraph = text_paragraph.replace('  +', '')
                    cd.write(text_paragraph + '\n\n\n\n')

            # ---------------------
        context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
