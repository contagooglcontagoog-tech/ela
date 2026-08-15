import os
from flask import Flask, render_template, jsonify
from api.eship_api import EShipAPI

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
    if isinstance(res_ordens, dict):
        if "corpo" in res_ordens and "body" in res_ordens["corpo"] and "dados" in res_ordens["corpo"]["body"]:
            ordens = res_ordens["corpo"]["body"]["dados"]
        elif "data" in res_ordens:
            ordens = res_ordens["data"]
    elif isinstance(res_ordens, list):
        ordens = res_ordens

    resultado_tabelado = []
    
    for o in ordens[:30]:
        pedido = o.get('numero', o.get('id', 'N/A'))
        
        status_obj = o.get('status', {})
        status = status_obj.get('descricao', 'Lançado') if isinstance(status_obj, dict) else 'Lançado'
        
        destinatario = o.get('destinatario', {})
        cliente = destinatario.get('nome', 'N/A') if isinstance(destinatario, dict) else 'N/A'
        
        transporte = o.get('transporteSuperior', {})
        transportadora = transporte.get('nome', 'N/A') if isinstance(transporte, dict) else 'N/A'
        
        emissao = o.get('emissao', {})
        nota_fiscal = emissao.get('numero', 'Pendente') if isinstance(emissao, dict) else 'Pendente'
        chave_nf = emissao.get('chave', '') if isinstance(emissao, dict) else ''
        
        telefone = "Buscando..." 
        link_nf = f"https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=resumo&tipoConteudo=7PhJ%2BgAVw2g=&chNFe={chave_nf}" if chave_nf else "#"
        
        resultado_tabelado.append({
            "pedido": pedido,
            "status": status,
            "cliente": cliente,
            "telefone": telefone,
            "transportadora": transportadora,
            "nota_fiscal": nota_fiscal,
            "link_nf": link_nf,
            "chave_nf": chave_nf
        })
        
    return jsonify(resultado_tabelado)

if __name__ == '__main__':
    app.run()
