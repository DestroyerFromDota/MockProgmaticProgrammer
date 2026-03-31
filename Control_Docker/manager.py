import docker


class ContainerManager:
    """Класс для управления Docker контейнерами"""

    def __init__(self, base_url='unix:///var/run/docker.sock'):
        """Инициализация менеджера контейнеров"""
        self.client = docker.DockerClient(base_url=base_url)
        self.container = None
        self.username = None
        self.password = None

    def run_container(self, image, name, port_mapping, username, password):
        """
        Запуск контейнера с заданными параметрами

        Args:
            image: имя образа
            name: имя контейнера
            port_mapping: словарь с маппингом портов
            username: имя пользователя
            password: пароль
        """
        self.username = username
        self.password = password

        self.container = self.client.containers.run(
            image,
            detach=True,
            name=name,
            ports=port_mapping,
            environment={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return self.container

    def print_container_info(self):
        """Вывод информации о запущенном контейнере"""
        if self.container:
            print(f"Контейнер {self.container.name} запущен с ID {self.container.id[:12]}")
            print(f'Логопасс для подключения:\n login: {self.username}\n password: {self.password}')
        else:
            print("Контейнер не запущен")

    def stop_container(self):
        """Остановка контейнера"""
        if self.container:
            self.container.stop()
            print(f"Контейнер {self.container.name} остановлен")

    def remove_container(self):
        """Удаление контейнера"""
        if self.container:
            self.container.remove()
            print(f"Контейнер {self.container.name} удален")


# Использование класса
if __name__ == "__main__":
    # Создаем экземпляр менеджера
    manager = ContainerManager()

    # Запускаем контейнер
    manager.run_container(
        image='exam1',
        name='exam-student',
        port_mapping={'22/tcp': 2222},
        username='qwerty',
        password='1234'
    )

    # Выводим информацию
    manager.print_container_info()

    # При необходимости можно остановить и удалить контейнер
    # manager.stop_container()
    # manager.remove_container()