from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ContactMessage


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def contact_api(request):
    # Handle CORS preflight request
    if request.method == "OPTIONS":
        response = JsonResponse({"status": "ok"})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    try:
        # Parse JSON data
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        # Validate required fields
        if not name:
            return create_response({"success": False, "error": "Name is required"}, 400)
        if not email:
            return create_response({"success": False, "error": "Email is required"}, 400)
        if not message:
            return create_response({"success": False, "error": "Message is required"}, 400)

        # Basic email validation
        if '@' not in email or '.' not in email:
            return create_response({"success": False, "error": "Invalid email address"}, 400)

        # Save to database
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return create_response({
            "success": True,
            "message": "Your message has been received successfully!",
            "id": contact.id
        }, 201)

    except json.JSONDecodeError:
        return create_response({"success": False, "error": "Invalid JSON data"}, 400)
    except Exception as e:
        return create_response({"success": False, "error": str(e)}, 500)


def create_response(data, status=200):
    response = JsonResponse(data, status=status)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response
