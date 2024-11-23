import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os


os.environ['USER_AGENT'] = 'myagent'
lst = ["https://education.yandex.ru/handbook/ml/article/mashinnoye-obucheniye","https://education.yandex.ru/handbook/ml/article/linear-models","https://education.yandex.ru/handbook/ml/article/metricheskiye-metody","https://education.yandex.ru/handbook/ml/article/reshayushchiye-derevya","https://education.yandex.ru/handbook/ml/article/ansambli-v-mashinnom-obuchenii","https://education.yandex.ru/handbook/ml/article/gradientnyj-busting","https://education.yandex.ru/handbook/ml/article/metriki-klassifikacii-i-regressii","https://education.yandex.ru/handbook/ml/article/kross-validaciya","https://education.yandex.ru/handbook/ml/article/podbor-giperparametrov","https://education.yandex.ru/handbook/ml/article/veroyatnostnyj-podhod-v-ml","https://education.yandex.ru/handbook/ml/article/eksponencialnyj-klass-raspredelenij-i-princip-maksimalnoj-entropii","https://education.yandex.ru/handbook/ml/article/obobshyonnye-linejnye-modeli","https://education.yandex.ru/handbook/ml/article/kak-ocenivat-veroyatnosti","https://education.yandex.ru/handbook/ml/article/generativnyj-podhod-k-klassifikacii","https://education.yandex.ru/handbook/ml/article/bajesovskij-podhod-k-ocenivaniyu","https://education.yandex.ru/handbook/ml/article/modeli-s-latentnymi-peremennymi","https://education.yandex.ru/handbook/ml/article/nejronnye-seti","https://education.yandex.ru/handbook/ml/article/pervoe-znakomstvo-s-polnosvyaznymi-nejrosetyami","https://education.yandex.ru/handbook/ml/article/metod-obratnogo-rasprostraneniya-oshibki", "https://education.yandex.ru/handbook/ml/article/tonkosti-obucheniya","https://education.yandex.ru/handbook/ml/article/svyortochnye-nejroseti", "https://education.yandex.ru/handbook/ml/article/nejroseti-dlya-raboty-s-posledovatelnostyami","https://education.yandex.ru/handbook/ml/article/transformery","https://education.yandex.ru/handbook/ml/article/grafovye-nejronnye-seti","https://education.yandex.ru/handbook/ml/article/nejroseti-dlya-oblakov-tochek", "https://education.yandex.ru/handbook/ml/article/obuchenie-predstavlenij", "https://education.yandex.ru/handbook/ml/article/distillyaciya-znanij", "https://education.yandex.ru/handbook/ml/article/vvedenie-v-generativnoe-modelirovanie", "https://education.yandex.ru/handbook/ml/article/variational-autoencoder-(vae)", "https://education.yandex.ru/handbook/ml/article/generativno-sostyazatelnye-seti-(gan)", "https://education.yandex.ru/handbook/ml/article/normalizuyushie-potoki", "https://education.yandex.ru/handbook/ml/article/diffuzionnye-modeli", "https://education.yandex.ru/handbook/ml/article/yazykovye-modeli", "https://education.yandex.ru/handbook/ml/article/intro-recsys", "https://education.yandex.ru/handbook/ml/article/rekomendacii-na-osnove-matrichnyh-razlozhenij", "https://education.yandex.ru/handbook/ml/article/kontentnye-rekomendacii", "https://education.yandex.ru/handbook/ml/article/horoshie-svojstva-rekomendatelnyh-sistem", "https://education.yandex.ru/handbook/ml/article/klasterizaciya", "https://education.yandex.ru/handbook/ml/article/vremennye-ryady", "https://education.yandex.ru/handbook/ml/article/analitika-vremennyh-ryadov", "https://education.yandex.ru/handbook/ml/article/modeli-vida-arima", "https://education.yandex.ru/handbook/ml/article/zadacha-ranzhirovaniya", "https://education.yandex.ru/handbook/ml/article/obuchenie-s-podkrepleniem", "https://education.yandex.ru/handbook/ml/article/kraudsorsing", "https://education.yandex.ru/handbook/ml/article/bias-variance-decomposition", "https://education.yandex.ru/handbook/ml/article/teoriya-glubokogo-obucheniya-vvedenie", "https://education.yandex.ru/handbook/ml/article/obobshayushaya-sposobnost-klassicheskaya-teoriya", "https://education.yandex.ru/handbook/ml/article/pac-bajesovskie-ocenki-riska", "https://education.yandex.ru/handbook/ml/article/seti-beskonechnoj-shiriny", "https://education.yandex.ru/handbook/ml/article/landshaft-funkcii-poter", "https://education.yandex.ru/handbook/ml/article/implicit-bias", "https://education.yandex.ru/handbook/ml/article/optimizaciya-v-ml", "https://education.yandex.ru/handbook/ml/article/proksimalnye-metody", "https://education.yandex.ru/handbook/ml/article/metody-vtorogo-poryadka", "https://education.yandex.ru/handbook/ml/article/shodimost-sgd", "https://education.yandex.ru/handbook/ml/article/onlajn-obuchenie-i-stohasticheskaya-optimizaciya", "https://education.yandex.ru/handbook/ml/article/regulyarizaciya-v-onlajn-obuchenii", "https://education.yandex.ru/handbook/ml/article/metody-optimizacii-v-deep-learning", "https://education.yandex.ru/handbook/ml/article/matrichnoe-differencirovanie", "https://education.yandex.ru/handbook/ml/article/matrichnaya-faktorizaciya", "https://education.yandex.ru/handbook/ml/article/veroyatnostnye-raspredeleniya", "https://education.yandex.ru/handbook/ml/article/mnogomernye-raspredeleniya", "https://education.yandex.ru/handbook/ml/article/nezavisimost-i-uslovnye-raspredeleniya-veroyatnostej", "https://education.yandex.ru/handbook/ml/article/parametricheskie-ocenki"]

loader = WebBaseLoader(
    web_paths=("https://education.yandex.ru/handbook/ml/article/entropiya-i-semejstvo-eksponencialnyh-raspredelenij",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("hljs_hljs-atelier-heath__2Efzm styles_content__xVCO4", "mord mathbb", "katex-html","katex", "yfm-latex", "katex-display")
        )
    ),
)

docs = loader.load()
print(docs[0].page_content)

with open('data/handbook_ML_page64.txt', 'w', encoding='utf-8') as file:
    # Проходим по каждому документу и записываем его содержимое в файл
    for doc in docs:
        file.write(doc.page_content + '\n')

print("Результат успешно сохранен в файл 'output.txt'")