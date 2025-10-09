import re
import requests
from urllib.parse import urlparse
import tldextract

class PhishingDetector:
    def __init__(self):
        self.suspicious_keywords = [
            'verify your account', 'click here', 'urgent action',
            'suspended account', 'confirm identity', 'limited time',
            'update payment', 'security alert', 'unusual sign-in'
        ]
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.top', '.click', '.download']
        self.brand_names = ['paypal', 'amazon', 'microsoft', 'apple', 'google', 'facebook']
        self.virustotal_api_key = None  # Set your API key in config

    def analyze_email(self, email_data):
        score = 0
        reasons = []
        
        # Sender analysis
        sender = email_data.get('from', '').lower()
        if self._is_suspicious_sender(sender):
            score += 30
            reasons.append("Suspicious sender domain")
        
        # Link analysis
        links = email_data.get('links', [])
        for link in links:
            link_score, link_reasons = self._analyze_link(link)
            score += link_score
            reasons.extend(link_reasons)
        
        # Content analysis
        body = email_data.get('body', '').lower()
        for keyword in self.suspicious_keywords:
            if keyword in body:
                score += 15
                reasons.append(f"Suspicious keyword: '{keyword}'")
        
        # Brand impersonation check
        for brand in self.brand_names:
            if brand in body and brand not in sender:
                score += 25
                reasons.append(f"Potential {brand} impersonation")
        
        # Attachment analysis
        if email_data.get('has_attachments', False):
            score += 20
            reasons.append("Suspicious attachments detected")
        
        # Classification
        if score >= 50:
            return {"result": "PHISHING", "score": score, "reasons": reasons}
        elif score >= 30:
            return {"result": "SUSPICIOUS", "score": score, "reasons": reasons}
        else:
            return {"result": "SAFE", "score": score, "reasons": reasons}

    def _is_suspicious_sender(self, sender):
        extracted = tldextract.extract(sender)
        return (
            extracted.suffix in self.suspicious_tlds or
            'noreply' not in sender or
            len(extracted.domain) < 3
        )

    def _analyze_link(self, url):
        score = 0
        reasons = []
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            extracted = tldextract.extract(domain)
            
            # Check suspicious TLDs
            if extracted.suffix in self.suspicious_tlds:
                score += 25
                reasons.append(f"Suspicious TLD: {extracted.suffix}")
            
            # Check for homograph attacks
            if self._is_homograph_attack(domain):
                score += 30
                reasons.append("Possible homograph attack")
            
            # Check for URL shorteners
            if self._is_shortener(domain):
                score += 15
                reasons.append("URL shortener detected")
            
            # Check with VirusTotal if API key available
            if self.virustotal_api_key:
                vt_result = self._check_virustotal(url)
                if vt_result:
                    score += vt_result['score']
                    reasons.append(vt_result['reason'])
                    
        except Exception:
            score += 10
            reasons.append("Malformed URL")
        
        return score, reasons

    def _is_homograph_attack(self, domain):
        # Simplified homograph detection (can be enhanced)
        suspicious_chars = ['а', 'с', 'е', 'о', 'р', 'у', 'х']  # Cyrillic chars
        return any(char in domain for char in suspicious_chars)

    def _is_shortener(self, domain):
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        return any(shortener in domain for shortener in shorteners)

    def _check_virustotal(self, url):
        try:
            params = {'apikey': self.virustotal_api_key, 'url': url}
            response = requests.post(
                'https://www.virustotal.com/vtapi/v2/url/scan',
                params=params,
                timeout=5
            )
            if response.status_code == 200:
                return {'score': 40, 'reason': "Flagged by VirusTotal"}
        except:
            pass
        return None
