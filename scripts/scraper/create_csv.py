from json import loads

DATA = []

with open('/home/miguel/Workspace/scraper/data.json', 'r') as f:
    DATA = loads(f.read())

AVOID = ["Detalhes do imóvel", "Detalhes do condominio", "IPTU", "Condomínio"]

HEADERS = ["valor", "cep", "cidade", "bairro", "logradouro", "categoria", "area", "qtde_quartos", "qtde_vagas", "qtde_banheiros"]

csv_data = ",".join(HEADERS) + '\n'

lines = set()

for item in DATA:

    location = item['location']
    properties = item['properties']

    vagas = properties.get('Vagas na garagem')
    if vagas:
        vagas.replace(' ou mais', '+')

    banheiros = properties.get('Banheiros')
    if banheiros:
        banheiros.replace(' ou mais', '+')   

    area = properties.get('Área útil', properties.get('Área construída'))

    if area:
        area.replace('m²', '')

    line = f"{item['price']},{location.get('CEP')},{location.get('Município')},{location.get('Bairro')},{location.get('Logradouro')},{properties.get('Categoria')},{area},{properties.get('Quartos')},{vagas},{banheiros}"
    
    lines.add(line)

csv_data += '\n'.join(lines)

with open('/home/miguel/Workspace/scraper/data.csv', 'w+') as f:
    f.write(csv_data)
