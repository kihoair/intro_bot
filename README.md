# intro_bot
Tweet bot for everyday Intro practice jam

## Environment
* serverless (node.js)
* AWS account
* awscli
* Node.js 24.x

## How to deploy (Node.js version)

### 1. Install dependencies
```bash
cd lambda-node
npm install
```

### 2. Deploy Lambda Function
```bash
cd lambda-node
sls deploy
```

### 3. Configure Environment Variables
AWS Console > Lambda > introTweetBot > Configuration > Environment variables:
- `BEARER_TOKEN`
- `API_KEY`
- `API_KEY_SECRET`
- `ACCESS_TOKEN`
- `ACCESS_TOKEN_SECRET`

## Testing

### Local Test (Node.js)
```bash
cd lambda-node

# Test with today's date
node test_local.js

# Test with specific date
DEBUG_DATE=2025-12-20 node test_local.js
```

### AWS Lambda Console Test
1. Go to AWS Console > Lambda > introTweetBot
2. Click "Test" tab
3. Configure test event:
```json
{
  "DEBUG_MODE": "true",
  "DEBUG_DATE": "2025-12-20"
}
```
4. Or set environment variables:
   - `DEBUG_MODE`: `true`
   - `DEBUG_DATE`: `2025-12-20` (YYYY-MM-DD format)
5. Click "Test" button

**Note:** When `DEBUG_MODE=true`, tweets are NOT sent. Only the generated tweet text is returned.

## Debug Mode

| Variable | Description |
|----------|-------------|
| `DEBUG_MODE` | Set to `true` to prevent actual tweets |
| `DEBUG_DATE` | Test with specific date (YYYY-MM-DD format). Only works when DEBUG_MODE=true |

## Project Structure
```
intro_bot/
├── lambda-node/             # Node.js Lambda (recommended)
│   ├── index.js             # Main handler
│   ├── webscrape.js         # Web scraping logic
│   ├── test_local.js        # Local test script
│   ├── serverless.yml       # Lambda config
│   └── package.json         # Node.js dependencies
├── lambda/                  # Python Lambda (deprecated)
│   ├── lambda_function.py
│   ├── webscrape.py
│   └── ...
├── selenium-layer/          # (deprecated - not needed for Node.js)
└── README.md
```

## Migration Notes

The project was migrated from Python+Selenium to Node.js+Puppeteer because:
- `@sparticuz/chromium` provides actively maintained Chrome binaries for Lambda
- No need for separate Lambda Layer setup
- npm manages all dependencies automatically
