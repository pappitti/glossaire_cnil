import json

with open('cnil_glossary.json', 'r') as f:
    data = json.load(f)

    html = ""

    for item in data:
        html += f"<h2>{item['term'].strip()}</h2>"
        for p in item['definition'].split('\n'):
            html += f"<p>{p}</p>"


    with open('cnil_glossary.html', 'w') as f:
        f.write(html)