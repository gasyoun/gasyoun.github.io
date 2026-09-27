---
name: karta-domain-index
description: How the annotated domain map karta/ on gasyoun.github.io is built (H5527) — generator, data file, coverage guard, probe mode
metadata:
  type: reference
  last-updated: 2026-09-27
---

# Karta — аннотированная карта домена (H5527)

`karta/index.html` строится генератором, никогда не правится руками:

1. **Данные:** `scripts/karta/karta_data.py` — 54 пункта `K###` (ID глобальные,
   стабильные, никогда не переиспользуются), поля: `key` (путь на диске, для
   каталога с `/`), опц. `href` (оверрайд ссылки, когда у каталога нет
   index.html), `status` (green/amber/tomb), `note` (RU, 1–2 предложения),
   `sec` (рубрика A–G; G = острова project-pages других репо, у них `url`).
2. **Генератор:** `scripts/karta/gen_karta_index.py` — `--emit` (собрать),
   `--check` (byte-parity с диском/данными), `--probe-islands` (HTTP-аудит всех
   ссылок). Каверидж-гард: любой контентный ключ верхнего уровня без пункта в
   данных валит emit/check — карта не устаревает молча (уже поймал `diagrams/`).
3. **Решения MG 27-09-2026:** охват — весь домен (не только этот репо); корень
   не трогать (index.html = Ригведа 12.4 МБ); karta живёт на `/karta/`.
4. **Известные хвосты (GTD):** `reverse20-ouput/` — опечатка в имени каталога;
   `index2.html` — бойлерплейт GitHub, кандидат на удаление.

_Гасунс_
