# quickBooksOAuthFlow
 These python files can be run in Lambda to create the OAuth flow for Quickbooks.

## Step 1
Create the 2 function in Lambda with a public URL trigger. THis trigger url will become your redirect URI. 

## Step 2
Create the 3 function in Lambda with a public URL. Update the 2 function URL at the bottom with this URL. 

## Step 3
Publish lambda functions 2 & 3

## Step 4
Create the URL using the client values and the redirect URI from the 2 function.

