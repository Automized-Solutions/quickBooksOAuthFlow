# Used to manually create the link for connecting the OAUTH Flow. Recommend creating a gui for clients.

import urllib.parse
import uuid

base_authorization_url = "https://appcenter.intuit.com/connect/oauth2"
client_id = "ABmPx2JtPgXa6zDOUm38Wzy2Bdb0zGAJ7lD3FSKJKZWkXmfpx1"
redirect_uri = "https://gb5wx4evj35w7c6wi6v5clkgxa0gxzuw.lambda-url.us-east-1.on.aws"
scope = "com.intuit.quickbooks.accounting"
state = str(uuid.uuid4().int)[:8]

authorization_url = f"{base_authorization_url}?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&response_type=code&scope={scope}&state={state}"
print(authorization_url)