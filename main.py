import requests
import time
import csv

API_KEY = 'de1ba68a024f735318919a0a05968c613469a51d8095ae9d4dac1373fe120082fa097cf89906527d'

def check_ip(ip_address):
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '365'
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()['data']
        abuse_score = data['abuseConfidenceScore']

        print(f"\n🔍 IP: {data['ipAddress']}")
        print(f"Abuse Confidence Score: {abuse_score}")
        print(f"Country: {data['countryCode']}")
        print(f"ISP: {data['isp']}")
        print(f"Domain: {data.get('domain')}")
        print(f"Usage Type: {data.get('usageType')}")
        print(f"Total Reports: {data['totalReports']}")
        print(f"Last Reported: {data.get('lastReportedAt')}")

        if abuse_score >= 50:
            return {
                'IP': data['ipAddress'],
                'Score': abuse_score,
                'Country': data['countryCode'],
                'Domain': data.get('domain'),
                'Last Reported': data.get('lastReportedAt')
            }
    else:
        print(f"❌ Error checking {ip_address}: {response.status_code} - {response.text}")
    
    return None

if __name__ == "__main__":
    print("=== Threat Feed Analyzer: Batch IP Check ===")
    with open('ips.txt', 'r') as file:
        ips = [line.strip() for line in file if line.strip()]

    flagged_ips = []

    for ip in ips:
        result = check_ip(ip)
        if result:
            flagged_ips.append(result)
        time.sleep(1.5)  # Respect API rate limits

    # Write flagged IPs to CSV
    if flagged_ips:
        with open('flagged_ips.csv', 'w', newline='') as csvfile:
            fieldnames = ['IP', 'Score', 'Country', 'Domain', 'Last Reported']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flagged_ips)
        print(f"\n✅ Exported {len(flagged_ips)} flagged IP(s) to flagged_ips.csv")
    else:
        print("\n✅ No flagged IPs found.")
