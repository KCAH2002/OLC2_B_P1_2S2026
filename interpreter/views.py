from django.http import JsonResponse


def health_check(request):
    """
    comprueba que la api del interprete este funcionando
    """

    return JsonResponse(
        {
            "success": True,
            "message": "La API de OxigenScript está funcionando correctamente.",
        }
    )
# JsonResponse convierte el diccionario de Python en una respuesta JSON.