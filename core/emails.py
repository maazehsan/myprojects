import logging

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

PORTAL_URL = "https://portal.devnautics.studio"
WEBSITE_URL = "https://devnautics.studio"
ADMIN_EMAIL = "maazehsan2007@gmail.com"

FONT_FAMILY = '"Roboto Slab", Georgia, "Times New Roman", serif'


def _black_email_template(heading, body_html):
    """Wrap content in a black-background, white-text email layout."""
    return (
        '<!DOCTYPE html>'
        '<html lang="en" xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:o="urn:schemas-microsoft-com:office:office">'
        '<head>'
        '<meta charset="utf-8"/>'
        '<meta http-equiv="X-UA-Compatible" content="IE=edge"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'
        '<meta name="color-scheme" content="light dark"/>'
        '<meta name="supported-color-schemes" content="light dark"/>'
        '<title>DevNautics</title>'
        '<!--[if gte mso 9]>'
        '<xml><o:OfficeDocumentSettings>'
        '<o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch>'
        '</o:OfficeDocumentSettings></xml>'
        '<![endif]-->'
        '<!--[if mso]>'
        '<style type="text/css">'
        'body,table,td,p,h1,h2,div,span,a{font-family:Georgia,"Times New Roman",serif!important;}'
        '</style>'
        '<![endif]-->'
        '<style type="text/css">'
        '@import url("https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;600&display=swap");'
        'body,html,table,td,div,p,h1,h2,span,a{margin:0;padding:0;}'
        'body,html{width:100%!important;height:100%!important;-webkit-text-size-adjust:100%;'
        '-ms-text-size-adjust:100%;background-color:#000000!important;}'
        'img{border:0;line-height:100%;outline:none;text-decoration:none;}'
        'u+#body a{color:inherit;text-decoration:none;font-size:inherit;font-weight:inherit;line-height:inherit;}'
        '#outlook a{padding:0;}'
        ':root{color-scheme:light dark;}'
        '</style>'
        '</head>'
        '<body id="body" style="margin:0;padding:0;width:100%;height:100%;'
        f'background-color:#000000;color:#ffffff;font-family:{FONT_FAMILY};'
        '-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;" bgcolor="#000000">'

        # Preheader (hidden text for email previews)
        f'<div style="display:none;font-size:1px;color:#000000;line-height:1px;'
        f'max-height:0;max-width:0;opacity:0;overflow:hidden;">'
        f'{heading}'
        '</div>'

        # Full-width black wrapper — this table MUST be 100% to kill white borders
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'width="100%" height="100%" bgcolor="#000000" '
        'style="background-color:#000000;margin:0;padding:0;width:100%;height:100%;'
        'min-width:100%;border-collapse:collapse;">'
        '<tr>'
        '<td align="center" valign="top" bgcolor="#000000" '
        'style="background-color:#000000;padding:0;margin:0;">'

        # Inner 600px container
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'width="600" bgcolor="#000000" '
        'style="max-width:600px;width:100%;background-color:#000000;border-collapse:collapse;">'

        # Heading row — separate row so it always renders
        '<tr>'
        '<td bgcolor="#000000" align="left" '
        f'style="padding:40px 30px 10px 30px;background-color:#000000;">'
        f'<h1 style="margin:0;padding:0;color:#ffffff;font-size:30px;line-height:1.3;'
        f'font-family:{FONT_FAMILY};font-weight:700;display:block;'
        'mso-line-height-rule:exactly;">'
        f'{heading}</h1>'
        '</td>'
        '</tr>'

        # Divider row
        '<tr>'
        '<td bgcolor="#000000" style="padding:0 30px;background-color:#000000;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">'
        '<tr><td style="border-bottom:2px solid #333333;font-size:1px;line-height:1px;height:1px;">&nbsp;</td></tr>'
        '</table>'
        '</td>'
        '</tr>'

        # Body row
        '<tr>'
        '<td bgcolor="#000000" '
        f'style="padding:20px 30px 40px 30px;background-color:#000000;color:#ffffff;'
        f'font-family:{FONT_FAMILY};font-size:16px;line-height:1.7;font-weight:400;">'
        f'{body_html}'
        '</td>'
        '</tr>'

        # Footer row
        '<tr>'
        '<td bgcolor="#000000" '
        'style="padding:0 30px 30px 30px;background-color:#000000;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">'
        '<tr><td style="border-top:1px solid #333333;font-size:1px;line-height:1px;height:1px;">&nbsp;</td></tr>'
        '</table>'
        f'<p style="color:#888888;font-size:12px;margin:15px 0 0 0;font-family:{FONT_FAMILY};line-height:1.5;">'
        f'&copy; DevNautics &mdash; '
        f'<a href="{WEBSITE_URL}" style="color:#888888;text-decoration:underline;">devnautics.studio</a>'
        '</p>'
        '</td>'
        '</tr>'

        '</table>'
        # End inner container

        '</td>'
        '</tr>'
        '</table>'
        # End full-width wrapper

        '</body></html>'
    )


