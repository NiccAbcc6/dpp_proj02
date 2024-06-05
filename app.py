from flask import Flask, render_template, request, redirect, url_for
import rdflib
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Carica l'ontologia
g = rdflib.Graph()
g.parse("dpp_ontology_populated.owl", format="xml")

# Funzione per estrarre dati dall'ontologia
def get_product_info(product_uri):
    query = """
    PREFIX ex: <http://example.com/tessile.owl#>
    SELECT ?brandName ?colore ?composizioneFibrosa ?certificazioneName ?lavaggioTemperatura ?lavaggioDelicatezza
           ?candeggio ?asciugamentoTipo ?asciugamentoTemperatura ?stiraturaTipo ?ricicloOpzioni ?ricicloPunti
    WHERE {
        <""" + product_uri + """> ex:brandName ?brandName ;
                             ex:colore ?colore ;
                             ex:hasComposizione ?composizione .
        ?composizione ex:composizioneFibrosa ?composizioneFibrosa .
        <""" + product_uri + """> ex:hasCertificazione ?certificazione .
        ?certificazione ex:certificazioneName ?certificazioneName .
        <""" + product_uri + """> ex:hasManutenzione ?manutenzione .
        ?manutenzione ex:hasLavaggio ?lavaggio .
        ?lavaggio ex:lavaggioTemperatura ?lavaggioTemperatura ;
                  ex:lavaggioDelicatezza ?lavaggioDelicatezza ;
                  ex:candeggio ?candeggio ;
                  ex:asciugamentoTipo ?asciugamentoTipo ;
                  ex:asciugamentoTemperatura ?asciugamentoTemperatura .
        ?manutenzione ex:stiraturaTipo ?stiraturaTipo .
        <""" + product_uri + """> ex:hasRiciclo ?riciclo .
        ?riciclo ex:ricicloOpzioni ?ricicloOpzioni ;
                 ex:ricicloPunti ?ricicloPunti .
    }
    """
    result = g.query(query)
    for row in result:
        return {
            "brandName": row.brandName,
            "colore": row.colore,
            "composizioneFibrosa": row.composizioneFibrosa,
            "certificazioneName": row.certificazioneName,
            "lavaggioTemperatura": row.lavaggioTemperatura,
            "lavaggioDelicatezza": row.lavaggioDelicatezza,
            "candeggio": row.candeggio,
            "asciugamentoTipo": row.asciugamentoTipo,
            "asciugamentoTemperatura": row.asciugamentoTemperatura,
            "stiraturaTipo": row.stiraturaTipo,
            "ricicloOpzioni": row.ricicloOpzioni,
            "ricicloPunti": row.ricicloPunti
        }
    return None

users = {"admin": "password123"}

@app.route('/')
def index():
    app.logger.debug("Rendering index page")
    product_info = get_product_info("http://example.com/tessile.owl#PatagoniaGiacca")
    return render_template('index.html', product=product_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.debug("Login attempt")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            app.logger.debug("Login successful")
            return redirect(url_for('special_access'))
        else:
            app.logger.debug("Login failed")
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/special_access')
def special
