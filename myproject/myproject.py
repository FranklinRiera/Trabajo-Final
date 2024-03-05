import requests
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import json
import boto3
from datetime import datetime

app = Flask(__name__)
@app.route("/generar", methods=['POST', 'OPTIONS'])


def generar():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        numero = request.json.get('numero')
        if numero:
            response_data = {'mensaje': 'Clave Acceso recibida correctamente', 'numero': numero}
            resultado = consulta_doc(numero)
            response = jsonify(resultado)
        else:
            response = jsonify({'error': 'Clave de Acceso no Especificada'})
            response.status_code = 400
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permitir solicitudes CORS desde cualquier origen
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Permitir el encabezado Content-Type
    return response


def consulta_doc(numero):

    #numero= '2902202401010139227200120011000000002250000081416'
    url = 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'

    # Datos XML a enviar al web service del SRI
    datos_xml = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.autorizacion">
    <soapenv:Header/>
    <soapenv:Body>
    <ec:autorizacionComprobante>
    <claveAccesoComprobante>{numero}</claveAccesoComprobante>
    </ec:autorizacionComprobante>
    </soapenv:Body>
    </soapenv:Envelope>
    """

    bytes_data = datos_xml.encode("ascii")

    # Encabezados para indicar que estás enviando XML
    headers = {
        'Content-Type': 'text/xml'
    }

    # Realizar la solicitud POST con los datos XML
    response = requests.post(url, data=bytes_data, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        datos_respuesta = response.text
        if encuentra_estado(datos_respuesta):
            xml_documento= obtener_resultado_xml(datos_respuesta)
            file_name = numero + ".xml"
            upload_string_to_s3(xml_documento, "datasri", file_name)
            json_data=obtiene_campos_xml(xml_documento,numero)
            return json_data
        else:
            return ({'error': 'Clave de Acceso no encontrada en el SRI'})
    else:
        print("La solicitud no fue exitosa. Código de estado:", response.text)

def obtiene_campos_xml(xml_string,numero):
    root = ET.fromstring(xml_string)

    # Obtener el valor del campo 'razonSocial'
    razon_social = root.find(".//razonSocial").text
    estab = root.find(".//estab").text
    ptoemi= root.find(".//ptoEmi").text
    secuencial = root.find(".//secuencial").text
    print("Razon Social:", razon_social, estab,ptoemi,secuencial)
    # Obtener el valor del campo 'totalSinImpuestos'
    total_sin_impuestos = root.find(".//totalSinImpuestos").text
    print("Total Sin Impuestos:", total_sin_impuestos)

    data = {
        "razon_social": razon_social,
        "total_sin_impuestos": total_sin_impuestos
        }
    # Convertir el diccionario a formato JSON
    json_data = json.dumps(data, indent=4)
    secuencia = estab + "-" + ptoemi + "-" + secuencial
    timestamp_actual = datetime.now().timestamp()
    fechahora=datetime.fromtimestamp(timestamp_actual)
    fecha_hora_formateada = fechahora.strftime('%d/%m/%Y %H:%M:%S')
    datalog = {
        "numero" : numero,
        "secuencia" : secuencia, 
        "razon" : razon_social.strip(),
        "total" : total_sin_impuestos,
        "hora" :  fecha_hora_formateada
    }
    grabalog(datalog)
    return json_data

def grabalog(data):
    url = "https://gxf4dvb3y6.execute-api.us-east-1.amazonaws.com/REGISTRAR"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data)
    print(data)
    print(response)



def obtener_resultado_xml(xml_string):
    # Parsear el XML
    root = ET.fromstring(xml_string)


    # Utilizar los espacios de nombres en la búsqueda del nodo
    #node = root.find(".//soap:Envelope/soap:Body/ns2:autorizacionComprobanteResponse/RespuestaAutorizacionComprobante/autorizaciones/autorizacion/comprobante", namespaces)
    node = root.find(".//comprobante")
    if node is not None:
        # Obtener el XML del nodo
    #    resultado_xml = ET.tostring(node, encoding="unicode")

        return node.text
    else:
        return ""

def encuentra_estado(textoXml):
    root = ET.fromstring(textoXml)
    estado_element = root.find('.//estado')

# Obtener el valor del elemento 'estado'
    if estado_element is not None:
        estado = estado_element.text
        if estado == "AUTORIZADO":
            return True
        else:
            return False
    else:
            return False

def upload_string_to_s3(text, bucket_name, file_name):
    # Inicializar el cliente de S3

    ACCESS_KEY_ID= "YOUR_AWS_access_key"
    ACCESS_SECRET_KEY = "YOUR_AWS_secret_key"
    REGION_NAME = "us-east-1"

  #S3 Connect
    s3 = boto3.client(
      's3',
    aws_access_key_id = ACCESS_KEY_ID,
    aws_secret_access_key = ACCESS_SECRET_KEY,
    region_name = REGION_NAME)

    try:
        # Subir el texto string como un archivo en el bucket de S3
        s3.put_object(Body=text, Bucket=bucket_name, Key=file_name)
        print(f"Archivo '{file_name}' subido exitosamente al bucket '{bucket_name}'.")
    except Exception as e:
        print(f"No se pudo subir el archivo al bucket: {e}")


if __name__ == "__main__":
        app.run(host='0.0.0.0')
