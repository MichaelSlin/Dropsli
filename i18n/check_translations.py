# check_translations.py

from i18n import translations

def check_translations():
    languages = list(translations.keys())
    if not languages:
        print("❌   Нет доступных языков для проверки.")
        return

    reference_lang = 'en'
    reference_keys = set(translations.get(reference_lang, {}).keys())

    all_ok = True
    total_keys = len(reference_keys)

    for lang, lang_translations in translations.items():
        if lang == reference_lang:
            continue

        lang_keys = set(lang_translations.keys())

        missing_keys = reference_keys - lang_keys
        extra_keys = lang_keys - reference_keys

        if missing_keys:
            print(f"\n[{lang}] ❗   Отсутствуют ключи перевода:")
            for key in sorted(missing_keys):
                print(f"  - {key}")
            all_ok = False

        if extra_keys:
            print(f"\n[{lang}] ⚠️   Найдены ключи, которых нет в '{reference_lang}':")
            for key in sorted(extra_keys):
                print(f"  - {key}  (возможно, этот ключ должен быть добавлен в {reference_lang})")
            all_ok = False

    if all_ok:
        print(f"\n✅    Все переводы найдены! Проверено {total_keys} ключа/ключей.")
    else:
        print("\n⚠️     Проверка завершена с предупреждениями или ошибками.")

if __name__ == "__main__":
    check_translations()
