import logging
import os


def test_system_echo(capfd):
    os.system("echo hello")
    captured = capfd.readouterr()
    assert captured.out == "hello\n"


def test_system_echo_binary(capfdbinary):
    os.system("echo hello")
    captured = capfdbinary.readouterr()
    assert captured.out == b"hello\n"


def test_logging_info_caplog(caplog):
    logging.info("hello")
    # logging.info(caplog.text)
    assert caplog.text == "INFO     root:test_capture_stdout_stderr_output.py:18 hello\n"


def test_print_capsys(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_print_capsysbinary(capsysbinary):
    print("hello")
    captured = capsysbinary.readouterr()
    assert captured.out == b"hello\n"
