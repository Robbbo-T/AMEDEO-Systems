#!/usr/bin/env python3
"""Health check for GAIA AIR blockchain nodes"""

import requests
import sys
import os

def check_health():
    """Check node health status"""
    try:
        # Determine node type from environment
        node_type = os.getenv('NODE_TYPE', 'validator')
        
        if node_type == 'api':
            url = 'http://localhost:8080/health'
        else:
            url = 'https://localhost:9443/healthz'
        
        response = requests.get(url, timeout=5, verify=False)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    
    return False

if __name__ == '__main__':
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)