# Strategiya monetizatsii servisa dlya tendernyh komand

## Kontekst i glavnyj vyvod

Produkt nahoditsya mezhdu dvumya rynkami:

1. **Excel/Google Sheets process** - komandy uzhe rabotayut besplatno ili pochti besplatno, no teryayut vremya na ruchnoe vedenie statusov, dedlajnov, dokumentov i kommunikacii.
2. **Professional tender stack** - kompanii uzhe platyat za agregatory, CRM, API i avtomatizaciyu tendernogo otdela.

Iz-etogo sleduet, chto odna cena dlya vseh budet oshibkoj. Nuzhna **segmentnaya monetizaciya**: nizkij vhod dlya zameny Excel, srednij tarif dlya komand s platnym agregatorom i vysokij tarif/enterprise dlya tendernyh otdelov.

## Rynochnye orientiry

| Kategoriya | Primer | Public price / orientir | Chto znachit dlya nas |
| --- | --- | --- | --- |
| Excel / tablicy | Google Sheets, Excel | 0 rub. ili vhodit v ofisnyj paket | Etot segment boleznenno reagiruet na cenu vyshe 2-3k rub./mes. |
| CRM dlya SMB | amoCRM | 599-1 699 rub./user/mes. | Polzovatelskaya cena v SMB privychna, no bez tendernoj specializacii. |
| CRM dlya komand | Bitrix24 | 2 490-13 990 rub./mes. za paket, Enterprise ot 33 990 rub./mes. | Kompanii gotovy platit za workflow i komandu, esli produkt stanovitsya operacionnoj sistemoj. |
| Tender search SMB | TenderGuru | okolo 19 900 rub./god za Standard; API-only ot 10 000 rub./mes. | Est nizkij godovoj chek za poisk i vysokij chek za API/integracii. |
| Tender search SMB | Tenderplan | okolo 35 000 rub./god, ili ~2 900 rub./mes. pri godovoj oplate | Potolok dlya samostoyatelnyh malyh komand blizok k 3k rub./mes. |
| Tender aggregators/API | Saby Trade API | 15 000-34 000 rub., paket Maximum+API okolo 30 000 rub. | Esli klient uzhe platit za agregator/API, servis-upravlenie mozet stoit 7-20k rub./mes. |
| Tender aggregators/API | Kontur.Zakupki | 16 200-58 000 rub./god; API module ot 26 000 rub. | Baza poiskovogo SaaS v RF - desyatki tys. v god, API doprodazha. |
| Tender department automation | Seldon.Doc | individualno; vstrechayutsya partner packages i kompleksnye vnedreniya | Etot produkt prodajotsya ne kak "zamena Excel", a kak avtomatizaciya tendernogo otdela. |

## Segmenty i willingness to pay

### 1. Solo / mikrokomanda: "uhodim iz Excel"

**Kto eto:** IP, malyj postavshik, 1-2 cheloveka, uchastie v tenderah neregulyarno ili tolko nachinaetsya.

**Boli:**

- ne propustit dedlajn;
- videt statusy;
- hranit ssylki i dokumenty;
- poluchat prostye napominaniya;
- ne dublirivat tender v tablice.

**Cena:** 990-2 990 rub./mes. ili 24 000-30 000 rub./god.

**Ogranicheniya tarifa:**

- 1-2 polzovatelya;
- ogranichennye doski/proekty;
- bez API;
- bez slozhnoj analitiki;
- bez komandnyh soglasovanij;
- import iz Excel i rucnoy dobavlenie tenderov.

**Logika:** etot tarif dolzhen konvertirovat s Excel. Ego nuzhno prodavat prosto: "ne propuskajte dedlajny i vedite tendernuyu voronku za cenu meneye odnoj oshibki".

### 2. SMB tender team: "est agregator, nuzhen process"

**Kto eto:** kompaniya, kotoraya uzhe platit za Saby/Kontur/TenderGuru/Tenderplan/Seldon ili poluchaet tendernye podborki.

**Boli:**

