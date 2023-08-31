# -*- coding: utf-8 -*-

"""
    Установка строки кодировки в заголовке файла
"""

import os
import colorama


class EncodingInspector:
    """
    Класс с методами для поиска файлов без заголовка кодировки
    и установки заголовка в них
    """

    def __init__(self, directory_path: str = "."):
        self.directory_path: str = directory_path
        self.__incorrect_files: list[str] = []
        self.__set_header_for_incorrect_files()

        colorama.init()

        self.find_incorrect_headers(directory_path)
        self.show_directory(self.directory_path)
        self.show_incorrect_files()
        self.__set_header_for_incorrect_files()

    @classmethod
    def __is_correct_header(cls, file_path: str) -> bool:
        header1: str = "# coding: utf8"
        header2: str = "# -*- coding: utf-8 -*-"
        is_correct: bool = False

        with open(f"{file_path}", "r") as file:
            file_header: str = file.readline().strip()
            if file_header == header1 or file_header == header2:
                is_correct = True

        return is_correct

    @classmethod
    def __is_py_file(cls, file_name: str) -> bool:
        """
            Проверка расширения файла
        :param file_name:
        :return:
        """
        return file_name[-3:] == ".py"

    def __show_file_in_directory(self, directory: str, file_name: str, level: int) -> None:
        """
            Вывод информации о конкретном файле
        :param directory:
        :param file_name:
        :param level:
        :return:
        """
        indents: str = '\t' * level + "│" + "-"

        if self.__is_py_file(file_name):
            if f"{directory}/{file_name}" in self.__incorrect_files:
                print(f"{indents}>{colorama.Fore.RED}{file_name}{colorama.Fore.RESET}")
            else:
                print(f"{indents}>{colorama.Fore.GREEN}{file_name}{colorama.Fore.RESET}")
        elif os.path.isdir(f"{directory}/{file_name}/"):
            print(f"{indents}>{colorama.Fore.LIGHTWHITE_EX}{file_name}{colorama.Fore.RESET}")
        else:
            print(f"{indents}>{colorama.Fore.WHITE}{file_name}{colorama.Fore.RESET}")

    def show_directory(self, directory: str = ".", level: int = 0) -> None:
        """
            Вывод всех файлов и подкатологов в консоль
        :param directory:
        :param level:
        :return:
        """
        for file_name in os.listdir(directory):
            self.__show_file_in_directory(directory, file_name, level)

            if os.path.isdir(f"{directory}/{file_name}/"):
                self.show_directory(f"{directory}/{file_name}", level + 1)

    def find_incorrect_headers(self, directory_find: str) -> None:
        """
            Поиск файлов без заголовка кодировки и добавление их в список
        :param directory_find:
        :return:
        """
        for file_name in os.listdir(directory_find):
            if self.__is_py_file(file_name):
                if not self.__is_correct_header(f"{directory_find}/{file_name}"):
                    self.__incorrect_files.append(f"{directory_find}/{file_name}")

            if os.path.isdir(f"{directory_find}/{file_name}"):
                self.find_incorrect_headers(f"{directory_find}/{file_name}")

    def show_incorrect_files(self) -> None:
        """
            Вывод списка файлов без заголовка кодировки
        :return:
        """
        if len(self.__incorrect_files) != 0:
            print(f"\nFound {len(self.__incorrect_files)} files without encoding header:")
            for file in self.__incorrect_files:
                print(file)
            print()
        else:
            print("\nAll file's headers in directory correct\n")

    def __set_header_for_incorrect_files(self) -> None:
        """
            Обработка списка .py файлов без заголовков кодировки
        :return:
        """

        header = "# -*- coding: utf-8 -*-"

        for file_name in self.__incorrect_files:
            with open(file_name, 'r+') as file:
                content = file.read()
                file.seek(0, 0)
                file.write(header.rstrip('\r\n') + '\n' + content)


if __name__ == '__main__':
    EncodingInspector()
