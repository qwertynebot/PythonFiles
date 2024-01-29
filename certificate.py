import subprocess
import requests
import time
import shutil
import docker

vm_ip = "192.168.1.103"

def generate_self_signed_certificate():
    try:
        subprocess.run(["openssl", "req", "-new", "-newkey", "rsa:2048", "-days", "365", "-nodes", "-x509", "-keyout", "jenkins.key", "-out", "jenkins.crt", "-subj", "/CN=jenkins"])

        shutil.move("jenkins.crt", "/var/jenkins_home/jenkins.crt")
        shutil.move("jenkins.key", "/var/jenkins_home/jenkins.key")
        print("Сертифікат згенеровано.")
    except Exception as e:
        print(f"Помилка підписання сертифікату для Jenkins: {e}")

def start_jenkins_container():
    client = docker.from_env()
    container = client.containers.run("jenkins/jenkins", detach=True, ports={'8080/tcp': 8080, '50000/tcp': 50000}, volumes={'/var/jenkins_home'})
    return container

def wait_for_jenkins_to_start():
    url = f"http://{vm_ip}:8080"
    max_attempts = 30
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("Jenkins стартував.")
            return
        except Exception:
            time.sleep(10)
            attempts += 1
    print("Jenkins не запустився за цей час.")

def start_nginx_container():
    client = docker.from_env()
    nginx_container = client.containers.run("nginx", detach=True, ports={'80/tcp': 80, '443/tcp': 443}, volumes={'/path/to/your/nginx/conf:/etc/nginx/conf.d'})
    return nginx_container

if __name__ == "__main__":
    # 1
    jenkins_container = start_jenkins_container()
    # 2
    wait_for_jenkins_to_start()
    # 3
    generate_self_signed_certificate()
    # 4
    nginx_container = start_nginx_container()
