import re
import pymorphy2

# Создаём морфологический анализатор
morph = pymorphy2.MorphAnalyzer()


# def search_strings(strings, keyword):
def search_strings(query: list, fields: list, base):
    # Анализируем ключевое слово
    base2 = []
    for el in base:
        base2.append([el.id, [el.title.lower(), el.additional_info.lower(), el.category.lower()], el])
    query_norm = []
    for keyword in query:
        query_norm.append(keyword.lower())
        for el in morph.parse(keyword):
            query_norm.append(el.normal_form)
            try:
                query_norm.append(el.inflect({'gent'}).word.lower())  # Родительный
                query_norm.append(el.inflect({'plur', 'gent'}).word.lower())
                query_norm.append(el.inflect({'datv'}).word.lower())  # Дательный
                query_norm.append(el.inflect({'plur', 'datv'}).word.lower())
                query_norm.append(el.inflect({'accs'}).word.lower())  # Винительный
                query_norm.append(el.inflect({'plur', 'accs'}).word.lower())
                query_norm.append(el.inflect({'ablt'}).word.lower())  # Творительный
                query_norm.append(el.inflect({'plur', 'ablt'}).word.lower())
                query_norm.append(el.inflect({'loct'}).word.lower())  # Предложный
                query_norm.append(el.inflect({'plur', 'loct'}).word.lower())
            except AttributeError:
                break
    query_norm = set(query_norm)

    matching_strings = []
    for keyword in query_norm:
        for strings in base2:
            # Ищем строки, соответствующие ключевому слову
            for string in strings[1]:
                # Анализируем строку
                words = string.split()
                words = set(words)
                for word in words:
                    # Удаляем знаки препинания
                    word = re.sub(r'[^\w\s]', '', word)
                    # Сравниваем слово с ключевым словом
                    if keyword == word:
                        matching_strings.append(strings[2])
                        break

    return set(matching_strings)

