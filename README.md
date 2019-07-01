# Mars Clock as Serverless API

We use zeit now as our serverless platform.

## What does it do

This API provides several endpoints to help Martians with their daily life.

### Endpoints

1. `/`: meta data of the api including descriptions of endpoints
2. `/now`: get the martian time for now
3. `/epoch/(epoch_time)`: calculate martian time based on the unix eopch time input

Examples:

1. `https://marsapi.interimm.org/now`
2. `https://marsapi.interimm.org/epoch/1562018066`

## Development

1. Write your function and add routes to `now.json`.
2. Deplow with `now`.

## References

1. [Barebone Serverless Python JSON API on Zeit Now](https://camillovisini.com/barebone-serverless-python-json-api-on-zeit-now/)
2. [visini/barebone-serverless-api-zeit-now](https://github.com/visini/barebone-serverless-api-zeit-now)