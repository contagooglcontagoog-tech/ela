import os
from flask import Flask, render_template, jsonify
from api.eship_api import EShipAPI

# Configuramos o template_folder para achar o arquivo na raiz do projeto
app = Flask(__name__, template_folder='../templates')
api = EShipAPI("e3662260858f65ce772ee2d3bf06e13e")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pedidos')
def get_pedidos():
    res_ordens = api.consultar_ordens({"periodoLancamento": 10004})
    
    if 'erro' in res_ordens and res_ordens['erro']:
        return jsonify({"erro": "Falha ao puxar da API da eShip"})

    ordens = []
    if isinstance(res_ordens, list):
        ordens = res_ordens
    elif isinstance(res_ordens, dict):
        if "data" in res_ordens:
            ordens = res_ordens["data"]
        else:
            ordens = list(res_ordens.values())[0] if res_ordens else []

    resultado_tabelado = []
    
    # Processa os primeiros 30 pro Vercel nao dar timeout na serverless function
    for o in ordens[:30]:
        pedido = o.get('Nº da Compra', o.get('numero_compra', o.get('id', 'N/A')))
        status = o.get('Situação da nota', o.get('Status', 'N/A'))
        cliente = o.get('Destinatário', o.get('destinatario', 'N/A'))
        transportadora = o.get('Serviço Transporte', o.get('transportadora', 'N/A'))
        nota_fiscal = o.get('Nº da Nota venda', o.get('numero_nota', 'N/A'))
        chave_nf = o.get('Chave', o.get('chave', ''))
        
        # Telefone default (na real precisaria varrer os contatos pra cada id)
        telefone = "Buscando..." 
        
        link_nf = f"https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=resumo&tipoConteudo=7PhJ%2BgAVw2g=&chNFe={chave_nf}" if chave_nf else "#"
        
        resultado_tabelado.append({
            "pedido": pedido,
            "status": status,
            "cliente": cliente,
            "telefone": telefone,
            "transportadora": transportadora,
            "nota_fiscal": nota_fiscal,
            "link_nf": link_nf
        })
        
    return jsonify(resultado_tabelado)

# Pro vercel rodar o app
if __name__ == '__main__':
    app.run()
