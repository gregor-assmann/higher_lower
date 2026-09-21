import json

def clean_price(pricetag:str):
    """
    Converts Price to a float. Removes symbols and stuff
    """
    if pricetag is None:
        raise ValueError("Price must not be empty")

    raw_price = str(pricetag).strip().replace(" ", "")
    has_decimal_separator = "," in raw_price
    cleaned_price = raw_price.replace("ab", "").replace("€", "").replace(".", "")
    cleaned_price = cleaned_price.replace(",", ".")

    if not cleaned_price:
        raise ValueError("Price must not be empty")
    if not has_decimal_separator and cleaned_price.isdigit():
        return float(cleaned_price) / 100
    return float(cleaned_price)
            
def remove_duplicates(list):
    """
    Entfernt doppelte Produkte
    """
    new_list = []

    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

def export_to_json(data, filename="data.json"):
    """
    Exportiert das Dictionary an Artikeln in eine JSON
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported data to {filename}")

    except Exception as e:
        print(f"Error exporting to JSON: {e}")