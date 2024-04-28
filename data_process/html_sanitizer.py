

# def flatten_divs(soup):
#     """Flatten nested divs that do not contribute to content or structure."""
#     divs = soup.find_all("div", recursive=True)
#     for div in divs:
#         while div.find_all("div", recursive=False) == 1 and not meaningful_attributes(div):
#             child = div.find("div")
#             div.replace_with(child)


# def contains_important_content(div):
#     """Check if the div contains important elements like text, input fields, or other interactive elements."""
#     if div.get_text(strip=True):
#         return True
#     interactive_tags = ['input', 'textarea', 'select', 'button', 'a', 'label', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
#     return any(div.find(tag) for tag in interactive_tags)


# def extract_important_divs(soup):
#     """Extract divs containing important content or elements."""
#     important_divs = []
#     for div in soup.find_all("div"):
#         if contains_important_content(div):
#             important_divs.append(div)
#     new_soup = BeautifulSoup('', 'html.parser')
#     for div in important_divs:
#         new_soup.append(div.extract())
#     return new_soup

from bs4 import NavigableString, Comment
import re
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime

# def remove_empty_divs(soup):
#     """Remove all divs that have no meaningful content and keep checking until no empty divs remain."""
#     changes = True
#     while changes:
#         changes = False  # Reset change flag on each pass
#         for div in soup.find_all("div", recursive=True):
#             # Check if the div only contains <br>, whitespaces, or is completely empty
#             if (not div.contents or
#                 all((isinstance(c, (NavigableString, Comment)) and not c.strip()) or 
#                     (c.name == 'br') for c in div.contents)):
#                 div.decompose()
#                 changes = True  # Continue while loop if changes are made


def remove_divs_with_aria_hidden(soup):
    """Remove all div elements with aria-hidden="true" from the HTML content."""
    
    # Find all div elements with aria-hidden="true"
    for div in soup.find_all("div", {"aria-hidden": "true"}):
        div.decompose()  # Remove the div from the soup


def remove_tags_with_type_hidden(soup):
    """
    Removes all tags with a 'type="hidden"' attribute from the BeautifulSoup object.

    Args:
    soup: The BeautifulSoup object.
    """
    # Find all tags with the 'type="hidden"' attribute
    hidden_tags = soup.find_all(attrs={"type": "hidden"})
    for tag in hidden_tags:
        tag.decompose()  # Remove the tag from the soup


def remove_noscript_tags(soup):
    """
    Removes all <noscript> tags from the BeautifulSoup object.

    Args:
    soup: The BeautifulSoup object.
    """
    noscript_tags = soup.find_all('noscript')
    for tag in noscript_tags:
        tag.decompose()  # This removes the tag from the soup
            
            
def remove_empty_list_items(soup):
    """Remove all empty <li> elements from the HTML content."""
    # Iterate over all <li> elements
    for li in soup.find_all("li"):
        # Check if the <li> is effectively empty
        if not li.get_text(strip=True) and not any(child for child in li.children if isinstance(child, NavigableString) and child.strip()):
            li.decompose()  # Remove the <li> if it's empty
            
            
def remove_empty_sections(soup):
    """Remove all empty <section> elements from the HTML content."""
    for section in soup.find_all("section"):
        if not section.contents or all(isinstance(c, (NavigableString, Comment)) and not c.strip() for c in section.contents):
            section.decompose()


def remove_empty_spans(soup):
    """Remove all empty <span> elements from the HTML content."""
    # Iterate over all <span> elements
    for span in soup.find_all("span"):
        # Check if the <span> is effectively empty
        if not span.get_text(strip=True) and not any(child for child in span.children if not isinstance(child, NavigableString) or child.strip()):
            span.decompose()  # Remove the <span> if it's empty


def remove_elements_with_country_codes(soup, tags=('li', 'button')):
    """
    Removes specified tags containing country codes or numeric codes.

    Args:
    soup: The BeautifulSoup object.
    tags: Tuple of tag names to check for numeric codes.
    """
    country_code_pattern = re.compile(r'\+\d+')

    for tag_name in tags:
        elements = soup.find_all(tag_name)
        for element in elements:
            if country_code_pattern.search(element.get_text()):
                # If a country code is found, decompose the highest parent specified in 'tags'
                highest_parent = element
                while highest_parent.parent and highest_parent.parent.name in tags:
                    highest_parent = highest_parent.parent
                highest_parent.decompose()