- tenderov mnogo, a process razvalivaetsya;
- nuzhno raspredelyat tendera po otvetstvennym;
- nuzhny etapnost, kommentarii, failovaya istoriya;
- rukovoditel hochet videt voronku i rezultat;
- nuzhno ubrat dublikatnye tendera iz neskolkih istochnikov.

**Cena:** 5 900-14 900 rub./mes. za komandu.

**Cennost:** eto ne konkurenciya agregatoru, a "operacionnyj sloj poverh agregatorov". Esli klient uzhe platit 15 000-30 000 rub./mes. za dannye, dopolnitelnye 7 000-15 000 rub./mes. za upravlenie rabotoj i deduplication mogut byt vosprinaty normalno.

### 3. Professional / tender department

**Kto eto:** tendernyj otdel, filialy, neskolko menedzherov, vysokaya chastota uchastiya.

**Boli:**

- SLA po podgotovke zayavok;
- kontrol rukovoditelya;
- history/audit;
- integracii s CRM, Bitrix24, 1C, pochtoj, agregatorami;
- roli, prava, shablony dokumentov;
- analytics po prichinam proigryshej, marzhe, konversiyam.

**Cena:** 24 900-49 900 rub./mes. ili individualno.

**Logika:** etot segment sravnivaet ne s Excel, a s zarplatami, poteryannymi zayavkami, Seldon.Doc, integraciyami i stoimostyu tendernogo otdela.

### 4. Enterprise / integracii

**Kto eto:** gruppy kompanij, proizvoditeli, distributory, holdingi, tendernye agentstva.

**Cena:** ot 75 000 rub./mes. ili ot 600 000-1 500 000 rub./god.

**Chto prodavat:**

- custom API;
- SSO;
- role model;
- integracii s vnutrennimi sistemami;
- migraciya istorii;
- private deployment / special SLA;
- personalnyj customer success.

## Rekomenduemaya tarifnaya setka

### Free / Trial

- 14 dnej polnogo dostupa ili freemium s 5-10 tenderami.
- Cel: pokazat cennost workflow i mobile UX.
- Bez API i komandnyh integracij.

### Start - 1 990 rub./mes. ili 19 900 rub./god

**Dlya zameny Excel.**

- 1 polzovatel;
- do 100 aktivnyh tenderov;
- statusy, dedlajny, kommentarii;
- import/export Excel;
- bazovye napominaniya;
- deduplication po nomeru zakupki i ssylke.

Mozhno derzhat "psihologicheskij potolok" do 3 000 rub./mes., no pri godovoj oplate dat oshchutimuyu skidku.

### Team - 7 900 rub./mes. ili 79 000 rub./god

**Dlya komand, kotorye uzhe platit za agregator.**

- 3-5 polzovatelej;
- komandnaya doska;
- otvetstvennye i roli;
- rasshirennye napominaniya;
- mass import;
- dedup iz neskolkih istochnikov;
- bazovaya analitika po voronke;
- email/telegram notifications.

### Pro - 14 900 rub./mes. ili 149 000 rub./god

**Dlya aktivnogo tendernogo otdela.**

- 10 polzovatelej;
- custom stages;
- shablony processov;
- integracii s agregatorami/API pri nalichii klucha klienta;
- BI export;
- istorija izmenenij;
- analytics po prichinam otkaza/proigrysha;
- priority support.

### Business - 29 900 rub./mes. ili 299 000 rub./god

**Dlya otdelov i filialov.**

- 20+ polzovatelej;
- rights/roles;
- filialy/komandy;
- integrations with Bitrix24/amoCRM/1C;
- advanced duplicate rules;
- audit log;
- onboarding session.

### Enterprise - individualno, ot 75 000 rub./mes.

- SSO;
- custom integrations;
- SLA;
- dedicated support;
- data residency/deployment requirements;
- custom reports.

## Chto imenno monetizirovat

Ne stoit monetizirovat tolko "hranenie tenderov". Eto legko sravnit s Excel i obescenit.

Monetiziruemye capability:

