import requests

AWS_PRODUCTS_URL = "https://aws.amazon.com/api/dirs/items/search?item.directoryId=aws-products&sort_by=item.additionalFields.productNameLowercase&sort_order=asc&size=500&item.locale=en_US&tags.id=GLOBAL%23tech-category%23storage%7CGLOBAL%23tech-category%23security-identity-compliance%7CGLOBAL%23tech-category%23satellite%7CGLOBAL%23tech-category%23robotics%7CGLOBAL%23tech-category%23quantum%7CGLOBAL%23tech-category%23networking-content-dev%7CGLOBAL%23tech-category%23media-services%7CGLOBAL%23tech-category%23migration%7CGLOBAL%23tech-category%23mgmt-govern%7CGLOBAL%23tech-category%23ai-ml%7CGLOBAL%23tech-category%23iot%7CGLOBAL%23tech-category%23euc%7CGLOBAL%23tech-category%23mobile%7CGLOBAL%23tech-category%23app-integration%7CGLOBAL%23tech-category%23analytics%7CGLOBAL%23tech-category%23blockchain%7CGLOBAL%23tech-category%23business-apps%7CGLOBAL%23tech-category%23cost-mgmt%7CGLOBAL%23tech-category%23compute%7CGLOBAL%23tech-category%23containers%7CGLOBAL%23tech-category%23databases%7CGLOBAL%23tech-category%23devtools&tags.id=aws-products%23type%23service&tags.id=!aws-products%23type%23variant"
ANKI_TEXT_FILE = "anki_cards.txt"

def retrieve_raw_products_list(aws_products_url):
    # Retrieve the payload and check status
    req = requests.get(aws_products_url)
    if req.status_code != 200:
        raise ValueError(f"Got status code {req.status_code} for {aws_products_url}")

    # Parse the relevant information
    return req.json()['items']

def parse_raw_products(raw_products):
    products = []
    for raw_product in raw_products:
        # Retrieve relevant information
        additional_fields = raw_product['item']['additionalFields']
        name = additional_fields['productName']
        summary = additional_fields['productSummary']
        category = additional_fields['productCategory']

        # Clean up string
        summary = summary.replace('amp;', '')
        summary = summary.replace('<p>', '')
        summary = summary.replace('</p>', '')
        summary = summary.replace('\n', '')
        summary = summary.replace('\r', '')

        # Append product to list
        products.append({
            'category': category,
            'name': name,
            'summary': summary
        })

    return products

def export_product_to_anki_card(products, text_file):
    with open(text_file, 'w') as ff:
        # Write headers
        ff.write("#separator:tab\n#html:true")
        for product in products:
            ff.write(f"\n{product['name']}\t\"<i><b>{product['category']}</b></i> - {product['summary']}\"\t{product['category']}")

if __name__ == "__main__":
    raw_products = retrieve_raw_products_list(AWS_PRODUCTS_URL)
    products = parse_raw_products(raw_products)
    export_product_to_anki_card(products, ANKI_TEXT_FILE)
    print(f"File saved to {ANKI_TEXT_FILE}")