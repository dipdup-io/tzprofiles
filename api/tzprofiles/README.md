# tzprofiles

DipDup indexer for Tezos Profiles

## Installation

This project is based on [DipDup](https://dipdup.io), a framework for building featureful dapps.

You need a Linux/macOS system with Python 3.11 installed. To install DipDup with pipx for the current user:

```shell
curl -Lsf https://dipdup.io/install.py | python3
```

See the [Installation](https://dipdup.io/docs/installation) page for all options.

## Usage

Run the indexer in memory:

```shell
dipdup run
```

Store data in SQLite database:

```shell
dipdup -c . -c configs/dipdup.sqlite.yaml run
```

Or spawn a Compose stack with PostgreSQL and Hasura:

```shell
cd deploy
cp .env.default .env
# Edit .env file before running
docker-compose up
```

## Development setup

To set up the development environment:

```shell
pdm install
$(pdm venv activate)
```

Run `make all` to run full CI check or `make help` to see other available commands.

## Usage

For now, only a GraphQL API is available at `/v1/graphql` (to be used with
POST). Following are a couple examples of queries.

Retrieve the profile for an account:
```javascript
// Query (escape line returns in strings)
{
  "query":"query MyQuery {
      tzprofiles_by_pk(account: \"tz1XUUF8dS4CxkdNE26DX8SEUPTZnt5t97Tt\") {
        account
        website
        twitter
        logo
        github
        ethereum
        domain_name
        discord
        description
        contract
        alias
      }
    }",
  "variables":null,
  "operationName":"MyQuery"
}

// Response
{
  "data": {
    "tzprofiles_by_pk": {
      "account": "tz1XUUF8dS4CxkdNE26DX8SEUPTZnt5t97Tt",
      "alias": "Testman",
      "contract": "KT1AUeTZ4eyGWpMjxu7b8VLZA8uHnNcwZ4ZF",
      "description": "Test",
      "discord": null,
      "domain_name": null,
      "ethereum": null,
      "github": null,
      "logo": "Testing",
      "twitter": "TestTes57849868",
      "website": "Testing"
    }
  }
}
```

Retrieve the total number of profiles and their account:
```javascript
// Query (escape line returns in strings)
{
  "query":"query MyQuery {
      tzprofiles_aggregate(distinct_on: account) {
        aggregate {
          count(columns: account)
        }
        nodes {
          account
          contract
        }
      }
    }",
  "variables":null,
  "operationName":"MyQuery"
}

// Response
{
  "data": {
    "tzprofiles_aggregate": {
      "aggregate": {
        "count": 13
      },
      "nodes": [
        ...
      ]
    }
  }
}
```

## Architecture

```
┌──────────┐      ┌────┐
│Blockchain◄──────┤TzKT│
└──────────┘      └──▲─┘
                     │
             ┌───────┼──────┐
┌──────┐     │  ┌────┴───┐  │
│Kepler◄─────┼──┤DipDup +│  │
└──────┘     │  │Handlers│  │
             │  └────┬───┘  │
             │       │      │
             │ ┌─────▼────┐ │
             │ │PostgresQL│ │
             │ └─────▲────┘ │
             │       │      │
             │   ┌───┴──┐   │
             │   │Hasura│   │
             │   └──▲───┘   │
             └──────┼───────┘
                  Indexer
                    │

                    o
                   -|-
                   / \
```

## Limitations

### Failures in handler

Because Tezos profiles have an off-chain component (HTTP for now), it means the
processing of an origination/update of a profile can fail whilst fetching the
claims. With the current implementation, the indexer will simply store an empty
list of claims and stay that way until the profile is updated or the indexer
restarted.

### Off-chain modifications

Claims are stored off-chain but the indexer only listens to updates to the
smart-contract. For example, if a claim is deleted in Kepler, and the user does
not remove the claim from the list in the contract -- the indexer will continue
to serve the claim.
