"""
IP Feature Engineering Module
Extracts comprehensive features from IP addresses for ML models
"""

import ipaddress
import socket
import logging
from typing import Dict, Any, Optional
import geoip2.database
import dns.resolver
import requests
from ipwhois import IPWhois

logger = logging.getLogger(__name__)


class IPFeatureExtractor:
    """Extract features from IP addresses for masked IP detection"""
    
    def __init__(self, geoip_db_path: str = None, asn_db_path: str = None):
        """
        Initialize feature extractor
        
        Args:
            geoip_db_path: Path to MaxMind GeoIP2 City database
            asn_db_path: Path to MaxMind GeoIP2 ASN database
        """
        self.geoip_db_path = geoip_db_path
        self.asn_db_path = asn_db_path
        
        # Initialize GeoIP readers if paths provided
        self.geo_reader = None
        self.asn_reader = None
        
        if geoip_db_path:
            try:
                self.geo_reader = geoip2.database.Reader(geoip_db_path)
                logger.info("GeoIP database loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load GeoIP database: {e}")
        
        if asn_db_path:
            try:
                self.asn_reader = geoip2.database.Reader(asn_db_path)
                logger.info("ASN database loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load ASN database: {e}")
    
    def extract_all_features(self, ip: str) -> Dict[str, Any]:
        """Extract all available features from an IP address"""
        
        features = {
            'ip_address': ip,
        }
        
        # Basic IP features
        features.update(self._extract_basic_ip_features(ip))
        
        # Geolocation features
        features.update(self._extract_geo_features(ip))
        
        # ASN features
        features.update(self._extract_asn_features(ip))
        
        # DNS features
        features.update(self._extract_dns_features(ip))
        
        # Network features
        features.update(self._extract_network_features(ip))
        
        # Reputation features
        features.update(self._extract_reputation_features(ip))
        
        return features
    
    def _extract_basic_ip_features(self, ip: str) -> Dict[str, Any]:
        """Extract basic IP address features"""
        
        features = {}
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            features['ip_version'] = ip_obj.version
            features['is_private'] = int(ip_obj.is_private)
            features['is_reserved'] = int(ip_obj.is_reserved)
            features['is_loopback'] = int(ip_obj.is_loopback)
            features['is_multicast'] = int(ip_obj.is_multicast)
            features['is_link_local'] = int(ip_obj.is_link_local)
            
            # IP numerical representation
            features['ip_int'] = int(ip_obj)
            
            # Octets for IPv4
            if ip_obj.version == 4:
                octets = str(ip).split('.')
                features['octet_1'] = int(octets[0])
                features['octet_2'] = int(octets[1])
                features['octet_3'] = int(octets[2])
                features['octet_4'] = int(octets[3])
            else:
                features['octet_1'] = 0
                features['octet_2'] = 0
                features['octet_3'] = 0
                features['octet_4'] = 0
            
        except Exception as e:
            logger.error(f"Error extracting basic IP features for {ip}: {e}")
            features.update({
                'ip_version': 0,
                'is_private': 0,
                'is_reserved': 0,
                'is_loopback': 0,
                'is_multicast': 0,
                'is_link_local': 0,
                'ip_int': 0,
                'octet_1': 0,
                'octet_2': 0,
                'octet_3': 0,
                'octet_4': 0,
            })
        
        return features
    
    def _extract_geo_features(self, ip: str) -> Dict[str, Any]:
        """Extract geolocation features"""
        
        features = {
            'country_code': 'Unknown',
            'country_name': 'Unknown',
            'city': 'Unknown',
            'latitude': 0.0,
            'longitude': 0.0,
            'accuracy_radius': 0,
            'is_anonymous_proxy': 0,
            'is_satellite_provider': 0,
        }
        
        if not self.geo_reader:
            return features
        
        try:
            response = self.geo_reader.city(ip)
            
            if response.country:
                features['country_code'] = response.country.iso_code or 'Unknown'
                features['country_name'] = response.country.name or 'Unknown'
            
            if response.city:
                features['city'] = response.city.name or 'Unknown'
            
            if response.location:
                features['latitude'] = response.location.latitude or 0.0
                features['longitude'] = response.location.longitude or 0.0
                features['accuracy_radius'] = response.location.accuracy_radius or 0
            
            if hasattr(response, 'traits'):
                features['is_anonymous_proxy'] = int(
                    response.traits.is_anonymous_proxy or False
                )
                features['is_satellite_provider'] = int(
                    response.traits.is_satellite_provider or False
                )
            
        except Exception as e:
            logger.debug(f"Could not get geo data for {ip}: {e}")
        
        return features
    
    def _extract_asn_features(self, ip: str) -> Dict[str, Any]:
        """Extract ASN (Autonomous System Number) features"""
        
        features = {
            'asn': 0,
            'asn_org': 'Unknown',
            'asn_network': 'Unknown',
        }
        
        if self.asn_reader:
            try:
                response = self.asn_reader.asn(ip)
                features['asn'] = response.autonomous_system_number or 0
                features['asn_org'] = response.autonomous_system_organization or 'Unknown'
                features['asn_network'] = str(response.network) if response.network else 'Unknown'
            except Exception as e:
                logger.debug(f"Could not get ASN data for {ip}: {e}")
        else:
            # Fallback to IPWhois
            try:
                obj = IPWhois(ip)
                results = obj.lookup_rdap(depth=1)
                features['asn'] = int(results.get('asn', 0).replace('AS', ''))
                features['asn_org'] = results.get('asn_description', 'Unknown')
            except Exception as e:
                logger.debug(f"IPWhois lookup failed for {ip}: {e}")
        
        return features
    
    def _extract_dns_features(self, ip: str) -> Dict[str, Any]:
        """Extract DNS-related features"""
        
        features = {
            'has_ptr_record': 0,
            'ptr_record': 'None',
            'ptr_contains_host': 0,
            'ptr_contains_ip': 0,
        }
        
        try:
            # Reverse DNS lookup
            hostname = socket.gethostbyaddr(ip)[0]
            features['has_ptr_record'] = 1
            features['ptr_record'] = hostname
            
            # Check if PTR contains common hosting/VPN keywords
            keywords = ['host', 'server', 'vpn', 'proxy', 'tor', 'node', 'exit']
            features['ptr_contains_host'] = int(
                any(kw in hostname.lower() for kw in keywords)
            )
            
            # Check if PTR contains IP digits
            features['ptr_contains_ip'] = int(
                any(digit in hostname for digit in ip.replace('.', ''))
            )
            
        except Exception as e:
            logger.debug(f"DNS lookup failed for {ip}: {e}")
        
        return features
    
    def _extract_network_features(self, ip: str) -> Dict[str, Any]:
        """Extract network-related features"""
        
        features = {
            'ping_responsive': 0,
            'common_ports_open': 0,
        }
        
        # Note: Port scanning should be done carefully and only on authorized networks
        # This is a placeholder for feature structure
        
        return features
    
    def _extract_reputation_features(self, ip: str) -> Dict[str, Any]:
        """Extract IP reputation features"""
        
        features = {
            'in_tor_list': 0,
            'in_proxy_list': 0,
            'in_vpn_list': 0,
            'in_abuse_list': 0,
            'reputation_score': 50,  # Default neutral score
        }
        
        # These would be populated from your collected databases
        # In real implementation, query against your IP reputation database
        
        return features
    
    def __del__(self):
        """Cleanup database readers"""
        if self.geo_reader:
            self.geo_reader.close()
        if self.asn_reader:
            self.asn_reader.close()


