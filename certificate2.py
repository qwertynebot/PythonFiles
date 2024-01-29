import docker
import subprocess

def run_apache_container():
    try:
        client = docker.from_env()
        container = client.containers.run(
            'httpd:2.4',  
            name='my-apache-container',
            ports={'80': 80, '443': 443},  
            detach=True,
        )
        print(f"Apache container ID: {container.id}")
    except docker.errors.APIError as e:
        print(f"Error running Apache container: {e}")

def issue_ssl_certificate(domain):
    try:
        certbot_command = [
            "certbot",
            "certonly",
            "--non-interactive",
            "--standalone",
            "--agree-tos",
            "--email your_email@example.com", 
            "-d", domain,
        ]
        
        subprocess.run(certbot_command, check=True)
        
        print(f"SSL certificate issued for {domain}")
    except subprocess.CalledProcessError as e:
        print(f"Error issuing SSL certificate: {e}")

def main():
    run_apache_container()
    
    domain_to_certificate = "example.com"
    issue_ssl_certificate(domain_to_certificate)

if __name__ == "__main__":
    main()
