import spacy
from faker import Faker 


nlp = spacy.load('pt_core_news_sm')
fake = Faker('pt_BR')

text = "João Silva nasceu em São Paulo, se formou em Engenharia Elétrica, e seu CPF é 188.426.779-01."

def substituir_entidades(texto):
    doc = nlp(texto)
    texto_modificado = texto
    
    for ent in doc.ents:
        if ent.label_ == "PER":
            fake_name = fake.name()
            texto_modificado = texto_modificado.replace(ent.text, fake_name)
        elif ent.label_ == "LOC":
            fake_city = fake.city()
            texto_modificado = texto_modificado.replace(ent.text, fake_city)
        elif ent.label_ == "ORG":
            fake_company = fake.company()
            texto_modificado = texto_modificado.replace(ent.text, fake_company)
        elif ent.label_ == "CPF":
            fake_cpf = fake.cpf()
            texto_modificado = texto_modificado.replace(ent.text, '[CPF]')
    
    return texto_modificado

print(substituir_entidades(text))