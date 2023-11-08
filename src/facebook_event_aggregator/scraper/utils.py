from os.path import join
from urllib.request import urlretrieve 

def read_pages_from_env(replace_locale=True):
    """ LOADING & PARSING PAGES FROM .ENV """
    raw_pages = loads(getenv("pages"))
    pages = []
    for raw_page in raw_pages:
        page_type = raw_page[0].lower().strip()
        url = raw_page[1]

        match page_type:
            case "page":
                func = parse_page
            case "community":
                func = parse_community
            case _:  # Default
                func = parse_page
    
        if replace_locale:
            # Specify localisation
            url = facebook_www_to_locale(url)

        pages.append((func, url))
    return pages


def save_image(event, image_url, img_dir):
    if ".png" in image_url:
        ext = ".png"
    else:
        ext = ".jpg"
    print(event.uid)
    urlretrieve(image_url, join(img_dir, event.uid + ext))
