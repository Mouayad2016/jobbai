from bs4 import BeautifulSoup
from .html_sanitizer import *



def clean_html(html_content):
    """Clean the HTML content by removing unwanted tags and attributes, and simplifying the structure."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove specific unwanted tags completely
    for tag in soup(["script", "style", "link", "option", "svg", "img", "video","template", "br", "picture"]):
        tag.decompose()

    # Remove specific attributes from all tags
    essential_attributes = {
            'href', 'src', 'alt', 'action', 'method', 'type', 'value',
            'placeholder', 'title', 'role', 
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

    # remove_empty_divs(important_soup)
    remove_divs_with_aria_hidden(important_soup)

    
    remove_empty_list_items(important_soup)
    remove_empty_spans(important_soup)
    remove_empty_sections(important_soup)
    remove_noscript_tags(important_soup)
    remove_elements_with_country_codes(soup,tags=('li', 'button'))
    remove_elements_with_long_text(soup, 200)
    remove_elements_by_keywords(soup, ['cookie', 'privacy', 'consent'])
    remove_tags_with_type_hidden(soup)
    remove_links_by_keyword(soup, ['cookie-policy', 'privacy'])
    remove_empty_tags_exclusions(soup)
    remove_html_comments(soup)
    
    
    remove_divs_keep_children(important_soup)
    remove_spans_keep_text(important_soup)
    remove_sections_keep_content(important_soup)
    remove_tags_keep_content(important_soup, ['ppc-container', "ppc-content", "figure"])
    # Flatten redundant divs in the important soup
    # flatten_divs(important_soup)
    
    remove_tags_containing_special_keywords(soup, [ 'Collection of personal data', 'personal data', 'privacy', 'Users rights', 'Already working', "About the team", "Powered by", "Accept all", "Liknande yrken", "JOBBFÖRSLAG",])

    # Return the cleaned HTML as a string
    cleaned_html = str(soup)
    return cleaned_html