# Cisco IOS XR Automation Framework

This repository provides a modular Python-based automation tool for configuring Cisco IOS XR routers across multiple services and protocols. It leverages Netmiko for SSH connectivity and JSON-based configuration files for reproducibility, scalability, and operational clarity.

## 🚀 Features

- Multi-device provisioning via IP list
- Modular configuration functions for:
  - IP addressing
  - MPLS LDP
  - OSPF
  - ISIS
  - Layer 2 VPN (VPWS & VPLS)
- JSON-driven configuration inputs
- Exception handling for robust deployment

## 📁 File Structure

| File                  | Purpose                                      |
|-----------------------|----------------------------------------------|
| `ios_xr.py`           | Main automation script                       |
| `cred.json`           | Stores device login credentials              |
| `ip_config.json`      | Interface IP configurations per device       |
| `mpls_config.json`    | MPLS LDP interface mappings                  |
| `ospf_config.json`    | OSPF area and interface assignments          |
| `isis_config.json`    | ISIS interface and address-family mappings   |
| `vpws_config.json`    | VPWS peer and interface definitions          |
| `vpls_config.json`    | VPLS bridge-domain and VFI configurations    |

## 🧠 Design Rationale

### 📦 Why Use JSON Uploads?

This framework uses external `.json` files to define device configurations for several key reasons:

- **Separation of Logic and Data**: Configuration data is decoupled from the automation logic, making the script reusable across environments.
- **Reproducibility**: JSON files serve as version-controlled inputs for auditability and rollback.
- **Scalability**: Adding new devices or services is as simple as updating a JSON file.
- **Security**: Credentials are stored separately in `cred.json`, simplifying encryption and access control.
- **Flexibility**: Each device can have unique configurations without modifying the core script.

### 🧩 Why This Modular Structure?

- **Granular Control**: Each protocol is configured via its own function.
- **Ease of Maintenance**: Isolated logic makes debugging and updates straightforward.
- **Parallel Development**: Teams can work on different modules independently.
- **Future-Proofing**: New services can be added without disrupting existing logic.

## 🛠 Requirements

- Python 3.8+
- `netmiko`
- `paramiko`

Install dependencies:
```bash
pip install netmiko paramiko


This project is open to improvement. If you have ideas for new features, better modularity, or support for additional platforms, feel free to fork the repo, submit pull requests, or open issues. Collaboration is welcome—whether you're refining the logic, optimizing performance, or expanding protocol support.