def remove_elements_with_long_text(soup, max_length):
    """
    Removes elements with text content longer than 'max_length'.

    Args:
    soup: The BeautifulSoup object.
    max_length: The maximum allowed length of text content.
    """
    # Find all elements
    all_elements = soup.find_all('p')  # 'True' finds all tags
    for element in all_elements:
        # Check if the text content of the element is longer than the max_length
        if len(element.get_text(strip=True)) > max_length:
            element.decompose()  # Remove the element from the soup
            
            
def remove_elements_by_keywords(soup, keywords):
    """
    Removes elements that contain specific keywords in their text or within specific attributes like class or id.

    Args:
    soup: The BeautifulSoup object.
    keywords: List of keywords to search for in elements' text or attributes.
    """
    import re
    # Combine the keywords into a regular expression
    keywords_regex = '|'.join(keywords)

    # Find all elements containing the keyword in their text
    for element in soup.find_all(text=re.compile(keywords_regex, re.IGNORECASE)):
        element.extract()

    # Find all elements with attributes containing the keyword
    for element in soup.find_all(lambda tag: any(re.search(keywords_regex, str(tag.get(attr)), re.IGNORECASE) for attr in ['id', 'class', 'name', 'data-role'] if tag.get(attr))):
        element.decompose()
def remove_placeholder_links(soup):
    """
    Removes <a> tags that have a href attribute set to "#" indicating a placeholder link.

    Args:
    soup: The BeautifulSoup object.
    """
    # Find all <a> tags with href attributes equal to "#"
    for a_tag in soup.find_all('a', href="#"):
        a_tag.decompose()  # Remove the <a> tag
  
        
def remove_links_by_keyword(soup, keywords):
    """
    Removes <a> tags that contain specified keywords in their href attributes.

    Args:
    soup: The BeautifulSoup object.
    keywords: List of keywords to search for in href attributes.
    """
    # Compile a regular expression from the keywords
    keyword_regex = re.compile('|'.join(keywords), re.IGNORECASE)

    # Find all <a> tags with href attributes
    for a_tag in soup.find_all('a', href=True):
        if keyword_regex.search(a_tag['href']):
            a_tag.decompose()  # Remove the <a> tag if the href matches the keywords
            
            
def remove_divs_keep_children(soup, keywords=None):
    """
    Removes all <div> tags from the BeautifulSoup object while keeping their children intact,
    unless a <div> tag contains any of the specified keywords in any of its attribute names or values.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object to modify.
        keywords (list, optional): A list of keywords to look for within any attribute key or value of the <div> tags. 
                                   If None or an empty list, all <div> tags are unwrapped.
    """
    divs = soup.find_all('div')
    for div in divs:
        if keywords:
            # Check if any keyword is found in any attribute name or value
            if any(keyword in str(attr) for attr in div.attrs for keyword in keywords) or \
               any(keyword in str(value) for value in div.attrs.values() for keyword in keywords):
                continue  # Skip unwrapping this div
        # Unwrap the div to keep its children but remove the div itself
        div.unwrap()

        
def remove_spans_keep_text(soup):
    """
    Removes all <span> tags from the BeautifulSoup object while keeping their contents.
    """
    spans = soup.find_all('span')
    for span in spans:
        span.unwrap()
        
def remove_br_keep_text(soup):
    """
    Removes all <span> tags from the BeautifulSoup object while keeping their contents.
    """
    spans = soup.find_all('br')
    for span in spans:
        span.unwrap()
        
def remove_b_keep_text(soup):
    """
    Removes all <span> tags from the BeautifulSoup object while keeping their contents.
    """
    tags = soup.find_all('b')
    for b in tags:
        b.decompose()
        
def remove_sections_keep_content(soup):
    """
    Removes all <section> tags from the BeautifulSoup object while keeping their contents.
    """
    sections = soup.find_all('section')
    for section in sections:
        section.unwrap()

def remove_tags_keep_content(soup, keywords):
    """
    Removes all <section> tags from the BeautifulSoup object while keeping their contents.
    """
    for tag_name in keywords:
        for tag in soup.find_all(tag_name):
            tag.unwrap()

