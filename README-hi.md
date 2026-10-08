# dsh-forecast-penalty — पूर्वानुमान-सटीकता मूल्यांकन रजिस्टर और मूल्यांकन-शुल्क की अंकगणितीय जाँच

`dsh-forecast-penalty` एक पूर्वानुमान-सटीकता मूल्यांकन रजिस्टर पढ़ता है — हेडर और प्रत्येक मूल्यांकन अवधि की एक पंक्ति — और उसी रजिस्टर की पूर्णता तथा अंकगणित की जाँच करता है: क्या अवधि, मूल्यांकन का विषय और बाज़ार-प्रकार दर्ज हैं, क्या पूर्वानुमान, वास्तविक और सटीकता के अंक संख्याओं के रूप में पढ़े जा सकते हैं, क्या दर्ज सटीकता आपके द्वारा कॉन्फ़िगर किए गए परिभाषा-सूत्र से और मूल्यांकन शुल्क आपके द्वारा कॉन्फ़िगर किए गए गणना-सूत्र से मेल खाता है, क्या मुद्रा तीन अक्षरों के कोड के रूप में लिखी है, क्या कोई मूल्यांकन अवधि दोहराई नहीं गई है, और क्या टिप्पणी-कॉलम में कोई अपूरित प्लेसहोल्डर शेष नहीं है। जो जाँच चल नहीं सकती, वह `skipped` में अपना कारण बताती है।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| रजिस्टर में नहीं लिखा है कि मूल्यांकन किस स्टेशन और किस बाज़ार का है, और एक पंक्ति में पूर्वानुमान मूल्य `--` है। | `FP-001` मूल्यांकन के विषय और बाज़ार-प्रकार के दर्ज होने की अपेक्षा करता है, और `FP-002` पूर्वानुमान मूल्य के संख्या के रूप में पढ़े जाने की, इसलिए `--` दर्ज होता है। `FP-001` यह देखता है कि दोनों भरे हैं, यह नहीं कि स्टेशन का नाम सही है; `FP-002` यह नहीं तय करता कि पूर्वानुमान सही था या नहीं। |
| मेरे रजिस्टर की सटीकता मेरे बाज़ार के परिभाषा-सूत्र से मेल नहीं खाती, और शुल्क भी आधार गुणा इकाई-दर से मेल नहीं खाता। | `FP-003` दर्ज अंक की तुलना नियम-संग्रह में कॉन्फ़िगर परिभाषा-सूत्र से करता है — फ़ैक्टरी सूत्र एक प्रचलित परिपाटी और उदाहरण है, आपके बाज़ार का नियम नहीं, इसलिए `expression` बदलें या यह नियम बंद करें — सहनशीलता 1.5 अंक। `FP-004` शुल्क की तुलना `考核基数 × 考核单价` से 0.01 की सहनशीलता पर करता है; आधार आप स्वयं भरते हैं। दोनों में से कोई यह नहीं तय करता कि मूल्यांकन विधि लागू होती है या शुल्क लिया जाना चाहिए। |
| मुद्रा कॉलम कुछ पंक्तियों में खाली है और कुछ में `元` लिखा है। | `FP-005` तीन बड़े अक्षरों का कोड मांगता है, जैसे CNY या USD, इसलिए खाली कोष्ठक और `元` दोनों दर्ज होते हैं; इस नियम की सीमा यह है कि यह केवल प्रारूप देखता है और यह तय नहीं करता कि रॅनमिन्बी के लिए आपकी संस्था कौन-सा कोड लिखे। यह भी नहीं तय करता कि चुनी गई मुद्रा सही है। |
| एक ही मूल्यांकन अवधि एक से अधिक पंक्तियों में आई है। | `FP-006` दोहराई गई अवधि दर्ज करता है, क्योंकि दोहराव से शुल्क दो बार जुड़ जाता है और यह स्पष्ट नहीं रहता कि अवधि दो बार दर्ज हुई या दो बार मूल्यांकित हुई; तुलना में रिक्त स्थान छोड़ दिए जाते हैं। एक ही अवधि का समय-खंड और श्रेणी के अनुसार मूल्यांकन वैध रूप से कई पंक्तियाँ बना सकता है — उन्हें टिप्पणी-कॉलम में या अलग अवधि-चिह्न से अलग दिखाएँ, या नियम बंद करें। यह तय नहीं करता कि कौन-सी पंक्ति दोहराई गई है। |
| टिप्पणी-कॉलम में अब भी `【】`, `XXX` या `TBD` पड़ा है। | `FP-007` उस पंक्ति को दर्ज करता है जिसके टिप्पणी-कॉलम में नियम-संग्रह में कॉन्फ़िगर प्लेसहोल्डर में से कोई मिलता है, क्योंकि टेम्पलेट से उतारा रजिस्टर पढ़ने वाले को यह मानने पर उकसाता है कि वास्तविक मूल्यांकन हो चुका है। `terms` सूची आप अपने टेम्पलेट के अनुसार बदल सकते हैं, और यह नियम यह नहीं तय करता कि टिप्पणी का पाठ सच है। |
| मेरी सामग्री में कोई पूरा कॉलम ही न हो — क्या नियम चुपचाप पास हो जाता है? | नहीं। कॉलम-आधारित नियम (`FP-002`, `FP-005`, `FP-006`, `FP-007`) `skipped` में स्वयं को दर्ज करते हैं और बताते हैं कि सामग्री में वह कॉलम नहीं है; रिपोर्ट इस स्थिति को उस नियम से अलग रखती है जो चला और जिसे कोई भिन्न पंक्ति नहीं मिली। जो जाँच कभी चली ही नहीं, उसे पूरी हुई जाँच के रूप में नहीं दिखाया जाता। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账可追溯性） | FP-001 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为算术可行性） | FP-002 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为本机构配置的准确率定义式） | FP-003 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为本机构配置的考核算式） | FP-004 |
| 《表示货币的代码》 | GB/T 12406—2022（表示货币的代码；2022-12-30 发布并实施；全部代替 GB/T 12406—2008（该版名称为「表示货币和资金的代码」）——注意旧版名称含"资金"；修改采用 ISO 4217:2015，非等同采用；条号本次未取得） | FP-005 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账唯一性） | FP-006 |
| 电力市场考核办法与并网调度协议（无国家标准） | 无统一标准（本条依据为台账真实性） | FP-007 |

