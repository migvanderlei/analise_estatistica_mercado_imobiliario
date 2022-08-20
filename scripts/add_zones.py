zones_index = {'null': 'null'}

with open('/home/miguel/UEA/estatistica/bairro-zona.txt') as f:
  lines = f.read().splitlines()

  for line in lines:
    neighborhood, zone = line.split(';')
    zones_index[neighborhood] = zone

# print(zones_index)


HEADERS = ["valor", "cep", "cidade", "bairro", "zona", "logradouro", "categoria", "area", "qtde_quartos", "qtde_vagas", "qtde_banheiros"]

data = []
new_data = ",".join(HEADERS) + '\n'

with open('/home/miguel/UEA/estatistica/scraper/data.csv') as f:
  data = f.read().splitlines()

  for line in data[1:]:
    valor, cep, cidade, bairro, logradouro, categoria, area, qtde_quartos, qtde_vagas, qtde_banheiros = line.split(',')
    zona = zones_index.get(bairro) 

    new_data += f"{valor},{cep},{cidade},{bairro},{zona},{logradouro},{categoria},{area},{qtde_quartos},{qtde_vagas},{qtde_banheiros}\n"

with open('/home/miguel/UEA/estatistica/scraper/data_v2.csv', 'w+') as f:
  f.write(new_data)
