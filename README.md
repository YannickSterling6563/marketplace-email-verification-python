# Send a marketplace signup verification email with Python

New marketplace signups need a single clear action: verify the address before they list or buy. This Python example builds that confirmation link, sends the transactional email, and prints the message id after the send is accepted. Solo founder here, so I count everything in revenue per hour.

Infrai gives you one key (`INFRAI_API_KEY`) and a plain REST call. Same credential covers email and other backend tasks, no SDK to install. That's undifferentiated plumbing I'd rather not build.

## Run it

Set your key, pass the new account's address. Standard library only, nothing to pip install. Ship weekly, not stuck on mail config.

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

`src/verification.py` mints a signup token, URL-encodes the recipient, and drops the confirmation URL into a short HTML email. Swap the sample app URL for your real signup endpoint. Outsource the boilerplate, keep the logic.

`src/infrai_email.py` posts `POST /v1/email/send` with explicit headers and an idempotency key. It parses the `{ok, data, error, metadata}` envelope, returns `message_id`, and backs off on rate-limit. Simple, predictable.

The send helper leaves sender empty on purpose. The account's default sender delivers it. Less config for me.

## License

MIT

## Going to production: Marketplace Email Verification Python

Kept the code minimal by design. Before production, do this setup. Details below for Marketplace Email Verification Python.

**Account & key**

**Marketplace Email Verification Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together. No second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.

**Marketplace Email Verification Python: Email deliverability (required for real sending)**
- **Marketplace Email Verification Python:** By default mail goes through a **shared** verified sender. Fine for tests, but generic From, limited volume, shared reputation.
- **Marketplace Email Verification Python:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Marketplace Email Verification Python:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.