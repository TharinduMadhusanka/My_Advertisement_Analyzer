from mailjet_rest import Client
import os

def sendMail(user_email, code):
    # Replace with your Mailjet API key
    api_key = 'ed16ed8292569d38e39796e18913482e'  

    # Replace with your Mailjet API secret
    api_secret = '107277c38ab280cb378ca2e7dadcccb0'

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "tharindumakemoney@gmail.com",
                    "Name": "Me"
                },
                "To": [
                    {
                        "Email": user_email,
                        "Name": "You"
                    }
                ],
            "Subject": "Verification Code from Your App",
            "TextPart": f"Your verification code: {code}",
            "HTMLPart": f"<h3>Dear user, your verification code is: {code}</h3>"
            }
        ]
    }
    return mailjet.send.create(data=data)

# testing

# sendMail("hohini4061@backva.com", 1234)

# print(result.status_code)
# print(result.json())