def handle_embedded_html_in_iframe(driver):
    all_html_content = []  # List to store HTML contents of each iframe

    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    # Iterate through each iframe
    for index, iframe in enumerate(iframes):
        try:
            # Switch to the iframe
            driver.switch_to.frame(iframe)

            # Now within the iframe, check for the presence of an HTML body
            content_found = WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "body, div, header")  # More general
            )
            
            print(f"Content found in iframe index {index}")
            
            # Get the HTML of the iframe
            iframe_html = driver.page_source
            all_html_content.append(iframe_html)
            
            # After interactions, switch back to the main document
            driver.switch_to.default_content()

        except Exception as e:
            print(f"Failed to interact with iframe index {index}: {e}")
            # Ensure we switch back to the main document even if an error occurs
            driver.switch_to.default_content()

    return all_html_content

# def simplify_nested_divs(soup, max_depth=2):
#     """
#     Simplifies nested div structures by collapsing unnecessary nesting.
#     Keeps content within max_depth levels deep.
#     """
#     def get_depth(element):
#         depth = 0
#         while element.parent:
#             if element.parent.name == 'div':
#                 depth += 1
#             element = element.parent
#         return depth

#     all_divs = soup.find_all('div')
#     for div in all_divs:
#         current_depth = get_depth(div)
#         if current_depth > max_depth:
#             # Get deepest content that is not a div or where div has more than one child
#             deepest_child = div
#             while len(deepest_child.find_all(True, recursive=False)) == 1 and deepest_child.find(True, recursive=False).name == 'div':
#                 deepest_child = deepest_child.find(True, recursive=False)

#             # Preserve the deepest child by moving its contents up to the current div's position
#             if deepest_child and deepest_child != div:
#                 div.clear()
#                 for content in deepest_child.contents:
#                     div.append(content)


def remove_empty_tags_exclusions(soup, exclusions=('a', 'input', 'textarea')):
    """
    Removes empty tags from the BeautifulSoup object, except for specified tags.

    Args:
    soup: The BeautifulSoup object.
    exclusions: A tuple of tag names to exclude from removal.
    """
    for tag in soup.find_all():
        if tag.name in exclusions:
            continue  # Skip removal if the tag is in the list of exclusions
        if not tag.contents or (len(tag.contents) == 1 and isinstance(tag.contents[0], str) and not tag.contents[0].strip()):
            tag.decompose()

# Call the function to remove empty tags
def remove_header_and_footer(soup):
    """
    Removes all elements that are `<header>`, `<footer>`, or custom elements containing 'header' or 'footer' in their tag names.
    """
    # Define a function to determine if a tag's name contains 'header' or 'footer'
    def is_header_or_footer(tag):
        return tag.name and ('header' in tag.name or 'footer' in tag.name)

    # Find and decompose all tags identified by the function
    for element in soup.find_all(is_header_or_footer):
        element.decompose()
        
def remove_html_comments(soup):
    # Find all comment objects in the HTML
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()  # Remove each comment from the soup
        
def remove_tags_containing_special_keywords(soup, keywords):
    """
    Removes tags that contain text matching any of the specified keywords.

    Args:
    soup: The BeautifulSoup object.
    keywords: List of keywords to identify relevant to tags.
    """
    # Join the keywords into a single regular expression pattern
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b', re.IGNORECASE) # type: ignore

    tags = soup.find_all(True)
    for tag in tags:
        # Use regular expression search to check text against the pattern
        if pattern.search(tag.get_text(separator=" ", strip=True)):
            tag.decompose()  # Remove the tag if the pattern matches
            
            
def extract_forms(html):
    """Extract all forms from the given HTML content and return them within one <body> tag."""
    soup = BeautifulSoup(html, 'html.parser')
    forms = soup.find_all('form')

    # Create a new soup object to hold the new body
    new_soup = BeautifulSoup('', 'html.parser')
    body_tag = new_soup.new_tag('body')

    # Append each form to the new body tag
    for form in forms:
        body_tag.append(form)

    # Return the string representation of the new body tag with all forms
    return str(body_tag)






def clean_form(html_content):
    """Clean the provided HTML form content."""
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove year options older than 1950
    for option in soup.find_all('option'):
        try:
            if int(option['value']) < 1950:
                option.decompose()
        except ValueError:
            # Ignore values that can't be converted to integers
            pass

    # Define a set of allowed countries
    allowed_countries = {'Sweden', 'Norway', 'Finland', 'Denmark', 'England', 'Germany'}

    # Remove country options not in the allowed list
    for option in soup.find_all('option'):
        if option.get_text().strip() not in allowed_countries:
            option.decompose()

    return str(soup)


