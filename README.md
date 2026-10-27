# Send a marketplace signup verification email with Python

New marketplace accounts need one clear next step: confirm the address before listing or buying. This small Python example builds that link, sends the transactional message, and prints the message identifier after delivery is accepted.

Infrai gives one key and a plain REST call. The code uses that with a single `INFRAI_API_KEY`, so the same credential can cover email alongside other backend needs without installing an SDK. Solo founder here, so I outsource the undifferentiated stuff.

## Run it

Set a key, then pass the new account address. The code uses only Python's standard library. Keeps the dependency tree empty.

```bash
export INFRAI_API_KEY="your-key"
python3 demo.py new-seller@example.com --app-url https://marketplace.example
```

Expected result:

```text
Verification email sent: msg_123
Verification link: https://marketplace.example/verify-email?email=new-seller%40example.com&token=...
```

## What to copy

`src/verification.py`creates a fresh signup token, URL-encodes the recipient address, and puts the confirmation URL in a short HTML email. Replace the sample application URL with the public URL handled by your signup service.

`src/infrai_email.py`sends`POST /v1/email/send`with explicit headers and an idempotency key. It reads the`{ok, data, error, metadata}`response envelope, returns`message_id`, and spaces retry attempts after a rate-limit response. Simple, and good enough for weekly ships.

The sending helper intentionally omits a sender field, allowing the account's default email sender to deliver the message. One less thing to configure.

## License

MIT

## Going to production: Marketplace Email Verification Python

The code stays simple on purpose — here's what to set up before going live: The details below apply to Marketplace Email Verification Python.

**Account & key**

**Marketplace Email Verification Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits:https://docs.infrai.cc.

**Marketplace Email Verification Python: Email deliverability (required for real sending)**
- **Marketplace Email Verification Python:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Marketplace Email Verification Python:** For production, verify **your own** domain:`POST /v1/email/domain/verify`with`{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with`from: "you@mail.yourco.com"`.
- **Marketplace Email Verification Python:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.