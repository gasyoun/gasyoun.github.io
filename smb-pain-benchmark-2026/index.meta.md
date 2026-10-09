_Created: 09-10-2026 · Last updated: 09-10-2026_

# Metadoc — smb-pain-benchmark-2026/index.html

- **Что:** дашборд «похожа ли школа (ОРС/Systema) на типовой профиль малого бизнеса»: сезонная матрица выручки 2024–2026 (календарные сезоны, декабрь из прошлого года — рулинг Q3 грилла MG), помесячный ряд, сверка контуров денег 2026 (CRM/Tochka/PayPal, ±10%), вердикты по 10 болям SMB + 5 «наших» болей вне топ-10.
- **Родитель:** H6296 (Uprava), рулинги — [DECISIONS_SMB_PAIN_BENCHMARK_GRILL_09-10-2026](https://github.com/gasyoun/Uprava/blob/main/docs/DECISIONS_SMB_PAIN_BENCHMARK_GRILL_09-10-2026.md) (7 рулингов, 09-10-2026).
- **Данные:** [data.json](https://github.com/gasyoun/gasyoun.github.io/blob/master/smb-pain-benchmark-2026/data.json) — единственный источник чисел страницы (страница несёт ту же копию inline); каждое число трассируемо grep'ом по нему.
- **Пересборка:** скрипты снятия/сборки заархивированы `~/Documents/backups/h6296-smb-benchmark-2026-10-09/` (pull ретро Metrika/GSC + билдер + верификатор 49 проверок). Живые источники: БД Systema (ssh root@100.85.73.83, mysql laravel, read-only: paid-строки без псевдо-тарифов «Расход»/«salary_payout»), Tochka-агрегаты (Uprava data/tochka_monthly_aggregates.tsv, срез 03-09), PayPal-реконсил (Uprava docs, §2 помесячный), Metrika 18296974 (samskrtam.ru) + 106964341 (samskrte.ru, с фев-2026), GSC samskrtam.ru.
- **Свежесть:** срез 09-10-2026; осень-2026 «в ходу» (сентябрь полный + 9 дней октября); обновление = перезапуск снятия + билдера.
- **PII:** только агрегаты; publish-safety свип пройден (0 имён/emails/построчных сумм).
- **Regenerate-контракт:** не редактировать index.html руками — править билдер и пересобирать (прецедент: генераторы `scripts/` этого репо).

_к.ф.н. М.Ю. Гасунс_
