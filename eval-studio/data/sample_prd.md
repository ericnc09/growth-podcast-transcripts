# Fieldnote Auto-Synthesis: PRD

*Fieldnote is a fictional research repository for product teams. This sample PRD was written for Dawson City and has some problems on purpose.*

**Status:** Draft for review · **Target beta:** Q1 · **Team:** Synthesis pod (1 PM, 3 engineers, 1 designer, 1 researcher)

## Problem

Researchers and PMs on Fieldnote run 6 to 15 customer interviews per study, then spend 1 to 2 days tagging transcripts and writing a synthesis. In our Q3 survey, 64% of PM users said they skip synthesis entirely when a study runs late, and studies without a synthesis are opened 70% less by the rest of the team. The research is done, but the insight never travels.

## Users

- **Primary:** PMs at 50- to 500-person software companies who run their own interviews and have no dedicated researcher.
- **Secondary:** Researchers who want a first draft to edit rather than a blank page.

## Proposed solution

When a study has at least 3 transcribed interviews, a "Synthesize" button appears. Auto-Synthesis reads every transcript in the study and produces:

1. **Themes:** 4 to 8 themes, each with a one-line claim, how many participants raised it, and 2 or 3 supporting quotes linked to the transcript timestamp.
2. **Surprises:** points where participants contradicted the study's stated hypothesis.
3. **Open questions:** things participants raised that the study didn't cover.

The synthesis opens as an editable draft. Nothing is shared until the author publishes it.

## Requirements

| Input | Expected behaviour |
| --- | --- |
| 8 interviews where 5 people complain about onboarding emails | A theme about onboarding emails, "5 of 8 participants", with quotes from at least 2 different people |
| A theme that only one participant raised, but at length | Listed under open questions, not as a theme |
| A participant says "I'd never pay for that" and later describes paying for a workaround | Both quotes appear, and the contradiction is noted under surprises |
| Quotes in a theme | Every quote appears word for word in a transcript, with a working timestamp link |

## Quality and evaluation

We'll measure quality with three standard metrics from our evaluation vendor: a faithfulness score, a hallucination score and a coherence score. We'll also run a ROUGE comparison against 20 syntheses our researcher wrote by hand last year.

Our researcher will rate a sample of syntheses from 1 to 5 on usefulness, accuracy and clarity. After the first month, an LLM judge will take over the rating so we can score every synthesis automatically.

We'll keep a set of 40 studies as our test set and won't ship until average scores are above 4.5 out of 5.

## Launch and monitoring

Beta with 25 design-partner accounts for 6 weeks, then general availability. After launch we'll track:

- Synthesis publish rate: the share of generated drafts that get published
- Edit distance between the draft and the published version
- Thumbs up or down on each theme, with an optional reason
- A monthly review of 30 published syntheses by our researcher, comparing themes against the transcripts

## Cost and latency

Synthesis will use the most capable model available so the output impresses users in the beta. We'll revisit cost once we see usage.

## Risks

- **Fabricated quotes.** Mitigated by the requirement that every quote matches a transcript word for word, checked in code before display.
- **Over-generalising from small studies.** Mitigated by showing participant counts on every theme.
- **Privacy.** Transcripts stay in the customer's region; no transcript data is used for training.
