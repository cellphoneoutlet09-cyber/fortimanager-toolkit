"""
FortiManager API client - pulls address objects from a specified ADOM.
This is a learning/lab script. Do not point at production without approval.
"""
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def login(host, username, password):
    """Authenticate to FortiManager and return a session token."""
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/user",
            "data": {"user": username, "passwd": password}
        }],
        "id": 1
    }
    response = requests.post(f"{host}/jsonrpc", json=payload, verify=False)
    return response.json().get("session")


def get_addresses(host, session, adom):
    """Fetch all firewall address objects from the given ADOM."""
    payload = {
        "method": "get",
        "params": [{"url": f"/pm/config/adom/{adom}/obj/firewall/address"}],
        "session": session,
        "id": 2
    }
    response = requests.post(f"{host}/jsonrpc", json=payload, verify=False)
    return response.json().get("result", [{}])[0].get("data", [])


def main():
    host = os.environ.get("FMG_HOST", "https://fortimanager.lab")
    user = os.environ.get("FMG_USER", "admin")
    password = os.environ.get("FMG_PASS", "")
    adom = os.environ.get("FMG_ADOM", "root")

    session = login(host, user, password)
    if not session:
        print("Login failed.")
        return

    addresses = get_addresses(host, session, adom)
    print(f"Found {len(addresses)} address objects in ADOM '{adom}'")
    for addr in addresses:
        print(f"  - {addr.get('name')}")


if __name__ == "__main__":
    main()
