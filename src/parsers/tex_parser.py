import re
from typing import List

from icecream import ic
from langchain.schema import Document
from TexSoup import TexSoup


class TexParser:
    """
    Класс для конвертации .tex файлов в Langchain Document объекты.
    """

    def __init__(self):
        """
        Инициализация конвертера.
        При необходимости здесь можно добавить параметры конфигурации.
        """
        pass

    def convert_single_file(self, file_path: str) -> Document:
        """
        Конвертирует один .tex файл в LangchainDocument.

        Args:
            file_path (str): Путь к .tex файлу

        Returns:
            Document: Langchain Document объект
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tex_content = file.read()

            soup = TexSoup(tex_content)

            metadata = {}

            try:
                title = soup.find("title")
                if title:
                    metadata["title"] = str(title.string)
            except:
                pass

            try:
                author = soup.find("author")
                if author:
                    metadata["author"] = str(author.string)
            except:
                pass

            try:
                date = soup.find("date")
                if date:
                    metadata["date"] = str(date.string)
            except:
                pass

            text_content = str(soup)

            text_content = self._clean_tex_content(text_content)

            metadata["source"] = file_path

            document = Document(page_content=text_content, metadata=metadata)

            return document

        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")
            return None

    def convert_multiple_files(self, file_paths: List[str]) -> List[Document]:
        """
        Обрабатывает несколько .tex файлов и возвращает список Document объектов.

        Args:
            file_paths (List[str]): Список путей к .tex файлам

        Returns:
            List[Document]: Список Langchain Document объектов
        """
        documents = []
        for file_path in file_paths:
            doc = self.convert_single_file(file_path)
            if doc:
                documents.append(doc)
        return documents

    def _clean_tex_content(self, text_content: str) -> str:
        """
        Очищает текст от LaTeX команд и форматирования.

        Args:
            text_content (str): Исходный текст с LaTeX разметкой

        Returns:
            str: Очищенный текст
        """
        # Удаляем команды вида \command{...}
        text_content = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", "", text_content)
        # Удаляем одиночные команды вида \command
        text_content = re.sub(r"\\[a-zA-Z]+", "", text_content)
        # Удаляем окружения begin/end
        text_content = re.sub(
            r"\\begin\{[^}]*\}.*?\\end\{[^}]*\}", "", text_content, flags=re.DOTALL
        )
        # Удаляем комментарии
        text_content = re.sub(r"%.*$", "", text_content, flags=re.MULTILINE)
        # Удаляем лишние пробелы и переносы строк
        text_content = re.sub(r"\s+", " ", text_content).strip()

        return text_content


ic(TexParser().convert_single_file("lecture01-intro.tex"))
