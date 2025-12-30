import pytest
from user_system import UserManager

# Фікстура створює чистий об'єкт перед кожним тестом
@pytest.fixture
def manager():
    return UserManager()

# --- Тести додавання (add_user) ---
def test_add_normal(manager):
    res = manager.add_user("Alex", 25)
    assert res == "Додано"
    assert "Alex" in manager.data

def test_add_duplicate(manager):
    manager.add_user("Ivan", 30)
    # Перевіряємо, чи випадає помилка при повторі
    with pytest.raises(ValueError):
        manager.add_user("Ivan", 40)

def test_add_negative_age(manager):
    # Перевіряємо помилку при від'ємному віці
    with pytest.raises(ValueError):
        manager.add_user("Baby", -1)

# --- Тести перевірки статусу (check_status) ---
def test_status_adult(manager):
    manager.add_user("Oleg", 20)
    assert manager.check_status("Oleg") == "Дорослий"

def test_status_child(manager):
    manager.add_user("Max", 10)
    assert manager.check_status("Max") == "Дитина"

def test_status_not_found(manager):
    assert manager.check_status("Ghost") is None

# --- Тести видалення (delete_user) ---
def test_delete_success(manager):
    manager.add_user("Anna", 22)
    result = manager.delete_user("Anna")
    assert result is True
    assert "Anna" not in manager.data

def test_delete_fail(manager):
    result = manager.delete_user("NoName")
    assert result is False