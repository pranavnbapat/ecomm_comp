import deepl

auth_key = "d35a289e-47d2-a38e-09a7-f0de53284a56:fx"  # Replace with your key
translator = deepl.Translator(auth_key)
#
result = translator.translate_text("Kaas", target_lang="EN-GB")
print(result.text)  # "Bonjour, le monde !"


def translate_text(t):
    result = translator.translate_text(t, target_lang="EN-GB")
    return result.text


def translate_list(text_list):
    return [translate_text(t) for t in text_list]


text_list = ['Kaas']
translated_list = translate_list(text_list)
print(translated_list)
