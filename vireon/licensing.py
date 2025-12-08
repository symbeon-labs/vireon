"""
VIREON License Validation System
---------------------------------

Validates enterprise license keys against central server.
Used to gate premium features in the orchestration engine.
"""

import hashlib
import platform
import uuid
import os
from typing import Dict, Optional
from datetime import datetime, timedelta

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class LicenseError(Exception):
    """Raised when license validation fails or limits are exceeded."""
    pass


class LicenseValidator:
    """
    Validates VIREON license keys.
    
    License tiers:
    - Community: No key needed, limited to 2 agents
    - Professional: License key required, up to 10 agents
    - Enterprise: License key + contract, unlimited
    """
    
    VALIDATION_SERVER = os.getenv(
        "VIREON_LICENSE_SERVER",
        "https://license.vireon.ai/api/v1/validate"
    )
    
    def __init__(self, license_key: Optional[str] = None):
        """
        Initialize validator.
        
        Args:
            license_key: License key string (or None for Community)
        """
        self.license_key = license_key
        self._cached_validation: Optional[Dict] = None
        self._cache_expiry: Optional[datetime] = None
    
    def validate(self, force_refresh: bool = False) -> Dict:
        """
        Validate license key.
        
        Returns:
            Dict with validation result:
            {
                "valid": bool,
                "tier": "community" | "professional" | "enterprise",
                "max_agents": int,
                "features": List[str],
                "expires_at": str (ISO format, or None),
                "error": str (if invalid)
            }
        """
        # Check cache first
        if not force_refresh and self._is_cache_valid():
            return self._cached_validation
        
        # No license key = Community tier
        if not self.license_key:
            return self._community_tier()
        
        # Validate against server
        if REQUESTS_AVAILABLE:
            result = self._validate_online()
        else:
            result = self._validate_offline()
        
        # Cache for 1 hour
        self._cached_validation = result
        self._cache_expiry = datetime.now() + timedelta(hours=1)
        
        return result
    
    def _validate_online(self) -> Dict:
        """Validate license key against remote server."""
        try:
            response = requests.post(
                self.VALIDATION_SERVER,
                json={
                    "key": self.license_key,
                    "machine_id": self._get_machine_id(),
                    "timestamp": datetime.now().isoformat(),
                    "version": "0.2.0"
                },
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "valid": False,
                    "tier": "community",
                    "max_agents": 2,
                    "error": f"Server returned {response.status_code}"
                }
        
        except Exception as e:
            # Fallback to offline validation on network error
            print(f"[VIREON] License server unreachable: {e}")
            print("[VIREON] Falling back to offline validation")
            return self._validate_offline()
    
    def _validate_offline(self) -> Dict:
        """
        Offline validation (less secure, fallback only).
        
        License format: VIREON-{TIER}-{HASH}
        Example: VIREON-PRO-A1B2C3D4E5F6
        """
        if not self.license_key.startswith("VIREON-"):
            return {
                "valid": False,
                "tier": "community",
                "max_agents": 2,
                "error": "Invalid license format"
            }
        
        parts = self.license_key.split("-")
        if len(parts) < 3:
            return {
                "valid": False,
                "tier": "community",
                "max_agents": 2,
                "error": "Malformed license key"
            }
        
        tier_map = {
            "PRO": ("professional", 10),
            "ENT": ("enterprise", 999)
        }
        
        tier_code = parts[1]
        if tier_code in tier_map:
            tier, max_agents = tier_map[tier_code]
            return {
                "valid": True,
                "tier": tier,
                "max_agents": max_agents,
                "features": ["governance_rules", "audit_logs"],
                "expires_at": None,  # Unknown in offline mode
                "offline_mode": True
            }
        
        return self._community_tier()
    
    def _community_tier(self) -> Dict:
        """Return Community tier limitations."""
        return {
            "valid": True,
            "tier": "community",
            "max_agents": 2,
            "features": ["basic_orchestration"],
            "expires_at": None
        }
    
    def _get_machine_id(self) -> str:
        """Generate unique machine identifier."""
        machine_data = f"{platform.node()}-{uuid.getnode()}"
        return hashlib.sha256(machine_data.encode()).hexdigest()[:16]
    
    def _is_cache_valid(self) -> bool:
        """Check if cached validation is still valid."""
        if not self._cached_validation or not self._cache_expiry:
            return False
        return datetime.now() < self._cache_expiry
    
    def get_tier(self) -> str:
        """Get current license tier."""
        return self.validate().get("tier", "community")
    
    def can_use_feature(self, feature: str) -> bool:
        """Check if license allows a specific feature."""
        validation = self.validate()
        features = validation.get("features", [])
        return feature in features
    
    def can_use_agents(self, count: int) -> bool:
        """Check if license allows this many agents."""
        validation = self.validate()
        max_agents = validation.get("max_agents", 2)
        return count <= max_agents


def get_license_from_env() -> Optional[str]:
    """Get license key from environment variable."""
    return os.getenv("VIREON_LICENSE_KEY")


# Singleton instance
_validator: Optional[LicenseValidator] = None

def get_validator() -> LicenseValidator:
    """Get global license validator instance."""
    global _validator
    if _validator is None:
        license_key = get_license_from_env()
        _validator = LicenseValidator(license_key)
    return _validator
