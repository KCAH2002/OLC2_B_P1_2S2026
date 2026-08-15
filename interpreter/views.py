import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    """
    comprueba que la api del interprete este funcionando
    """

    return JsonResponse(
        {
            "success": True,
            "message": "La API de OxigenScript esta funcionando correctamente.",
        }
    )

# JsonResponse convierte el diccionario de Python en una respuesta JSON.

@csrf_exempt
def analyze_code(request):
    """
    recibe codigo fuente de oxigenscript en formato json
    """

    # solo se permite utilizar el metodo post
    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Este endpoint solamente acepta solicitudes POST.",
            },
            status=405,
        )

    try:
        # convierte el cuerpo de la solicitud en un diccionario de python
        data = json.loads(request.body)

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "success": False,
                "message": "El cuerpo de la solicitud no contiene un JSON valido.",
            },
            status=400,
        )

    # obtiene la propiedad code del json recibido
    code = data.get("code")

    # comprueba que code exista y que sea una cadena
    if not isinstance(code, str):
        return JsonResponse(
            {
                "success": False,
                "message": "La propiedad 'code' es obligatoria y debe ser una cadena.",
            },
            status=400,
        )

    # impide analizar codigo vacio o formado solamente por espacios
    if not code.strip():
        return JsonResponse(
            {
                "success": False,
                "message": "El código fuente no puede estar vacio.",
            },
            status=400,
        )

    # respuesta temporal mientras se construye el analizador
    return JsonResponse(
        {
            "success": True,
            "message": "El codigo fue recibido correctamente.",
            "code": code,
        },
        status=200,
    )