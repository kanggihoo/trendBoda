# TrendBoda

TrendBoda is a personal system that collects market, news, and subscribed-source updates, summarizes important changes, and delivers them to the owner.

## Language

**TrendBoda**:
A personal information system that turns subscribed sources into summarized signals and alerts.
_Avoid_: Signal Hub, personal assistant, news app, stock app

**Owner**:
The single person who configures sources, receives alerts, and reviews summaries.
_Avoid_: User, customer, account

**Source**:
An external place the system checks for new market, disclosure, technology, or developer-trend information.
_Avoid_: Subscription, feed, channel

**Market Source**:
A source that provides prices, market movement, or end-of-day market context for watched stocks and ETFs.
_Avoid_: Stock app

**Disclosure Source**:
A source that provides official company disclosures or filings.
_Avoid_: News, announcement

**Developer Trend Source**:
A source that provides high-interest developer projects or engineering news.
_Avoid_: Geek news, tech feed

**GeekNews Provider**:
The first provider adapter used to collect items from a Developer Trend Source.
_Avoid_: Developer Trend Source, Geek news

**GeekNews Item Content**:
Raw HTML body from a GeekNews entry that may later be rendered or sanitized.
_Avoid_: Rendered text, summary, excerpt

**GeekNews Signal**:
A developer-trend signal collected from GeekNews for quick scanning and source-link navigation.
_Avoid_: AI summary, AI preview note, report

**Signal**:
A source item or market change that is worth showing to the owner.
_Avoid_: Notification, post, update

**Routine Briefing**:
A scheduled summary of non-urgent signals, such as market status, overnight US market movement, or daily developer trends.
_Avoid_: Alert, push, report

**Urgent Alert**:
An immediate message for exceptional signals that should not wait for the next routine briefing.
_Avoid_: Notification, briefing

**Commute Briefing**:
A routine briefing timed for the owner to read during commute periods.
_Avoid_: News digest

**Interactive Bot**:
A Telegram interface that lets the owner request summaries, current prices, source details, or saved signals.
_Avoid_: Chatbot, assistant

**Watchlist**:
The set of stocks, ETFs, sectors, or themes the owner wants the system to monitor.
_Avoid_: Portfolio, holdings

**Focus Universe**:
The broader set of sectors and large-cap technology themes the system can answer questions about even when they are not in the watchlist.
_Avoid_: Market coverage, default topics

**Market Coverage**:
The markets the system treats as first-class for prices, disclosures, news, and market questions.
_Avoid_: Region, exchange support

**Market Question**:
An owner-initiated question about a watched asset, sector, market movement, disclosure, or related news.
_Avoid_: Chat, prompt

**Investment Analysis**:
An evidence-backed explanation of risks, catalysts, valuation context, and relevant signals for a watched asset.
_Avoid_: Investment advice, buy signal, sell signal

**AI Cost Dashboard**:
A product dashboard view that shows OpenRouter usage, cost, latency, errors, and budget progress by feature and model.
_Avoid_: Grafana dashboard, billing page

**Price Snapshot**:
A deterministic view of current or recent asset prices without AI-generated explanation.
_Avoid_: Analysis, summary

**Done Work Item**:
A PRD or issue whose acceptance criteria have been implemented and accepted as complete.
_Avoid_: Completed, closed, finished

## Relationships

- **TrendBoda** has exactly one **Owner**
- An **Owner** configures one or more **Sources**
- A **Source** may be a **Market Source**, **Disclosure Source**, or **Developer Trend Source**
- A **GeekNews Provider** collects items for a **Developer Trend Source**
- A **GeekNews Provider** produces **GeekNews Signals**
- A **GeekNews Signal** is normally reviewed through dashboard or **Interactive Bot** links without AI-generated explanation
- A **Signal** is delivered through either a **Routine Briefing** or an **Urgent Alert**
- Most **Signals** are delivered through **Routine Briefings**
- A **Commute Briefing** is a **Routine Briefing** focused on major news
- An **Interactive Bot** can retrieve recent **Signals** and trigger fresh summaries on demand
- A **Watchlist** determines which market signals are monitored closely
- The **Owner** can add or remove items from the **Watchlist**
- The **Focus Universe** covers semiconductors, AI, technology stocks, and large-cap market leaders by default
- The **Market Coverage** includes both US and Korean markets
- A **Market Question** may produce **Investment Analysis**, but not direct buy or sell instructions
- The **AI Cost Dashboard** groups OpenRouter usage by date, model, feature, request, and monthly budget progress
- A **Price Snapshot** does not use AI unless the owner asks for explanation or analysis
- A PRD or issue uses `Status: done` when it becomes a **Done Work Item**

## Example dialogue

> **Dev:** "Should **TrendBoda** support multiple users from day one?"
> **Domain expert:** "No. The first version is for one **Owner** only, so every alert and dashboard view belongs to that owner."
>
> **Dev:** "Is a GitHub trending repo a news item?"
> **Domain expert:** "No. It comes from a **Developer Trend Source**, because it signals developer interest rather than market news."
>
> **Dev:** "Should every stock price movement trigger Telegram immediately?"
> **Domain expert:** "No. Most market movement belongs in a **Routine Briefing** unless it is exceptional enough to become an **Urgent Alert**."
>
> **Dev:** "Should GitHub trending projects be sent every day?"
> **Domain expert:** "No. Developer trends are slower moving, so weekly or monthly **Routine Briefings** are enough."
>
> **Dev:** "Can the bot tell the **Owner** whether to buy a stock?"
> **Domain expert:** "No. It provides **Investment Analysis** with supporting signals, but the decision stays with the **Owner**."
>
> **Dev:** "Should every price message include AI-generated reasons?"
> **Domain expert:** "No. A **Price Snapshot** should avoid AI cost and only show deterministic price data unless the **Owner** asks for analysis."
>
> **Dev:** "Should every **GeekNews Signal** be summarized with OpenRouter?"
> **Domain expert:** "No. GeekNews already provides enough title, description, and source links for scanning; OpenRouter remains available for other AI-backed TrendBoda features."

## Flagged ambiguities

- "GeekNews summary" implied automatic AI summarization -- resolved: GeekNews uses **GeekNews Signals** for scanning and link navigation; OpenRouter-backed AI remains available outside the default GeekNews flow.
- "AI assistant" was too broad — resolved: this product is **TrendBoda**, focused on monitored information signals, summaries, and alerts.
- "subscription" was too broad — resolved: use **Source** for anything the system checks repeatedly.
- "notification" was too broad — resolved: use **Routine Briefing** for scheduled summaries and **Urgent Alert** for exceptional immediate messages.
- "Telegram bot" was ambiguous — resolved: use **Interactive Bot** when the owner can ask for information, not only receive messages.
- "investment advice" was too broad and risky — resolved: use **Investment Analysis** for evidence-backed explanations without buy or sell instructions.
- "GeekNews" was ambiguous — resolved: use **GeekNews Provider** for the adapter and **Developer Trend Source** for the domain concept.
- "completed", "closed", and "finished" were ambiguous issue tracker states — resolved: use `Status: done` for completed PRDs and issues.
