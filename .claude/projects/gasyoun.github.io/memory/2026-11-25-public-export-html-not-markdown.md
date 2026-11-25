---
name: public-export-html-not-markdown
description: MG ruling 25-11-2026 — anything meant for export/readers is a self-contained HTML page on gasyoun.github.io, not a Markdown file
metadata:
  type: ruling
  last-updated: 2026-11-25
---

# MG ruling 25-11-2026: «на экспорт — HTML на публичной странице, не MD»

MG, 25-11-2026, verbatim: «когда что-то на экспорт, то МД файлы это не хорошо. Нужен html на публичной странице».

Применяется ко всем читательским/внешним материалам: инструкции, гайды, описания продуктов, страницы для рассылок. Поставляемый вид — самодостаточный HTML в отдельной папке на `gasyoun.github.io` (Pages собирается с `master`, см. `AGENTS.md` репозитория), а не `.md` в репозитории и не вложение.

Почему: MD-файл не является artefact'ом для читателя — у него нет публичного адреса, он не рендерится как страница и обычно лежит внутри репозитория со служебным контекстом.

Обратная сторона того же решения — [2026-11-25-internal-external-content-separation.md](2026-11-25-internal-external-content-separation.md): внешняя страница не должна содержать внутренних сведений.

_Гасунс_
