
GC-Schedule Spreadsheet Link:
https://docs.google.com/spreadsheets/d/1AHqHIE94mWCxdjJEJgV3Kf1zbDW4xcjivPI3QmA48s0/edit?usp=sharing




## How to Base64 Encode Your Google Credentials and Set the Environment Variable on Heroku

### 1. Base64 Encode the `google-creds.json` File

#### On UNIX/macOS/Linux

Run the following command in your terminal:

```bash
base64 google-creds.json > google-creds.b64
cat google-creds.b64

#### On Windows
python encode_creds.py

### 2. Set the Environment Variable on Heroku
heroku config:set GOOGLE_CREDS_BASE64='paste_the_base64_string_here'

### 3. Verify the Environment Variable is set
heroku config:get GOOGLE_CREDS_BASE64

### 4. Remove Env Variable if needed
heroku config:unset GOOGLE_CREDS_BASE64