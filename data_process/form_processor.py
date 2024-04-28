from bs4 import BeautifulSoup
from .html_sanitizer import *

def clean_from(html_content):
    """Clean the <form> tag content by removing unwanted tags and attributes, and simplifying the structure."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove specific unwanted tags completely
    for tag in soup(["script", "style", "link", "svg", "img", "video","template", "br", "picture"]):
        tag.decompose()

    # Remove specific attributes from all tags
    essential_attributes = {
            'href', 'src', 'alt', 'type', 'value',
            'placeholder', 'title', 'id', 
        }    
    essential_attributes.update({f'aria-{attr}' for attr in ['label', 'labelledby', 'hidden', 'live', 'controls', 'expanded', 'invalid']})
  # Remove all non-essential attributes from all elements
    for tag in soup.find_all(True):  # True finds all tags
        # Get a list of attributes to remove (those not in the essential list)
        attributes_to_remove = [attr for attr in tag.attrs if not attr in essential_attributes and not attr.startswith('aria-')]
        for attr in attributes_to_remove:
            del tag[attr]


 
    # extract_important_divs(soup)
    remove_header_and_footer(soup)

    # remove_empty_divs(soup)
    # remove_divs_with_aria_hidden(soup)

    remove_login_related_elements(soup,[
    'Login', 'Log in', 'Logga in', 'Inloggning', 
    'Sign in', 'Sign on', 'Anslut', 'Authentisera',
    'Access account', 'Signup', 'Sign up', 'Skapa konto', 'Bli medlem', 'Anmäl dig'])
    
    remove_empty_list_items(soup)
    remove_empty_spans(soup)
    remove_empty_sections(soup)
    remove_noscript_tags(soup)
    remove_elements_with_country_codes(soup,tags=('li', 'button'))
    remove_elements_with_long_text(soup, 600)
    remove_links_by_keyword(soup, ['cookie-policy', 'privacy'])
    remove_empty_tags_exclusions(soup)
    clean_age_options(soup)
    clean_country_options(soup)
    
    remove_html_comments(soup)
    remove_divs_keep_children(soup)
    remove_spans_keep_text(soup)
    remove_sections_keep_content(soup)
    remove_tags_keep_content(soup, ['ppc-container', "ppc-content", "figure"])
    remove_social_media_inputs(soup, ['facebook', 'linkedin'] )
    remove_checkboxes_by_keywords(soup, ['newsletter', 'updates', 'future_jobs'])
    remove_non_file_type_hidden_inputs(soup)
    remove_tags_containing_special_keywords(soup, [ 'Collection of personal data', 'personal data', 'privacy', 'Users rights', 'Already working', "Powered by", "Accept all", "Liknande yrken", "JOBBFÖRSLAG",])
    # Return the cleaned HTML as a string
    cleaned_html = str(soup)
    return cleaned_html