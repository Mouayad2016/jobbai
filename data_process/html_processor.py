from bs4 import BeautifulSoup, NavigableString, Comment
import re


def meaningful_attributes(tag):
    """Check if a tag has any meaningful attributes that could affect layout or styling."""
    ignored_attributes = {'class', 'id', 'style', 'role'}
    return any(attr in tag.attrs for attr in ignored_attributes)


def flatten_divs(soup):
    """Flatten nested divs that do not contribute to content or structure."""
    divs = soup.find_all("div", recursive=True)
    for div in divs:
        while div.find_all("div", recursive=False) == 1 and not meaningful_attributes(div):
            child = div.find("div")
            div.replace_with(child)


def contains_important_content(div):
    """Check if the div contains important elements like text, input fields, or other interactive elements."""
    if div.get_text(strip=True):
        return True
    interactive_tags = ['input', 'textarea', 'select', 'button', 'a', 'label', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    return any(div.find(tag) for tag in interactive_tags)


def extract_important_divs(soup):
    """Extract divs containing important content or elements."""
    important_divs = []
    for div in soup.find_all("div"):
        if contains_important_content(div):
            important_divs.append(div)
    new_soup = BeautifulSoup('', 'html.parser')
    for div in important_divs:
        new_soup.append(div.extract())
    return new_soup


def remove_empty_divs(soup):
    """Remove all divs that have no meaningful content and keep checking until no empty divs remain."""
    changes = True
    while changes:
        changes = False  # Reset change flag on each pass
        for div in soup.find_all("div", recursive=True):
            # Check if the div only contains <br>, whitespaces, or is completely empty
            if (not div.contents or
                all((isinstance(c, (NavigableString, Comment)) and not c.strip()) or 
                    (c.name == 'br') for c in div.contents)):
                div.decompose()
                changes = True  # Continue while loop if changes are made

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
            
            
def remove_divs_keep_children(soup):
    """
    Removes all <div> tags from the BeautifulSoup object while keeping their children intact.
    """
    divs = soup.find_all('div')
    for div in divs:
        # Unwrap each <div> to keep its children but remove the <div> itself
        div.unwrap()
        
def remove_spans_keep_text(soup):
    """
    Removes all <span> tags from the BeautifulSoup object while keeping their contents.
    """
    spans = soup.find_all('span')
    for span in spans:
        span.unwrap()

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
        
def simplify_nested_divs(soup, max_depth=2):
    """
    Simplifies nested div structures by collapsing unnecessary nesting.
    Keeps content within max_depth levels deep.
    """
    def get_depth(element):
        depth = 0
        while element.parent:
            if element.parent.name == 'div':
                depth += 1
            element = element.parent
        return depth

    all_divs = soup.find_all('div')
    for div in all_divs:
        current_depth = get_depth(div)
        if current_depth > max_depth:
            # Get deepest content that is not a div or where div has more than one child
            deepest_child = div
            while len(deepest_child.find_all(True, recursive=False)) == 1 and deepest_child.find(True, recursive=False).name == 'div':
                deepest_child = deepest_child.find(True, recursive=False)

            # Preserve the deepest child by moving its contents up to the current div's position
            if deepest_child and deepest_child != div:
                div.clear()
                for content in deepest_child.contents:
                    div.append(content)


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
        
def remove_divs_containing_privacy_info(soup, keywords):
    """
    Removes <div> tags that contain text matching any of the specified keywords.

    Args:
    soup: The BeautifulSoup object.
    keywords: List of keywords to identify relevant <div> tags.
    """
    # Join the keywords into a single regular expression pattern
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b', re.IGNORECASE) # type: ignore

    divs = soup.find_all('div')
    for div in divs:
        # Use regular expression search to check text against the pattern
        if pattern.search(div.get_text(separator=" ", strip=True)):
            div.decompose()  # Remove the div if the pattern matches


def clean_html(html_content):
    """Clean the HTML content by removing unwanted tags and attributes, and simplifying the structure."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove specific unwanted tags completely
    for tag in soup(["script", "style", "link", "option", "svg", "img", "video","template", "br", "picture"]):
        tag.decompose()

    # Remove specific attributes from all tags
    essential_attributes = {
            'href', 'src', 'alt', 'action', 'method', 'type', 'value', 
            'placeholder', 'title', 'role'
        }    
    essential_attributes.update({f'aria-{attr}' for attr in ['label', 'labelledby', 'hidden', 'live', 'controls', 'expanded', 'invalid']})
  # Remove all non-essential attributes from all elements
    for tag in soup.find_all(True):  # True finds all tags
        # Get a list of attributes to remove (those not in the essential list)
        attributes_to_remove = [attr for attr in tag.attrs if not attr in essential_attributes and not attr.startswith('aria-')]
        for attr in attributes_to_remove:
            del tag[attr]


    # Extract important divs and remove empty ones
    important_soup = soup
    # extract_important_divs(soup)
    remove_header_and_footer(important_soup)
    remove_divs_containing_privacy_info(soup, [ 'Collection of personal data', 'personal data', 'privacy', 'Users rights', 'Already working', "About the team", "Powered by", "Accept all", "Liknande yrken", "JOBBFÖRSLAG",])

    # remove_empty_divs(important_soup)
    remove_divs_with_aria_hidden(important_soup)

    
    remove_empty_list_items(important_soup)
    remove_empty_spans(important_soup)
    remove_empty_sections(important_soup)
    remove_noscript_tags(important_soup)
    remove_elements_with_country_codes(soup,tags=('li', 'button', 'input', 'a', 'div'))
    remove_elements_with_long_text(soup, 200)
    remove_elements_by_keywords(soup, ['cookie', 'privacy', 'consent'])
    remove_tags_with_type_hidden(soup)
    remove_links_by_keyword(soup, ['cookie-policy', 'privacy'])
    remove_empty_tags_exclusions(soup)
    # simplify_nested_divs(soup)
    remove_html_comments(soup)
    
    
    remove_divs_keep_children(important_soup)
    remove_spans_keep_text(important_soup)
    remove_sections_keep_content(important_soup)
    remove_tags_keep_content(important_soup, ['ppc-container', "ppc-content", "figure"])
    # Flatten redundant divs in the important soup
    flatten_divs(important_soup)

    # Return the cleaned HTML as a string
    cleaned_html = str(soup)
    return cleaned_html