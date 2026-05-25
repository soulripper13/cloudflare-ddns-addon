# Cloudflare DDNS Home Assistant Add-on
[![Support Development](https://img.shields.io/badge/Support-Development-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/soulripper13)

<div align="center">
  <img src="https://dummyimage.com/800x60/0d1117/ffffff&text=Cloudflare%20DDNS%20Home%20Assistant%20Add-on+-+%60%60%60yaml" alt="Hero Banner">
  <br><br>
  <strong>```yaml</strong> 
  <br><br> 
  <a href="https://ko-fi.com/soulripper13">
    <img src="https://storage.ko-fi.com/cdn/kofi5.png?v=6" alt="Support Cloudflare DDNS Home Assistant Add-on on Ko-fi" width="220">
  </a>
</div>

---

## Configuration
```yaml
api_token: "YOUR_CLOUDFLARE_API_TOKEN"
zone_id: "YOUR_ZONE_ID"
hosts:
  - host: "@"
    update_ipv4: true
    update_ipv6: true
    proxied: false
  - host: "vpn"
    update_ipv4: true
    update_ipv6: false
    proxied: true
check_interval: 300
```
### Options
- **api_token**: Your Cloudflare API Token. It needs `Zone.DNS` permissions.
- **zone_id**: The Zone ID for your domain (found on the Cloudflare dashboard).
- **hosts**: A list of records to keep updated.
  - **host**: The hostname (e.g., `vpn` or `@` for the root domain).
  - **update_ipv4**: Set to `true` to update the `A` record.
  - **update_ipv6**: Set to `true` to update the `AAAA` record.
  - **proxied**: Whether the record should be proxied by Cloudflare (orange cloud).
  - **ipv4_url** (optional): Custom URL to fetch public IPv4.
  - **ipv6_url** (optional): Custom URL to fetch public IPv6.
- **check_interval**: How often to check for IP changes (in seconds). Minimum 60.
## Credits
Inspired by the NameSilo DDNS add-on.

---
## Support the Project

This project is developed and maintained in spare time and is provided free to the community.

If you find it useful and would like to support ongoing development, maintenance, and improvements, any contribution is appreciated — but never required ❤️

### Ways to Support

* **Ko-fi**
  [https://ko-fi.com/soulripper13](https://ko-fi.com/soulripper13)

* **PayPal**
  [https://paypal.me/SKatoaroo](https://paypal.me/SKatoaroo)

* **Bitcoin (BTC)**
  `bc1qvu8a9gdy3dcxa94jge7d3rd7claapsydjsjxn0`

* **Solana (SOL)**
  `4jvCR2YFQLqguoyz9qAMPzVbaEcDsG5nzRHFG8SeaeBK`

You can also help by:

* Reporting bugs
* Submitting pull requests
* Suggesting features
* Helping other users
* Starring the repository ⭐

Thank you for being part of the community.
