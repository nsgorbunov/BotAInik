import os
import re
import bs4
from langchain_community.document_loaders import WebBaseLoader

os.environ["USER_AGENT"] = "myagent"
ml_handbook = [
    "https://education.yandex.ru/handbook/ml/article/mashinnoye-obucheniye",
    "https://education.yandex.ru/handbook/ml/article/linear-models",
    "https://education.yandex.ru/handbook/ml/article/metricheskiye-metody",
    "https://education.yandex.ru/handbook/ml/article/reshayushchiye-derevya",
    "https://education.yandex.ru/handbook/ml/article/ansambli-v-mashinnom-obuchenii",
    "https://education.yandex.ru/handbook/ml/article/gradientnyj-busting",
    "https://education.yandex.ru/handbook/ml/article/metriki-klassifikacii-i-regressii",
    "https://education.yandex.ru/handbook/ml/article/kross-validaciya",
    "https://education.yandex.ru/handbook/ml/article/podbor-giperparametrov",
    "https://education.yandex.ru/handbook/ml/article/veroyatnostnyj-podhod-v-ml",
    "https://education.yandex.ru/handbook/ml/article/eksponencialnyj-klass-raspredelenij-i-princip-maksimalnoj-entropii",
    "https://education.yandex.ru/handbook/ml/article/obobshyonnye-linejnye-modeli",
    "https://education.yandex.ru/handbook/ml/article/kak-ocenivat-veroyatnosti",
    "https://education.yandex.ru/handbook/ml/article/generativnyj-podhod-k-klassifikacii",
    "https://education.yandex.ru/handbook/ml/article/bajesovskij-podhod-k-ocenivaniyu",
    "https://education.yandex.ru/handbook/ml/article/modeli-s-latentnymi-peremennymi",
    "https://education.yandex.ru/handbook/ml/article/nejronnye-seti",
    "https://education.yandex.ru/handbook/ml/article/pervoe-znakomstvo-s-polnosvyaznymi-nejrosetyami",
    "https://education.yandex.ru/handbook/ml/article/metod-obratnogo-rasprostraneniya-oshibki",
    "https://education.yandex.ru/handbook/ml/article/tonkosti-obucheniya",
    "https://education.yandex.ru/handbook/ml/article/svyortochnye-nejroseti",
    "https://education.yandex.ru/handbook/ml/article/nejroseti-dlya-raboty-s-posledovatelnostyami",
    "https://education.yandex.ru/handbook/ml/article/transformery",
    "https://education.yandex.ru/handbook/ml/article/grafovye-nejronnye-seti",
    "https://education.yandex.ru/handbook/ml/article/nejroseti-dlya-oblakov-tochek",
    "https://education.yandex.ru/handbook/ml/article/obuchenie-predstavlenij",
    "https://education.yandex.ru/handbook/ml/article/distillyaciya-znanij",
    "https://education.yandex.ru/handbook/ml/article/vvedenie-v-generativnoe-modelirovanie",
    "https://education.yandex.ru/handbook/ml/article/variational-autoencoder-(vae)",
    "https://education.yandex.ru/handbook/ml/article/generativno-sostyazatelnye-seti-(gan)",
    "https://education.yandex.ru/handbook/ml/article/normalizuyushie-potoki",
    "https://education.yandex.ru/handbook/ml/article/diffuzionnye-modeli",
    "https://education.yandex.ru/handbook/ml/article/yazykovye-modeli",
    "https://education.yandex.ru/handbook/ml/article/intro-recsys",
    "https://education.yandex.ru/handbook/ml/article/rekomendacii-na-osnove-matrichnyh-razlozhenij",
    "https://education.yandex.ru/handbook/ml/article/kontentnye-rekomendacii",
    "https://education.yandex.ru/handbook/ml/article/horoshie-svojstva-rekomendatelnyh-sistem",
    "https://education.yandex.ru/handbook/ml/article/klasterizaciya",
    "https://education.yandex.ru/handbook/ml/article/vremennye-ryady",
    "https://education.yandex.ru/handbook/ml/article/analitika-vremennyh-ryadov",
    "https://education.yandex.ru/handbook/ml/article/modeli-vida-arima",
    "https://education.yandex.ru/handbook/ml/article/zadacha-ranzhirovaniya",
    "https://education.yandex.ru/handbook/ml/article/obuchenie-s-podkrepleniem",
    "https://education.yandex.ru/handbook/ml/article/kraudsorsing",
    "https://education.yandex.ru/handbook/ml/article/bias-variance-decomposition",
    "https://education.yandex.ru/handbook/ml/article/teoriya-glubokogo-obucheniya-vvedenie",
    "https://education.yandex.ru/handbook/ml/article/obobshayushaya-sposobnost-klassicheskaya-teoriya",
    "https://education.yandex.ru/handbook/ml/article/pac-bajesovskie-ocenki-riska",
    "https://education.yandex.ru/handbook/ml/article/seti-beskonechnoj-shiriny",
    "https://education.yandex.ru/handbook/ml/article/landshaft-funkcii-poter",
    "https://education.yandex.ru/handbook/ml/article/implicit-bias",
    "https://education.yandex.ru/handbook/ml/article/optimizaciya-v-ml",
    "https://education.yandex.ru/handbook/ml/article/proksimalnye-metody",
    "https://education.yandex.ru/handbook/ml/article/metody-vtorogo-poryadka",
    "https://education.yandex.ru/handbook/ml/article/shodimost-sgd",
    "https://education.yandex.ru/handbook/ml/article/onlajn-obuchenie-i-stohasticheskaya-optimizaciya",
    "https://education.yandex.ru/handbook/ml/article/regulyarizaciya-v-onlajn-obuchenii",
    "https://education.yandex.ru/handbook/ml/article/metody-optimizacii-v-deep-learning",
    "https://education.yandex.ru/handbook/ml/article/matrichnoe-differencirovanie",
    "https://education.yandex.ru/handbook/ml/article/matrichnaya-faktorizaciya",
    "https://education.yandex.ru/handbook/ml/article/veroyatnostnye-raspredeleniya",
    "https://education.yandex.ru/handbook/ml/article/mnogomernye-raspredeleniya",
    "https://education.yandex.ru/handbook/ml/article/nezavisimost-i-uslovnye-raspredeleniya-veroyatnostej",
    "https://education.yandex.ru/handbook/ml/article/parametricheskie-ocenki",
]
python_handbook = [
    "https://education.yandex.ru/handbook/python/article/spisochnye-vyrazheniya-model-pamyati-dlya-tipov-yazyka-python",
    "https://education.yandex.ru/handbook/python/article/vstroennye-vozmozhnosti-po-rabote-s-kollekciyami",
    "https://education.yandex.ru/handbook/python/article/potokovyj-vvodvyvod-rabota-s-tekstovymi-fajlami-json",
    "https://education.yandex.ru/handbook/python/article/pozicionnye-i-imenovannye-argumenty-funkcii-vysshih-poryadkov-lyambda-funkcii",
    "https://education.yandex.ru/handbook/python/article/rekursiya-dekoratory-generatory",
    "https://education.yandex.ru/handbook/python/article/obuektnaya-model-python-klassy-polya-i-metody",
    "https://education.yandex.ru/handbook/python/article/volshebnye-metody-pereopredelenie-metodov-nasledovanie",
    "https://education.yandex.ru/handbook/python/article/model-isklyuchenij-python-try-except-else-finally-moduli",
    "https://education.yandex.ru/handbook/python/article/modul-requests",
]
algorithms = [
    "https://education.yandex.ru/handbook/algorithms/article/polnyj-perebor-i-optimizaciya-perebora",
    "https://education.yandex.ru/handbook/algorithms/article/zhadnye-algoritmy",
    "https://education.yandex.ru/handbook/algorithms/article/dinamicheskoe-programmirovanie",
    "https://education.yandex.ru/handbook/algorithms/article/rekursivnye-algoritmy",
    "https://education.yandex.ru/handbook/algorithms/article/razdelyaj-i-vlastvuj",
    "https://education.yandex.ru/handbook/algorithms/article/randomizirovannye-algoritmy",
    "https://education.yandex.ru/handbook/algorithms/article/zadachi-o-chislah-fibonachchi",
    "https://education.yandex.ru/handbook/algorithms/article/stek",
    "https://education.yandex.ru/handbook/algorithms/article/ochered-s-prioritetom",
    "https://education.yandex.ru/handbook/algorithms/article/dek-(veque-double-ended-queue)",
    "https://education.yandex.ru/handbook/algorithms/article/priroda-grafa",
    "https://education.yandex.ru/handbook/algorithms/article/predstavlenie-grafa-v-pamyati-kompyutera",
    "https://education.yandex.ru/handbook/algorithms/article/obhody-grafa",
]


