document.addEventListener('DOMContentLoaded', function() {

  // Buttons change view and the url
  document.querySelector('#inbox').addEventListener('click', () => {
    load_mailbox('inbox');
    history.pushState({ mailbox: 'inbox' }, "", "/mail/inbox2");
  });

  document.querySelector('#sent').addEventListener('click', () => {
    load_mailbox('sent');
    history.pushState({ mailbox: 'sent' }, "", "/mail/sent");
  });

  document.querySelector('#archived').addEventListener('click', () => {
    load_mailbox('archive');
    history.pushState({ mailbox: 'archive' }, "", "/mail/archive");
  });

  document.querySelector('#compose').addEventListener('click', () => {
    compose_email();
    history.pushState({ page: 'compose' }, "", "/mail/compose");
  });


  // By default, load the inbox but when refresh at other page then load that page
  const path = window.location.pathname;
  if (path === "/mail/inbox2") {
    load_mailbox('inbox');
  } else if (path === "/mail/sent") {
    load_mailbox('sent');
  } else if (path === "/mail/archive") {
    load_mailbox('archive');
  } else if (path === "/mail/compose") {
    compose_email();
  } else {
    load_mailbox('inbox');
  }
});

// Going forward or backwards in browser 
window.onpopstate = function(event) {
  if (event.state) {
    if (event.state.mailbox) {
      load_mailbox(event.state.mailbox);
    } else if (event.state.page === 'compose') {
      compose_email();
    }
  }
};
 
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Handle form submission once, outside of compose_email function
document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#compose-form').onsubmit = function(event) {
    event.preventDefault(); // Prevent full page reload

    fetch('/mail/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent'); // After sending, show Sent mailbox
      history.pushState({ mailbox: 'sent' }, "", "/mail/sent");
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };
});


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails from the server
  fetch(`/mail/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Check if mailbox is empty
    if (emails.length === 0) {
      const emptyState = document.createElement('div');
      emptyState.className = 'empty-state';
      
      // Different messages based on mailbox type
      let message = '';
      let icon = '';
      
      if (mailbox === 'inbox') {
        icon = '📭';
        message = 'Your inbox is empty';
      } else if (mailbox === 'sent') {
        icon = '📤';
        message = 'No sent emails yet';
      } else if (mailbox === 'archive') {
        icon = '📦';
        message = 'No archived emails';
      }
      
      emptyState.innerHTML = `
        <div class="empty-icon">${icon}</div>
        <div class="empty-message">${message}</div>
      `;
      
      document.querySelector('#emails-view').append(emptyState);
    } else {
      // Display emails
      emails.forEach(email => {
        const element = document.createElement('div');
        element.innerHTML = `<strong>${email.sender}</strong> ${email.subject} <span style="float:right;">${email.timestamp}</span>`;
        element.className = 'email-item';
        if (email.read) {
          element.classList.add("read");
        } else {
          element.classList.add("unread");
        }

        // Clicking opens the email
        element.addEventListener('click', () => view_email(email.id));

        document.querySelector('#emails-view').append(element);
      });
    }
  });
}

function view_email(id) {
  // Show single email view
  document.querySelector('#emails-view').innerHTML = '';

  fetch(`/mail/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      const container = document.createElement('div');
      container.innerHTML = `
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Subject:</strong> ${email.subject}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
      `;

      // Mark as read
      fetch(`/mail/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({ read: true })
      });
      
      const currentUser = document.body.dataset.user;

      // Only the receiver will be shown these buttons
      if (email.sender !== currentUser) {

        // Archive and Unarchive button
        const archiveButton = document.createElement('button');
        archiveButton.textContent = email.archived ? 'Unarchive' : 'Archive';
        archiveButton.className = 'btn btn-primary';
        archiveButton.addEventListener('click', () => {
          fetch(`/mail/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ archived: !email.archived })
          }).then(() => {
            load_mailbox('inbox');
            history.pushState({ mailbox: 'inbox' }, "", "/mail/inbox");
          });
        });

        // Reply button
        const replyButton = document.createElement('button');
        replyButton.textContent = 'Reply';
        replyButton.className = 'btn btn-primary';
        replyButton.addEventListener('click', () => {
          compose_email();
          history.pushState({ page: 'compose' }, "", "/mail/compose");
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : 'Re: ' + email.subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n`;
        });

        container.append(archiveButton);
        container.append(replyButton);
      }

      document.querySelector('#emails-view').append(container);
    });
}