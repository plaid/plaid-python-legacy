plaid-python-legacy [![Circle CI](https://circleci.com/gh/plaid/plaid-python-legacy.svg?style=svg&circle-token=fe2984b874ce1ba2b219c3c84a10f652ece7e966)](https://circleci.com/gh/plaid/plaid-python-legacy)
============

Client library for Plaid's legacy API.

## Table of Contents

- [plaid-python-legacy](#plaid-python-legacy)
  * [Install](#install)
  * [Documentation](#documentation)
  * [Getting Started](#getting-started)
    + [Public Endpoints](#public-endpoints)
    + [Authenticated Endpoints](#authenticated-endpoints)
  * [Support](#support)
  * [Known Issues](#known-issues)
  * [Contribute](#contribute)
  * [Contributers](#contributers)
  * [License](#license)


## Install

Via pip:

```console
pip install plaid-python-legacy
```

Via source:

```console
git clone git@github.com:plaid/plaid-python-legacy.git
python setup.py install
```

## Documentation

The module supports all Plaid API endpoints.  For complete information about the API, head to the [docs][2].

## Getting Started

### Configuration

```python
from plaid import Client

Client.config({
    'url': 'https://tartan.plaid.com'
})
```

By default, all non-200 responses will throw an error.

For more information on Plaid response codes, head to [codes][3].

```python
from plaid import Client
from plaid import errors as plaid_errors


client = Client(client_id='***', secret='***')
try:
    response = client.connect('bofa', {
        'username': '[something_invalid]',
        'password': '***'
    })
except plaid_errors.UnauthorizedError:
     # handle this
```

If you would prefer to handle non-20x status codes yourself,
you can configure the client to suppress these exceptions

```python
import json

from plaid import Client

Client.config({
    'url': 'https://tartan.plaid.com',
    'suppress_http_errors': True,
})

client = Client(client_id='***', secret='***')

response = client.connect('bofa', {
    'username': '[something_invalid]',
    'password': '***'
})

if response.ok:
    user = response.json()
else:
    # handle non-20x status codes
```

### Public Endpoints

Public endpoints (category information) require no authentication and can be accessed as follows:

```python
from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json


client = Client(client_id='***', secret='***')
categories = client.categories().json()
```

### Authenticated Endpoints
Authenticated endpoints require a valid `client_id` and `secret` to access.  You can use the sandbox client_id and secret for testing (`test_id` and `test_secret`) during development mode.


### Add Connect user

```python
from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json


client = Client(client_id='***', secret='***')
account_type = 'bofa'

try:
    response = client.connect(account_type, {
     'username': '***',
     'password': '***'
    })
except plaid_errors.PlaidError:
     pass
else:
    connect_data = response.json()
```

### MFA add Connect User

```python
from plaid import Client
from plaid import errors as plaid_errors
from plaid.utils import json


client = Client(client_id='***', secret='***')
account_type = 'bofa'

try:
    response = client.connect(account_type, {
     'username': '***',
     'password': '***'
    })
except plaid_errors.PlaidError, e:
     pass
else:
    if response.status_code == 200:
        # User connected
        data = response.json()
    elif response.stat_code == 201:
        # MFA required
        try:
            mfa_response = answer_mfa(response.json())
        except plaid_errors.PlaidError, e:
            pass
        else:
            # check for 200 vs 201 responses
            # 201 indicates that additional MFA steps required


def answer_mfa(data):
    if data['type'] == 'questions':
        # Ask your user for the answer to the question[s].
        # Although questions is a list, there is only ever a
        # single element in this list, at present
        return answer_question([q['question'] for q in data['mfa']])
    elif data['type'] == 'list':
        return answer_list(data['mfa'])
    elif data['type'] == 'selection':
        return answer_selections(data['mfa'])
    else:
        raise Exception('Unknown mfa type from Plaid')


def answer_question(questions):
    # We have magically inferred the answer
    # so we respond immediately
    # In the real world, we would present questions[0]
    # to our user and submit their response
    answer = 'dogs'
    return client.connect_step(account_type, answer)


def answer_list(devices):
    # You should specify the device to which the passcode is sent.
    # The available devices are present in the devices list
    return client.connect_step('bofa', None, options={
        'send_method': {'type': 'phone'}
    })


def answer_selections(selections):
    # We have magically inferred the answers
    # so we respond immediately
    # In the real world, we would present the selection
    # questions and choices to our user and submit their responses
    # in a JSON-encoded array with answers provided
    # in the same order as the given questions
    answer = json.dumps(['Yes', 'No'])
    return client.connect_step(account_type, answer)
```

### Add Auth User

Effectively the same as Connect.

```python
client = Client(client_id='***', secret='***')
response = client.auth('bofa', {
    'username': '***',
    'password': '***'
})
```

### MFA add Auth User

Effectively the same as Connect.

```python
client = Client(client_id='***', secret='***')
response = client.auth('bofa', {
    'username': '***',
    'password': '***'
})

mfa_response = client.auth_step('bofa', 'my_answer')
```

### Upgrade Account

Add a product (auth or connect to the user)

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.upgrade('connect')
```

### Delete User

```python
client = Client(client_id='***', secret='***', access_token='usertoken')

client.connect_delete()  ## deletes Connect user

# OR

client.auth_delete()  ## deletes Auth user
```

### Exchange

Exchange a `public_token` from [Plaid Link][4] for a Plaid access token and then
retrieve account data:

```python
client = Client(client_id='***', secret='***')
response = client.exchange_token('test,chase,connected')
# client.access_token should now be populated with a
# valid access_token;  we can make authenticated requests
client.auth('chase', {
    'username': '***',
    'password': '***'
})
```

### Get Accounts

User previously Auth-ed

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
accounts = client.auth_get().json()
```

### Get Account Balances

User previously added

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.balance()
```

### Get Transactions

User previously Connect-ed

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.connect_get()
transactions = response.json()
```

### Get Info

User previously Info-ed

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.info_get()
info = response.json()
```

### Get Income

User previously Income-ed

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.income_get()
income = response.json()
```
### Get Risk

User previously Risk-ed

```python
client = Client(client_id='***', secret='***', access_token='usertoken')
response = client.risk_get()
risk = response.json()
```

### Institutions

To search through or retrieve a list of all financial institutions supported by Plaid, use the `/institutions/all/search` and `/institutions/all` endpoints:

```python
client = Client(client_id='***', secret='***')

# Search for an institution matching the name 'redwood credit' that supports Connect
institutionSearchResults = client.institution_all_search('redwood credit', 'connect'):

# Pull 200 institutions with, offseting 0 institutions
institutions = client.institutions_all(count=200, offset=0).json()

# Pull 50 institutions that support both Auth and Connect
institutions = client.institutions_all(count=50, offset=0, products=["auth","connect"]).json()

# Pull a single institution
singleInstitution = client.institution('ins_100003').json()
```

For additional information, please see the [API Institutions docs](https://plaid.com/docs/legacy/api#institutions).

**Note:** Use of the `institution_search()` and `institutions()` methods has been deprecated. Use `institution_all_search()` and `institutions_all()` methods instead.

## Attribution & Maintenance

This repository was originally authored by [Chris Forrette](https://github.com/chrisforrette).
Version 1.0.0 was authored by [Ben Plesser](https://github.com/Bpless).

## Support

Open an [issue][5]!

## Known Issues

1. `SSLError: EOF occurred in violation of protocol (_ssl.c:581)`(https://github.com/plaid/plaid-python/issues/62) - Work around is installing `pyopenssl ndg-httpsclient pyasn1`

## Contribute

All pull requests should be linted with flake8 and tested by running:

```console
$ make test
```

## Contributors
- [@chrisforrette](https://github.com/chrisforrette) (Chris Forrette)
- [@gae123](https://github.com/gae123)

## License
[MIT][6]

[1]: https://plaid.com
[2]: https://plaid.com/docs/legacy/api
[3]: https://plaid.com/docs/legacy/api#response-codes
[4]: https://github.com/plaid/link
[5]: https://github.com/plaid/plaid-python-legacy/issues/new
[6]: https://github.com/plaid/plaid-python-legacy/blob/master/LICENSE
