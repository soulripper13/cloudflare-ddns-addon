# Cloudflare DDNS Home Assistant Add-on

Dynamic DNS client for Cloudflare supporting IPv4 and IPv6.

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