1. **Ne propustit dedlajn** - napominaniya, kalendar, escalation.
2. **Komandnyj process** - stage pipeline, otvetstvennye, komentarii, history.
3. **Deduplication** - esli tender prishol iz EIS, Saby i TenderGuru, komanda vidit odnu kartochku.
4. **Integracii** - Bitrix24, amoCRM, 1C, API agregatorov, email.
5. **Analytics** - skolko tenderov obrabotano, konversiya, prichiny otkaza, prichiny proigrysha.
6. **Audit and control** - kto chto sdelal, kakoe reshenie prinyato, pochemu ne uchastvovali.

## Pozicionirovanie

### Dlya Excel-segmenta

"Tendernaya doska vmesto Excel: dedlajny, statusy, dokumenty i napominaniya v odnom meste."

Ne govorit "CRM" v pervom ekrane: CRM zvuchit slozhno i dorogo. Govorit "zamena Excel dlya tenderov".

### Dlya segmenta s agregatorom

"Upravlenie tendernoj rabotoj poverh Saby, Kontur, TenderGuru, Tenderplan i EIS: odna kartochka tendera bez dublikatov."

### Dlya enterprise

"Operating system for tender departments: workflow, audit, integrations and performance analytics."

## Paketirovanie onboarding

- Start: self-service, import iz Excel, video-guide.
- Team: guided setup za doplatu ili vklyucheno pri godovoj oplate.
- Pro/Business: onboarding 20 000-50 000 rub. odnorazovo.
- Enterprise: project implementation individualno.

## Eksperimenty po cene

### Eksperiment A: Start price

Testirovat tri ceny:

- 990 rub./mes. - maksimalnaya konversiya iz Excel;
- 1 990 rub./mes. - balans ceny i cennosti;
- 2 990 rub./mes. - verhnyaya granica "ne bolno".

Metrika: trial-to-paid, retention 2-go mesyaca, aktivnost po tenderam.

### Eksperiment B: Team anchor

Pokazat sravnenie:

- agregator dannyh: 15 000-30 000 rub./mes.;
- nash process-layer: 7 900-14 900 rub./mes.;
- poterya odnogo tendera ili prosrochka dedlajna obyknovenno dorozhe.

Metrika: conversion iz klientov s agregatorom.

### Eksperiment C: Annual discount

Godovaya oplata dolzhna byt glavnoi dlya nizkih tarifov:

- Start: 19 900 rub./god;
- Team: 79 000 rub./god;
- Pro: 149 000 rub./god.

## Rekomendaciya

Zapusk ne s odnoj cenoj, a s trehurovnevoj cenovoj lestnice:

1. **Start do 3 000 rub./mes.** - zahvat Excel-segmenta.
2. **Team 7 900-14 900 rub./mes.** - osnovnoj kommercheskij fokus, klienty s agregatorami.
3. **Business/Enterprise ot 29 900 rub./mes.** - tendernye otdely, integracii, audit.

Glavnyj tezis: da, eto raznye platyashchie segmenty. Excel-segment ne kupit produkt za 15 000 rub./mes., no klient, kotoryj uzhe platit za agregator ili tendernyj otdel, mozhet kupit servis za takuyu cenu, esli produkt prodaetsya ne kak "eshche odna tablica", a kak upravlenie processom, deduplication, kontrol dedlajnov i integracii.

## Istochniki dlya proverki

- Saby Trade API: public pages show price range 15 000-34 000 rub. and API workflow.
- Kontur.Zakupki: public tariffs 16 200-58 000 rub./year, API module from 26 000 rub.
- TenderGuru: public tariffs around 19 900 rub./year for Standard; API-only plans from 10 000 rub./month.
- Tenderplan: public/partner pages show yearly plans around 24 000-35 000 rub./year.
- Bitrix24: public cloud tariffs around 2 490-13 990 rub./month, Enterprise from 33 990 rub./month.
- amoCRM: public tariffs around 599-1 699 rub./user/month.
- Seldon.Doc: public pages position it as automation/CRM for tender departments; pricing is individual or package-based via partners.
