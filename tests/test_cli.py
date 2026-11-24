
from unittest.mock import patch

from cli import main, display_inventory, show_low_stock


def test_display_inventory(capsys):
    display_inventory()

    output = capsys.readouterr().out

    assert "Mangoes" in output
    assert "Bananas" in output
    assert "Apples" in output


def test_show_low_stock(capsys):
    show_low_stock()

    output = capsys.readouterr().out

    assert "Avocados" in output
    assert "Oranges" in output


def test_main_exit(capsys):
    with patch("builtins.input", side_effect=["9"]):
        main()

    output = capsys.readouterr().out

    assert "Thank you for using Fresh Basket!" in output


def test_main_invalid_choice(capsys):
    with patch("builtins.input", side_effect=["invalid", "9"]):
        main()

    output = capsys.readouterr().out

    assert "Invalid choice" in output


def test_main_accepts_spaces(capsys):
    with patch("builtins.input", side_effect=[" 6 ", "9"]):
        main()

    output = capsys.readouterr().out

    assert "LOW STOCK FRUITS" in output