def clean_age_options(soup):
    """Keep only options for ages between 15 and 65 years old in specific select elements."""
    # Parsing the HTML input
    
    current_year = datetime.now().year # type: ignore
    min_year = current_year - 65  # Year of birth for a 65-year-old today
    max_year = current_year - 15  # Year of birth for a 15-year-old today

    # Iterate through each select element in the HTML
    for select in soup.find_all('select'):
        contains_year_values = False  # Flag to check if this select contains year values

        # Check if any option within this select element is a year within the expected age range
        for option in select.find_all('option'):
            try:
                year_value = int(option['value'])
                if min_year <= year_value <= max_year:
                    contains_year_values = True
                    break
            except ValueError:
                continue

        # If the select element contains year values, clean it up
        if contains_year_values:
            for option in select.find_all('option'):
                try:
                    year_value = int(option['value'])
                    if year_value < min_year or year_value > max_year:
                        option.decompose()
                except ValueError:
                    continue

    return str(soup)


def clean_country_options(soup):
    """Remove options for countries not in the allowed list from specific select elements."""
    # Parsing the HTML input
    
    # Include both English and Swedish names in the allowed list
    allowed_countries = {
        'Sweden', 'Sverige',  # Swedish name for Sweden
        'Norway', 'Norge',    # Norwegian name for Norway
        'Finland', 'Finland', # Same in Swedish
        'Denmark', 'Danmark', # Danish name for Denmark
        'England', 'England', # Same in Swedish
        'Germany', 'Tyskland' # Swedish name for Germany
    }

    # Iterate through each select element in the HTML
    for select in soup.find_all('select'):
        contains_country_values = False  # Flag to check if this select contains country values

        # Check if any option within this select element is a recognized country
        for option in select.find_all('option'):
            if option.get_text().strip() in allowed_countries:
                contains_country_values = True
                break

        # If the select element contains country values, clean it up
        if contains_country_values:
            for option in select.find_all('option'):
                if option.get_text().strip() not in allowed_countries:
                    option.decompose()

    return str(soup)

def remove_social_media_inputs(soup, keywords):
    """Remove hidden input elements related to social media from HTML content."""        
    # Find all hidden inputs
    hidden_inputs = soup.find_all('input', type='hidden')
    
    # Iterate over hidden inputs and check for social media related keywords
    for input_tag in hidden_inputs:
        if any(keyword in input_tag.get('name', '').lower() for keyword in keywords):
            input_tag.decompose()
        elif any(keyword in input_tag.get('id', '').lower() for keyword in keywords):
            input_tag.decompose()
            
    return str(soup)

def remove_checkboxes_by_keywords(soup, keywords):
    """
    Remove checkbox input elements based on a list of keywords found in their attributes.
    Parameters:
        html_content (str): The HTML content as a string.
        keywords (list): A list of keywords used to identify checkboxes to remove.
    Returns:
        str: The cleaned HTML content.
    """

    # Find all checkbox inputs
    checkboxes = soup.find_all('input', type='checkbox')
    
    # Iterate over checkboxes and check for keywords in their attributes
    for checkbox in checkboxes:
        # Check if any keyword is in any of the relevant attributes of the checkbox
        if any(keyword.lower() in (checkbox.get(attr, '').lower() for attr in ['id', 'name', 'value']) for keyword in keywords):
            checkbox.decompose()
    
    # Return the modified HTML
    return str(soup)

def remove_non_file_type_hidden_inputs(soup):
    """
    Remove all hidden input elements that do not have a 'type=file' attribute from HTML content.
    Parameters:
        html_content (str): The HTML content as a string.
    Returns:
        str: The cleaned HTML content.
    """
        # Find all hidden inputs that are not of type 'file'
    hidden_inputs = soup.find_all('input', type='hidden')
    for input_tag in hidden_inputs:
        if input_tag.get('type') != 'file':  # Check if the type is not 'file'
            input_tag.decompose()
    
    # Return the modified HTML
    return str(soup)


