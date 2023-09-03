def pytest_addoption(parser):
    parser.addoption("--url", default="https://ya.ru", help="URL для проверки")
    parser.addoption("--status-code", default=200, type=int, help="Ожидаемый статус код")