class Html_parser:
    @staticmethod
    def remove_headers(text):
        header_patterns = [
            r"^[А-ЯЁ\s]+:$",              
            r"^[А-ЯЁ][^\n]{0,50}\n",      
            r"^Вопрос на подумать.*?$",   
            r"^Ответ.*?$"                 
        ]
        
        for pattern in header_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)
        lines = text.splitlines()
        filtered_lines = []
        for line in lines:
            if len(line.strip()) < 10 or re.match(r"^\s*\d+\s*$", line) or len(line.split()) <= 2:
                continue
            filtered_lines.append(line)
        
        clean_text = '\n'.join(filtered_lines)
        clean_text = re.sub(r'\n{2,}', '\n', clean_text)
        
        return clean_text

    def web_page(self, urls: list):
        loader = WebBaseLoader(
            # web_paths=("https://education.yandex.ru/handbook/algorithms/article/obhody-grafa",),
            web_paths=(urls),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    # class_=("hljs_hljs-atelier-heath__2Efzm styles_content__xVCO4", "hljs cpp", "yfm-latex", "hljs python") # Algorithms Handbook
                    # class_=("hljs_hljs-atelier-heath__2Efzm styles_content__xVCO4", "hljs Python") # Python Handbook
                    class_=(
                        "hljs_hljs-atelier-heath__2Efzm styles_content__xVCO4",
                        "mord mathbb",
                        "katex-html",
                        "katex",
                        "yfm-latex",
                        "katex-display",
                    )  # ML Handbook
                )
            ),
        )

        docs = loader.load()
        for doc in docs:
            doc.page_content = self.remove_headers(
                doc.page_content
                )
        return docs

        # with open('algorithms/page12.txt', 'w', encoding='utf-8') as file:
        #     # Проходим по каждому документу и записываем его содержимое в файл
        #     for doc in docs:
        #         file.write(doc.page_content + '\n')

        # print("Результат успешно сохранен в файл 'output.txt'")