def remove_login_related_elements(soup, keywords):
    # Create a BeautifulSoup object from the HTML

    # List of tag types that might contain login actions
    tag_types = ['button', 'a', 'div']

    # Iterate over each type of tag
    for tag in tag_types:
            # Find all elements of this tag type
            elements = soup.find_all(tag)
            for element in elements:
                # Check if the text content of the element includes any of the keywords
                element_text = element.get_text().lower()  # Get the lowercased text once to avoid repeated conversions
                if any(keyword.lower() in element_text for keyword in keywords):
                    # Remove the element if any keyword is found
                    element.decompose()

        # Return the modified HTML as a string
    return str(soup)



def find_submit_elements(html_content, keywords):
    soup = BeautifulSoup(html_content, 'html.parser')
    matched_elements = []
    keywords = [keyword.lower() for keyword in keywords]

    forms = soup.find_all('form')
    for form in forms:
        elements = form.find_all(['button', 'input'])
        for element in elements:
            text = element.text.lower() or (element.get('value') or "").lower()
            if any(keyword in text for keyword in keywords):
                if element.get('id'):
                    matched_elements.append(f"#{element.get('id')}")
                elif element.get('name'):
                    matched_elements.append(f'input[name="{element.get('name')}"]')
                else:
                    # This will handle input types with a specific value attribute
                    if element.get('value'):
                        matched_elements.append(f'input[value="{element.get('value')}"]')
    
    return matched_elements


def extract_select_elements(html):
    soup = BeautifulSoup(html, 'html.parser')
    select_elements = soup.find_all('select')
    return {select.get('id') or select.get('name'): select for select in select_elements if select.get('id') or select.get('name')}

def find_new_selects(old_html, new_html):
    old_selects = extract_select_elements(old_html)
    new_selects = extract_select_elements(new_html)

    # Identifying new selects by keys (id or name)
    new_keys = set(new_selects.keys()) - set(old_selects.keys())
    return bool(new_keys)


def remove_non_human_text(soup):
    """
    Removes tags that contain non-human-readable placeholder text.

    Args:
    soup: The BeautifulSoup object.
    """
    # Regular expression to identify non-human-readable text
    non_human_text_regex = re.compile(r'\[#.*?#\]')

    # Find all tags that contain the specified non-human text
    for tag in soup.find_all(text=non_human_text_regex):
        if tag.parent:
            tag.parent.decompose()  # Remove the entire tag containing the non-human text

def remove_tech_jargon(soup):
    """
    Removes HTML elements that contain system-generated or technical text.

    Args:
    soup: The BeautifulSoup object.
    """
    # Define a regex pattern that matches typical system identifiers and tracking info
    pattern = re.compile(
        r'\b('
        r'_+[a-zA-Z0-9]{2,}|'  # Match identifiers starting with one or more underscores followed by at least two alphanumeric characters
        r'[a-zA-Z0-9]+_[a-zA-Z0-9]+|'  # Match strings with underscores in the middle (common in system identifiers)
        r'\d+\s*(månader|dag(ar)?s?)\b|'  # Match numbers followed by space and 'månader' (months) or 'dag' (days) in Swedish, allow optional plural
        r'HTTP|'  # Match HTTP
        r'Pixel|'  # Match Pixel
        r'Persistent|'  # Match Persistent
        r'IDB|'  # Match IDB
        r'Persistent:|'  # Include a colon if it frequently follows the word "Persistent"
        r'\bväntande\b|'  # Swedish for 'pending', often used in cookies and tracking
        r'\b[Vv][\d\.]+|'  # Match version numbers, e.g., V2, v1.5
        r'UUID|'  # Match UUID, a common format for identifiers
        r'[a-zA-Z]+Id\b|'  # Match any word ending with 'Id'
        r'[a-zA-Z]*[Cc]ookie|'  # Match words that contain 'cookie'
        r'[a-zA-Z]*[Tt]oken|'  # Match words that contain 'token'
        r'[a-zA-Z]*[Aa]nalytics|'  # Match words that contain 'analytics'
        r'[a-zA-Z]*[Ll]og(s)?'  # Match words that contain 'log' or 'logs'
        r')\b',
        re.IGNORECASE
    )
    # Iterate over all tags and examine their text content
    for tag in soup.find_all():
        if tag.string and pattern.search(tag.string):
            # If the tag's string matches the pattern, decompose the tag
            tag.decompose()
