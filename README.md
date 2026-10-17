# AI Compliance Mapper

Assess an AI system against **ISO/IEC 42001**, the **SDAIA AI Ethics
Principles**, the **Saudi PDPL**, and the **EU AI Act** — and get back a
prioritised risk register and gap report instead of a checklist.

Most AI governance tooling stops at a questionnaire. This one does the three
things a questionnaire does not: it decides which controls actually apply to
*your* system, it scores what is left undone as residual risk, and it tells you
what an assessor would ask to see.

```bash
python -m src.cli examples/property-ai-platform.yaml -o reports/assessment.md
```

```
Assessed Property Portfolio AI Platform: 48 applicable controls,
38% implemented, 30 gaps.
```

[→ Read the full generated report](reports/property-ai-platform.md)

---

## Why this exists

I built and shipped a production AI system — an Arabic-language retrieval
assistant over a property portfolio's tenancy and contract records. It worked.
It was tested. And when I sat down to answer the question *"is this
governable?"*, I found that the honest answer required a structure I did not
have.

So I built the structure, then pointed it at my own system. The example
assessment in this repository is that self-assessment, anonymised. It scores
38%. Publishing a failing grade on my own work is the point: a governance tool
that only ever produces green is not measuring anything.

## What it does

**Applicability resolution.** A control about training-data provenance is not a
finding for a system that does no training. The mapper reads the system's
declared characteristics and marks non-applicable controls as out of scope —
explicitly, in the report, so a reviewer can challenge the scoping decision
rather than discover it buried in a spreadsheet.

**Risk tiering.** The system's characteristics resolve to an indicative EU AI
Act tier (`prohibited` / `high` / `limited` / `minimal`), and that tier then
gates which obligations apply. Tiering is an input to scope, not a label.

**Residual risk scoring.** Each control carries a weight (1–3). Implementation
status reduces it: implemented removes the weight, partial halves it, missing
or unassessed leaves it whole. The total is a comparable number across systems
and across reassessments.

**Honest treatment of the unknown.** A control with no recorded status is
scored as missing *and* reported in its own section. An unassessed control is a
finding about the quality of the assessment, not only about the system — most
tools quietly drop these.

**Evidence expectations.** Every finding states what an assessor would ask to
see. This is the difference between "you need an AI policy" and a remediation
task someone can actually close.

## Output

The generated report has five sections:

| Section | Contents |
|---|---|
| 1. Summary | Coverage and residual risk per framework, severity counts |
| 2. Risk register | Every gap, ordered by severity then weight |
| 3. Findings in detail | Intent, evidence expectations, owner's note |
| 4. Not yet assessed | Controls with no recorded status |
| 5. Scope excluded | Controls ruled out, with the reason |

## Install and run

```bash
git clone https://github.com/shouq-alghamdi/ai-compliance-mapper.git
cd ai-compliance-mapper
pip install -r requirements.txt

# assess the worked example
python -m src.cli examples/property-ai-platform.yaml

# one framework only
python -m src.cli examples/property-ai-platform.yaml -f PDPL

# fail a CI pipeline on critical gaps
python -m src.cli examples/property-ai-platform.yaml --fail-on critical
```

Requires Python 3.10+ and PyYAML. No other dependencies.

## Assessing your own system

Copy `examples/property-ai-platform.yaml` and edit three blocks:

```yaml
system:
  name: "Your system"
  owner: "Named individual, not a department"
  purpose: "What it does, in one honest paragraph"

characteristics:
  processes_personal_data: true
  automated_decision_making: false
  uses_third_party_model: true
  data_crosses_border: true
  user_facing: true
  # ... these drive which controls apply

control_status:
  ISO42001-A.2.2: missing      # implemented | partial | missing
  PDPL-01: partial             # | not_applicable | not_assessed
```

Anything you leave out of `control_status` is reported as not assessed. That is
deliberate — the tool will not let you reach a good score by omission.

## Control library

| Framework | Controls | Source |
|---|---:|---|
| ISO/IEC 42001:2023 | 22 | Annex A control themes |
| SDAIA AI Ethics Principles | 15 | The seven published principles |
| Saudi PDPL | 10 | AI-relevant obligations |
| EU AI Act | 10 | Risk-tiered provider obligations |

The library is plain YAML in `controls/`. Adding a framework means adding a
file — no code change. The schema is documented in
[`controls/_schema.md`](controls/_schema.md).

## Method

The scoring model, its assumptions, and its known limitations are written up in
[`docs/methodology.md`](docs/methodology.md). Read it before trusting a number
this tool produces.

## Tests

```bash
python -m pytest tests/ -q
```

25 tests covering applicability logic, tier resolution, severity mapping,
residual scoring, library integrity, and an end-to-end assessment.

## Limitations — read this

- **This is not legal advice, an audit, or a certification.** It is a
  self-assessment aid built by an engineer, not a lawyer.
- **The control library is a practitioner mapping, not official text.** It was
  drafted from the published structure of each framework. It does not reproduce
  normative text and may diverge from current requirements. Verify against the
  source before relying on it.
- **A score is not compliance.** 100% coverage against this library means the
  declared statuses were all `implemented` — it does not mean the evidence
  exists or that an assessor would accept it.
- **Statuses are self-declared.** The tool has no way to verify them. It is
  structure for an honest assessment, not a substitute for one.

## Licence

MIT — see [LICENSE](LICENSE).

---

<div dir="rtl">

## بالعربية

**أداة لتقييم أنظمة الذكاء الاصطناعي** مقابل أربعة أطر: ISO/IEC 42001، ومبادئ
أخلاقيات الذكاء الاصطناعي الصادرة عن سدايا، ونظام حماية البيانات الشخصية
السعودي، وقانون الذكاء الاصطناعي الأوروبي.

الأداة لا تكتفي بقائمة تحقق. تقوم بثلاثة أمور لا تقوم بها القوائم: **تحدد أي
ضوابط تنطبق فعلاً** على نظامك بناءً على خصائصه، و**تحسب المخاطر المتبقية**
كرقم قابل للمقارنة، و**تذكر الدليل** الذي سيطلبه المدقق لكل ملاحظة.

### لماذا بُنيت

بنيتُ نظام ذكاء اصطناعي إنتاجياً — مساعد عربي قائم على الاسترجاع يعمل على
سجلات محفظة عقارية. النظام يعمل ومُختبَر. لكن حين سألت نفسي: *هل هذا النظام
قابل للحوكمة؟* وجدت أن الإجابة الصادقة تحتاج بنية لم تكن موجودة عندي.

فبنيتُ البنية، ثم وجّهتها إلى نظامي أنا. التقييم المرفق في المستودع هو ذلك
التقييم الذاتي، بعد إخفاء هوية العميل. **نتيجته 38%.** ونشر نتيجة راسبة على
عملي الخاص هو جوهر الفكرة: أداة حوكمة لا تُخرج إلا اللون الأخضر لا تقيس شيئاً.

### ملاحظة مهمة

هذه الأداة **ليست استشارة قانونية ولا تدقيقاً ولا شهادة امتثال**. ومكتبة
الضوابط فيها اجتهاد مهني مبني على الهياكل المنشورة للأطر، وليست نصاً رسمياً.
راجعي المصدر الرسمي قبل الاعتماد عليها في تقييم حقيقي.

</div>