def _send_email(to_email, subject, html_content):
    """Send an email via SendGrid. Returns True on success."""
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info("Email sent to %s — status %s", to_email, response.status_code)
        return True
    except Exception as exc:
        logger.error("SendGrid email failed for %s: %s", to_email, exc)
        return False


# ── 1. Request Submitted ─────────────────────────────────────────────────────

def send_request_received_email(project):
    """Sent when a user submits a new project request."""
    # Email to the client
    html = _black_email_template(
        "We've Received Your Request",
        f"""
        <p style="color:#ffffff;">Hi {project.full_name},</p>
        <p style="color:#ffffff;">
          Thank you for reaching out to us! Your project request for
          <strong>{project.business_name}</strong> has been successfully received.
        </p>
        <p style="color:#ffffff;">
          Our team will review the details and get back to you shortly.
          In the meantime, feel free to reply to this email if you have
          any additional information to share.
        </p>
        <p style="color:#ffffff;">We appreciate your interest and look forward to working with you!</p>
        <p style="color:#ffffff;">Best regards,<br/>The DevNautics Team</p>
        """,
    )
    _send_email(
        project.email,
        "Your Project Request Has Been Received",
        html,
    )

    # Notification email to admin
    admin_html = _black_email_template(
        "New Project Request Received",
        f"""
        <p style="color:#ffffff;">A new project request has been submitted.</p>
        <table style="color:#ffffff;font-size:16px;margin:10px 0;">
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Name:</td>
              <td style="color:#ffffff;">{project.full_name}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Email:</td>
              <td style="color:#ffffff;">{project.email}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Business:</td>
              <td style="color:#ffffff;">{project.business_name}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Package:</td>
              <td style="color:#ffffff;">{project.package}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Project ID:</td>
              <td style="color:#ffffff;">{project.project_id}</td></tr>
        </table>
        <p style="color:#ffffff;">Please review this request in the admin panel.</p>
        """,
    )
    return _send_email(
        ADMIN_EMAIL,
        f"New Project Request — {project.business_name}",
        admin_html,
    )


# ── 2. Request Reviewed / Approved ───────────────────────────────────────────

def send_welcome_email(project):
    """Sent when a project request is marked as 'reviewed'."""
    html = _black_email_template(
        "Welcome to DevNautics!",
        f"""
        <p style="color:#ffffff;">Hi {project.full_name},</p>
        <p style="color:#ffffff;">
          Great news — your project request has been reviewed and approved!
          We're excited to have you on board and can't wait to bring
          <strong>{project.business_name}</strong> to life.
        </p>
        <p style="color:#ffffff;">
          You can now access your dedicated project portal to track progress,
          communicate with our team, and view updates in real time.
        </p>
        <p style="margin:25px 0;">
          <a href="{PORTAL_URL}"
             style="background-color:#ffffff;color:#000000;padding:12px 28px;
                    text-decoration:none;font-weight:bold;border-radius:4px;
                    display:inline-block;">
            Go to Your Portal
          </a>
        </p>
        <p style="color:#ffffff;">
          Use the following credentials to log in:
        </p>
        <table style="color:#ffffff;font-size:16px;margin:10px 0;">
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Project ID:</td>
              <td style="color:#ffffff;">{project.project_id}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;color:#ffffff;">Email:</td>
              <td style="color:#ffffff;">{project.email}</td></tr>
        </table>
        <p style="color:#ffffff;">
          Use this ID and your email to log in to the portal.
        </p>
        <p style="color:#ffffff;">Best regards,<br/>The DevNautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Welcome to DevNautics — Your Portal Is Ready",
        html,
    )


# ── 3. Project Completed ─────────────────────────────────────────────────────

def send_project_completed_email(project):
    """Sent when a project is marked as 'completed'."""
    html = _black_email_template(
        "Thank You!",
        f"""
        <p style="color:#ffffff;">Hi {project.full_name},</p>
        <p style="color:#ffffff;">
          We're happy to let you know that your project for
          <strong>{project.business_name}</strong> has been marked as
          <strong>completed</strong>.
        </p>
        <p style="color:#ffffff;">
          It has been a pleasure working with you. We hope the final
          result meets — and exceeds — your expectations.
        </p>
        <p style="color:#ffffff;">
          If you have any feedback or need further assistance, don't
          hesitate to reach out. We'd love to hear from you!
        </p>
        <p style="color:#ffffff;">Thank you for choosing DevNautics.</p>
        <p style="color:#ffffff;">Warm regards,<br/>The DevNautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Your Project Is Complete — Thank You!",
        html,
    )


# ── 4. Request Rejected ──────────────────────────────────────────────────────

def send_request_rejected_email(project):
    """Sent when a project request is marked as 'rejected'."""
    html = _black_email_template(
        "Project Request Update",
        f"""
        <p style="color:#ffffff;">Hi {project.full_name},</p>
        <p style="color:#ffffff;">
          After careful review, we're unable to proceed with your project
          request for <strong>{project.business_name}</strong> at this time.
        </p>
        <p style="color:#ffffff;">
          If you have any questions or would like to discuss this further,
          please feel free to reach out to us.
        </p>
        <p style="color:#ffffff;">Best regards,<br/>The DevNautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Update on Your Project Request",
        html,
    )