**Boundary:** this plugin checks a **预测准确率考核台账** for arithmetic — that the period and subject are
identified, that forecast and actual figures parse, that the accuracy figure matches the definition formula
you configure, that the assessment charge matches your charge formula, that the currency follows its format,
that periods do not repeat, and that no placeholder survives. It does **not** decide whether a charge should be
levied, whether accuracy passes, or whether a waiver or appeal applies. **Those depend on the market rules, the
exemption cases and the dispute procedure.**

> ### ⚠️ This is a market rule, not a national standard — and the pack says so
>
> The accuracy definition, the exemption threshold, the unit rate and the settlement basis are set by **each
> power market's assessment rules and the grid-connection dispatch agreement**. Provinces differ sharply (some
> use `1 − deviation`, some use root-mean-square error, some assess by time block and band), and **no unified
> national standard exists**. So this pack does not fabricate a standard number: every rule's `excerpt` states
> plainly that its basis is arithmetic self-consistency or a locally configured convention and that **no
> citable clause exists**.
>
> **Two formulas ship as examples, and both are marked as such:**
>
> - `FP-003` **accuracy** defaults to `预测值 ÷ 实际值 × 100` with a 1.5-point tolerance. That is **one common
>   convention, not any market's rule**. Before use, replace `expression` with the formula from your market's
>   rules — or disable the rule. The note spells this out.
> - `FP-004` **charge** checks `考核费用 = 考核基数 × 考核单价`. The base is **entered by you** after working
>   it out under your market's rules, because the threshold, the bands and the volume basis are the market's
>   business and this plugin will not derive them. No unit rate is built in anywhere.
>
> A consequence worth knowing: the accuracy rule ships at `info` severity precisely because its formula is a
> deployment choice rather than a verified requirement.

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-forecast-penalty
dsh --profile <name> --dump-config | grep 'dsh-forecast-penalty'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/forecast-penalty.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-forecast-penalty
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-forecast-penalty contributors.
