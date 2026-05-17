import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime

OPTIONS_FILE = "/data/options.json"

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}", flush=True)

def get_public_ip(ipv6=False, custom_url=None):
    url = custom_url if custom_url else ("https://ipv6.icanhazip.com" if ipv6 else "https://ipv4.icanhazip.com")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        log(f"Error fetching {'IPv6' if ipv6 else 'IPv4'} from {url}: {e}")
        return None

def cloudflare_request(method, endpoint, api_token, data=None):
    url = f"https://api.cloudflare.com/client/v4/{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    req_body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            error_body = json.loads(e.read().decode("utf-8"))
            log(f"Cloudflare API Error ({endpoint}): {error_body.get('errors', 'Unknown error')}")
        except:
            log(f"HTTP Error calling Cloudflare ({endpoint}): {e}")
        return None
    except Exception as e:
        log(f"Unexpected error calling Cloudflare ({endpoint}): {e}")
        return None

def update_dns():
    if not os.path.exists(OPTIONS_FILE):
        log(f"Config file not found: {OPTIONS_FILE}")
        return

    try:
        with open(OPTIONS_FILE, "r") as f:
            options = json.load(f)
    except Exception as e:
        log(f"Error reading options: {e}")
        return

    api_token = options.get("api_token")
    zone_id = options.get("zone_id")
    hosts_config = options.get("hosts", [])
    
    if not api_token or not zone_id:
        log("API Token or Zone ID missing in config.")
        return

    if not hosts_config:
        log("No hosts configured.")
        return

    # Fetch zone info to get the domain name if needed
    zone_info = cloudflare_request("GET", f"zones/{zone_id}", api_token)
    if not zone_info or not zone_info.get("success"):
        log(f"Failed to fetch zone info for {zone_id}")
        return
    
    zone_name = zone_info["result"]["name"]

    # Fetch existing records for this zone
    records_resp = cloudflare_request("GET", f"zones/{zone_id}/dns_records?per_page=100", api_token)
    if not records_resp or not records_resp.get("success"):
        log(f"Failed to fetch DNS records for zone {zone_id}")
        return

    records = records_resp["result"]
    
    for config in hosts_config:
        host = config.get("host", "@")
        full_host = zone_name if host == "@" else (host if zone_name in host else f"{host}.{zone_name}")
        update_ipv4 = config.get("update_ipv4", True)
        update_ipv6 = config.get("update_ipv6", False)
        proxied = config.get("proxied", False)
        ipv4_url = config.get("ipv4_url")
        ipv6_url = config.get("ipv6_url")

        # Process IPv4
        if update_ipv4:
            current_ipv4 = get_public_ip(False, ipv4_url)
            if current_ipv4:
                found_record = next((r for r in records if r["name"] == full_host and r["type"] == "A"), None)
                if found_record:
                    if found_record["content"] != current_ipv4 or found_record["proxied"] != proxied:
                        log(f"Updating {full_host} (A) to {current_ipv4} (proxied: {proxied})")
                        update_data = {
                            "type": "A",
                            "name": full_host,
                            "content": current_ipv4,
                            "ttl": 1 if proxied else 3600,
                            "proxied": proxied
                        }
                        res = cloudflare_request("PATCH", f"zones/{zone_id}/dns_records/{found_record['id']}", api_token, update_data)
                        if res and res.get("success"):
                            log(f"Successfully updated {full_host} (A)")
                        else:
                            log(f"Failed to update {full_host} (A)")
                    else:
                        log(f"{full_host} (A) is already up to date ({current_ipv4})")
                else:
                    log(f"Record {full_host} (A) not found. Creating it...")
                    create_data = {
                        "type": "A",
                        "name": full_host,
                        "content": current_ipv4,
                        "ttl": 1 if proxied else 3600,
                        "proxied": proxied
                    }
                    res = cloudflare_request("POST", f"zones/{zone_id}/dns_records", api_token, create_data)
                    if res and res.get("success"):
                        log(f"Successfully created {full_host} (A)")
                    else:
                        log(f"Failed to create {full_host} (A)")

        # Process IPv6
        if update_ipv6:
            current_ipv6 = get_public_ip(True, ipv6_url)
            if current_ipv6:
                found_record = next((r for r in records if r["name"] == full_host and r["type"] == "AAAA"), None)
                if found_record:
                    if found_record["content"] != current_ipv6 or found_record["proxied"] != proxied:
                        log(f"Updating {full_host} (AAAA) to {current_ipv6} (proxied: {proxied})")
                        update_data = {
                            "type": "AAAA",
                            "name": full_host,
                            "content": current_ipv6,
                            "ttl": 1 if proxied else 3600,
                            "proxied": proxied
                        }
                        res = cloudflare_request("PATCH", f"zones/{zone_id}/dns_records/{found_record['id']}", api_token, update_data)
                        if res and res.get("success"):
                            log(f"Successfully updated {full_host} (AAAA)")
                        else:
                            log(f"Failed to update {full_host} (AAAA)")
                    else:
                        log(f"{full_host} (AAAA) is already up to date ({current_ipv6})")
                else:
                    log(f"Record {full_host} (AAAA) not found. Creating it...")
                    create_data = {
                        "type": "AAAA",
                        "name": full_host,
                        "content": current_ipv6,
                        "ttl": 1 if proxied else 3600,
                        "proxied": proxied
                    }
                    res = cloudflare_request("POST", f"zones/{zone_id}/dns_records", api_token, create_data)
                    if res and res.get("success"):
                        log(f"Successfully created {full_host} (AAAA)")
                    else:
                        log(f"Failed to create {full_host} (AAAA)")

def main():
    log("Cloudflare DDNS starting...")
    while True:
        try:
            update_dns()
        except Exception as e:
            log(f"Unhandled exception in loop: {e}")
        
        interval = 300
        try:
            if os.path.exists(OPTIONS_FILE):
                with open(OPTIONS_FILE, "r") as f:
                    options = json.load(f)
                    interval = options.get("check_interval", 300)
        except:
            pass
        
        log(f"Waiting {interval} seconds...")
        time.sleep(max(60, interval))

if __name__ == "__main__":
    main()
