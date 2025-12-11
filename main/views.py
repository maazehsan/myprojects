from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import ContactMessage


def get_email_template(name, message):
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Reaching Out</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0D0D0D; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0D0D0D; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width: 600px; width: 100%;">
                    
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding-bottom: 30px;">
                            <table role="presentation" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td style="background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 16px; padding: 20px 30px;">
                                        <span style="font-family: 'Courier New', monospace; font-size: 24px; font-weight: bold; color: #FFFFFF;">maaz<span style="color: #888888;">.dev</span></span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Main Content Card -->
                    <tr>
                        <td>
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 20px; overflow: hidden;">
                                
                                <!-- Gradient Header Bar -->
                                <tr>
                                    <td style="height: 4px; background: linear-gradient(90deg, #888888 0%, #FFFFFF 50%, #888888 100%);"></td>
                                </tr>
                                
                                <!-- Content -->
                                <tr>
                                    <td style="padding: 50px 40px;">
                                        
                                        <!-- Greeting -->
                                        <h1 style="margin: 0 0 10px 0; font-size: 28px; font-weight: 600; color: #FFFFFF;">Hey {name}! 👋</h1>
                                        <p style="margin: 0 0 30px 0; font-size: 18px; color: #A0A0A0;">Thank you for reaching out</p>
                                        
                                        <!-- Divider -->
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-bottom: 30px;">
                                            <tr>
                                                <td style="height: 1px; background: #2A2A2A;"></td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Message -->
                                        <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.8; color: #E8E8E8;">
                                            I've received your message and I'm excited to connect with you! I typically respond within <strong style="color: #FFFFFF;">24-48 hours</strong>.
                                        </p>
                                        
                                        <!-- Your Message Box -->
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-bottom: 30px;">
                                            <tr>
                                                <td style="background: #141414; border: 1px solid #2A2A2A; border-radius: 12px; padding: 25px;">
                                                    <p style="margin: 0 0 12px 0; font-size: 12px; font-weight: 600; color: #666666; text-transform: uppercase; letter-spacing: 2px;">Your Message</p>
                                                    <p style="margin: 0; font-size: 15px; line-height: 1.7; color: #A0A0A0; font-style: italic;">"{message}"</p>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 1.8; color: #E8E8E8;">
                                            In the meantime, feel free to explore my portfolio or connect with me on social media. I'm always happy to discuss new projects and creative ideas!
                                        </p>
                                        
                                        <!-- CTA Button -->
                                        <table role="presentation" cellspacing="0" cellpadding="0" style="margin-bottom: 30px;">
                                            <tr>
                                                <td style="background: #FFFFFF; border-radius: 8px;">
                                                    <a href="https://maazehsan.github.io" target="_blank" style="display: inline-block; padding: 14px 32px; font-size: 14px; font-weight: 600; color: #0D0D0D; text-decoration: none;">View Portfolio</a>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Signature -->
                                        <p style="margin: 0; font-size: 16px; color: #E8E8E8;">Looking forward to connecting!</p>
                                        <p style="margin: 10px 0 0 0; font-size: 18px; font-weight: 600; color: #FFFFFF;">— Maaz Ehsan</p>
                                        <p style="margin: 5px 0 0 0; font-size: 14px; color: #666666;">Web Developer • Django • Frontend</p>
                                        
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Social Links -->
                    <tr>
                        <td align="center" style="padding: 40px 0 20px 0;">
                            <table role="presentation" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td style="padding: 0 10px;">
                                        <a href="https://github.com/maazehsan" target="_blank" style="display: inline-block; width: 44px; height: 44px; background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 10px; text-align: center; line-height: 44px; text-decoration: none;">
                                            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" height="20" alt="GitHub" style="vertical-align: middle; filter: brightness(0) invert(1);">
                                        </a>
                                    </td>
                                    <td style="padding: 0 10px;">
                                        <a href="https://instagram.com/maaz.dev" target="_blank" style="display: inline-block; width: 44px; height: 44px; background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 10px; text-align: center; line-height: 44px; text-decoration: none;">
                                            <img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png" width="20" height="20" alt="Instagram" style="vertical-align: middle;">
                                        </a>
                                    </td>
                                    <td style="padding: 0 10px;">
                                        <a href="https://www.linkedin.com/in/maazehsan" target="_blank" style="display: inline-block; width: 44px; height: 44px; background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 10px; text-align: center; line-height: 44px; text-decoration: none;">
                                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" height="20" alt="LinkedIn" style="vertical-align: middle;">
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 20px 0;">
                            <p style="margin: 0 0 8px 0; font-size: 13px; color: #666666;">© 2025 maaz.dev — Made with passion</p>
                            <p style="margin: 0; font-size: 12px; color: #404040;">This is an automated response to your contact form submission</p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''


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

        # Send confirmation email to the user with HTML template
        try:
            from django.core.mail import EmailMultiAlternatives
            
            subject = 'Thanks for reaching out! — maaz.dev'
            text_content = f'''Hi {name},\n\nThank you for reaching out! I have received your message and will get back to you within 24-48 hours.\n\nYour message:\n"{message}"\n\nBest regards,\nMaaz Ehsan\nWeb Developer'''
            html_content = get_email_template(name, message)
            
            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send(fail_silently=False)
            email_sent = True
        except Exception as e:
            email_sent = False
            print(f"Email sending failed: {e}")

        return create_response({
            "success": True,
            "message": "Your message has been sent successfully!",
            "email_sent": email_sent,
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