class BehavioralFeatureExtractor:
    """Extract behavioral features from request patterns"""
    
    def __init__(self):
        self.ip_history = {}
    
    def extract_behavioral_features(
        self, 
        ip: str, 
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract behavioral features from request patterns"""
        
        features = {
            'request_count': 0,
            'unique_user_agents': 0,
            'avg_time_between_requests': 0,
            'requests_per_minute': 0,
            'failed_auth_attempts': 0,
            'different_endpoints': 0,
            'suspicious_patterns': 0,
        }
        
        # Track IP history
        if ip not in self.ip_history:
            self.ip_history[ip] = {
                'requests': [],
                'user_agents': set(),
                'endpoints': set(),
                'timestamps': [],
            }
        
        # Update history
        history = self.ip_history[ip]
        history['requests'].append(request_data)
        
        if 'user_agent' in request_data:
            history['user_agents'].add(request_data['user_agent'])
        
        if 'endpoint' in request_data:
            history['endpoints'].add(request_data['endpoint'])
        
        if 'timestamp' in request_data:
            history['timestamps'].append(request_data['timestamp'])
        
        # Calculate features
        features['request_count'] = len(history['requests'])
        features['unique_user_agents'] = len(history['user_agents'])
        features['different_endpoints'] = len(history['endpoints'])
        
        # Calculate request rate
        if len(history['timestamps']) > 1:
            timestamps = sorted(history['timestamps'])
            time_diffs = [
                (timestamps[i+1] - timestamps[i]).total_seconds() 
                for i in range(len(timestamps)-1)
            ]
            features['avg_time_between_requests'] = sum(time_diffs) / len(time_diffs)
            
            # Requests per minute
            total_time = (timestamps[-1] - timestamps[0]).total_seconds() / 60
            if total_time > 0:
                features['requests_per_minute'] = len(timestamps) / total_time
        
        return features


def main():
    """Test feature extraction"""
    
    logging.basicConfig(level=logging.INFO)
    
    # Test IP addresses
    test_ips = [
        '8.8.8.8',  # Google DNS
        '1.1.1.1',  # Cloudflare
        '192.168.1.1',  # Private IP
    ]
    
    extractor = IPFeatureExtractor()
    
    for ip in test_ips:
        print(f"\n{'='*50}")
        print(f"Features for {ip}:")
        print('='*50)
        
        features = extractor.extract_all_features(ip)
        
        for key, value in features.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()