# Presales — Dettaglio Opportunità: MILANO RISTORAZIONE

> Fonte dati: file locale canale Teams (OneDrive sync). Documento sorgente principale: `TODO_Meeting_Tecnico_Adesso_MiRi.md` (checklist preparazione meeting tecnico con Adesso.it), più `Business_Case_MVP_Ticketing_MiRi.xlsx` e 2 PDF (analisi As-Is/To-Be, ticketing). Sezione "Idee proposte dall'agente" in fondo: contenuto generato, non proveniente dal cliente.

## Perimetro e scopo

**MVP Ticketing** per Milano Ristorazione, in collaborazione con il partner Adesso.it:
- login/registrazione utenti;
- lista e dettaglio ticket;
- apertura e risposta ticket;
- stato ticket;
- propagazione del profilo utente a **Dynamics CRM**.

**Esplicitamente escluso dal perimetro MVP:** rette, iscrizioni, presenze, diete, pagamenti, CMS completo; migrazione/decommissioning non ancora definiti.

## Richiesta cliente

Milano Ristorazione necessita di un portale di ticketing rivolto a famiglie, scuole e operatori, con integrazione dei profili utente nel CRM Dynamics esistente. Il progetto è condotto in un modello a tre attori: **Milano Ristorazione** (cliente, sponsor/owner di business e IT), **Adesso.it** (presidio relazione e coordinamento con il cliente), **ENG** (architettura, integrazioni, delivery tecnico). È in preparazione un **meeting tecnico con Adesso.it** per allineare perimetro MVP, domande tecniche, stima preliminare di effort e modello organizzativo.

## Stato

**Fase:** preparazione meeting tecnico (checklist non ancora completata). WBS e stima ROM già elaborate come baseline di lavoro, **non ancora una stima contrattuale**.

**WBS e stima (13 work package MVP):** baseline avvio ottobre 2026, go-live target **giugno 2027**.

| Scenario | Effort pre-riserva | Effort con riserva 15% | FTE medi su 9 mesi |
|---|---:|---:|---:|
| Basso | ~506 gg-persona | ~582 gg-persona | ~3,2 |
| Base | 633 gg-persona | ~728 gg-persona | ~4,0 |
| Alto | ~792 gg-persona | ~911 gg-persona | ~5,1 |

Picco stimato: **~6,5 FTE a febbraio 2027** (riserva inclusa). Composizione principale: Portale/ticketing (115 gg), API Gateway/bus/listener CRM (96 gg), Identity/onboarding (58 gg), Governance/PMO (55 gg), Configurazione Dynamics (32 gg), Test integrati (64 gg), UAT/formazione (24 gg), Cutover/hypercare (21 gg), tra gli altri.

**Assunzioni della stima:** disponibilità tempestiva di ambienti/API/referenti cliente, nessuna migrazione dati, perimetro Dynamics limitato al flusso MVP. Ritardi su identity-to-CRM o dipendenze esterne possono spostare effort e calendario.

**Dati ancora mancanti (da richiedere al cliente prima di una stima vincolante):** utenti potenziali per categoria, volumi ticket attuali e stagionalità, picchi di accesso concorrenti, percentuale ticket con allegati, SLA attesi, sistemi sorgente/API/limiti (CRM, SPID/CIE, identità B2C, API Gateway), regole di identity matching, vincoli privacy/DPIA/accessibilità, data di scadenza licenze attuali.

**Modello organizzativo proposto (da formalizzare in RACI):** governance tripartita su 6 livelli (sponsor/priorità, steering, coordinamento quotidiano, architettura/integrazioni, prodotto/processi, esercizio), con ruoli e accountable distinti per Milano Ristorazione, Adesso.it, ENG.

**Gate consigliato (da fonte originale):** non impegnare prezzo e data di go-live come baseline vincolante finché non sono verificati volumi, requisiti operativi, identity-to-CRM, disponibilità integrazioni e opzione di proroga licenze.

## Idee proposte dall'agente

> Contenuto generato da questo agente (non dal cliente/partner), da validare prima di presentarlo ad Adesso.it/Milano Ristorazione. Approccio ispirato ai planner ENGenius (ANALYSIS, FP_SIZING, WBS, ACTIVITY).

1. **Raffinare la stima ROM con Function Point / SNAP sizing**: la WBS attuale è per work package; affiancarla con un sizing a Function Point (planner ENGenius `FP_SIZING`, eventualmente supportato dal tool `mcp-fp-snap-server`) darebbe una seconda misura indipendente da confrontare con la stima a gg-persona.
2. **Vertical slice identity-to-CRM come prova di fattibilità anticipata**: proporla come primo "sprint 0" a pagamento separato per validare il collegamento più critico (identità → Dynamics) prima di impegnarsi sulla stima completa.
3. **RACI formalizzata prima del meeting, non durante**: portare in meeting una bozza di RACI già compilata invece di limitarsi a discuterne il modello.
4. **Tre profili di volume (normale/picco/stress) come allegato tecnico separato**: template già strutturato da far compilare a Milano Ristorazione nel workshop.
5. **Dependency matrix con data di scadenza esplicita per ciascuna dipendenza**: collegata visibilmente al gate "non impegnare prezzo/data".
6. **Piano di escalation change request già abbozzato in fase di proposta**: anticipare come verranno gestite le change request post-baseline, per evitare conflitti a metà progetto.
