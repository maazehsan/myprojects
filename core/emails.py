import logging

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

PORTAL_URL = "https://portal.devnautics.studio"
WEBSITE_URL = "https://devnautics.studio"
ADMIN_EMAIL = "info@devnautics.com"

FONT_FAMILY = '"Roboto Slab", Georgia, "Times New Roman", serif'


def _black_email_template(heading, body_html):
    """Wrap content in a black-background, white-text email layout."""
    return (
        '<!DOCTYPE html>'
        '<html lang="en" xmlns="http://www.w3.org/1999/xhtml">'
        '<head>'
        '<meta charset="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'
        '<meta name="color-scheme" content="light only"/>'
        '<meta name="supported-color-schemes" content="light only"/>'
        '<title>DevNautics</title>'
        '<!--[if mso]>'
        '<style>body,table,td,p,h1,div,span{font-family:Georgia,"Times New Roman",serif!important;'
        'background-color:#000000!important;color:#ffffff!important;}</style>'
        '<![endif]-->'
        '<style>'
        '@import url("https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;580&display=swap");'
        '*{margin:0;padding:0;}'
        'body,html{width:100%;height:100%;'
        'background-color:#000000!important;color:#ffffff!important;}'
        'body{-webkit-text-size-adjust:none;-ms-text-size-adjust:none;}'
        'u+.body .email-bg{background:#000000!important;}'
        '</style>'
        '</head>'
        f'<body class="body" style="margin:0;padding:0;width:100%;'
        f'background-color:#000000;color:#ffffff;font-family:{FONT_FAMILY};" bgcolor="#000000">'
        # Full-width black wrapper
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'width="100%" bgcolor="#000000" '
        'style="background-color:#000000;margin:0;padding:0;" class="email-bg">'
        '<tr>'
        '<td align="center" valign="top" bgcolor="#000000" '
        'style="background-color:#000000;padding:0;">'
        # Inner 600px container
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'width="600" bgcolor="#000000" '
        'style="max-width:600px;width:100%;background-color:#000000;">'
        '<tr>'
        '<td bgcolor="#000000" '
        f'style="padding:40px 20px;background-color:#000000;color:#ffffff;font-family:{FONT_FAMILY};">'
        # Heading
        f'<h1 style="color:#ffffff!important;font-size:28px;margin:0 0 20px 0;'
        f'font-family:{FONT_FAMILY};font-weight:580;">{heading}</h1>'
        # Body
        f'<div style="color:#ffffff!important;font-size:16px;line-height:1.6;'
        f'font-family:{FONT_FAMILY};font-weight:400;">'
        f'{body_html}'
        '</div>'
        # Footer
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" '
        'style="margin-top:30px;border-top:1px solid #333333;padding-top:20px;">'
        '<tr><td bgcolor="#000000" style="background-color:#000000;">'
        f'<p style="color:#999999!important;font-size:12px;margin:0;font-family:{FONT_FAMILY};">'
        f'&copy; DevNautics &mdash; '
        f'<a href="{WEBSITE_URL}" style="color:#999999!important;text-decoration:none;">devnautics.studio</a>'
        '</p>'
        '</td></tr></table>'
        '</td>'
        '</tr>'
        '</table>'
        '</td>'
        '</tr>'
        '</table>'
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
