import urllib.parse

"""
Genutzt um den Link zu einem high-res Bild aus den low-res Bildern der Produkt übersicht zu erstellen
nutzt die <alt> Beschreibung des <img> um auf high-res Link zu schließen
"""

def parse_alt_img_link(link):
    """
    Konvertiert den alt des low-res Bilds in ein Format als Identifier für das high-res Bild
    """
    original_string = link
    stripped_string = ''.join(e for e in original_string if e.isalnum() or e == " ")
    parsed_string = ""
    for char in original_string:
        if char.isalnum():
            match char:
                case "ä":
                    parsed_string += "ae"
                case "ö":
                    parsed_string += "oe"
                case "ü":
                    parsed_string += "ue"
                case _:
                    parsed_string += char
        else:
            parsed_string += " "
    parsed_string = " ". join(parsed_string. split())

    url_encoded_string = urllib.parse.quote_plus(parsed_string.lower())
    url_encoded_string = url_encoded_string.replace("+", "-")

    return url_encoded_string


def strip_original_link(original_link:str):
    """
    Kürzt den low-res Link in ein Format das für den high-res Link verwendet werden kann
    """
    stripped_link = ""
    for char in original_link:
        if char == "?":
            break
        stripped_link += char
    return stripped_link

def get_high_quality_link(original_link:str, alt_img_link:str):
    """
    Erstellt den Link für ein high-res Bild aus dem low-res Link und der alt-Beschreibung des low-res Bildes
    """
    url_encoded_string = parse_alt_img_link(alt_img_link)
    stripped_link = strip_original_link(original_link)

    final_link = ""
    final_link += stripped_link + "/"
    final_link += url_encoded_string +".jpg"
    final_link += "?$formatz$"

    return final_link