import docker

client = docker.DockerClient(base_url='unix:///var/run/docker.sock')

# Запустить контейнер с параметрами как в docker run
container = client.containers.run(
    'nginx-exam',                    # образ
    detach=True,                     # -d
    name='exam-student',             # --name
    ports={
        '22/tcp': 2222               # -p 2222:22
    }
)

print(f"Контейнер {container.name} запущен с ID {container.id[:12]}")