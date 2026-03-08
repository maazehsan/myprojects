import logging

from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

PORTAL_URL = "https://portal.devnautics.studio"


def _black_email_template(heading, body_html):
    """Wrap content in a black-background, white-text email layout."""
    return f"""
    <div style="background-color:#000000;color:#ffffff;padding:40px 20px;font-family:Arial,Helvetica,sans-serif;">
      <div style="max-width:600px;margin:0 auto;">
        <h1 style="color:#ffffff;font-size:28px;margin-bottom:20px;">{heading}</h1>
        <div style="color:#ffffff;font-size:16px;line-height:1.6;">
          {body_html}
        </div>
        <hr style="border:1px solid #333;margin:30px 0;" />
        <p style="color:#999999;font-size:12px;">
          &copy; Devnautics &mdash; <a href="{PORTAL_URL}" style="color:#999999;">portal.devnautics.studio</a>
        </p>
      </div>
    </div>
    """


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
    html = _black_email_template(
        "We've Received Your Request",
        f"""
        <p>Hi {project.full_name},</p>
        <p>
          Thank you for reaching out to us! Your project request for
          <strong>{project.business_name}</strong> has been successfully received.
        </p>
        <p>
          Our team will review the details and get back to you shortly.
          In the meantime, feel free to reply to this email if you have
          any additional information to share.
        </p>
        <p>We appreciate your interest and look forward to working with you!</p>
        <p>Best regards,<br/>The Devnautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Your Project Request Has Been Received",
        html,
    )


# ── 2. Request Reviewed / Approved ───────────────────────────────────────────

def send_welcome_email(project):
    """Sent when a project request is marked as 'reviewed'."""
    html = _black_email_template(
        "Welcome to Devnautics!",
        f"""
        <p>Hi {project.full_name},</p>
        <p>
          Great news — your project request has been reviewed and approved!
          We're excited to have you on board and can't wait to bring
          <strong>{project.business_name}</strong> to life.
        </p>
        <p>
          You can now access your dedicated project portal to track progress,
          communicate with our team, and view updates in real time.
        </p>
        <p style="margin:25px 0;">
          <a href="{PORTAL_URL}"
             style="background-color:#ffffff;color:#000000;padding:12px 28px;
                    text-decoration:none;font-weight:bold;border-radius:4px;">
            Go to Your Portal
          </a>
        </p>
        <p>
          Use the following credentials to log in:
        </p>
        <table style="color:#ffffff;font-size:16px;margin:10px 0;">
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;">Project ID:</td>
              <td>{project.project_id}</td></tr>
          <tr><td style="padding:4px 12px 4px 0;font-weight:bold;">Email:</td>
              <td>{project.email}</td></tr>
        </table>
        <p>
          Use this ID and your email to log in to the portal.
        </p>
        <p>Best regards,<br/>The Devnautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Welcome to Devnautics — Your Portal Is Ready",
        html,
    )


# ── 3. Project Completed ─────────────────────────────────────────────────────

def send_project_completed_email(project):
    """Sent when a project is marked as 'completed'."""
    html = _black_email_template(
        "Thank You!",
        f"""
        <p>Hi {project.full_name},</p>
        <p>
          We're happy to let you know that your project for
          <strong>{project.business_name}</strong> has been marked as
          <strong>completed</strong>.
        </p>
        <p>
          It has been a pleasure working with you. We hope the final
          result meets — and exceeds — your expectations.
        </p>
        <p>
          If you have any feedback or need further assistance, don't
          hesitate to reach out. We'd love to hear from you!
        </p>
        <p>Thank you for choosing Devnautics.</p>
        <p>Warm regards,<br/>The Devnautics Team</p>
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
        <p>Hi {project.full_name},</p>
        <p>
          After careful review, we're unable to proceed with your project
          request for <strong>{project.business_name}</strong> at this time.
        </p>
        <p>
          If you have any questions or would like to discuss this further,
          please feel free to reach out to us.
        </p>
        <p>Best regards,<br/>The Devnautics Team</p>
        """,
    )
    return _send_email(
        project.email,
        "Update on Your Project Request",
        html,
    )
