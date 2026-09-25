# Awesome KI-Tools auf Deutsch [![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)

> Kuratierte Liste der besten KI-Tools, auf Deutsch erklärt, geprüft und nach Einsatzzweck sortiert. Mit Praxis-Deep-Dives von **[PROMPTGOTT](https://promptgott.substack.com/?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de)**, dem deutschsprachigen Substack für abgefahrene AI-Use-Cases, Prompt Engineering und AI-SEO.

🇬🇧 [English version](README.md) · 📬 [PROMPTGOTT abonnieren](https://promptgott.substack.com/subscribe?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) · ➕ [Tool vorschlagen](#mitmachen)

Diese Liste basiert auf [Awesome AI Tools](https://github.com/mahseema/awesome-ai-tools) (MIT-Lizenz) und ist für den deutschsprachigen Raum überarbeitet:

- **Übersetzt und gekürzt:** Jede Beschreibung sagt in einem Satz, wofür das Tool gut ist.
- **Link-Check (Stand: 25.09.2026):** Nicht mehr erreichbare Tools (404, 5xx, Domain tot) sind entfernt, Affiliate- und Referral-Parameter entfernt.
- **Aktualisiert:** Umbenannte Produkte korrigiert (z. B. Bing Chat → Microsoft Copilot, Metaphor → Exa), aktuelle Standard-Tools ergänzt.
- **DACH-Fokus:** Eigene Abschnitte für Übersetzung/Lokalisierung, SEO und Automatisierung. Anbieter mit Sitz in der EU sind mit 🇪🇺 markiert. Das ist ein Hinweis, keine Datenschutz-Prüfung: Für DSGVO-Konformität zählen AVV, Serverstandort und Einstellungen im Einzelfall.
- **PROMPTGOTT-Praxis:** Wo ein Deep Dive zeigt, *wie* man eine Tool-Kategorie in echte Ergebnisse übersetzt, steht ein 💡-Hinweis.

**Legende:** `OSS` = Open Source · 🇪🇺 = Anbieter mit Sitz in der EU · 💡 = PROMPTGOTT-Deep-Dive zum Thema

## Inhalt

- [🌟 Empfehlungen der Redaktion](#empfehlungen-der-redaktion)
- [🔥 PROMPTGOTT Deep Dives](#promptgott-deep-dives)
- [📝 Text und Sprache](#text-und-sprache)
  - [Sprachmodelle und APIs](#sprachmodelle-und-apis)
  - [Chatbots und Assistenten](#chatbots-und-assistenten)
  - [KI-Suchmaschinen](#ki-suchmaschinen)
  - [Lokal und privat mit Dokumenten chatten](#lokal-und-privat-mit-dokumenten-chatten)
  - [Schreibassistenten](#schreibassistenten)
  - [Übersetzung und Lokalisierung](#übersetzung-und-lokalisierung)
  - [Browser-Erweiterungen und Add-ons](#browser-erweiterungen-und-add-ons)
  - [Produktivität](#produktivität)
  - [Meeting-Assistenten](#meeting-assistenten)
  - [Wissenschaft und Recherche](#wissenschaft-und-recherche)
  - [Kundenservice](#kundenservice)
- [🤖 Automatisierung und KI-Agenten](#automatisierung-und-ki-agenten)
- [🛠️ Entwickler-Tools und LLMOps](#entwickler-tools-und-llmops)
- [💻 Programmieren mit KI](#programmieren-mit-ki)
- [🖼️ Bilder](#bilder)
- [📽️ Video](#video)
- [🎶 Audio](#audio)
- [🎯 Marketing und SEO](#marketing-und-seo)
- [📞 KI-Telefonagenten](#ki-telefonagenten)
- [🎒 Weitere KI-Tools](#weitere-ki-tools)
- [🎓 Lernen: Prompting und KI-Grundlagen](#lernen-prompting-und-ki-grundlagen)
- [🔗 Verwandte Listen](#verwandte-listen)
- [➕ Mitmachen](#mitmachen)


## Empfehlungen der Redaktion

Der schnelle Einstieg: ein Tool pro typischer Aufgabe, bewusst mit EU-Alternativen.

- [ChatGPT](https://chatgpt.com) - Der Allrounder für Text, Analyse, Bilder und Recherche.
- [Claude](https://claude.ai/) - Stark bei langen Dokumenten, sauberem Schreiben und Code.
- [Le Chat von Mistral](https://chat.mistral.ai) - 🇪🇺 Französischer KI-Assistent, die naheliegende EU-Alternative zu ChatGPT.
- [DeepL](https://www.deepl.com/translator) - 🇪🇺 Übersetzer aus Köln, bei Deutsch meist natürlicher als generische Chatbots.
- [Perplexity](https://www.perplexity.ai/) - Antwortmaschine mit Quellenangaben für schnelle Recherche.
- [NotebookLM](https://notebooklm.google.com/) - Chattet nur mit deinen eigenen Quellen und erzeugt daraus Zusammenfassungen und Audio-Überblicke.
- [n8n](https://n8n.io) - 🇪🇺 Workflow-Automatisierung aus Berlin, selbst hostbar, mit KI-Agenten-Bausteinen.
- [FLUX von Black Forest Labs](https://bfl.ai) - 🇪🇺 Bildmodelle aus Freiburg, Spitzenklasse bei Fotorealismus und Text im Bild.
- [ElevenLabs](https://elevenlabs.io/) - Sehr realistische Stimmen, Voice Cloning und Vertonung auf Deutsch.
- [Cursor](https://cursor.com) - Code-Editor mit KI-Agent, der ganze Projekte versteht und ändert.


## PROMPTGOTT Deep Dives

[PROMPTGOTT](https://promptgott.substack.com/?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) ist der Substack von *PromptGott AI SEO Hacks* ("Prompt Engineering Junkie, SEO-Dinosaurier und Spielkind in einem"). Die Artikel zeigen, wie man aus KI-Tools Systeme baut: Programmatic SEO, Content-Fabriken, Datensätze, Automatisierung. Diese Tabelle ordnet jeden Artikel den passenden Tool-Kategorien dieser Liste zu.

| Artikel | Kernidee | Passende Tools |
|---|---|---|
| [Der Greyhat-Eid](https://promptgott.substack.com/p/der-greyhat-eid?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Warum „Best Practices“ Verlierer produzieren | Einstieg: Haltung und Denkweise der Serie |
| [Google ist kein Suchsystem](https://promptgott.substack.com/p/google-ist-kein-suchsystem?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Es ist eine Daten-Extraktionsmaschine | [KI-Suchmaschinen](#ki-suchmaschinen), [Marketing und SEO](#marketing-und-seo) |
| [Das Ende einzelner Webseiten](https://promptgott.substack.com/p/das-ende-einzelner-webseiten?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Die Zukunft gehört Such-Territorien | [Marketing und SEO](#marketing-und-seo) |
| [Die Machine](https://promptgott.substack.com/p/die-machine?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Webseiten sind Projekte. Systeme sind Imperien. | [Automatisierung und KI-Agenten](#automatisierung-und-ki-agenten) |
| [Die Infrastruktur](https://promptgott.substack.com/p/die-infrastruktur?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Maschinen statt Webseiten bauen | [Programmieren mit KI](#programmieren-mit-ki), [Entwickler-Tools](#entwickler-tools-und-llmops) |
| [The Merchant Brain](https://promptgott.substack.com/p/the-merchant-brain?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | merchants.json als zentrales Nervensystem | [Automatisierung und KI-Agenten](#automatisierung-und-ki-agenten), [Marketing und SEO](#marketing-und-seo) |
| [Programmatic SEO Architecture](https://promptgott.substack.com/p/programmatic-seo-architecture?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Template × Datensatz = Dominanz | [Marketing und SEO](#marketing-und-seo), [Programmieren mit KI](#programmieren-mit-ki) |
| [Datensätze sind die neue Währung](https://promptgott.substack.com/p/datensatze-sind-die-neue-wahrung?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Das Internet als Datenbank | [Produktivität](#produktivität), [Entwickler-Tools](#entwickler-tools-und-llmops) |
| [The Index Swarm](https://promptgott.substack.com/p/the-index-swarm?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Millionen URLs ohne Qualitätsverlust | [Marketing und SEO](#marketing-und-seo) |
| [Die Content Factory](https://promptgott.substack.com/p/die-content-factory?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Industrielle Informationsproduktion | [Schreibassistenten](#schreibassistenten), [Automatisierung](#automatisierung-und-ki-agenten) |
| [Der Authority Layer](https://promptgott.substack.com/p/der-authority-layer?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Warum Trust hauptsächlich Mathematik ist | [Marketing und SEO](#marketing-und-seo) |
| [Die Lokalisierungs-Bombe](https://promptgott.substack.com/p/die-lokalisierungs-bombe?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Jede Stadt wird ein Revenue-Node | [Übersetzung und Lokalisierung](#übersetzung-und-lokalisierung) |
| [Der FAQ-Reaktor](https://promptgott.substack.com/p/der-faq-reaktor?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | „People Also Ask“ als unendliches Inventar | [Marketing und SEO](#marketing-und-seo), [Kundenservice](#kundenservice) |
| [The Programmatic Revenue Machine](https://promptgott.substack.com/p/the-programmatic-revenue-machine?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) | Gastbeitrag von HanSEO Hafen | [Marketing und SEO](#marketing-und-seo) |


## Text und Sprache

### Sprachmodelle und APIs

*Umfangreichere Modell-Liste: [Awesome AI Models](https://github.com/dariubs/awesome-ai-models)*

- [OpenAI API](https://platform.openai.com) - Zugriff auf die GPT-Modelle für eigene Anwendungen, Automatisierungen und Agenten.
- [Anthropic API](https://docs.anthropic.com) - Die Claude-Modelle per API, stark bei langen Kontexten, Werkzeugnutzung und Code.
- [Google Gemini API](https://ai.google.dev) - Gemini-Modelle über Google AI Studio und die Gemini API, multimodal (Text, Bild, Audio, Video).
- [Mistral AI](https://mistral.ai) - 🇪🇺 Offene und kommerzielle Modelle aus Paris, per API oder selbst gehostet.
- [Llama](https://www.llama.com) - Metas Familie offener Sprachmodelle zum Selbsthosten und Feintunen. `OSS`
- [DeepSeek](https://www.deepseek.com) - Chinesische Modellreihe mit offenen Gewichten, besonders günstig im Reasoning.
- [Qwen](https://qwenlm.github.io) - Offene Modellfamilie von Alibaba, von klein bis sehr groß, stark mehrsprachig. `OSS`
- [Bloom](https://huggingface.co/docs/transformers/model_doc/bloom) - Offenes, mehrsprachiges Modell aus dem BigScience-Projekt von Hugging Face (46 Sprachen). `OSS`
- [Hugging Face](https://huggingface.co) - Die zentrale Plattform für offene Modelle, Datensätze und Demo-Apps (Spaces).

### Chatbots und Assistenten

- [ChatGPT](https://chatgpt.com) - Der Chat-Assistent von OpenAI für Text, Analyse, Bilder und Websuche.
- [Claude](https://claude.ai/) - Assistent von Anthropic, stark bei langen Dokumenten, Schreiben und Code.
- [Gemini](https://gemini.google.com) - Googles Assistent, eng verzahnt mit Gmail, Docs und Drive.
- [Microsoft Copilot](https://copilot.microsoft.com) - Microsofts Assistent (früher Bing Chat), integriert in Windows, Edge und Microsoft 365.
- [Le Chat von Mistral](https://chat.mistral.ai) - 🇪🇺 Der Chat-Assistent von Mistral AI, schnell und mit Websuche.
- [Langdock](https://langdock.com) - 🇪🇺 KI-Plattform aus Deutschland, die Unternehmen mehrere Modelle in einer DSGVO-orientierten Oberfläche bereitstellt.
- [DeepSeek](https://www.deepseek.com) - Kostenloser Chat mit den DeepSeek-Modellen, stark bei Mathe und Code.
- [Character.AI](https://character.ai/) - Eigene Figuren erstellen und mit ihnen chatten.
- [ChatPDF](https://www.chatpdf.com/) - PDF hochladen und Fragen dazu stellen.
- [ChatSonic](https://writesonic.com/chat) - Assistent von Writesonic für Text- und Bilderstellung.
- [Phind](https://www.phind.com/) - Suchmaschine und Assistent speziell für Programmierer, auch als VS-Code-Erweiterung.
- [Tiledesk](https://tiledesk.com/) - No-Code-Framework für Chatbots mit LLM-Anbindung, Open Source. `OSS`
- [AICamp](https://aicamp.so/) - ChatGPT-Arbeitsbereich für Teams.
- [Gali Chat](https://www.galichat.com/) - KI-Support-Assistent für Websites, rund um die Uhr.
- [dmwithme](https://dmwithme.com) - KI-Begleiter mit Emotionen, der auch widerspricht.

### KI-Suchmaschinen

> 💡 **PROMPTGOTT-Praxis:** [Google ist kein Suchsystem](https://promptgott.substack.com/p/google-ist-kein-suchsystem?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Warum Suchmaschinen eigentlich Daten-Extraktionsmaschinen sind und was das für Sichtbarkeit in KI-Antworten bedeutet.

- [Perplexity](https://www.perplexity.ai/) - Antwortmaschine mit Quellenangaben für schnelle, belegte Recherche.
- [Exa](https://exa.ai) - Semantische Suche per API (früher Metaphor), gebaut für KI-Anwendungen und Agenten.
- [Phind](https://phind.com/) - KI-Suche für Entwickler-Fragen.
- [You.com](https://you.com/) - KI-Suchmaschine mit Fokus auf Privatsphäre und Anpassbarkeit.
- [Komo AI](https://komo.ai/) - KI-Suche mit kurzen, schnellen Antworten.
- [Telborg](https://telborg.com/) - KI-Recherche zum Klimawandel, ausschließlich mit Daten von Regierungen, Institutionen und Unternehmen.
- [MemFree](https://github.com/memfreeme/memfree) - Hybride KI-Suche über Web, Lesezeichen, Notizen und Dokumente. `OSS`
- [Refinder AI](https://refinder.ai/) - Universelle KI-Suche über alle Arbeitswerkzeuge.
- [Agentset.ai](https://agentset.ai/) - Semantische Suche und RAG für eigene Daten. `OSS`

### Lokal und privat mit Dokumenten chatten

Für alle, die Daten nicht in eine Cloud geben wollen oder dürfen.

- [Ollama](https://ollama.com/) - Sprachmodelle mit einem Befehl lokal auf dem eigenen Rechner ausführen. `OSS`
- [LM Studio](https://lmstudio.ai) - Desktop-App, um offene Modelle lokal herunterzuladen und offline zu nutzen.
- [Open WebUI](https://openwebui.com) - Selbst gehostete ChatGPT-ähnliche Oberfläche für lokale und API-Modelle. `OSS`
- [privateGPT](https://github.com/imartinez/privateGPT) - Fragen an eigene Dokumente stellen, komplett ohne Internetverbindung. `OSS`
- [quivr](https://github.com/StanGirard/quivr) - "Zweites Gehirn": Dateien ablegen und per LLM mit ihnen chatten. `OSS`
- [gpt4all](https://github.com/nomic-ai/gpt4all) - Lokaler Chat-Client für offene Modelle, läuft auch ohne GPU. `OSS`

### Schreibassistenten

*Umfangreichere Liste: [Awesome AI Writing](https://github.com/xaramore/awesome-ai-writing)*

> 💡 **PROMPTGOTT-Praxis:** [Die Content Factory](https://promptgott.substack.com/p/die-content-factory?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Wie aus Schreib-Tools eine industrielle Informationsproduktion wird.

- [DeepL Write](https://www.deepl.com/write) - 🇪🇺 Verbessert Stil, Grammatik und Tonalität deutscher und englischer Texte.
- [neuroflash](https://neuroflash.com) - 🇪🇺 KI-Texter aus Hamburg, spezialisiert auf deutschsprachige Marketing-Texte.
- [Jasper](https://www.jasper.ai/) - Content-Plattform für Marketing-Teams mit Markenstimme und Vorlagen.
- [Compose AI](https://www.compose.ai/) - Chrome-Erweiterung mit KI-Autovervollständigung beim Schreiben.
- [Rytr](https://rytr.me/) - Günstiger KI-Schreibassistent für kurze und mittellange Texte.
- [Wordtune](https://www.wordtune.com/) - Formuliert Sätze um, kürzt oder erweitert sie.
- [HyperWrite](https://hyperwriteai.com/) - Schreibassistent von der Idee bis zum fertigen Entwurf.
- [Nexus AI](https://mynexusai.com/) - Plattform für Texte, Code, Voiceover, Recherche und Bilder.
- [Moonbeam](https://www.gomoonbeam.com/) - Längere Blogartikel in einem Bruchteil der Zeit.
- [Copy.ai](https://www.copy.ai/) - Marketing-Texte und GTM-Workflows mit KI.
- [Anyword](https://anyword.com/) - Werbetexte mit Performance-Vorhersage.
- [Contenda](https://contenda.co/) - Macht aus vorhandenem Content (Videos, Talks) neue Formate.
- [Hypotenuse AI](https://www.hypotenuse.ai/) - Aus wenigen Keywords Artikel, Produktbeschreibungen und Social-Posts; stark im E-Commerce.
- [Lavender](https://www.lavender.ai/) - E-Mail-Coach für mehr Antworten auf Vertriebsmails.
- [Lex](https://lex.page/) - Textverarbeitung mit eingebauter KI.
- [Jenni](https://jenni.ai/) - Schreibassistent für wissenschaftliche Texte mit Zitaten.
- [LAIKA](https://www.writewithlaika.com/) - Trainiert eine KI auf deinen eigenen Schreibstil, für kreatives Schreiben.
- [QuillBot](https://quillbot.com) - Paraphrasieren, Zusammenfassen und Grammatikprüfung.
- [Postwise](https://postwise.ai/) - Posts für X/Twitter schreiben und planen.
- [RapidTextAI](https://app.rapidtextai.com/) - Artikel mit mehreren Modellen (GPT, Gemini, DeepSeek, Grok) erstellen.
- [Copysmith](https://copysmith.ai/) - Content-Erstellung für Unternehmen und E-Commerce.
- [Yomu](https://www.yomu.ai) - Schreibassistent für Studierende und Forschende.
- [Quick Creator](https://quickcreator.io) - SEO-optimierte Blog-Plattform mit KI.
- [Trolly.ai](https://trolly.ai/) - SEO-Artikel schneller erstellen.
- [PulsePost](https://pulsepost.io/) - KI-Autor, der direkt auf die eigene Website veröffentlicht.
- [Shy Editor](https://www.shyeditor.com) - Moderne KI-Schreibumgebung für Prosa aller Art.
- [Headlinesai.pro](https://www.headlinesai.pro/) - Klickstarke Überschriften für YouTube, Medium, Reddit und mehr.
- [GPTLocalhost](https://gptlocalhost.com/demo/) - Word-Add-in, das lokale LLMs in Microsoft Word nutzt, Alternative zu Copilot in Word.

### Übersetzung und Lokalisierung

> 💡 **PROMPTGOTT-Praxis:** [Die Lokalisierungs-Bombe](https://promptgott.substack.com/p/die-lokalisierungs-bombe?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Warum jede Stadt ein Revenue-Node werden kann.

- [DeepL Übersetzer](https://www.deepl.com/translator) - 🇪🇺 Übersetzt Texte und ganze Dokumente, mit Glossar für feste Begriffe.
- [DeepL Write](https://www.deepl.com/write) - 🇪🇺 Glättet übersetzte Texte stilistisch nach.
- [X-doc AI](https://x-doc.ai/) - KI-Übersetzer für Dokumente mit Erhalt des Layouts.
- [ElevenLabs Dubbing](https://elevenlabs.io/) - Vertont Videos in andere Sprachen mit der Originalstimme.
- [HeyGen](https://www.heygen.com) - Übersetzt Videos mit Lippensynchronisation.

### Browser-Erweiterungen und Add-ons

- [Merlin](https://merlin.foyer.work/) - KI-Assistent auf jeder Website, per Tastenkürzel.
- [Gist AI](https://www.gistai.tech) - Kostenlose Zusammenfassungen für Websites, YouTube und PDFs.
- [WebChatGPT](https://chrome.google.com/webstore/detail/webchatgpt-chatgpt-with-i/lpfemeioodjbpieminkklglpmhlngfcn) - Ergänzt ChatGPT-Prompts um aktuelle Web-Ergebnisse.
- [GPT for Sheets and Docs](https://workspace.google.com/marketplace/app/gpt_for_sheets_and_docs/677318054654) - KI-Funktionen direkt in Google Sheets und Docs, ideal für Massen-Texte in Tabellen.
- [YouTube Summary with ChatGPT](https://chrome.google.com/webstore/detail/youtube-summary-with-chat/nmmicjeknamkfloonkhhcjmomieiodli) - Fasst YouTube-Videos zusammen.
- [ChatGPT Prompt Genius](https://chrome.google.com/webstore/detail/chatgpt-prompt-genius/jjdnakkfjnnbbckhifcfchagnpofjffo) - Prompts entdecken, teilen und Chat-Verlauf lokal speichern.
- [ChatGPT for Search Engines](https://chrome.google.com/webstore/detail/chatgpt-for-search-engine/feeonheemodpkdckaljcjogdncpiiban) - Zeigt KI-Antworten neben Google-, Bing- und DuckDuckGo-Ergebnissen.
- [ShareGPT](https://sharegpt.com/) - ChatGPT-Unterhaltungen teilen und entdecken.
- [ChatGPT Writer](https://chatgptwriter.ai/) - Komplette E-Mails und Nachrichten per KI schreiben.
- [ChatGPT for Jupyter](https://github.com/TiesdeKok/chat-gpt-jupyter-extension) - KI-Hilfsfunktionen in Jupyter Notebook und Jupyter Lab. `OSS`
- [editGPT](https://www.editgpt.app/) - Korrekturlesen mit Änderungsverfolgung in ChatGPT.
- [Chatbot UI](https://github.com/mckaywrigley/chatbot-ui) - Open-Source-Oberfläche für ChatGPT und andere Modelle. `OSS`
- [Forefront](https://www.forefront.ai/) - Alternative Oberfläche für Chat-Modelle.
- [AI Character for GPT](https://chromewebstore.google.com/detail/ai-character-for-gpt/daoeioifimkjegafelcaljboknjkkohh) - Rollen für ChatGPT und andere Bots per Klick, für bessere Antworten.

### Produktivität

> 💡 **PROMPTGOTT-Praxis:** [Datensätze sind die neue Währung](https://promptgott.substack.com/p/datensatze-sind-die-neue-wahrung?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Warum strukturierte Daten mehr wert sind als einzelne Texte.

- [Notion AI](https://www.notion.so/product/ai) - Schreiben, Zusammenfassen und Fragen an den eigenen Notion-Workspace.
- [NotebookLM](https://notebooklm.google.com/) - Chat, Zusammenfassungen und Audio-Überblicke aus eigenen Quellen.
- [Napkin](https://www.napkin.ai/) - Verwandelt Text in Diagramme und Grafiken.
- [Gamma](https://gamma.app/) - Präsentationen, Dokumente und Webseiten aus einem Prompt.
- [Mem](https://mem.ai/) - Notiz-App, die sich selbst organisiert.
- [Taskade](https://www.taskade.com/) - Aufgaben, Teamarbeit und KI-Agenten in einem Workspace.
- [Nekton AI](https://nekton.ai) - Workflows in Alltagssprache beschreiben und automatisieren.
- [Elephas](https://elephas.app/) - Persönlicher KI-Schreibassistent für den Mac.
- [Google Sheets Formula Generator](https://bettersheets.co/google-sheets-formula-generator) - Formeln für Google Sheets aus Text erzeugen.
- [CreateEasily](https://createeasily.com/) - Kostenlose Transkription von Audio- und Videodateien bis 2 GB.
- [Cosmos](https://meetcosmos.com/) - Lokale, offline KI-Suche in eigenen Fotos und Videos.
- [aiPDF](https://aipdf.ai) - KI-Dokumentenassistent für PDFs.
- [Summary With AI](https://www.summarywithai.com/) - Fasst lange PDFs über alle Seiten hinweg zusammen.
- [Emilio](https://getemil.io) - Priorisiert und automatisiert E-Mails.
- [Pieces](https://pieces.app/) - On-Device-Copilot für Entwickler, der Code-Schnipsel und Kontext speichert.
- [Huntr AI Resume Builder](https://huntr.co/product/ai-resume-builder/) - ATS-freundliche Lebensläufe mit KI.
- [Chat With PDF by Copilot.us](https://copilot.us/apps/chat-with-pdf) - Mit mehreren PDFs gleichzeitig chatten.
- [Recall](https://www.getrecall.ai/) - Fasst Artikel, Videos und Podcasts zusammen und baut eine Wissensbasis.
- [Talently AI](https://interview.talently.ai/) - KI-Interviewer für Bewerbungsgespräche mit Echtzeit-Bewertung.
- [AnkiDecks AI](https://anki-decks.com) - Lernkarten aus Dateien oder Text erzeugen.
- [AI for Google Slides](https://www.aiforgoogleslides.com/) - Präsentationen für Google Slides mit KI.
- [FARSITE](https://far.site/) - Compliance-Software für US-Regierungsauftragnehmer.
- [BrainSoup](https://www.nurgo-software.com/products/brainsoup) - Multi-Agenten-Client für mehrere LLMs mit Gedächtnis und Werkzeugen.
- [MindPal](https://mindpal.space/) - "Zweites Gehirn" mit einem Team aus KI-Agenten.
- [fabric](https://github.com/danielmiessler/fabric/) - KI im Terminal mit einer Bibliothek bewährter Prompt-Muster. `OSS`
- [SlidesWizard](https://slideswizard.io) - PowerPoint- und Google-Slides-Präsentationen zu jedem Thema.
- [Transgate](https://transgate.ai/) - Sprache-zu-Text mit KI.
- [RabbitHoles AI](https://www.rabbitholes.ai/) - Chat mit KI auf einer unendlichen Leinwand.
- [Rember](https://www.rember.com/) - Spaced-Repetition-System zum besseren Merken.
- [Qurate](https://qurate.appcradle.net/) - Findet passende Zitate zum Kontext.
- [FirmOS](https://www.firmos.ai/) - Automatisierung für Steuer- und Buchhaltungskanzleien.
- [Whisper API](https://whisper-api.com) - Transkriptions-API auf Basis von OpenAI Whisper, 5 kostenlose Transkriptionen pro Tag.
- [Smmry](https://smmry.com/) - Fasst lange Inhalte in klare Kernaussagen zusammen.
- [Nudge AI](https://getnudgeai.com/) - KI-Dokumentationsassistent für das Gesundheitswesen.
- [Summara](https://summara.io/) - Widget für YouTube-Zusammenfassungen und Transkripte.
- [Marblism](https://marblism.com) - KI-"Mitarbeiter" für kleine Unternehmen.
- [Spell](https://spellapp.com) - KI-Alternative zu Google Docs.
- [Kosmik](https://www.kosmik.app) - 🇪🇺 KI-Moodboards und visuelle Recherche.
- [Magic Potion](https://www.magicpotion.app) - Visueller Prompt-Editor.
- [MinusX](https://minusx.ai/) - KI-Analyst, der Datenfragen in Metabase beantwortet.
- [Excelmatic](https://excelmatic.ai) - Excel-Daten per Chat analysieren und visualisieren, ohne Formeln.
- [Langfa.st](https://langfa.st/) - Spielwiese ohne Anmeldung zum Testen und Teilen von Prompt-Vorlagen.
- [SalesAgent Chat](https://www.salesagent.chat) - KI-Vertriebscoach mit Echtzeit-Unterstützung.

### Meeting-Assistenten

- [tl;dv](https://tldv.io) - 🇪🇺 Zeichnet Zoom, Teams und Google Meet auf, transkribiert und fasst zusammen, auch auf Deutsch.
- [Fireflies.ai](https://fireflies.ai) - Meeting-Notizen, Transkripte und Suche über alle Calls.
- [Otter.ai](https://otter.ai/) - Nimmt Meetings auf, schreibt mit und fasst zusammen.
- [MeetGeek](https://meetgeek.ai/) - Nimmt Meetings auf, transkribiert und liefert Kernpunkte.
- [Cogram](https://www.cogram.com/) - Automatische Notizen und Aufgaben aus virtuellen Meetings.
- [Sybill](https://www.sybill.ai/) - Fasst Vertriebsgespräche zusammen, inklusive Pain Points und nächsten Schritten.
- [Scribbl](https://www.scribbl.co) - KI-Meeting-Notizen für Google Meet.

### Wissenschaft und Recherche

- [Elicit](https://elicit.com) - Automatisiert Teile der Literaturrecherche.
- [Consensus](https://consensus.app/search/) - Suchmaschine, die Antworten aus wissenschaftlichen Studien liefert.
- [SciSpace](https://scispace.com/) - Chat mit wissenschaftlichen PDFs.
- [NotebookLM](https://notebooklm.google.com/) - Chat mit eigenen Dokumenten, Links und Texten.
- [genei](https://www.genei.io/) - Fasst Fachartikel in Sekunden zusammen.
- [Explainpaper](https://www.explainpaper.com/) - Unverständliche Stellen in Papers markieren und erklären lassen.
- [Sourcely](https://www.sourcely.net/) - Findet passende Quellen und Zitate für wissenschaftliche Arbeiten.
- [Mathos AI](https://www.mathgptpro.com/) - KI-Mathe-Löser und Tutor.

### Kundenservice

> 💡 **PROMPTGOTT-Praxis:** [Der FAQ-Reaktor](https://promptgott.substack.com/p/der-faq-reaktor?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Wie aus Kundenfragen und „People Also Ask“ ein unendliches Content-Inventar wird.

- [SiteGPT](https://sitegpt.ai/) - Trainiert einen Support-Bot auf die eigene Website.
- [GPTHelp.ai](https://gpthelp.ai/) - KI-Chatbot für den Website-Support.
- [SiteSpeakAI](https://sitespeak.ai) - Automatisiert den Kundenservice mit KI.
- [Dear AI](https://www.dearai.online) - Chatbot für Kundenservice und Vertrieb.
- [Inline Help](https://inlinehelp.com) - Beantwortet Kundenfragen, bevor sie gestellt werden.
- [Aidbase](https://www.aidbase.ai) - KI-Support für SaaS-Startups.
- [Twig](https://www.twig.so/) - Löst Kundenanfragen sofort, für Kunden und Support-Teams.
- [EmailTriager](https://www.emailtriager.com/) - Entwirft E-Mail-Antworten automatisch im Hintergrund.


## Automatisierung und KI-Agenten

> 💡 **PROMPTGOTT-Praxis:** [Die Machine](https://promptgott.substack.com/p/die-machine?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (Systeme statt Einzelprojekte) und [The Merchant Brain](https://promptgott.substack.com/p/the-merchant-brain?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (eine zentrale Datei als Nervensystem für alle Automationen).

*Umfangreichere Liste: [Awesome Workflow Automation](https://github.com/dariubs/awesome-workflow-automation)*

- [n8n](https://n8n.io) - 🇪🇺 Workflow-Automatisierung aus Berlin, selbst hostbar (fair-code), mit KI-Agenten-Knoten.
- [Make](https://www.make.com) - 🇪🇺 Visuelle Automatisierungsplattform aus Prag mit Tausenden App-Anbindungen.
- [Zapier](https://zapier.com) - Verbindet Tausende Apps per Automatisierung, inklusive KI-Schritten und Agenten.
- [MindStudio](https://mindstudio.ai/) - KI-Agenten ohne Code bauen, mit über 100 Vorlagen.
- [Taskade](https://www.taskade.com/) - Autonome KI-Agenten für Aufgaben und Team-Workflows.
- [Nekton AI](https://nekton.ai) - Workflows Schritt für Schritt in Alltagssprache beschreiben.
- [AI-Flow](https://ai-flow.net/) - Mehrere KI-Modelle visuell miteinander verbinden.
- [Shotstack Workflows](https://shotstack.io/product/workflows/) - No-Code-Automatisierung für KI-Medienproduktion.
- [Hyperbrowser](https://hyperbrowser.ai/) - Browser-Infrastruktur für KI-Agenten mit Proxys und Session-Aufzeichnung.
- [Notte](https://github.com/nottelabs/notte) - Framework für Agenten, die den Browser bedienen. `OSS`


## Entwickler-Tools und LLMOps

- [LangChain](https://langchain.com/) - Framework für Anwendungen und Agenten auf Basis von Sprachmodellen. `OSS`
- [LlamaIndex](https://www.llamaindex.ai/) - Daten-Framework für LLM-Anwendungen mit eigenen Daten (RAG). `OSS`
- [Haystack](https://haystack.deepset.ai/) - 🇪🇺 Framework aus Berlin für Agenten, semantische Suche und Frage-Antwort-Systeme. `OSS`
- [Cohere](https://cohere.com/) - Sprachmodelle und Embeddings für Unternehmen, stark bei Suche und Reranking.
- [Langfuse](https://langfuse.com/) - 🇪🇺 LLM-Engineering-Plattform aus Berlin zum Debuggen, Tracen und Bewerten. [`OSS`](https://github.com/langfuse/langfuse)
- [Keploy](https://keploy.io/) - Wandelt echten Nutzer-Traffic in Testfälle und Datenstubs um. `OSS`
- [Portia AI](https://www.portialabs.ai/) - Agenten-Framework, bei dem Agenten ihre geplanten Schritte offenlegen und unterbrechbar bleiben. [`OSS`](https://github.com/portiaAI/portia-sdk-python)
- [LMQL](https://lmql.ai/) - Abfragesprache für Sprachmodelle. `OSS`
- [Phoenix](https://phoenix.arize.com/) - Observability für LLM- und ML-Modelle im Notebook. `OSS`
- [Prediction Guard](https://www.predictionguard.com/) - Private, kontrollierte und compliance-konforme LLM-Nutzung.
- [Portkey](https://portkey.ai/) - LLMOps-Plattform zum Überwachen, Steuern und Verbessern von LLM-Apps.
- [OpenAI Downtime Monitor](https://status.portkey.ai/) - Kostenloses Monitoring von Verfügbarkeit und Latenz verschiedener LLM-Anbieter.
- [ChatWithCloud](https://chatwithcloud.ai/) - AWS per natürlicher Sprache im Terminal steuern.
- [SinglebaseCloud](https://singlebase.cloud) - Backend mit Vektor-DB, Dokument-DB und Auth für KI-Apps.
- [Maxim AI](https://www.getmaxim.ai/) - Evaluation und Observability für generative KI.
- [Wordware](https://www.wordware.ai) - Web-IDE, in der Fachleute und KI-Entwickler gemeinsam Agenten bauen; Prompting als Programmiersprache.
- [Hexabot](https://hexabot.ai) - No-Code-Baukasten für mehrsprachige Chatbots und Agenten. `OSS`
- [AI/ML API](https://aimlapi.com/) - Über 100 KI-Modelle über eine einzige API.
- [Opik](https://www.comet.com/site/products/opik/) - Testen, Bewerten und Überwachen von LLM-Anwendungen. `OSS`
- [Kiln](https://getkiln.ai) - Eigene Modelle bauen: synthetische Daten, Feintuning und Datensatz-Pflege ohne Code.
- [Calmo](https://getcalmo.com/) - Produktionsfehler mit KI schneller debuggen.
- [Cleanlab](https://help.cleanlab.ai/tlm/) - Erkennt und behebt Halluzinationen in LLM-Anwendungen.
- [Amazon Q Developer CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html) - Befehlsvervollständigung, Übersetzung von Absicht in Befehle und Agenten-Chat im Terminal.
- [Agentic Radar](https://github.com/splx-ai/agentic-radar) - Sicherheits-Scanner für agentische Workflows. `OSS`
- [VoltAgent](https://github.com/voltagent/voltagent) - TypeScript-Framework für KI-Agenten mit Werkzeugen und Gedächtnis. `OSS`
- [TensorZero](https://www.tensorzero.com/) - LLM-Gateway, Observability, Optimierung und Evaluation in einem Framework. `OSS`
- [ToolHive](https://github.com/stacklok/toolhive) - Passende MCP-Server finden und per Klick bereitstellen. `OSS`
- [AgentDock](https://agentdock.ai) - Ein API-Schlüssel für alle Dienste, die ein Agent braucht.
- [Codeflash](https://www.codeflash.ai/) - Optimiert Python-Code automatisch auf Geschwindigkeit.
- [Agenta](https://agenta.ai/) - Prompt-Management, Evaluation und Observability. [`OSS`](https://github.com/agenta-ai/agenta)
- [Pagerly](https://www.pagerly.io) - Operations-Copilot für Slack und Teams, unterstützt die Rufbereitschaft beim Debuggen.
- [Harbor](https://github.com/av/harbor) - LLM-Backends, APIs und Oberflächen mit einem Befehl starten. `OSS`
- [Petals](https://github.com/bigscience-workshop/petals) - Große Modelle verteilt im BitTorrent-Stil ausführen. `OSS`
- [Context Data](https://contextdata.ai/) - Datenaufbereitung und ETL für generative KI.


## Programmieren mit KI

*Umfangreichere Liste: [Awesome AI Coding Tools](https://github.com/ai-for-developers/awesome-ai-coding-tools)*

> 💡 **PROMPTGOTT-Praxis:** [Die Infrastruktur](https://promptgott.substack.com/p/die-infrastruktur?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) und [Programmatic SEO Architecture](https://promptgott.substack.com/p/programmatic-seo-architecture?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de): Maschinen statt Webseiten bauen, nach dem Prinzip Template × Datensatz.

- [Cursor](https://cursor.com) - KI-Code-Editor mit Agent, der ganze Codebasen versteht und ändert.
- [Claude Code](https://www.anthropic.com/claude-code) - Agentisches Coding-Tool von Anthropic für Terminal, IDE und Web.
- [GitHub Copilot](https://github.com/features/copilot) - Code-Vorschläge, Chat und Coding-Agent direkt im Editor und auf GitHub.
- [Windsurf](https://www.windsurf.com) - KI-Code-Editor mit agentischem Assistenten.
- [Lovable](https://lovable.dev) - 🇪🇺 Web-Apps per Chat bauen, aus Stockholm.
- [Bolt.new](https://bolt.new) - Full-Stack-Web-Apps im Browser aus einem Prompt.
- [v0](https://v0.app) - Erzeugt UI und Web-Apps mit React und Next.js aus Text.
- [Kilo Code](https://kilocode.ai) - Open-Source-Coding-Assistent in VS Code zum Planen, Bauen und Fixen. `OSS`
- [Amazon Q Developer](https://aws.amazon.com/q/developer/) - KI-Coding-Assistent für VS Code und IntelliJ mit Chat und Agenten-Workflows.
- [Tabnine](https://www.tabnine.com/) - Code-Vervollständigung, auch als private On-Premise-Variante.
- [Replit](https://replit.com) - Browser-IDE mit KI-Agent, der Apps baut und bereitstellt.
- [GoCodeo](https://www.gocodeo.com/) - KI-Agent für Code und Tests.
- [CodeRabbit](https://coderabbit.ai/) - Automatische KI-Code-Reviews für Pull Requests.
- [PR-Agent](https://github.com/Codium-ai/pr-agent) - Automatische PR-Analyse, Feedback und Vorschläge. `OSS`
- [Gito](https://github.com/Nayjest/Gito) - KI-Code-Reviewer für GitHub Actions oder lokal, mit jedem LLM nutzbar. `OSS`
- [CodiumAI / Qodo](https://www.codium.ai/) - Schlägt sinnvolle Tests direkt in der IDE vor.
- [Mintlify](https://mintlify.com/) - KI-gestützte Dokumentation für Entwickler.
- [Stenography](https://stenography.dev/) - Automatische Code-Dokumentation.
- [AI2sql](https://www.ai2sql.io/) - SQL-Abfragen aus natürlicher Sprache.
- [poorcoder](https://github.com/vgrichina/poorcoder) - Bash-Skripte, die das Terminal mit Web-Assistenten wie Claude oder Grok verbinden. `OSS`
- [TurboPilot](https://github.com/ravenscroftj/turbopilot) - Selbst gehosteter Copilot-Klon, der mit 4 GB RAM läuft. `OSS`
- [GPT-Code UI](https://github.com/ricklamers/gpt-code-ui) - Open-Source-Nachbau des ChatGPT Code Interpreter. `OSS`
- [MetaGPT](https://github.com/geekan/MetaGPT) - Multi-Agenten-Framework: aus einer Anforderung werden PRD, Design, Aufgaben und Code. `OSS`
- [Plandex](https://github.com/plandex-ai/plandex) - Terminal-basierte KI-Programmierumgebung für komplexe Aufgaben. `OSS`
- [MutahunterAI](https://github.com/codeintegrity-ai/mutahunter) - Mutationstests mit KI für bessere Testabdeckung. `OSS`
- [AI Kernel Explorer](https://github.com/mathiscode/ai-kernel-explorer) - Linux-Kernel-Quellcode mit KI-Zusammenfassungen erkunden. `OSS`
- [WhoDB](https://github.com/clidey/whodb) - Datenbank-Explorer für SQL, NoSQL, Graph und Cache mit KI-Chat. `OSS`
- [DataPup](https://github.com/DataPupOrg/DataPup) - Datenbank-Client mit KI-Unterstützung für Abfragen. `OSS`
- [FlexApp](https://flexapp.ai/) - Mobile Apps mit KI bauen, ohne Code.
- [Capacity](https://capacity.so) - Aus Ideen in Minuten funktionierende Web-Apps.
- [Runcell](https://runcell.dev) - KI-Agent für Jupyter Lab, der Code schreibt, ausführt und Ergebnisse analysiert.
- [Manifest](https://github.com/mnfst/manifest) - Backend-Alternative zu Supabase für KI-Code-Editoren und Vibe Coding. `OSS`
- [Code to Flow](https://codetoflow.com) - Macht aus Code interaktive Flussdiagramme.


## Bilder

*Umfangreichere Listen: [Best Image AI Tools](IMAGE.md) und [Awesome AI Image](https://github.com/xaramore/awesome-ai-image)*

### Bildmodelle

- [FLUX von Black Forest Labs](https://bfl.ai) - 🇪🇺 Bildmodelle aus Freiburg, stark bei Fotorealismus, Text im Bild und Bildbearbeitung.
- [Midjourney](https://www.midjourney.com/) - Bildgenerator mit markantem, künstlerischem Stil.
- [Stable Diffusion](https://huggingface.co/CompVis/stable-diffusion-v1-4) - Offenes Text-zu-Bild-Modell von Stability AI, lokal ausführbar. `OSS`
- [Imagen](https://imagen.research.google/) - Googles Text-zu-Bild-Modell mit hohem Fotorealismus.
- [Ideogram](https://ideogram.ai) - Bildgenerator, der besonders gut lesbare Schrift in Bildern erzeugt.
- [Adobe Firefly](https://firefly.adobe.com) - Bildgenerierung von Adobe, trainiert auf lizenzierten Inhalten, integriert in Photoshop.
- [DALL·E](https://openai.com/dall-e-2/) - Bildmodell von OpenAI, heute direkt in ChatGPT nutzbar.
- [Make-A-Scene](https://ai.facebook.com/blog/greater-creative-control-for-ai-image-generation/) - Metas Forschungsansatz, der Text und Skizze kombiniert.
- [DragGAN](https://github.com/XingangPan/DragGAN) - Bilder per Punkt-Ziehen interaktiv verformen. `OSS`

### Bild-Dienste

- [Canva](https://www.canva.com/ai-image-generator/) - KI-Bilder direkt in der Design-Plattform erzeugen und bearbeiten.
- [Leonardo.ai](https://leonardo.ai) - Bildgenerator mit vielen Stil-Modellen, beliebt für Game-Assets und Marketing.
- [KREA](https://www.krea.ai/) - Echtzeit-Bildgenerierung, Upscaling und Video in einer Oberfläche.
- [PhotoRoom](https://www.photoroom.com/) - 🇪🇺 Produktfotos per Smartphone: Hintergrund entfernen und ersetzen, aus Paris.
- [ClipDrop](https://clipdrop.co/) - Professionelle Visuals ohne Fotostudio: freistellen, retuschieren, erweitern.
- [Magic Eraser](https://www.magiceraser.io/) - Störende Objekte in Sekunden aus Bildern entfernen.
- [Craiyon](https://www.craiyon.com/) - Kostenloser Bildgenerator (früher DALL-E mini).
- [DreamStudio](https://beta.dreamstudio.ai/) - Einfache Oberfläche für Stable Diffusion.
- [Artbreeder](https://www.artbreeder.com/) - Bilder mischen und gemeinsam weiterentwickeln.
- [GauGAN2](http://gaugan.org/gaugan2/) - Fotorealistische Landschaften aus Wörtern und Skizzen (NVIDIA).
- [Magic Studio](https://magicstudio.com/imagine) - Bilder aus einer Beschreibung erzeugen.
- [Patience.ai](https://www.patience.ai/) - App für Bilder mit Stable Diffusion.
- [GenShare](https://www.genshare.io/) - Kostenlos Kunst generieren und teilen.
- [Playground AI](https://playgroundai.com/) - Kostenloser Bildgenerator für Social Posts, Poster und Logos.
- [Pixelz AI Art Generator](https://pixelz.ai/) - Kunst aus Text mit mehreren Algorithmen.
- [PhotoGuruAI](https://photoguruai.com/) - Professionelle KI-Bewerbungsfotos in vielen Stilen.
- [Avatar AI](https://avatarai.me/) - Eigene KI-Avatare erstellen.
- [RunDiffusion](https://rundiffusion.com/) - Cloud-Arbeitsplatz für KI-Kunst.
- [Human Generator](https://generated.photos/human-generator) - Realistische Fotos von Menschen, die es nicht gibt.
- [VectorArt.ai](https://vectorart.ai) - Vektorgrafiken mit KI erzeugen.
- [Room Reinvented](https://roomreinvented.com) - Raumfoto hochladen und über 30 Einrichtungsstile ausprobieren.
- [Gensbot](https://gensbot.com) - Personalisiertes Merchandise aus einem Prompt.
- [PlantPhotoAI](https://www.plantphotoai.com/) - Kostenlose KI-Pflanzenbilder.
- [Black Headshots](https://www.blackheadshots.com) - KI-Bewerbungsfotos für Schwarze Berufstätige.
- [iColoring](https://icoloring.ai) - Kostenlose Ausmalbilder mit KI.
- [Suit me Up](https://suitmeup.pictures/) - Fotos von dir im Anzug erzeugen.
- [AI Photo Forge](https://aiphotoforge.com/) - Telegram-Bot für KI-Fotos von dir.
- [AI Boost](https://boost.pictures/) - All-in-one: Upscaling, Face Swap, Avatare, virtuelle Anprobe, Hintergründe.
- [PlantTattoosAI](https://www.planttattoosai.com/) - Tattoo-Designs mit Pflanzen und Blumen.

### Grafikdesign

- [Gamma](https://gamma.app/) - Präsentationen und Webseiten ohne Formatierungsarbeit.
- [Microsoft Designer](https://designer.microsoft.com/) - Designs für Social Media und Einladungen in Sekunden.
- [Canva](https://www.canva.com/) - Design-Plattform mit KI-Funktionen zum Erzeugen und Bearbeiten.
- [Brandmark](https://brandmark.io/) - Logo-Design mit KI.
- [Text2Infographic](https://text2infographic.com/) - Infografiken aus Text generieren und bearbeiten.
- [Seede.ai](https://seede.ai/) - Poster in einer Minute.
- [Magic Patterns](https://www.magicpatterns.com/) - UI-Entwürfe mit Figma-Export und React-Code.

### Bildarchive und Prompt-Sammlungen

- [KREA](https://www.krea.ai/) - Millionen KI-Bilder durchsuchen und Prompt-Sammlungen anlegen.
- [OpenArt](https://openart.ai/) - Über 10 Millionen Prompts durchsuchen und selbst generieren.
- [Libraire](https://libraire.ai/) - Große Bibliothek KI-generierter Bilder.
- [Phygital](https://app.phygital.plus/) - Vorlagen zum Erzeugen und Bearbeiten von Bildern.
- [PublicPrompts](https://publicprompts.art/) - Kostenlose Prompts für Stable Diffusion.

### Modell-Bibliotheken und Stable-Diffusion-Ressourcen

- [Civitai](https://civitai.com/) - Community-Plattform für Bildmodelle und LoRAs.
- [Stable Diffusion Models](https://rentry.org/sdmodels) - Umfangreiche Liste von Stable-Diffusion-Checkpoints.
- [Stable Horde](https://stablehorde.net/) - Verteiltes Community-Cluster für Stable Diffusion.
- [Hugging Face Diffusion Models Course](https://github.com/huggingface/diffusion-models-class) - Kostenloser Kurs zu Diffusionsmodellen in Python. `OSS`


## Video

- [Google Veo](https://deepmind.google/models/veo/) - Googles Videomodell für realistische Clips mit Ton.
- [Sora](https://openai.com/sora) - Videomodell von OpenAI für Clips aus Text und Bild.
- [Kling AI](https://app.klingai.com/global/) - Bild- und Videogenerierung mit sehr flüssiger Bewegung.
- [RunwayML](https://runwayml.com/) - Kreativ-Suite für KI-Video, Bearbeitung und Effekte.
- [Luma Dream Machine](https://lumalabs.ai) - Videos aus Text und Bildern mit realistischer Physik.
- [Pika](https://pika.art) - Kurze, verspielte KI-Videos und Effekte.
- [Synthesia](https://www.synthesia.io/) - Videos mit KI-Sprechern aus reinem Text, über 100 Sprachen inklusive Deutsch.
- [HeyGen](https://www.heygen.com) - Avatar-Videos und Video-Übersetzung mit Lippensynchronisation.
- [D-ID](https://www.d-id.com/) - Sprechende, interaktive Avatare per Klick.
- [Descript](https://www.descript.com) - Videos und Podcasts bearbeiten wie ein Textdokument.
- [Opus Clip](https://www.opus.pro) - Schneidet lange Videos automatisch in virale Shorts.
- [Clipwing](https://clipwing.pro/) - Zerlegt lange Videos in Dutzende kurze Clips.
- [Recast Studio](https://recast.studio) - KI-Assistent für Podcast-Marketing.
- [Based AI](https://www.basedlabs.ai/) - Intuitive Oberfläche für KI-Videos.
- [Sisif](https://sisif.ai/) - Aus Text in Sekunden ein Video.
- [Melies](https://melies.co) - Software für KI-Filmproduktion.


## Audio

### Stimmen und Voice Cloning

*Umfangreichere Liste: [Awesome AI Music](https://github.com/xaramore/awesome-ai-music)*

- [ElevenLabs](https://elevenlabs.io/) - Sehr realistische Stimmen, Voice Cloning und Vertonung in vielen Sprachen inklusive Deutsch.
- [Murf AI](https://murf.ai/) - Einfache Plattform für hochwertige Voiceover, beliebt im Marketing.
- [Descript Overdub](https://www.descript.com/overdub) - Voice Cloning direkt im Schnitt- und Transkriptionswerkzeug von Descript.
- [Respeecher](https://www.respeecher.com/) - Professionelles Voice Cloning für Film und Fernsehen.
- [Resemble AI](https://www.resemble.ai/) - Echtzeit-Sprachsynthese und Voice Cloning mit vielen Anpassungen.
- [WellSaid Labs](https://www.wellsaidlabs.com/) - Natürliche Sprecherstimmen für E-Learning und Unternehmensvideos.
- [iSpeech](https://www.ispeech.org/) - Sprachsynthese in vielen Sprachen für Unternehmensanwendungen.
- [Microsoft Azure Neural TTS](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/) - Skalierbare Sprachsynthese für Unternehmensanwendungen.
- [Zenmic.com](https://zenmic.com) - Erzeugt Podcast-Folgen (Skript und Audio) mit KI.
- [Audify AI](https://audify-ai.ahmedtokyo.com) - Sprachsynthese mit anpassbaren Stimmen und Anweisungen.
- [TTS WebUI](https://github.com/rsxdalv/tts-generation-webui) - Oberfläche für über 15 Sprach- und Musikmodelle. `OSS`

### Sprache zu Text und Text zu Sprache

- [TorToiSe](https://github.com/neonbjb/tortoise-tts) - Text-zu-Sprache mit mehreren Stimmen und Fokus auf Qualität. `OSS`
- [Bark](https://github.com/suno-ai/bark) - Transformer-Modell für Text zu Audio. `OSS`
- [CustomPod.io](https://custompod.io) - Tägliche News-Podcasts nur zu deinen Themen.
- [EKHOS AI](https://ekhos.ai) - Transkription mit Korrekturfunktionen und Echtzeit-Aufnahme.
- [Whisper API](https://whisper-api.com) - Transkriptions-API auf Basis von OpenAI Whisper.

### Musik

- [Suno](https://suno.com) - Komplette Songs mit Gesang aus einem Prompt, auch auf Deutsch.
- [Udio](https://www.udio.com) - Songs und Instrumentals in hoher Klangqualität generieren.
- [AIVA](https://www.aiva.ai) - KI-Komponist für klassische und cineastische Musik.
- [Mubert](https://www.mubert.com) - Lizenzfreie, generative Musik in Echtzeit für Creator und Marken.
- [Soundraw](https://soundraw.io) - Musik nach Stimmung und Stil anpassen.
- [Beatoven.ai](https://www.beatoven.ai) - Hintergrundmusik, die gezielt Emotionen erzeugt.
- [Boomy](https://www.boomy.com) - Schnell Songs erstellen und veröffentlichen.
- [Ecrett Music](https://www.ecrettmusic.com) - Lizenzfreie Musik für Videos.
- [Loudly](https://www.loudly.com) - KI-Musik mit Community-Funktionen.
- [Soundful](https://www.soundful.com) - Hochwertige, lizenzfreie Musik für Content Creator.
- [AI Song Maker](https://www.aisongmaker.io) - Songs mit KI erstellen.
- [Harmonai](https://www.harmonai.org/) - Community für Open-Source-Audiowerkzeuge.
- [MusicLM](https://google-research.github.io/seanet/musiclm/examples/) - Googles Forschungsmodell für Musik aus Text.
- [Remusic](https://remusic.ai/en) - Kostenloser Musikgenerator und Lernplattform.


## Marketing und SEO

*Umfangreichere Liste (Englisch): [Marketing List](marketing.md)*

> 💡 **PROMPTGOTT-Praxis für SEO:** Die Kern-Serie zu KI-gestütztem SEO:
> [Programmatic SEO Architecture](https://promptgott.substack.com/p/programmatic-seo-architecture?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (Template × Datensatz) ·
> [The Index Swarm](https://promptgott.substack.com/p/the-index-swarm?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (Millionen URLs ohne Qualitätsverlust) ·
> [Der Authority Layer](https://promptgott.substack.com/p/der-authority-layer?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (Trust als Mathematik) ·
> [Der FAQ-Reaktor](https://promptgott.substack.com/p/der-faq-reaktor?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) („People Also Ask“ als Inventar) ·
> [Das Ende einzelner Webseiten](https://promptgott.substack.com/p/das-ende-einzelner-webseiten?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) (Such-Territorien) ·
> [The Programmatic Revenue Machine](https://promptgott.substack.com/p/the-programmatic-revenue-machine?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de)

### SEO und Content-Optimierung

- [Semrush](https://www.semrush.com) - SEO-Suite für Keywords, Wettbewerber und Site-Audits, mit KI-Funktionen und Sichtbarkeits-Tracking in KI-Suchen.
- [Ahrefs](https://www.ahrefs.com) - SEO-Suite mit großem Backlink-Index und KI-Content-Werkzeugen.
- [Surfer](https://surferseo.com) - Optimiert Texte datenbasiert auf Suchintention und Konkurrenz.
- [Frase](https://frase.io) - SEO-Briefings und Content-Optimierung aus den Top-Suchergebnissen.
- [MarketMuse](https://www.marketmuse.com/) - Themen-Planung und Content-Optimierung mit KI.
- [Luthor](https://luthor.ai/) - Programmatisches Content-Marketing in großem Umfang.
- [Quick Creator](https://quickcreator.io) - SEO-optimierte Blog-Plattform mit KI.
- [Headlinesai.pro](https://www.headlinesai.pro/) - Überschriften für verschiedene Plattformen optimieren.

### Werbung, Social und Personalisierung

- [Jasper](https://www.jasper.ai/) - Marketing-Content wie Blogs, E-Mails und Anzeigen mit Markenstimme.
- [neuroflash](https://neuroflash.com) - 🇪🇺 Deutschsprachige Marketing-Texte mit Markenrichtlinien.
- [Mutiny](https://www.mutinyhq.com/) - Personalisiert Websites mit KI für mehr Conversions.
- [Clearbit](https://clearbit.com/) - Lead-Anreicherung und Firmendaten (heute Teil von HubSpot).
- [Seventh Sense](https://www.theseventhsense.com/) - Optimiert den Versandzeitpunkt von E-Mails.
- [Smartly.io](https://www.smartly.io/) - 🇪🇺 Automatisiert Erstellung und Optimierung von Social Ads, aus Helsinki.
- [Adzooma](https://www.adzooma.com/) - KI-gestützte Verwaltung von PPC-Kampagnen.
- [Phrasee](https://www.phrasee.co/) - Optimierte Marketing-Texte für E-Mail, Push und Social.
- [Brandwatch](https://www.brandwatch.com) - Social Listening und Sentiment-Analyse (inklusive des früheren Crimson Hexagon).
- [Chatfuel](https://www.chatfuel.com/) - Chatbots für Messenger, Instagram und WhatsApp.
- [LogicBalls](https://logicballs.com/) - KI-Schreibwerkzeug für jede Art von Content.
- [Rupert AI](https://www.getrupert.com/) - KI-Werkzeuge für Designer und Marketer.
- [Publish7](https://publish7.com/) - KI-Agenten für digitales Marketing im Handel und E-Commerce.
- [Keyla.AI](https://keyla.ai/) - Video-Anzeigen in Minuten.
- [Persuva](https://persuva.ai) - Überzeugende, konversionsstarke Anzeigentexte in großem Umfang.
- [Taplio](https://taplio.com/) - All-in-one-Tool für LinkedIn mit KI.
- [Socialsonic](https://socialsonic.com) - LinkedIn-Coach: Content, Trends und Planung.
- [Podify.io](https://podify.io) - Wachstum auf LinkedIn mit KI und Community.
- [PressPulse AI](https://www.presspulse.ai/) - Jeden Morgen passende Medien-Anfragen für PR.
- [GummySearch](https://gummysearch.com/) - Kundenrecherche auf Reddit: Probleme, Stimmungen und Kaufinteresse finden.


## KI-Telefonagenten

- [AICaller.io](https://aicaller.io/) - Automatisierte Massenanrufe mit generativer KI, etwa für Lead-Qualifizierung, mit API.
- [DialLink AI Voice Agents](https://diallink.com/) - Sprachagenten für Geschäftsanrufe und Routineaufgaben.
- [Cald.ai](https://cald.ai) - KI-Anrufagenten für ein- und ausgehende Telefonate.
- [Rosie](https://heyrosie.com/) - KI-Telefonservice, der Anrufe entgegennimmt.


## Weitere KI-Tools

- [PromptBase](https://promptbase.com/) - Marktplatz zum Kaufen und Verkaufen von Prompts.
- [Promptly](https://searchpromptly.com/) - Prompts entdecken, erstellen und teilen.
- [Myriad](https://www.namepepper.com/free-tools/ai-content-prompt-tool) - Prompts für alle Content-Arten bauen und verfeinern.
- [Have I Been Trained?](https://haveibeentrained.com/) - Prüfen, ob eigene Bilder zum Training von KI-Modellen verwendet wurden.
- [This Image Does Not Exist](https://thisimagedoesnotexist.com/) - Teste, ob du KI-Bilder von echten unterscheiden kannst.
- [Taranify](https://www.taranify.com) - Findet Spotify-Playlists, Serien, Bücher und Essen nach deinem Geschmack.
- [AI Dungeon](https://aidungeon.io/) - Textadventure, das die KI live weitererzählt.
- [Scale Spellbook](https://scale.com/spellbook) - LLM-Apps bauen, vergleichen und bereitstellen.
- [Scenario](https://www.scenario.com/) - KI-generierte Assets für Spiele.
- [Teleprompter](https://github.com/danielgross/teleprompter) - Lokale KI, die in Meetings zuhört und Formulierungen vorschlägt. `OSS`
- [FinChat](https://finchat.io/) - Beantwortet Fragen zu börsennotierten Unternehmen und Investoren.
- [FairyTailAI](https://fairytailai.com/) - Personalisierte Gute-Nacht-Geschichten.
- [GradGPT](https://www.gradgpt.com/) - Hilfe bei Uni-Bewerbungen: Essays, Anforderungen, Hochschulsuche.
- [Architecture Helper](https://architecturehelper.com) - Architekturstile analysieren und eigene erzeugen.
- [AI Wedding Toast](https://aiweddingtoast.com) - Persönliche Hochzeitsrede mit KI.
- [Interviews Chat](https://www.interviews.chat/) - Vorbereitung und Copilot für Vorstellungsgespräche.
- [ezJobs](https://www.getezjobs.com/) - Automatisierte Jobsuche und Bewerbung.
- [Compass](https://www.getwhys.io/compass) - KI-Antworten auf SaaS-Recherchefragen.
- [Interview Solver](https://interviewsolver.com) - KI-Copilot für Live-Coding-Interviews.
- [AI Watermark Remover](https://aiwatermarkremover.io/) - Wasserzeichen aus Bildern und Videos entfernen.
- [AISaver](https://aisaver.io) - Sammlung von KI-Video- und Fototools.
- [LangMagic](https://easytolearn.io) - Sprachen mit Inhalten von Muttersprachlern lernen.
- [fynk](https://fynk.com/) - 🇪🇺 KI-gestütztes Vertragsmanagement aus Österreich.
- [LooksMax AI](https://looksmax.ai) - Bewertet Fotos von dir per KI.
- [ResumeDive](https://resumedive.com) - Lebenslauf-Optimierung mit KI.
- [Bricks](https://www.thebricks.com/) - Tabellenkalkulation mit eingebauter KI.
- [Daruy](https://daruy.space/) - Personalisierte Geschenkideen.
- [NVIDIA Omniverse AI Animal Explorer](https://docs.omniverse.nvidia.com/extensions/latest/ext_animal-explorer.html#installation) - Omniverse-Erweiterung für schnelle 3D-Tier-Prototypen.


## Lernen: Prompting und KI-Grundlagen

- [PROMPTGOTT](https://promptgott.substack.com/?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) - Deutschsprachiger Substack mit abgefahrenen AI-Use-Cases, Prompt-Engineering-Tricks und AI-SEO-Systemen. Einstieg: [Der Greyhat-Eid](https://promptgott.substack.com/p/der-greyhat-eid?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de).
- [Learn Prompting](https://learnprompting.org/) - Kostenloser Open-Source-Kurs zur Kommunikation mit KI.
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) - Leitfaden und Ressourcen zum Prompt Engineering.
- [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) - Kurzkurs von Isa Fulford (OpenAI) und Andrew Ng (DeepLearning.AI).
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) - Beispiele und Anleitungen zur OpenAI API.
- [Robert Miles AI Safety](https://www.youtube.com/@RobertMilesAI) - YouTube-Kanal über KI-Sicherheit.

### Machine Learning

- [Machine Learning Roadmap](https://github.com/mrdbourke/machine-learning-roadmap) - Landkarte der wichtigsten ML-Konzepte, mit Lernwegen und Werkzeugen.
- [Andrew Ngs Machine Learning (Stanford)](https://www.coursera.org/learn/machine-learning) - Einsteigerfreundlicher Grundlagenkurs.
- [Sebastian Thruns Intro to Machine Learning](https://www.udacity.com/course/intro-to-machine-learning--ud120) - Solide Einführung von einem der Pioniere autonomen Fahrens.
- [AI and Machine Learning Roadmaps](https://www.scaler.com/blog/category/artificial-intelligence-machine-learning/) - Lernpfade mit Konzepten, Methoden und Werkzeugen.
- [How To Learn Artificial Intelligence](https://www.appliedaicourse.com/blog/how-to-learn-artificial-intelligence-ai/) - Schritt-für-Schritt-Anleitung von Python und Mathe bis Deep Learning.

### Deep Learning

- [fast.ai](https://www.fast.ai/) - Praxisnahe, kostenlose Deep-Learning-Kurse von Jeremy Howard.
- [Coursera Deep Learning Specialization (Notizen)](https://github.com/pratham5368/coursera-deep-learning-specialization) - Notizen, Aufgaben und Quizze zur Spezialisierung von deeplearning.ai.
- [PyTorch-Notizen](https://github.com/pratham5368/Tecnologies-I-Learn/tree/main/31-pytorch) - PyTorch-Grundlagen mit Beispielen in Google Colab.


## Verwandte Listen

- [Awesome AI Tools (Original, Englisch)](https://github.com/mahseema/awesome-ai-tools) - Die Grundlage dieser Liste.
- [PROMPTGOTT](https://promptgott.substack.com/?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de) - Deep Dives zu AI-Use-Cases und AI-SEO auf Deutsch.
- [Altern](https://altern.ai) - Verzeichnis für KI-Tools.
- [AI For Developers](https://aifordevelopers.org) - Liste von KI-Entwicklerwerkzeugen.
- [Best of AI](https://github.com/best-of-ai/best-of-ai) - Eine Art Michelin-Führer für KI.
- [Awesome AI Models](https://github.com/dariubs/awesome-ai-models) - Kuratierte Liste von KI-Modellen und LLMs.
- [Awesome AI Coding Tools](https://github.com/ai-for-developers/awesome-ai-coding-tools) - KI-Werkzeuge für Entwickler.
- [Awesome Vibe Coding](https://github.com/dariubs/awesome-vibe-coding) - Werkzeuge und Ressourcen für Vibe Coding.
- [Awesome AI Books](https://github.com/mahseema/aibooks) - Bücher zu KI und Machine Learning.
- [AI for Productivity](https://productivity.directory/category/ai) - KI-Apps für Produktivität.
- [Awesome Workflow Automation](https://github.com/dariubs/awesome-workflow-automation) - Werkzeuge für Workflow-Automatisierung.
- [Awesome Marketing](https://github.com/marketingtoolslist/awesome-marketing) - Marketing-Werkzeuge.
- [Top AI Directories](https://github.com/best-of-ai/ai-directories) - Verzeichnisse, in die man KI-Tools eintragen kann.


## Mitmachen

Neues Tool, toter Link oder bessere Beschreibung? Pull Requests sind willkommen:

1. Ein Tool pro Pull Request.
2. Format: `- [Name](https://url) - Ein Satz auf Deutsch, wofür das Tool gut ist.` Ohne Affiliate- oder Referral-Parameter.
3. Ans Ende der passenden Kategorie setzen. 🇪🇺 nur, wenn der Anbieter seinen Sitz in der EU hat. `OSS` nur bei echtem Open-Source-Code.
4. Link vorher prüfen: Das Tool muss erreichbar und nutzbar sein.

---

Deutsche Bearbeitung mit Praxisbezug zu [PROMPTGOTT](https://promptgott.substack.com/?utm_source=github&utm_medium=referral&utm_campaign=awesome-ki-tools-de). Original: [Awesome AI Tools](https://github.com/mahseema/awesome-ai-tools) von [Mahsima Dastan](https://github.com/mahseema), MIT-Lizenz.
