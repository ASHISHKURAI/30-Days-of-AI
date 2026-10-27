# System prompt comparison

**Question:** What is inflation?

**Model:** openai/gpt-oss-120b

## Explain to a 10-year-old
**System prompt:** You explain things to a 10-year-old. Use simple words and one everyday example. Maximum 3 sentences.
**Tokens:** 101 in, 135 out

Inflation is when the prices of things go up, so the same amount of money buys less than before.  
For example, if a candy bar cost $1 last year and this year it costs $1.10, the extra 10 cents is inflation.

## Economics professor
**System prompt:** You are an economics professor. Give a precise, formal definition and mention one cause and one effect.
**Tokens:** 98 in, 402 out

**Inflation (formal definition)**  
Inflation is a sustained, economy‑wide increase in the general price level of goods and services measured over a given period, typically expressed as an annual percentage change in a broad price index such as the Consumer Price Index (CPI) or the Harmonised Index of Consumer Prices (HICP). Formally, if \(P_t\) denotes the price index at time \(t\), the inflation rate \(\pi_t\) over the interval \([t-1, t]\) is  

\[
\pi_t = \frac{P_t - P_{t-1}}{P_{t-1}} \times 100\%.
\]

When \(\pi_t > 0\) for an extended sequence of periods, the economy is said to be experiencing inflation.

---

### One common cause  
**Demand‑pull pressure:** When aggregate demand (consumption, investment, government spending, net exports) grows faster than the economy’s productive capacity, excess demand bids up prices, generating a positive inflation rate.

### One typical effect  
**Erosion of real purchasing power:** As the nominal price level rises, the real value of money falls, meaning that a given amount of currency buys fewer goods and services than before. This reduces consumers’ real income and can alter consumption and saving decisions.

## One-line answers only
**System prompt:** Answer in exactly one short sentence. No extra words.
**Tokens:** 89 in, 117 out

Inflation is the general rise in prices reducing purchasing power.

## My notes

- Which answer was most useful, and why?
- Which one used the most tokens?
